from odoo import models, fields

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    kewarganegaraan = fields.Selection(
        selection=[('wni', 'WNI'), ('wna', 'WNA')],
        string="Kewarganegaraan",
        required=True,
        default='wni'
    )