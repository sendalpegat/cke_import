from odoo import fields, models, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    purchase_order_ref = fields.Char(
        string='PO Reference',
        compute='_compute_purchase_order_ref',
        store=True
    )

    @api.depends('origin')
    def _compute_purchase_order_ref(self):
        for move in self:
            move.purchase_order_ref = move.origin