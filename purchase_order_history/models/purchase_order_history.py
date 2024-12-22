from odoo import api, models, fields

class PurchaseOrderHistory(models.Model):
    _name = 'purchase.order.history'
    _description = 'Purchase Order History'

    product_id = fields.Many2one('product.product', string='Product', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True, domain="[('supplier', '=', True)]")
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)
    date_approve = fields.Date(string='Order Date', compute='_compute_date_approve', store=True)
    quantity = fields.Float(related='purchase_order_id.order_line.product_qty', string='Quantity')
    price_unit = fields.Float(related='purchase_order_id.order_line.price_unit', string='Unit Price')

    @api.depends('purchase_order_id.date_approve')
    def _compute_date_approve(self):
        for record in self:
            record.date_approve = record.purchase_order_id.date_approve.date() if record.purchase_order_id.date_approve else False

    @api.model
    def _compute_history(self):
        # Logic for fetching data if required
        pass