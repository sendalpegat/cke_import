# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

_STAGE_SELECTION = [
    ('loaded', 'Loaded'),
    ('boarded', 'Boarded'),
    ('customs', 'Customs'),
    ('arrived', 'Arrived'),
    ('gudang_vsj', 'Gudang VSJ'),
]
_STAGE_ORDER = ['loaded', 'boarded', 'customs', 'arrived', 'gudang_vsj']


class StockMoveStageInfo(models.Model):
    _inherit = 'stock.move'

    # Stage info (compute-only)
    stage_current = fields.Selection(_STAGE_SELECTION, string='Stage', compute='_compute_stage_tracking', store=False)
    stage_from = fields.Selection(_STAGE_SELECTION, string='From Stage', compute='_compute_stage_tracking', store=False)
    stage_to = fields.Selection(_STAGE_SELECTION, string='To Stage', compute='_compute_stage_tracking', store=False)
    stage_move_date = fields.Date(string='Stage Date', compute='_compute_stage_tracking', store=False)

    # Badge HTML (pakai class Bootstrap: btn-*)
    stage_badge_html = fields.Html(
        string='Stage',
        compute='_compute_stage_tracking',
        sanitize=False,  # biar class "btn ..." tidak disterilkan
        store=False,
    )

    # Container number (diambil dari modul lain secara defensif)
    container_number = fields.Char(
        string='Container #',
        compute='_compute_container_number',
        store=False,
        help="Diambil dari picking atau PO (modul purchase_advance_payment)."
    )

    # ---------- helpers ----------
    def _stage_locations(self):
        Location = self.env['stock.location']
        out = {}
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
        root = Location.search([('name', '=', 'Logistics Transit'), ('usage', '=', 'internal')], limit=1)
        if not root:
            root = Location.create({'name': 'Logistics Transit', 'usage': 'internal'})

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

    def _map_location_to_stage(self, loc, stage_locs):
        if not loc:
            return False
        for stage, s_loc in stage_locs.items():
            if loc.id == s_loc.id:
                return stage
        return False

    # ---------- compute stage + badge ----------
    @api.depends('product_id', 'company_id', 'picking_id', 'reference', 'po_reference', 'date')
    def _compute_stage_tracking(self):
        """
        Prinsip:
        - DEFAULT: 'loaded'.
        - Stage berganti hanya jika ada internal move antar stage yang TERKAIT dokumen (origin mengandung 'PO:<po_ref>' atau reference == <po_ref>).
        - Tidak membaca QUANT global (menghindari nyasar ke Gudang VSJ).
        - Badge HTML dibentuk sesuai stage_current dengan class 'btn-*'.
        """
        Move = self.env['stock.move']
        label_map = dict(_STAGE_SELECTION)
        class_map = {
            'loaded':     'btn btn-secondary btn-xs',
            'boarded':    'btn btn-warning btn-xs',
            'customs':    'btn btn-danger btn-xs',
            'arrived':    'btn btn-primary btn-xs',
            'gudang_vsj': 'btn btn-success btn-xs',
        }

        for rec in self:
            # default
            rec.stage_current = 'loaded'
            rec.stage_from = False
            rec.stage_to = False
            rec.stage_move_date = False
            rec.stage_badge_html = '<span class="btn btn-secondary btn-xs">Loaded</span>'

            if not rec.product_id or rec.product_id.type not in ('product', 'consu'):
                continue

            po_ref = getattr(rec, 'po_reference', False)
            if not po_ref:
                if rec.picking_id and rec.picking_id.date_done:
                    try:
                        rec.stage_move_date = fields.Date.to_date(rec.picking_id.date_done)
                    except Exception:
                        pass
                # badge already set to Loaded
                continue

            stage_locs = rec._stage_locations()
            stage_loc_ids = [s.id for s in stage_locs.values()]

            domain = [
                ('product_id', '=', rec.product_id.id),
                ('company_id', '=', rec.company_id.id),
                ('picking_id.picking_type_id.code', '=', 'internal'),
                ('location_id', 'in', stage_loc_ids),
                ('location_dest_id', 'in', stage_loc_ids),
                '|', ('origin', 'ilike', 'PO:%s' % po_ref), ('reference', '=', po_ref),
            ]
            if rec.date:
                domain.append(('date', '>=', rec.date))

            last = Move.search(domain, order='date desc, id desc', limit=1)
            if last:
                from_stage = rec._map_location_to_stage(last.location_id, stage_locs)
                to_stage = rec._map_location_to_stage(last.location_dest_id, stage_locs)

                rec.stage_from = from_stage or False
                rec.stage_to = to_stage or False
                rec.stage_current = to_stage or from_stage or 'loaded'
                try:
                    rec.stage_move_date = fields.Date.to_date(last.date) if last.date else False
                except Exception:
                    rec.stage_move_date = False

            # build badge
            label = label_map.get(rec.stage_current, rec.stage_current or '')
            klass = class_map.get(rec.stage_current, 'btn btn-light btn-xs')
            rec.stage_badge_html = '<span class="%s">%s</span>' % (klass, label)

    # ---------- compute container ----------
    @api.depends('picking_id', 'picking_id.write_date', 'purchase_line_id', 'purchase_line_id.order_id')
    def _compute_container_number(self):
        """
        Cari 'container_number' dari:
        1) stock.picking (jika field ada, mis. ditambah modul purchase_advance_payment)
        2) purchase.order (via purchase_line_id.order_id) dengan berbagai kemungkinan nama field
        """
        for sm in self:
            val = False
            # 1) dari picking
            pk = sm.picking_id
            if pk:
                for fname in ('container_number', 'container_no', 'x_container_number', 'x_container_no'):
                    if fname in pk._fields:
                        v = getattr(pk, fname)
                        if v:
                            val = v
                            break
            # 2) dari PO
            if not val and 'purchase_line_id' in sm._fields and sm.purchase_line_id and sm.purchase_line_id.order_id:
                po = sm.purchase_line_id.order_id
                for fname in ('container_number', 'container_no', 'x_container_number', 'x_container_no'):
                    if fname in po._fields:
                        v = getattr(po, fname)
                        if v:
                            val = v
                            break
            sm.container_number = val or False