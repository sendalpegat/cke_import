from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoice_date_due = fields.Date(
        string="Invoice Due Date",
        compute="_compute_invoice_date_due",
        store=True
    )

    @api.depends('invoice_ids.invoice_date_due')
    def _compute_invoice_date_due(self):
        for order in self:
            invoices = order.invoice_ids.filtered(lambda inv: inv.move_type == 'in_invoice')
            if invoices:
                order.invoice_date_due = max(invoices.mapped('invoice_date_due'))
            else:
                order.invoice_date_due = False