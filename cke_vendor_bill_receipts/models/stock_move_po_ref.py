# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Tetap simpan nomor PO agar tampil di Picking List
    po_reference = fields.Char(string='PO', compute='_compute_po_reference', store=True, index=True)

    @api.depends('picking_id', 'picking_id.origin', 'picking_id.name', 'group_id')
    def _compute_po_reference(self):
        for sm in self:
            po_name = False
            pk = sm.picking_id

            # (1) dari picking (product_bundle_pack mungkin isi field-field ini)
            if pk:
                for f in ('purchase_id', 'po_id', 'x_purchase_id'):
                    if f in pk._fields:
                        rec = getattr(pk, f)
                        if rec:
                            try:
                                po_name = rec.name
                            except Exception:
                                po_name = False
                            if po_name:
                                break
                if not po_name and 'x_po_reference' in pk._fields and getattr(pk, 'x_po_reference'):
                    po_name = pk.x_po_reference

            # (2) kalau ada purchase_stock
            if not po_name and 'purchase_line_id' in sm._fields:
                try:
                    if sm.purchase_line_id and getattr(sm.purchase_line_id, 'order_id', False):
                        po_name = sm.purchase_line_id.order_id.name
                except Exception:
                    po_name = False

            # (3) procurement group
            if not po_name and 'group_id' in sm._fields and sm.group_id and sm.group_id.name:
                po_name = sm.group_id.name

            # (4) fallback dari origin
            if not po_name and pk and pk.origin:
                origin = pk.origin or ''
                tokens = [t.strip() for t in re.split(r'[,;/\s]+', origin) if t.strip()]
                po_like = next((t for t in tokens if t.upper().startswith('PO')), None)
                po_name = po_like or origin

            sm.po_reference = po_name or False

    @api.model_create_multi
    def create(self, vals_list):
        # FAST-PATH: isi reference sebelum super() agar tidak ada write kedua
        Pol = self.env['purchase.order.line']
        for vals in vals_list:
            # hanya incoming picking yang relevan
            # (kalau belum tahu picking_type_id di sini, tetap aman – kita isi reference jika bisa)
            if not vals.get('reference'):
                po_name = False
                # pakai purchase_line_id jika ada (umum saat create dari PO)
                pol_id = vals.get('purchase_line_id')
                if pol_id:
                    pol = Pol.browse(pol_id)
                    if pol and pol.order_id:
                        po_name = pol.order_id.name
                # fallback: biarkan _compute_po_reference yang isi (akan jalan setelah create)
                if po_name:
                    vals['reference'] = po_name
        return super().create(vals_list)

    def write(self, vals):
        # HAPUS sinkronisasi agresif ke 'reference' supaya tidak menambah beban
        # (po_reference tetap terhitung otomatis via compute)
        return super().write(vals)