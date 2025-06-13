from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_send_to_commercial(self):
        """Metode untuk mengirim faktur ke komersial."""
        self.write({'state': 'commercial'})
        return True

    def action_commercial_approve(self):
        """Metode untuk menyetujui faktur oleh komersial."""
        self.write({'state': 'posted'})
        return True