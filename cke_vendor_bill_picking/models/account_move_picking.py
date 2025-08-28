# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    picking_ids = fields.Many2many('stock.picking', string='Receipts', copy=False)

    def _get_incoming_picking_type(self):
        """Cari Picking Type incoming sesuai company dokumen."""
        self.ensure_one()
        company = self.company_id or self.env.company
        # Prioritas: gudang perusahaan dokumen
        wh = self.env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
        if wh and wh.in_type_id:
            return wh.in_type_id
        # Fallback: tipe 'incoming' di company yang sama
        return self.env['stock.picking.type'].search([
            ('code', '=', 'incoming'),
            ('warehouse_id.company_id', '=', company.id)
        ], limit=1)

    def action_view_pickings(self):
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        if len(self.picking_ids) == 1:
            action.update({'view_mode': 'form', 'res_id': self.picking_ids.id})
        return action

    def action_create_picking_from_bill(self):
        """
        Buat Incoming Picking dari Vendor Bill yang sudah posted.
        - Hanya baris product type 'product' atau 'consu'
        - Skip display_type (section/note)
        - Konversi UoM dari invoice line ke UoM produk
        """
        for move in self:
            if move.state != 'posted' or move.move_type != 'in_invoice':
                raise UserError(_("This button is only available on posted Vendor Bills."))

            # Jika ada picking dari PO yang masih open (opsional jika ada custom relasi)
            po_pickings = self.env['stock.picking']
            if hasattr(move, 'purchase_id') and move.purchase_id:
                po_pickings = move.purchase_id.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))
            if po_pickings:
                move.picking_ids = [(6, 0, po_pickings.ids)]
                continue  # lanjut next move, lalu tampilkan action di bawah

            picking_type = move._get_incoming_picking_type()
            if not picking_type:
                raise UserError(_("No incoming picking type found for company %s.") % (move.company_id.display_name,))

            partner = move.partner_id
            # Lokasi supplier
            src_loc = partner.property_stock_supplier.id
            # Lokasi tujuan: dari picking_type; fallback ke lot_stock_id warehouse
            dst_loc = picking_type.default_location_dest_id.id or \
                      (picking_type.warehouse_id and picking_type.warehouse_id.lot_stock_id.id)
            if not dst_loc:
                raise UserError(_("No destination location configured for the incoming picking type."))

            # Ambil baris produk valid
            lines = move.invoice_line_ids.filtered(
                lambda l: not l.display_type
                and l.product_id
                and l.product_id.type in ('product', 'consu')
                and l.quantity > 0
            )
            if not lines:
                raise UserError(_("No stockable/consumable product lines found on this bill."))

            move_vals = []
            for line in lines:
                product = line.product_id
                product_uom = product.uom_id
                qty = line.quantity
                # Konversi UoM jika berbeda
                if line.product_uom_id and line.product_uom_id != product_uom:
                    qty = line.product_uom_id._compute_quantity(qty, product_uom)

                move_vals.append({
                    'name': line.name or product.display_name,
                    'product_id': product.id,
                    'product_uom': product_uom.id,
                    'product_uom_qty': qty,
                    'location_id': src_loc,
                    'location_dest_id': dst_loc,
                    'company_id': move.company_id.id,
                    'picking_type_id': picking_type.id,
                    'date': fields.Datetime.now(),
                    'origin': move.name or move.ref or move.invoice_origin or _('Vendor Bill'),
                })

            picking_vals = {
                'picking_type_id': picking_type.id,
                'partner_id': partner.id,
                'origin': move.name or move.ref or '',
                'location_id': src_loc,
                'location_dest_id': dst_loc,
                'company_id': move.company_id.id,
                'move_ids_without_package': [(0, 0, vals) for vals in move_vals],
            }
            picking = self.env['stock.picking'].create(picking_vals)
            move.picking_ids = [(4, picking.id)]

        # Tampilkan daftar picking untuk record aktif (single) atau pertama
        return self[0].action_view_pickings()