from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'stock.picking'

    demand_quantity = fields.Float(string="No. Demand Quantity", compute='_compute_total_quantity')
    done_quantity = fields.Float(string="No. Done Quantity", compute='_compute_total_quantity')

    def _compute_total_quantity(self):
        for delivery_order in self:
            delivery_order.demand_quantity = sum(delivery_order.move_ids_without_package.mapped('product_uom_qty'))
            delivery_order.done_quantity = sum(delivery_order.move_ids_without_package.mapped('quantity_done'))
