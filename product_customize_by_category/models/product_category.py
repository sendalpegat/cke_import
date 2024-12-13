from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_field_ids = fields.One2many(
        'product.category.custom.field',
        'category_id',
        string='Custom Fields',
    )

    @api.model
    def create(self, vals):
        # Tambahkan default value untuk custom_field_ids
        if 'custom_field_ids' not in vals:
            vals['custom_field_ids'] = [(0, 0, {
                'name': 'Default Name',
                'field_type': 'char',
            })]
        return super(ProductCategory, self).create(vals)