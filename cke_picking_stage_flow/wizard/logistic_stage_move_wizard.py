# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime as _dt, time as _time

# Urutan tahap otomatis
_STAGE_ORDER = ['loaded', 'boarded', 'customs', 'arrived', 'gudang_vsj']


class LogisticStageMoveWizard(models.TransientModel):
    _name = 'logistic.stage.move.wizard'
    _description = 'Auto Step Logistic Stage (Internal Transfer from Picking List)'

    move_ids = fields.Many2many('stock.move', string='Picking List Items', required=True)
    move_date = fields.Date(string='Move Date', required=True, default=fields.Date.today)
    auto_validate = fields.Boolean(string='Validate Transfer Now', default=True)

    # ---------------------------
    # Defaults
    # ---------------------------
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('default_move_ids') or self.env.context.get('active_ids') or []
        if active_ids:
            res['move_ids'] = [(6, 0, active_ids)]
        return res

    # ---------------------------
    # Helpers lokasi stage
    # ---------------------------
    def _stage_locations(self):
        """
        Ambil lokasi per stage, urutan:
        1) xmlid modul ini
        2) cari by name
        3) buat baru di bawah 'Logistics Transit'
        """
        Location = self.env['stock.location']
        xmlids = {
            'loaded': 'cke_picking_stage_flow.loc_loaded',
            'boarded': 'cke_picking_stage_flow.loc_boarded',
            'customs': 'cke_picking_stage_flow.loc_customs',
            'arrived': 'cke_picking_stage_flow.loc_arrived',
            'gudang_vsj': 'cke_picking_stage_flow.loc_gudang_vsj',
        }
        names = {
            'loaded': 'Loaded',
            'boarded': 'Boarded',
            'customs': 'Customs',
            'arrived': 'Arrived',
            'gudang_vsj': 'Gudang VSJ',
        }
        # root transit
        root = Location.search([('name', '=', 'Logistics Transit'), ('usage', '=', 'internal')], limit=1)
        if not root:
            root = Location.create({'name': 'Logistics Transit', 'usage': 'internal'})

        out = {}
        for key in _STAGE_ORDER:
            rec = None
            try:
                rec = self.env.ref(xmlids[key])
            except Exception:
                rec = None
            if not rec:
                rec = Location.search([('name', '=', names[key]), ('usage', '=', 'internal')], limit=1)
            if not rec:
                rec = Location.create({'name': names[key], 'usage': 'internal', 'location_id': root.id})
            out[key] = rec
        return out

    def _date_as_datetime(self):
        """Konversi Date → Datetime (00:00) string sesuai format Odoo."""
        dt = _dt.combine(self.move_date, _time(0, 0, 0))
        return fields.Datetime.to_string(dt)

    def _internal_picking_type(self, company):
        pt = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id.company_id', '=', company.id)
        ], limit=1)
        if pt:
            return pt
        return self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

    def _available_in_location(self, product, location, company):
        """Qty tersedia (non-reserved) untuk product di location & children."""
        Quant = self.env['stock.quant'].sudo()
        try:
            qty = Quant._get_available_quantity(product, location, lot_id=None, owner_id=None, package_id=None, strict=False)
            return max(qty, 0.0)
        except Exception:
            quants = Quant.search([
                ('product_id', '=', product.id),
                ('location_id', 'child_of', location.id),
                ('company_id', '=', company.id),
            ])
            total = 0.0
            for q in quants:
                total += (q.quantity - q.reserved_quantity)
            return max(total, 0.0)

    def _receipt_dest_locations(self):
        """
        Kumpulkan lokasi tujuan receipt (incoming) dari baris yang dipilih.
        Ini dipakai sebagai sumber 'bootstrap' ke Loaded bila belum ada stok di stage.
        """
        loc_ids = set()
        for mv in self.move_ids:
            pk = mv.picking_id
            if pk and pk.picking_type_id and pk.picking_type_id.code == 'incoming':
                loc_ids.add(pk.location_dest_id.id)
        if not loc_ids:
            # Fallback: pakai lokasi stok gudang perusahaan
            company = self.move_ids[:1].company_id if self.move_ids else self.env.company
            wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
            if wh and wh.lot_stock_id:
                loc_ids.add(wh.lot_stock_id.id)
        return self.env['stock.location'].browse(list(loc_ids))

    def _sample_po_for_product(self, product):
        """
        Ambil PO reference dari salah satu move sumber (move_ids) yang punya product sama.
        Berguna untuk menuliskan PO ke field 'origin' pada internal picking.
        """
        mv = self.move_ids.filtered(lambda m: m.product_id.id == product.id)[:1]
        return getattr(mv, 'po_reference', False) if mv else False

    # ---------------------------
    # Main
    # ---------------------------
    def action_confirm(self):
        self.ensure_one()
        if not self.move_ids:
            raise UserError(_("Please select at least one Picking List row."))

        company = self.move_ids[0].company_id
        date_dt = self._date_as_datetime()
        stage_locs = self._stage_locations()
        Picking = self.env['stock.picking']
        MoveLine = self.env['stock.move.line']

        # Kuantitas target per product (pakai qty_done kalau ada; else demand), distandarkan ke UoM produk
        product_qty = {}
        for mv in self.move_ids:
            if not mv.product_id or mv.product_id.type not in ('product', 'consu'):
                continue
            qty_src = mv.quantity_done or mv.product_uom_qty or 0.0
            if qty_src <= 0:
                continue
            qty = qty_src
            if mv.product_uom and mv.product_uom != mv.product_id.uom_id:
                qty = mv.product_uom._compute_quantity(qty_src, mv.product_id.uom_id)
            product_qty[mv.product_id.id] = product_qty.get(mv.product_id.id, 0.0) + qty

        if not product_qty:
            raise UserError(_("All selected lines have zero quantity."))

        # 1) Coba pindahkan dari stage yang ada → next stage
        groups = {}  # (src_id, dst_id) -> list move_vals
        for prod_id, qty_needed in product_qty.items():
            product = self.env['product.product'].browse(prod_id)
            remaining = qty_needed

            for i in range(len(_STAGE_ORDER) - 1):
                if remaining <= 0:
                    break
                src_stage = _STAGE_ORDER[i]
                dst_stage = _STAGE_ORDER[i + 1]
                src_loc = stage_locs[src_stage]
                dst_loc = stage_locs[dst_stage]

                avail = self._available_in_location(product, src_loc, company)
                if avail <= 0:
                    continue

                qty_move = min(avail, remaining)
                po = self._sample_po_for_product(product)
                origin_note = _('Stage Auto: %s → %s') % (src_stage.title(), dst_stage.title())
                if po:
                    origin_note = 'PO:%s | %s' % (po, origin_note)

                key = (src_loc.id, dst_loc.id)
                groups.setdefault(key, [])
                groups[key].append({
                    'name': product.display_name,
                    'product_id': product.id,
                    'product_uom': product.uom_id.id,
                    'product_uom_qty': qty_move,
                    'location_id': src_loc.id,
                    'location_dest_id': dst_loc.id,
                    'company_id': company.id,
                    'date': date_dt,
                    'origin': origin_note,
                })
                remaining -= qty_move

            # Sisa diabaikan di langkah ini; bisa ter-handle saat bootstrap di bawah

        # 2) Jika TIDAK ada kuantitas di stage mana pun → auto-bootstrap: dari receipt dest → Loaded
        if not groups:
            receipt_locs = self._receipt_dest_locations()
            loaded_loc = stage_locs['loaded']

            for prod_id, qty_needed in product_qty.items():
                product = self.env['product.product'].browse(prod_id)
                remaining = qty_needed

                for src_loc in receipt_locs:
                    if remaining <= 0:
                        break
                    avail = self._available_in_location(product, src_loc, company)
                    if avail <= 0:
                        continue

                    qty_move = min(avail, remaining)
                    po = self._sample_po_for_product(product)
                    origin_note = _('Seed to Loaded')
                    if po:
                        origin_note = 'PO:%s | %s' % (po, origin_note)

                    key = (src_loc.id, loaded_loc.id)
                    groups.setdefault(key, [])
                    groups[key].append({
                        'name': product.display_name,
                        'product_id': product.id,
                        'product_uom': product.uom_id.id,
                        'product_uom_qty': qty_move,
                        'location_id': src_loc.id,
                        'location_dest_id': loaded_loc.id,
                        'company_id': company.id,
                        'date': date_dt,
                        'origin': origin_note,
                    })
                    remaining -= qty_move

        if not groups:
            # Detailkan produk yang kosong untuk membantu debugging
            empties = []
            for prod_id, qty_needed in product_qty.items():
                product = self.env['product.product'].browse(prod_id)
                total_avail = 0.0
                for stage in _STAGE_ORDER:
                    total_avail += self._available_in_location(product, stage_locs[stage], company)
                for loc in self._receipt_dest_locations():
                    total_avail += self._available_in_location(product, loc, company)
                if total_avail <= 0:
                    empties.append(product.display_name)
            msg = _("No available quantities found in any logistic stage or receipt destinations for selected products.")
            if empties:
                msg += _("\nEmpty: %s") % ", ".join(empties[:10])
            raise UserError(msg)

        # 3) Buat 1 picking per (src, dst)
        created_picking_ids = []
        pt = self._internal_picking_type(company)
        if not pt:
            raise UserError(_("No internal picking type found."))

        for (src_id, dst_id), move_vals in groups.items():
            picking_vals = {
                'picking_type_id': pt.id,
                'location_id': src_id,
                'location_dest_id': dst_id,
                'scheduled_date': date_dt,
                'origin': _('Picking List Auto Stage'),
                'company_id': company.id,
                'move_ids_without_package': [(0, 0, vals) for vals in move_vals],
            }
            picking = Picking.create(picking_vals)
            created_picking_ids.append(picking.id)

            # Confirm & Assign (boleh gagal assign; kita pakai qty_done)
            try:
                picking.action_confirm()
                picking.action_assign()
            except Exception:
                pass

            # Pastikan ADA qty_done (baik di move maupun move_line bila perlu)
            for mv in picking.move_lines:
                demand = mv.product_uom_qty
                if demand <= 0:
                    continue

                # Untuk tipe yang tidak show operations, Odoo cek mv.quantity_done
                mv.quantity_done = demand

                # Jika show operations atau produk tracked, isi move_line juga
                need_lines = bool(picking.picking_type_id.show_operations or mv.product_id.tracking != 'none')
                if need_lines:
                    if not mv.move_line_ids:
                        MoveLine.create({
                            'move_id': mv.id,
                            'product_id': mv.product_id.id,
                            'product_uom_id': mv.product_uom.id,
                            'qty_done': demand,
                            'location_id': src_id,
                            'location_dest_id': dst_id,
                            'date': date_dt,
                        })
                    else:
                        for mvl in mv.move_line_ids:
                            mvl.qty_done = demand
                            mvl.location_id = src_id
                            mvl.location_dest_id = dst_id
                            mvl.date = date_dt

                mv.date = date_dt

            if self.auto_validate:
                picking.button_validate()
                try:
                    picking.write({'date_done': date_dt})
                except Exception:
                    pass

        # 4) Kembalikan action
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        if len(created_picking_ids) == 1:
            action.update({'view_mode': 'form', 'res_id': created_picking_ids[0], 'domain': [('id', '=', created_picking_ids[0])]})
        else:
            action.update({'domain': [('id', 'in', created_picking_ids)]})
        return action