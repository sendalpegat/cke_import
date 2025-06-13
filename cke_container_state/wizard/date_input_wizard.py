from odoo import models, fields, api
<<<<<<< HEAD

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
=======
from datetime import datetime

class DateInputWizard(models.TransientModel):
    _name = 'date.input.wizard'
    _description = 'Wizard Input Tanggal Status'

    picking_id = fields.Many2one('stock.picking', string="Stock Picking")
    stage = fields.Char(string="Target Status")
    input_date = fields.Datetime(
        string="Tanggal",
        default=fields.Datetime.now,
        required=True
    )

    def action_confirm(self):
        # Update status dan tambahkan log ke message
        self.picking_id.write({'custom_stage': self.stage})
        
        # Format pesan log
        stage_label = dict(self.picking_id._fields['custom_stage'].selection).get(self.stage)
        message = f"Status diubah ke <b>{stage_label}</b> pada {self.input_date}"
        
        # Simpan ke chatter
        self.picking_id.message_post(body=message)
        
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
        return {'type': 'ir.actions.act_window_close'}