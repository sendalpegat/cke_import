from odoo import models, fields, api
from datetime import datetime, timedelta


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_check_vendor_bill_reminder(self):
        po_to_remind = self.search([
            ('state', '=', 'purchase'),
            ('invoice_status', '!=', 'invoiced'),
            ('date_order', '<=', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        ])
        for po in po_to_remind:
            # Kirim notifikasi email ke pengguna yang bertanggung jawab
            if po.user_id and po.user_id.partner_id.email:
                template = self.env.ref('purchase_reminder.email_template_vendor_bill_reminder')
                self.env['mail.template'].browse(template.id).send_mail(po.id, force_send=True)