from odoo import models, fields, api

class DateInputWizard(models.TransientModel):
    _name = 'custom.picking.date.wizard'
    _description = 'Wizard Input Tanggal Status'

    picking_id = fields.Many2one('stock.picking', string="Transfer", required=True)
    stage = fields.Char(string="Status", required=True)
    input_date = fields.Datetime(
        string="Tanggal Perubahan",
        required=True,
        default=fields.Datetime.now
    )

    def action_confirm(self):
        self.ensure_one()
        self.picking_id.custom_stage = self.stage
        stage_label = dict(self.picking_id._fields['custom_stage'].selection).get(self.stage)
        self.picking_id.message_post(
            body=f"Status diubah ke <b>{stage_label}</b> pada {self.input_date}"
        )
        return {'type': 'ir.actions.act_window_close'}