from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    additional_cost = fields.Monetary(
        string='FR COST & INS',
        default=0.0,
        currency_field='currency_id',
        help='Biaya tambahan di luar total barang/jasa'
    )

    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        store=True, readonly=True, compute='_compute_amount', currency_field='currency_id',
    )
    amount_tax = fields.Monetary(
        string='Tax',
        store=True, readonly=True, compute='_compute_amount', currency_field='currency_id',
    )
    amount_total = fields.Monetary(
        string='Total',
        store=True, readonly=True, compute='_compute_amount', currency_field='currency_id',
    )
    amount_total_signed = fields.Monetary(
        string='Total (Signed)', store=True, readonly=True, compute='_compute_amount', currency_field='currency_id',
    )
    amount_total_company_signed = fields.Monetary(
        string="Total in Company Currency",
        store=True, readonly=True, compute='_compute_amount', currency_field='company_currency_id',
    )

    @api.depends('line_ids.debit', 'line_ids.credit', 'additional_cost', 'line_ids.amount_currency')
    def _compute_amount(self):
        for move in self:
            total_untaxed = total_tax = 0.0
            for line in move.line_ids:
                if line.tax_line_id:
                    total_tax += line.balance
                elif not line.exclude_from_invoice_tab:
                    total_untaxed += line.balance

            # *** Perbaikan Sign ***
            if move.move_type in ('out_refund', 'in_refund'):
                sign = -1
            else:
                sign = 1

            move.amount_untaxed = sign * (total_untaxed)
            move.amount_tax = sign * (total_tax)
            move.amount_total = move.amount_untaxed + move.amount_tax + move.additional_cost
            move.amount_total_signed = move.amount_total * sign
            move.amount_total_company_signed = move.amount_total * sign / (move.currency_id.rate or 1.0)