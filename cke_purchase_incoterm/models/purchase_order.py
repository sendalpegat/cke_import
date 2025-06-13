from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    fob_cif = fields.Selection(
        selection=[
            ('fob', 'FOB'),
            ('cif', 'CIF'),
        ],
        string='FOB / CIF',
        help="Standard trade terms for international shipping",
    )

    packing_methods = fields.Selection(
        selection=[
            ('cswm', 'Complete Set With Motor'),
            ('cswtm', 'Complete Set Without Motor'),
            ('sp', 'SKD Packing'),
            ('cs', 'Complete Set'),
            ],
        string='Packing Methods',
    )