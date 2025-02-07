from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    bank_account_number = fields.Char(string="Bank Account Number", help="Vendor's bank account number")
    bank_name = fields.Char(string="Bank Name", help="Vendor's bank name")