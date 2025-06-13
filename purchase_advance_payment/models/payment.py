from odoo import fields, models

class AccountPayment(models.Model):

    _inherit = "account.payment"

    purchase_id = fields.Many2one(
        "purchase.order",
        "Purchase",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    percentage_advance = fields.Float("Advance Percentage", readonly=True)

    invoice_id = fields.Many2one('account.move', string="Vendor Bill", readonly=True)