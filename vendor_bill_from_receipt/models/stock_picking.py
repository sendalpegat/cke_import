# from odoo import models, fields, api
# from odoo.exceptions import UserError

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     def action_create_vendor_bill(self):
#         """Action to create a vendor bill manually for a single picking."""
#         self.ensure_one()
#         if self.picking_type_code != 'incoming':
#             raise UserError("This action is only available for incoming shipments.")
#         if not self.partner_id:
#             raise UserError("No vendor specified for this receipt.")

#         existing_invoice = self.env['account.move'].search([
#             ('invoice_origin', '=', self.name),
#             ('move_type', '=', 'in_invoice'),
#             ('state', '!=', 'cancel'),
#         ])
#         if existing_invoice:
#             raise UserError("A vendor bill has already been created for this receipt.")

#         invoice_vals = {
#             'partner_id': self.partner_id.id,
#             'invoice_date': fields.Date.today(),
#             'move_type': 'in_invoice',
#             'invoice_origin': self.name,
#             'invoice_line_ids': [],
#         }

#         for move in self.move_ids_without_package:
#             product = move.product_id
#             price_unit = product.standard_price or 0.0
#             invoice_line_vals = {
#                 'product_id': product.id,
#                 'quantity': move.quantity_done or move.product_uom_qty,
#                 'price_unit': price_unit,
#                 'name': product.name,
#                 'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
#             }
#             invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

#         if invoice_vals['invoice_line_ids']:
#             invoice = self.env['account.move'].create(invoice_vals)
#             return {
#                 'type': 'ir.actions.act_window',
#                 'res_model': 'account.move',
#                 'res_id': invoice.id,
#                 'view_mode': 'form',
#                 'target': 'current',
#             }
#         else:
#             raise UserError("No products with quantities received to create a vendor bill.")

#     def action_create_multiple_vendor_bills(self):
#         """Create a single vendor bill from multiple selected pickings."""
#         active_ids = self.env.context.get('active_ids', [])
#         pickings = self.env['stock.picking'].browse(active_ids)

#         # Filter hanya incoming shipment dan yang punya partner
#         valid_pickings = pickings.filtered(
#             lambda p: p.picking_type_code == 'incoming' and p.partner_id
#         )

#         if not valid_pickings:
#             raise UserError("Tidak ada penerimaan yang valid untuk dibuat faktur.")

#         # Cek apakah sudah ada invoice untuk origin tertentu
#         existing_invoices = self.env['account.move'].search([
#             ('invoice_origin', 'in', valid_pickings.mapped('name')),
#             ('move_type', '=', 'in_invoice'),
#             ('state', '!=', 'cancel'),
#         ])
#         existing_origins = set(existing_invoices.mapped('invoice_origin'))

#         # Ambil semua baris faktur
#         invoice_line_vals = []
#         partner = False

#         for picking in valid_pickings:
#             if picking.name in existing_origins:
#                 continue  # Lewati jika sudah ada faktur

#             if not partner:
#                 partner = picking.partner_id
#             elif picking.partner_id != partner:
#                 raise UserError("Semua penerimaan harus memiliki vendor yang sama.")

#             for move in picking.move_ids_without_package:
#                 product = move.product_id
#                 price_unit = product.standard_price or 0.0
#                 invoice_line_vals.append((0, 0, {
#                     'product_id': product.id,
#                     'quantity': move.product_uom_qty,
#                     'price_unit': price_unit,
#                     'name': f"{product.name} - {picking.name}",
#                     'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
#                 }))

#         if not invoice_line_vals:
#             raise UserError("Tidak ada produk untuk dibuatkan vendor bill.")

#         # Buat satu faktur
#         invoice_vals = {
#             'partner_id': partner.id,
#             'invoice_date': fields.Date.today(),
#             'move_type': 'in_invoice',
#             'invoice_origin': ', '.join(p.name for p in valid_pickings if p.name not in existing_origins),
#             'invoice_line_ids': invoice_line_vals,
#         }

#         invoice = self.env['account.move'].create(invoice_vals)

#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'account.move',
#             'res_id': invoice.id,
#             'view_mode': 'form',
#             'target': 'current',
#         }
    
