from odoo import models, fields, api

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    custom_stage = fields.Selection(
        selection=[
<<<<<<< HEAD
            ("loaded", "Loaded"),
            ("boarded", "Boarded"),
            ("customs", "Customs"),
            ("arrived", "Arrived"),
            ("done", "Done"),
        ],
        string="Status Penerimaan",
=======
            ("loaded", "Loaded in Container"),
            ("boarded", "Boarded on Vessel"),
            ("customs", "Arrived at Tj Priok"),
            ("arrived", "Arrived at IMF WH"),
            ("done", "Done"),
        ],
        string="Receipt Status",
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
        default="loaded",
        tracking=True,
    )

<<<<<<< HEAD
    def open_date_wizard(self, stage):
        return {
            'name': 'Input Tanggal',
            'type': 'ir.actions.act_window',
            'res_model': 'custom.picking.date.wizard',
=======
    # Fungsi untuk membuka wizard input tanggal
    def open_date_wizard(self, stage):
        return {
            'name': 'Input Tanggal Status',
            'type': 'ir.actions.act_window',
            'res_model': 'date.input.wizard',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'default_stage': stage,
            }
<<<<<<< HEAD
        }

    def button_validate(self):
        res = super().button_validate()
        self.message_post(body=f"Status diubah ke <b>Done</b> pada {fields.Datetime.now()}")
        self.custom_stage = "done"
        return res
=======
        }
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
