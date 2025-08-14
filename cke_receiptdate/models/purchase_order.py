from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        res._auto_set_receipt_date()
        return res

    def write(self, vals):
        result = super(PurchaseOrder, self).write(vals)
        self._auto_set_receipt_date()
        return result

    def _auto_set_receipt_date(self):
        for order in self:
            config = order.partner_id.po_auto_receipt_date or 'manual'
            if config == 'manual':
                continue
            # Gunakan tanggal order_date, fallback ke hari ini
            order_date = fields.Date.from_string(order.date_order) if order.date_order else fields.Date.today()
            offset_months = {
                '1_month': 1,
                '2_month': 2,
                '3_month': 3,
            }.get(config)
            if offset_months:
                planned_date = order_date + relativedelta(months=offset_months)
                for line in order.order_line:
                    line.date_planned = planned_date