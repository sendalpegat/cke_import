from odoo import api, models, fields

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase_order_ref = fields.Char(
        string='PO Reference',
        compute='_compute_purchase_order_ref',
        store=True
    )

    @api.depends('move_id.purchase_id')
    def _compute_purchase_order_ref(self):
        for line in self:
            line.purchase_order_ref = line.move_id.purchase_id.name if line.move_id.purchase_id else False