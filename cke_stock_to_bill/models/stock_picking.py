from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    def action_create_vendor_bill(self):
        for picking in self:
            if picking.picking_type_id.code == 'incoming' and picking.state == 'assigned':
                purchase_order = picking.purchase_id
                if purchase_order:
                    # Create vendor bill
                    move_lines = []
                    for move in picking.move_ids_without_package:
                        purchase_line = move.purchase_line_id
                        if purchase_line:
                            account = move.product_id.product_tmpl_id.get_product_accounts()['expense']
                            move_lines.append((0, 0, {
                                'product_id': move.product_id.id,
                                'name': move.product_id.name,
                                'quantity': move.quantity_done,
                                'price_unit': purchase_line.price_unit,
                                'account_id': account.id,
                                'tax_ids': [(6, 0, purchase_line.taxes_id.ids)],
                            }))
                    
                    bill = self.env['account.move'].create({
                        'move_type': 'in_invoice',
                        'partner_id': picking.partner_id.id,
                        'invoice_date': fields.Date.today(),
                        'invoice_origin': picking.name,
                        'purchase_id': purchase_order.id,
                        'journal_id': self.env['account.journal'].search([('type', '=', 'purchase')], limit=1).id,
                        'invoice_line_ids': move_lines,
                    })
                    
                    # Add link between bill and picking
                    picking.message_post(body=f"Vendor Bill Created: {bill.name}")
        return True