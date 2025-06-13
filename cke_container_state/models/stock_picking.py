from odoo import models, fields, api

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    custom_stage = fields.Selection(
        selection=[
            ("loaded", "Loaded"),
            ("boarded", "Boarded"),
            ("customs", "Customs"),
            ("arrived", "Arrived"),
            ("done", "Done"),
        ],
        string="Status Penerimaan",
        default="loaded",
        tracking=True,
    )

    def open_date_wizard(self, stage):
        return {
            'name': 'Input Tanggal',
            'type': 'ir.actions.act_window',
            'res_model': 'custom.picking.date.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'default_stage': stage,
            }
        }

    def button_validate(self):
        res = super().button_validate()
        self.message_post(body=f"Status diubah ke <b>Done</b> pada {fields.Datetime.now()}")
        self.custom_stage = "done"
        return res