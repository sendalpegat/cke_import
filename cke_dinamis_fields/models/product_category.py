from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    dynamic_field_ids = fields.One2many(
        'product.category.dynamic.field',
        'category_id',
        string='Dynamic Fields'
    )