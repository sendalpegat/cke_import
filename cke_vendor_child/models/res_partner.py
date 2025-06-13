from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    display_child_name = fields.Char(string="Beneficiary", compute="_compute_display_child_name")

    def _compute_display_child_name(self):
        for rec in self:
            rec.display_child_name = rec.name