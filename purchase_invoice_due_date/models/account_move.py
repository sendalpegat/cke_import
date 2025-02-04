from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="Due Status",
        compute="_compute_due_status",
        store=True,
        compute_sudo=True  # Menjalankan komputasi dengan hak akses superuser
    )

    @api.depends('invoice_date_due')
    def _compute_due_status(self):
        today = fields.Date.today()  # Gunakan fields.Date.today() untuk menjaga kompatibilitas timezone
        for move in self:
            if move.invoice_date_due:
                move.due_status = 'overdue' if move.invoice_date_due < today else 'not_due'
            else:
                move.due_status = False