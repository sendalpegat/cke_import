from odoo import models, fields

class ProductCategoryField(models.Model):
    _name = 'product.category.field'
    _description = 'Product Category Custom Field'

    name = fields.Char(string="Field Name", required=True)
    field_type = fields.Selection([
        ('char', 'Text'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Checkbox'),
        ('selection', 'Selection'),
        ('tags', 'Tags')
    ], string="Field Type", required=True, default='tags')

    selection_options = fields.Text(string="Selection Options", 
        help="Gunakan format: 'key:value,key2:value2' untuk pilihan dropdown.")