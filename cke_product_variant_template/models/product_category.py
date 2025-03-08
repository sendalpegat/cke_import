from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    variant_template_ids = fields.Many2many(
        'product.attribute.value',
        string='Variant Templates',
        help='Define product variants as templates in product categories.'
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self, vals):
        if 'categ_id' in vals:
            category = self.env['product.category'].browse(vals['categ_id'])
            if category.variant_template_ids:
                vals['attribute_value_ids'] = [(4, value.id) for value in category.variant_template_ids]
        return super(ProductProduct, self).create(vals)