from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_bill_count = fields.Integer(string="Vendor Bills", compute='_compute_vendor_bill_count')

    def _compute_vendor_bill_count(self):
        for order in self:
            order.vendor_bill_count = self.env['account.move'].search_count([
                ('purchase_id', '=', order.id),
                ('move_type', '=', 'in_invoice'),
                ('state', '!=', 'cancel'),
            ])

    def action_view_vendor_bills(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vendor Bills',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('purchase_id', '=', self.id), ('move_type', '=', 'in_invoice')],
            'context': {
                'default_purchase_id': self.id,
                'create': False
            },
        }