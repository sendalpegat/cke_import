from odoo import api, fields, models
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="Due Status",
        compute="_compute_due_status",
        store=True
    )

    @api.depends('invoice_date_due')
    def _compute_due_status(self):
        for move in self:
            if move.invoice_date_due:
                today = date.today()
                if move.invoice_date_due < today:
                    move.due_status = 'overdue'
                else:
                    move.due_status = 'not_due'
            else:
                move.due_status = False