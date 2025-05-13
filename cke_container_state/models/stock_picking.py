from odoo import models, fields, api

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"

    custom_stage = fields.Selection(
        selection=[
            ("loaded", "Loaded in Container"),
            ("boarded", "Boarded on Vessel"),
            ("customs", "Arrived at Tj Priok"),
            ("arrived", "Arrived at IMF WH"),
            ("done", "Done"),
        ],
        string="Receipt Status",
        default="loaded",
        tracking=True,
    )

    # Fungsi untuk membuka wizard input tanggal
    def open_date_wizard(self, stage):
        return {
            'name': 'Input Tanggal Status',
            'type': 'ir.actions.act_window',
            'res_model': 'date.input.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_picking_id': self.id,
                'default_stage': stage,
            }
        }