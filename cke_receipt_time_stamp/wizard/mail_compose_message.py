from odoo import models
from datetime import datetime


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        res = super(MailComposer, self).action_send_mail()
        purchase_id = self.env['purchase.order'].browse(self._context.get("active_id"))
        if not purchase_id.picking_ids:
            self.env['delivery.status.stamp'].create({
                'purchase_id': purchase_id.id,
                'picking_id': None,
                'delivery_status': 'RFQ Sent',
                'created_date': datetime.now(),
                'created_uid': self.env.user.id,
            })
        else:
            for picking_id in purchase_id.picking_ids:
                self.env['delivery.status.stamp'].create({
                    'sale_id': purchase_id.id,
                    'picking_id': picking_id.id,
                    'delivery_status': 'RFQ Sent',
                    'created_date': datetime.now(),
                    'created_uid': self.env.user.id,
                })
        return res