from odoo import models, fields, api
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_create_vendor_bill(self):
        """Action to create a vendor bill manually for a single picking."""
        self.ensure_one()
        if self.picking_type_code != 'incoming':
            raise UserError("This action is only available for incoming shipments.")
        if not self.partner_id:
            raise UserError("No vendor specified for this receipt.")

        existing_invoice = self.env['account.move'].search([
            ('invoice_origin', '=', self.name),
            ('move_type', '=', 'in_invoice'),
            ('state', '!=', 'cancel'),
        ])
        if existing_invoice:
            raise UserError("A vendor bill has already been created for this receipt.")

        purchase_order = False
        if self.origin:
            # self.origin biasanya nama PO
            purchase_order = self.env['purchase.order'].search([('name', '=', self.origin)], limit=1)

        invoice_vals = {
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': self.name,
            'invoice_line_ids': [],
            'purchase_id': purchase_order.id if purchase_order else False,
        }

        for move in self.move_ids_without_package:
            product = move.product_id
            price_unit = product.standard_price or 0.0
            invoice_line_vals = {
                'product_id': product.id,
                'quantity': move.quantity_done or move.product_uom_qty,
                'price_unit': price_unit,
                'name': product.name,
                'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
            }
            invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

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

    def action_create_multiple_vendor_bills(self):
        """Create a single vendor bill from multiple selected pickings."""
        active_ids = self.env.context.get('active_ids', [])
        pickings = self.env['stock.picking'].browse(active_ids)

        # Filter hanya incoming shipment dan yang punya partner
        valid_pickings = pickings.filtered(
            lambda p: p.picking_type_code == 'incoming' and p.partner_id
        )

        if not valid_pickings:
            raise UserError("Tidak ada penerimaan yang valid untuk dibuat faktur.")

        # Cek apakah sudah ada invoice untuk origin tertentu
        existing_invoices = self.env['account.move'].search([
            ('invoice_origin', 'in', valid_pickings.mapped('name')),
            ('move_type', '=', 'in_invoice'),
            ('state', '!=', 'cancel'),
        ])
        existing_origins = set(existing_invoices.mapped('invoice_origin'))

        # Ambil semua baris faktur
        invoice_line_vals = []
        partner = False

        for picking in valid_pickings:
            if picking.name in existing_origins:
                continue  # Lewati jika sudah ada faktur

            if not partner:
                partner = picking.partner_id
            elif picking.partner_id != partner:
                raise UserError("Semua penerimaan harus memiliki vendor yang sama.")

            for move in picking.move_ids_without_package:
                product = move.product_id
                price_unit = product.standard_price or 0.0
                invoice_line_vals.append((0, 0, {
                    'product_id': product.id,
                    'quantity': move.product_uom_qty,
                    'price_unit': price_unit,
                    'name': f"{product.name} - {picking.name}",
                    'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
                }))

        if not invoice_line_vals:
            raise UserError("Tidak ada produk untuk dibuatkan vendor bill.")

        # Buat satu faktur
        invoice_vals = {
            'partner_id': partner.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': ', '.join(p.name for p in valid_pickings if p.name not in existing_origins),
            'invoice_line_ids': invoice_line_vals,
        }

        invoice = self.env['account.move'].create(invoice_vals)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }

# from odoo import models, fields, api
# from odoo.exceptions import UserError


# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     def action_create_vendor_bill(self):
#         """Action to create a vendor bill manually."""
#         self.ensure_one()

#         # Pastikan picking adalah tipe receipt (incoming shipment)
#         if self.picking_type_code != 'incoming':
#             raise UserError("This action is only available for incoming shipments.")

#         if not self.partner_id:
#             raise UserError("No vendor specified for this receipt.")

#         # Cek apakah sudah ada invoice yang dibuat untuk picking ini
#         # existing_invoice = self.env['account.move'].search([
#         #     ('invoice_origin', '=', self.name),
#         #     ('move_type', '=', 'in_invoice'),
#         #     ('state', '!=', 'cancel'),
#         # ])
#         # if existing_invoice:
#         #     raise UserError("A vendor bill has already been created for this receipt.")

#         # Persiapkan data untuk invoice
#         invoice_vals = {
#             'partner_id': self.partner_id.id,
#             'invoice_date': fields.Date.today(),
#             'move_type': 'in_invoice',
#             'invoice_origin': self.name,
#             'invoice_line_ids': [],
#         }

#         # Tambahkan baris invoice berdasarkan move lines
#         for move in self.move_ids_without_package:
#             product = move.product_id

#             # Gunakan standard_price sebagai price_unit
#             price_unit = product.standard_price or 0.0

#             invoice_line_vals = {
#                 'product_id': product.id,
#                 'quantity': move.quantity_done,
#                 'price_unit': price_unit,
#                 'name': product.name,
#                 'account_id': product.property_account_expense_id.id or product.categ_id.property_account_expense_categ_id.id,
#             }
#             invoice_vals['invoice_line_ids'].append((0, 0, invoice_line_vals))

#         # Buat invoice
#         if invoice_vals['invoice_line_ids']:
#             invoice = self.env['account.move'].create(invoice_vals)
#             return {
#                 'type': 'ir.actions.act_window',
#                 'res_model': 'account.move',
#                 'res_id': invoice.id,
#                 'view_mode': 'form',
#                 'target': 'current',
#             }
#         else:
#             raise UserError("No products with quantities received to create a vendor bill.")