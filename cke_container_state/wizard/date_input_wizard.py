from odoo import models, fields, api
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
        
        return {'type': 'ir.actions.act_window_close'}