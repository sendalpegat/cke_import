# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

STAGES = [
    ('loaded', 'Loaded'),
    ('boarded', 'Boarded'),
    ('customs', 'Customs'),
    ('arrived', 'Arrived'),
    ('gudang_vsj', 'Gudang VSJ'),
]

class LogisticStageMoveWizard(models.TransientModel):
    _name = 'logistic.stage.move.wizard'
    _description = 'Move Logistic Stage (Internal Transfer)'

    move_id = fields.Many2one('account.move', string='Vendor Bill', required=True)
    current_stage = fields.Selection(STAGES, string='Current', required=True, readonly=True)
    target_stage = fields.Selection(STAGES, string='Target Stage', required=True)
    move_date = fields.Datetime(string='Move Date/Time', required=True, default=fields.Datetime.now)
    auto_validate = fields.Boolean(string='Validate Transfer Now', default=True)

    # Pemetaan stage -> lokasi
    def _stage_location(self, stage):
        if stage == 'boarded':
            return self.env.ref('cke_logistic_stage_flow.loc_boarded')
        if stage == 'customs':
            return self.env.ref('cke_logistic_stage_flow.loc_customs')
        if stage == 'arrived':
            return self.env.ref('cke_logistic_stage_flow.loc_arrived')
        if stage == 'gudang_vsj':
            return self.env.ref('cke_logistic_stage_flow.loc_gudang_vsj')
        return None  # loaded: gunakan lokasi stok hasil receipt

    def _default_internal_picking_type(self, company):
        # cari picking type internal di perusahaan aktif
        pt = self.env['stock.picking.type'].search([
            ('code', '=', 'internal'),
            ('warehouse_id.company_id', '=', company.id)
        ], limit=1)
        if pt:
            return pt
        # fallback: tipe internal manapun
        return self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

    def _source_location_for_loaded(self):
        """
        Ambil lokasi stok hasil receipt:
        - dari receipts (picking_ids) yang dikumpulkan modul cke_vendor_bill_receipts
        - pakai location_dest_id dari receipt pertama
        """
        move = self.move_id
        picks = move.picking_ids  # dari modul cke_vendor_bill_receipts
        if not picks:
            # fallback: warehouse utama perusahaan
            wh = self.env['stock.warehouse'].search([('company_id', '=', move.company_id.id)], limit=1)
            return wh.lot_stock_id if wh else None
        # pakai lokasi tujuan receipt pertama
        return picks[0].location_dest_id

    def _current_stage_location(self):
        if self.current_stage == 'loaded':
            return self._source_location_for_loaded()
        return self._stage_location(self.current_stage)

    @api.constrains('current_stage', 'target_stage')
    def _check_transition(self):
        for w in self:
            if w.current_stage == w.target_stage:
                raise UserError(_("Target stage must be different from current stage."))

    def action_confirm(self):
        self.ensure_one()
        bill = self.move_id
        if bill.state != 'posted' or bill.move_type != 'in_invoice':
            raise UserError(_("Only available on posted Vendor Bills."))

        src_loc = self._current_stage_location()
        dst_loc = self._stage_location(self.target_stage)
        if self.target_stage == 'loaded':
            raise UserError(_("Target 'Loaded' is not allowed (it's the initial stage)."))
        if not src_loc or not dst_loc:
            raise UserError(_("Source/Destination location is not configured."))

        # Ambil list produk dari Picking List (receipt_move_ids) modul cke_vendor_bill_receipts
        receipt_moves = bill.receipt_move_ids.filtered(lambda m: m.product_id and m.product_id.type in ('product', 'consu'))
        if not receipt_moves:
            raise UserError(_("No products found in Picking List."))

        pt = self._default_internal_picking_type(bill.company_id)
        if not pt:
            raise UserError(_("No internal picking type found."))

        # Siapkan moves (pindahkan total qty_done dari tiap produk)
        move_vals = []
        for rm in receipt_moves:
            qty = rm.quantity_done or rm.product_uom_qty
            if qty <= 0:
                continue
            move_vals.append({
                'name': rm.product_id.display_name,
                'product_id': rm.product_id.id,
                'product_uom': rm.product_uom.id,
                'product_uom_qty': qty,
                'location_id': src_loc.id,
                'location_dest_id': dst_loc.id,
                'date': self.move_date,
                'company_id': bill.company_id.id,
                'origin': bill.name or bill.ref or 'Vendor Bill',
            })
        if not move_vals:
            raise UserError(_("All product quantities are zero."))

        picking_vals = {
            'picking_type_id': pt.id,
            'location_id': src_loc.id,
            'location_dest_id': dst_loc.id,
            'scheduled_date': self.move_date,
            'origin': bill.name or bill.ref or '',
            'move_ids_without_package': [(0, 0, vals) for vals in move_vals],
            'company_id': bill.company_id.id,
        }
        picking = self.env['stock.picking'].create(picking_vals)

        # Confirm & (opsional) validate sekarang
        picking.action_confirm()
        picking.action_assign()
        if self.auto_validate:
            # set qty_done pada move lines = product_uom_qty
            for mv in picking.move_lines:
                # buat move_line jika belum ada
                if not mv.move_line_ids:
                    self.env['stock.move.line'].create({
                        'move_id': mv.id,
                        'product_id': mv.product_id.id,
                        'product_uom_id': mv.product_uom.id,
                        'qty_done': mv.product_uom_qty,
                        'location_id': src_loc.id,
                        'location_dest_id': dst_loc.id,
                        'lot_id': False,
                        'lot_name': False,
                        'date': self.move_date,
                    })
                else:
                    for mvl in mv.move_line_ids:
                        # set semua ke qty_done penuh
                        mvl.qty_done = mv.product_uom_qty
                        mvl.date = self.move_date
                mv.date = self.move_date
            # validasi
            res = picking.button_validate()
            # set tanggal selesai (best effort)
            try:
                picking.write({'date_done': self.move_date})
            except Exception:
                pass

        # Update stage di Vendor Bill
        bill.logistic_state = self.target_stage

        # Tampilkan picking yang baru dibuat
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('id', '=', picking.id)]
        action.update({'view_mode': 'form', 'res_id': picking.id})
        return action