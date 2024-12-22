from odoo import models

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_print_vendor_bill(self):
        """Generate and download the vendor bill report."""
        return self.env.ref('vendor_bills_print.vendor_bill_report_action').report_action(self)