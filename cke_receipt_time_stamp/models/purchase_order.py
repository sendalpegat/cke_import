from odoo import models, api
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        self.env['delivery.status.stamp'].create({
            'purchase_id': res.id,
            'picking_id': None,
            'delivery_status': dict(res._fields['state'].selection).get(res.state),
            'created_date': datetime.now(),
            'created_uid': self.env.user.id,
        })
        return res

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        for purchase_id in self:
            quotation_stamp_id = self.env['delivery.status.stamp'].search([
                ('purchase_id', '=', purchase_id.id),
                ('delivery_status', '=', 'RFQ')], limit=1)
            sent_stamp_id = self.env['delivery.status.stamp'].search([
                ('purchase_id', '=', purchase_id.id),
                ('delivery_status', '=', 'RFQ Sent')], limit=1)
            for picking_id in purchase_id.picking_ids:
                if picking_id.state in ["draft", "confirmed", "waiting", "assigned"]:
                    quotation_stamp_id.write({
                        'picking_id': picking_id.id
                    })
                    sent_stamp_id.write({
                        'picking_id': picking_id.id
                    })
                    self.env['delivery.status.stamp'].create({
                        'purchase_id': purchase_id.id,
                        'picking_id': picking_id.id,
                        'delivery_status': 'Transfer created',
                        'created_date': datetime.now(),
                        'created_uid': self.env.user.id,
                    })
        return res

    def button_cancel(self):
        res = super(PurchaseOrder, self).button_cancel()
        for picking_id in self.picking_ids:
            self.env['delivery.status.stamp'].create({
                'purchase_id': self.id,
                'picking_id': picking_id.id,
                'delivery_status': dict(self._fields['state'].selection).get(self.state),
                'created_date': datetime.now(),
                'created_uid': self.env.user.id,
            })
        return res