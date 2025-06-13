from odoo import _, api, exceptions, fields, models
from odoo.tools import float_compare


class AccountVoucherWizardInvoice(models.TransientModel):
    _name = "account.voucher.wizard.invoice"
    _description = "Vendor Bill Advance Payment Wizard"

    percentage_advance = fields.Float(string="Percentage (%)", required=True, default=0.0)
    invoice_id = fields.Many2one("account.move", required=True)
    journal_id = fields.Many2one("account.journal", required=True, domain=[("type", "in", ("bank", "cash"))])
    journal_currency_id = fields.Many2one("res.currency", compute="_compute_get_journal_currency")
    currency_id = fields.Many2one("res.currency", readonly=True)
    amount_total = fields.Monetary("Amount Total", readonly=True)
    amount_advance = fields.Monetary("Advance Amount", required=True, currency_field="journal_currency_id")
    date = fields.Date("Date", required=True, default=fields.Date.context_today)
    currency_amount = fields.Monetary("Currency Amount", readonly=True, currency_field="currency_id")
    payment_ref = fields.Char("Reference")
    partner_id = fields.Many2one('res.partner', related='invoice_id.partner_id', readonly=True)

    @api.depends("journal_id")
    def _compute_get_journal_currency(self):
        for rec in self:
            rec.journal_currency_id = rec.journal_id.currency_id.id or self.env.user.company_id.currency_id.id

    @api.constrains("percentage_advance", "amount_advance")
    def _check_amounts(self):
        for rec in self:
            if rec.percentage_advance < 0 or rec.percentage_advance > 100:
                raise exceptions.ValidationError(_("Percentage must be between 0 and 100."))
            if rec.amount_advance <= 0:
                raise exceptions.ValidationError(_("Amount must be positive."))

    @api.onchange("percentage_advance")
    def _onchange_percentage(self):
        self.amount_advance = (self.percentage_advance / 100) * self.amount_total

    @api.onchange("journal_id", "date", "amount_advance")
    def _onchange_amount(self):
        if self.journal_currency_id != self.currency_id:
            converted = self.journal_currency_id._convert(
                self.amount_advance, self.currency_id, self.invoice_id.company_id, self.date
            )
            self.currency_amount = converted
        else:
            self.currency_amount = self.amount_advance

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        invoice_ids = self.env.context.get("active_ids")
        if invoice_ids:
            invoice = self.env["account.move"].browse(invoice_ids[0])
            res.update({
                "invoice_id": invoice.id,
                "amount_total": invoice.amount_residual,
                "currency_id": invoice.currency_id.id,
            })
        return res

    def _prepare_payment_vals(self, invoice):
        return {
            "date": self.date,
            "amount": self.amount_advance,
            "payment_type": "outbound",
            "partner_type": "supplier",
            "ref": self.payment_ref or invoice.name,
            "journal_id": self.journal_id.id,
            "currency_id": self.journal_currency_id.id,
            "partner_id": invoice.partner_id.id,
            "payment_method_id": self.env.ref("account.account_payment_method_manual_out").id,
            "percentage_advance": self.percentage_advance,
            "invoice_id": invoice.id,
        }

    def make_advance_payment(self):
        self.ensure_one()
        invoice = self.invoice_id
        vals = self._prepare_payment_vals(invoice)
        payment = self.env["account.payment"].create(vals)
        invoice.advance_payment_ids |= payment
        payment.action_post()
        return {"type": "ir.actions.act_window_close"}