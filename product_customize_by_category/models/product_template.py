from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_field_ids = fields.One2many(
        'product.category.custom.field',
        'category_id',
        string='Product Template',
        help='Fields to be dynamically added to products under this category.'
    )

class ProductCategoryCustomField(models.Model):
    _name = 'product.category.custom.field'
    _description = 'Custom Field for Product Category'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Category', ondelete='cascade')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_field_data = fields.One2many(
        'product.template.custom.field',
        'product_id',
        string='Specification',
        compute='_compute_custom_field_data',
        store=True
    )

    @api.depends('categ_id')
    def _compute_custom_field_data(self):
        for product in self:
            if product.categ_id:
                custom_fields = product.categ_id.custom_field_ids
                field_data = []
                for field in custom_fields:
                    field_data.append({
                        'field_name': field.name,
                        'value': field.value,  # Default empty value
                        'product_id': product.id,
                    })
                product.custom_field_data = [(0, 0, data) for data in field_data]

class ProductTemplateCustomField(models.Model):
    _name = 'product.template.custom.field'
    _description = 'Custom Field Data for Product Template'

    field_name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')  # Field for storing custom data
    product_id = fields.Many2one('product.template', string='Product', ondelete='cascade')