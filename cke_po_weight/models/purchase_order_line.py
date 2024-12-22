from odoo import fields, models, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_weight = fields.Float(string='Weight', compute='_compute_product_weight')
    product_volume = fields.Float(string='Volume', compute='_compute_product_volume')

    @api.depends('product_id', 'product_qty')
    def _compute_product_weight(self):
        for record in self:
            record.product_weight = (record.product_id.weight * record.product_qty)

    def _compute_product_volume(self):
        for record in self:
            record.product_volume = (record.product_id.volume * record.product_qty)
