from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    purchase_id = fields.Many2one('purchase.order', string='Purchase Order', readonly=True)

    def action_post(self):
        res = super(AccountMove, self).action_post()

        for invoice in self:
            if invoice.move_type != 'in_invoice':
                continue

            origin = invoice.invoice_origin
            if not origin:
                continue

            # Relasi ke Purchase Order
            purchase = self.env['purchase.order'].search([('name', '=', origin)], limit=1)
            if purchase:
                invoice.purchase_id = purchase

            picking = self.env['stock.picking'].search([('name', '=', origin)], limit=1)
            if not picking or picking.state != 'assigned':
                continue

            invoice_lines_data = {}
            for line in invoice.invoice_line_ids:
                if line.product_id and line.quantity > 0:
                    invoice_lines_data[line.product_id.id] = line.quantity

            if not invoice_lines_data:
                continue

            updated_moves = self.env['stock.move']
            for move in picking.move_ids_without_package:
                inv_qty = invoice_lines_data.get(move.product_id.id, 0.0)
                if inv_qty > 0:
                    move.write({'quantity_done': inv_qty})
                    updated_moves |= move

            if not updated_moves:
                continue

            try:
                picking.button_validate()
            except Exception as e:
                raise UserError("Gagal memvalidasi penerimaan: %s" % str(e))

            remaining_moves = picking.move_ids_without_package.filtered(
                lambda m: m.product_uom_qty > m.quantity_done)
            if remaining_moves:
                backorder_wizard = self.env['stock.backorder.confirmation'].create({
                    'picking_id': picking.id,
                })
                backorder_wizard.process()

        return res

    @api.model
    def create(self, vals):
        # Auto cari dan set purchase_id jika invoice dibuat dari receipt
        if not vals.get('purchase_id') and vals.get('invoice_origin'):
            picking = self.env['stock.picking'].search([('name', '=', vals['invoice_origin'])], limit=1)
            if picking and picking.origin:
                purchase = self.env['purchase.order'].search([('name', '=', picking.origin)], limit=1)
                if purchase:
                    vals['purchase_id'] = purchase.id
        return super(AccountMove, self).create(vals)