from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_field_ids = fields.Many2many(
        'product.category.field', 
        string="Custom Fields"
    )