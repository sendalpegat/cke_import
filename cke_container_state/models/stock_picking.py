from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    receipt_status = fields.Selection([
        ('loading', 'Loaded in Container'),
        ('kapal', 'Boarded on Vessel'),
        ('pelabuhan', 'Arrived at Tj. Priok'),
        ('gudang', 'Arrived at IMF WH')
    ], string='Receipt Status', default='loading')