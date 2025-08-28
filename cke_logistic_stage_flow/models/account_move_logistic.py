# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

LOGISTIC_STAGES = [
    ('loaded', 'Loaded'),
    ('boarded', 'Boarded'),
    ('customs', 'Customs'),
    ('arrived', 'Arrived'),
    ('gudang_vsj', 'Gudang VSJ'),
]

class AccountMove(models.Model):
    _inherit = 'account.move'

    logistic_state = fields.Selection(
        LOGISTIC_STAGES, string='Logistic Stage',
        default='loaded', copy=False, tracking=True
    )

    def write(self, vals):
        # Saat bill di-post, pastikan logistic_state minimal 'loaded'
        res = super().write(vals)
        for rec in self:
            if rec.move_type == 'in_invoice' and rec.state == 'posted' and not rec.logistic_state:
                rec.logistic_state = 'loaded'
        return res

    def action_open_logistic_stage_wizard(self):
        self.ensure_one()
        if self.state != 'posted' or self.move_type != 'in_invoice':
            raise UserError(_("Only available on posted Vendor Bills."))
        return {
            'name': _('Change Logistic Stage'),
            'type': 'ir.actions.act_window',
            'res_model': 'logistic.stage.move.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_move_id': self.id,
                'default_current_stage': self.logistic_state or 'loaded',
            }
        }