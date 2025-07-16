# See LICENSE file for full copyright and licensing details.
from odoo import models


class IrModel(models.Model):
    _inherit = 'ir.model'
    
    def unlink(self):
        is_installed = self.env['ir.module.module'].sudo().search_count(
                [('name', '=', 'popup_reminder'), ('state', '=', 'installed')])
        for rec in self:
            if is_installed > 0:
                models = self.env['popup.reminder'].search(
                    [('model_id.model', '=', rec.model)])
                models.unlink()
        return super(IrModel, self).unlink()