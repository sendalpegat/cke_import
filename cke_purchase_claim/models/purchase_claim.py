from odoo import models, fields, api

class PurchaseClaim(models.Model):
    _name = 'purchase.claim'
    _description = 'Purchase Claim'

    name = fields.Char(string='Claim Name', required=True)
    description = fields.Text(string='Description', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='State', default='draft')
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    claim_date = fields.Date(string='Claim Date', default=fields.Date.today)
    resolution_date = fields.Date(string='Resolution Date')

    @api.multi
    def submit_claim(self):
        self.state = 'submitted'

    @api.multi
    def approve_claim(self):
        self.state = 'approved'
        self.resolution_date = fields.Date.today()

    @api.multi
    def reject_claim(self):
        self.state = 'rejected'