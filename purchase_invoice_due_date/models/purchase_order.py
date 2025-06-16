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
from dateutil.relativedelta import relativedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    expected_invoice_due_date = fields.Date(
        string="P.O Due Date",
        compute="_compute_expected_invoice_due_date",
        store=True
    )

    expected_due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="P.O Due Status",
        compute='_compute_expected_summary',
        store=False
    )

    expected_total_days = fields.Integer(
        string="P.O Total Days",
        compute='_compute_expected_summary',
        store=False
    )

    @api.depends('order_line.expected_invoice_due_date')
    def _compute_expected_summary(self):
        today = fields.Date.context_today(self)
        for order in self:
            if order.expected_invoice_due_date:
                order.expected_due_status = 'overdue' if order.expected_invoice_due_date < today else 'not_due'
                order.expected_total_days = (order.expected_invoice_due_date - today).days
            else:
                order.expected_due_status = False
                order.expected_total_days = 0

    @api.depends('date_order')
    def _compute_expected_invoice_due_date(self):
        for order in self:
            if order.date_order:
                order.expected_invoice_due_date = order.date_order + relativedelta(months=2)
            else:
                order.expected_invoice_due_date = False


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Estimasi (Expected)
    expected_invoice_due_date = fields.Date(
        string="P.O Due Date",
        related='order_id.expected_invoice_due_date',
        store=True,
        readonly=True
    )

    expected_due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="Expected Due Status",
        compute='_compute_expected_status',
        store=False
    )

    expected_total_days = fields.Integer(
        string="P.O Total Days",
        compute='_compute_expected_status',
        store=False
    )

    # Aktual (dari Vendor Bill)
    actual_invoice_due_date = fields.Date(
        string="Invoice Due Date",
        compute='_compute_actual_invoice_info',
        store=False
    )

    actual_due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="Actual Due Status",
        compute='_compute_actual_invoice_info',
        store=False
    )

    actual_total_days = fields.Integer(
        string="Total Days",
        compute="_compute_actual_invoice_info",
        store=False
    )

    @api.depends('expected_invoice_due_date')
    def _compute_expected_status(self):
        today = fields.Date.context_today(self)
        for line in self:
            if line.expected_invoice_due_date:
                line.expected_due_status = 'overdue' if line.expected_invoice_due_date < today else 'not_due'
                line.expected_total_days = (line.expected_invoice_due_date - today).days
            else:
                line.expected_due_status = False
                line.expected_total_days = 0

    @api.depends('order_id.invoice_ids')
    def _compute_actual_invoice_info(self):
        today = fields.Date.context_today(self)
        for line in self:
            invoices = line.order_id.invoice_ids.filtered(
                lambda inv: inv.state not in ['cancel'] and inv.amount_residual > 0 and inv.invoice_date_due)
            if invoices:
                latest_invoice = invoices.sorted(key=lambda inv: inv.invoice_date_due, reverse=True)[0]
                line.actual_invoice_due_date = latest_invoice.invoice_date_due
                line.actual_due_status = 'overdue' if latest_invoice.invoice_date_due < today else 'not_due'
                line.actual_total_days = (latest_invoice.invoice_date_due - today).days
            else:
                line.actual_invoice_due_date = False
                line.actual_due_status = False
                line.actual_total_days = 0