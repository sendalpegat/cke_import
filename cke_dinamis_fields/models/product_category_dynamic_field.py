from odoo import models, fields

class ProductCategoryDynamicField(models.Model):
    _name = 'product.category.dynamic.field'
    _description = 'Dynamic Field for Product Category'

    category_id = fields.Many2one('product.category', string='Category', required=True)
    name = fields.Char(string='Field Name', required=True)
    label = fields.Char(string='Label', required=True)
    field_type = fields.Selection([
        ('char', 'Character'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('text', 'Text'),
    ], string='Field Type', required=True)
    required = fields.Boolean(string='Required')