# from odoo import api, fields, models
# from datetime import date

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'

#     invoice_date_due = fields.Date(
#         string="Invoice Due Date",
#         compute="_compute_invoice_date_due",
#         store=True
#     )

#     today_date = fields.Date(
#         string="Today",
#         compute="_compute_today_date",
#         store=False
#     )

#     total_days = fields.Integer(  # Menggunakan Integer karena menghitung jumlah hari
#         string="Total Days",
#         compute="_compute_total_days",
#         store=False
#     )

#     @api.depends('invoice_ids.invoice_date_due')
#     def _compute_invoice_date_due(self):
#         for order in self:
#             invoices = order.invoice_ids.filtered(lambda inv: inv.move_type == 'in_invoice')
#             if invoices:
#                 order.invoice_date_due = max(invoices.mapped('invoice_date_due'))
#             else:
#                 order.invoice_date_due = False

#     @api.depends()
#     def _compute_today_date(self):
#         today = fields.Date.context_today(self)
#         for order in self:
#             order.today_date = today

#     @api.depends('date_approve')  # Memanggil field yang benar
#     def _compute_total_days(self):
#         today = fields.Date.context_today(self)
#         for order in self:
#             if order.date_approve:
#                 order.total_days = (today - order.date_approve.date()).days
#             else:
#                 order.total_days = 0  # Jika date_approve belum diset

from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta  # Untuk menambah bulan

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoice_date_due = fields.Date(
        string="Invoice Due Date",
        compute="_compute_invoice_date_due",
        store=True
    )

    today_date = fields.Date(
        string="Today",
        compute="_compute_today_date",
        store=False
    )

    total_days = fields.Integer(  # Menggunakan Integer karena menghitung jumlah hari
        string="Total Days",
        compute="_compute_total_days",
        store=False
    )

    @api.depends('date_approve')  # Menggunakan date_approve untuk perhitungan
    def _compute_invoice_date_due(self):
        for order in self:
            if order.date_approve:
                order.invoice_date_due = order.date_approve + relativedelta(months=2)
            else:
                order.invoice_date_due = False

    @api.depends()
    def _compute_today_date(self):
        today = fields.Date.context_today(self)
        for order in self:
            order.today_date = today

    @api.depends('date_approve')  # Memanggil field yang benar
    def _compute_total_days(self):
        today = fields.Date.context_today(self)
        for order in self:
            if order.date_approve:
                order.total_days = (today - order.date_approve.date()).days
            else:
                order.total_days = 0  # Jika date_approve belum diset