from odoo import api, fields, models
from odoo.tools import float_compare


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    payment_progress = fields.Selection(
        selection=[
            ('not_paid', 'Not Paid'),
            ('down_payment', 'Down Payment'),
            ('commercial_invoice', 'Commercial Invoice'),
            ('balance_payment', 'Balance Payment'),
            ('full_payment', 'Full Payment'),
        ],
        string='Payment Progress',
        compute='_compute_payment_progress',
        store=True,
    )

    account_payment_ids = fields.One2many(
        "account.payment", "purchase_id", string="Pay purchase advanced", readonly=True
    )
    amount_residual = fields.Float(
        "Residual amount",
        readonly=True,
        compute="_compute_purchase_advance_payment",
        store=True,
    )
    payment_line_ids = fields.Many2many(
        "account.move.line",
        string="Payment move lines",
        compute="_compute_purchase_advance_payment",
        store=True,
    )
    advance_payment_status = fields.Selection(
        selection=[
            ("not_paid", "Not Paid"),
            ("paid", "Paid"),
            ("partial", "Partially Paid"),
        ],
        string="TT Status",
        store=True,
        readonly=True,
        copy=False,
        tracking=True,
        compute="_compute_purchase_advance_payment",
    )

    @api.depends(
        "currency_id",
        "company_id",
        "amount_total",
        "account_payment_ids",
        "account_payment_ids.state",
        "account_payment_ids.move_id",
        "account_payment_ids.move_id.line_ids",
        "account_payment_ids.move_id.line_ids.date",
        "account_payment_ids.move_id.line_ids.debit",
        "account_payment_ids.move_id.line_ids.credit",
        "account_payment_ids.move_id.line_ids.currency_id",
        "account_payment_ids.move_id.line_ids.amount_currency",
        "order_line.invoice_lines.move_id",
        "order_line.invoice_lines.move_id.amount_total",
        "order_line.invoice_lines.move_id.amount_residual",
    )
    def _compute_purchase_advance_payment(self):
        for order in self:
            mls = order.account_payment_ids.mapped("move_id.line_ids").filtered(
                lambda x: x.account_id.internal_type == "payable"
                and x.parent_state == "posted"
            )
            advance_amount = 0.0
            for line in mls:
                line_currency = line.currency_id or line.company_id.currency_id
                # Exclude reconciled pre-payments amount because once reconciled
                # the pre-payment will reduce bill residual amount like any
                # other payment.
                line_amount = (
                    line.amount_residual_currency
                    if line.currency_id
                    else line.amount_residual
                )
                if line_currency != order.currency_id:
                    advance_amount += line.currency_id._convert(
                        line_amount,
                        order.currency_id,
                        order.company_id,
                        line.date or fields.Date.today(),
                    )
                else:
                    advance_amount += line_amount
            # Consider payments in related invoices.
            invoice_paid_amount = 0.0
            for inv in order.invoice_ids:
                # use the reconciled payment amounts instead of the invoice
                # amount_residual that also includes reconciled credit notes.
                for payment in inv._get_reconciled_invoices_partials():
                    if payment[2].journal_id.type != "purchase":
                        invoice_paid_amount += payment[1]
            amount_residual = order.amount_total - advance_amount - invoice_paid_amount
            payment_state = "not_paid"
            if mls or order.invoice_ids:
                has_due_amount = float_compare(
                    amount_residual, 0.0, precision_rounding=order.currency_id.rounding
                )
                if has_due_amount <= 0:
                    payment_state = "paid"
                elif has_due_amount > 0:
                    payment_state = "partial"
            order.payment_line_ids = mls
            order.amount_residual = amount_residual
            order.advance_payment_status = payment_state

    # Di dalam class PurchaseOrder
    advance_payment_count = fields.Integer(
        string="TT Count",
        compute="_compute_advance_payment_count",
        store=True,
    )

    @api.depends("account_payment_ids")
    def _compute_advance_payment_count(self):
        for order in self:
            order.advance_payment_count = len(order.account_payment_ids)

    @api.depends('account_payment_ids', 'invoice_ids.state', 'invoice_ids.move_type',
                 'invoice_ids.amount_residual', 'amount_total')
    def _compute_payment_progress(self):
        for order in self:
            payment_progress = 'not_paid'

            has_advance = bool(order.account_payment_ids)
            commercial_invoice_exist = any(
                inv.move_type == 'in_invoice' and inv.state == 'commercial_invoice'
                for inv in order.invoice_ids
            )

            total_residual = sum(inv.amount_residual for inv in order.invoice_ids if inv.move_type == 'in_invoice')
            has_balance = total_residual > 0

            if has_advance and not order.invoice_ids:
                payment_progress = 'down_payment'
            elif commercial_invoice_exist:
                payment_progress = 'commercial_invoice'
            elif has_balance:
                payment_progress = 'balance_payment'
            elif not has_balance and order.invoice_ids:
                payment_progress = 'full_payment'

            order.payment_progress = payment_progress