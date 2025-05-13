from odoo import models, fields, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_create_vendor_bill(self):
        """Action to create a vendor bill manually."""
        self.ensure_one()

        # Pastikan picking adalah tipe receipt (incoming shipment)
        if self.picking_type_code != 'incoming':
            raise UserError("This action is only available for incoming shipments.")

        if not self.partner_id:
            raise UserError("No vendor specified for this receipt.")

        # Cek apakah sudah ada invoice yang dibuat untuk picking ini
        existing_invoice = self.env['account.move'].search([
            ('invoice_origin', '=', self.name),
            ('move_type', '=', 'in_invoice'),
            ('state', '!=', 'cancel'),
        ])
        if existing_invoice:
            raise UserError("A vendor bill has already been created for this receipt.")

        # Persiapkan data untuk invoice
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': self.name,
            'invoice_line_ids': [],
        }

        # Tambahkan baris invoice berdasarkan move lines
        for move in self.move_ids_without_package:
            if move.purchase_line_id:
                price_unit = move.purchase_line_id.price_unit
            else:
                price_unit = 0.0

            invoice_line_vals = {
                'product_id': move.product_id.id,
                'quantity': move.quantity_done,
                'price_unit': price_unit,
                'name': move.product_id.name,
                'account_id': move.product_id.property_account_expense_id.id or move.product_id.categ_id.property_account_expense_categ_id.id,
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

        # Buat invoice
        if invoice_vals['invoice_line_ids']:
            invoice = self.env['account.move'].create(invoice_vals)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            raise UserError("No products with quantities received to create a vendor bill.")