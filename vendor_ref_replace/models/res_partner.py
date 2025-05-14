from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Tidak perlu menambahkan field baru, hanya mengubah posisi field yang ada