from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    default_specifications = fields.One2many(
        'product.template.specification', 'category_id', string='Default Specifications'
    )