from odoo import api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('order_id.partner_id')
    def _onchange_vendor(self):
        if self.order_id.partner_id:
            # Filter products based on vendor
            return {
                'domain': {
                    'product_id': [
                        ('seller_ids.name', '=', self.order_id.partner_id.id)
                    ]
                }
            }
        else:
            return {'domain': {'product_id': []}}