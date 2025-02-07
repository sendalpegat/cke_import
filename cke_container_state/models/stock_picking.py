from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Ready'),  # Moved directly after "Draft"
        ('loaded', 'Loaded in Container'),
        ('boarded', 'Boarded on Vessel'),
        ('customs', 'Arrived at Tj Priok'),
        ('arrived', 'Arrived at IMF WH'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')

    def action_assigned(self):
        self.state = 'assigned'

    def action_loaded(self):
        self.state = 'loaded'

    def action_boarded(self):
        self.state = 'boarded'

    def action_customs(self):
        self.state = 'customs'

    def action_arrived(self):
        self.state = 'arrived'