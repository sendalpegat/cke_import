# from odoo import models, fields

# class StockPicking(models.Model):
#     _inherit = 'stock.picking'

#     receipt_status = fields.Selection([
#         ('loading', 'Loaded in Container'),
#         ('kapal', 'Boarded on Vessel'),
#         ('pelabuhan', 'Arrived at Tj. Priok'),
#         ('gudang', 'Arrived at IMF WH')
#     ], string='Receipt Status', default='loading')

from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipment_status = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('assigned', 'Assigned'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Shipment Status', default='draft', track_visibility='onchange')

    def action_confirm(self):
        res = super(StockPicking, self).action_confirm()
        self.write({'shipment_status': 'waiting'})
        return res

    def action_assign(self):
        res = super(StockPicking, self).action_assign()
        self.write({'shipment_status': 'assigned'})
        return res

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.write({'shipment_status': 'done'})
        return res

    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()
        self.write({'shipment_status': 'cancel'})
        return res