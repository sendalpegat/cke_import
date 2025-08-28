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

    stage_current = fields.Selection(
        selection=_STAGE_SELECTION,
        string='Stage',
        compute='_compute_stage_tracking',
        store=False
    )
    stage_from = fields.Selection(
        selection=_STAGE_SELECTION,
        string='From Stage',
        compute='_compute_stage_tracking',
        store=False
    )
    stage_to = fields.Selection(
        selection=_STAGE_SELECTION,
        string='To Stage',
        compute='_compute_stage_tracking',
        store=False
    )
    stage_move_date = fields.Date(
        string='Stage Date',
        compute='_compute_stage_tracking',
        store=False
    )

    # ---------- helpers ----------
    def _stage_locations(self):
        """Ambil/siapkan lokasi stage. Tidak masalah jika modul stage belum diinstal; kita cari by xmlid, lalu by name, terakhir buat baru."""
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
        # root transit (opsional)
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

    # ---------- compute (DIPERKETAT) ----------
    @api.depends('product_id', 'company_id', 'picking_id', 'reference', 'po_reference', 'date')
    def _compute_stage_tracking(self):
        """
        Prinsip:
        - DEFAULT = 'loaded'.
        - Stage baru berubah jika ada internal move antar stage YANG TERKAIT dokumen ini.
          Keterkaitan kita batasi KERAS: origin mengandung 'PO:<po_reference>' atau reference == <po_reference>.
        - Tidak ada lagi fallback ke QUANT, sehingga stok global di Gudang VSJ tidak mempengaruhi dokumen ini.
        """
        Move = self.env['stock.move']
        for rec in self:
            rec.stage_current = 'loaded'
            rec.stage_from = False
            rec.stage_to = False
            rec.stage_move_date = False

            if not rec.product_id or rec.product_id.type not in ('product', 'consu'):
                continue

            # PO dokumen ini
            po_ref = getattr(rec, 'po_reference', False)
            if not po_ref:
                # tanpa PO, kita tidak bisa mengikat perpindahan antar stage → tetap 'loaded'
                # (set stage_move_date kira-kira dari receipt jika ada)
                if rec.picking_id and rec.picking_id.date_done:
                    try:
                        rec.stage_move_date = fields.Date.to_date(rec.picking_id.date_done)
                    except Exception:
                        pass
                continue

            stage_locs = rec._stage_locations()
            stage_loc_ids = [s.id for s in stage_locs.values()]

            # Cari internal move TERKAIT PO INI (origin ditulis wizard sebagai 'PO:<po_ref> | ...')
            domain = [
                ('product_id', '=', rec.product_id.id),
                ('company_id', '=', rec.company_id.id),
                ('picking_id.picking_type_id.code', '=', 'internal'),
                ('location_id', 'in', stage_loc_ids),
                ('location_dest_id', 'in', stage_loc_ids),
                '|', ('origin', 'ilike', 'PO:%s' % po_ref), ('reference', '=', po_ref),
            ]
            # (opsional) batasi waktu minimal setelah receipt move ini
            if rec.date:
                domain.append(('date', '>=', rec.date))

            last = Move.search(domain, order='date desc, id desc', limit=1)
            if not last:
                # belum ada transfer antar stage untuk PO ini → tetap 'loaded'
                if rec.picking_id and rec.picking_id.date_done:
                    try:
                        rec.stage_move_date = fields.Date.to_date(rec.picking_id.date_done)
                    except Exception:
                        pass
                continue

            from_stage = rec._map_location_to_stage(last.location_id, stage_locs)
            to_stage = rec._map_location_to_stage(last.location_dest_id, stage_locs)

            rec.stage_from = from_stage or False
            rec.stage_to = to_stage or False
            rec.stage_current = to_stage or from_stage or 'loaded'
            try:
                rec.stage_move_date = fields.Date.to_date(last.date) if last.date else False
            except Exception:
                rec.stage_move_date = False