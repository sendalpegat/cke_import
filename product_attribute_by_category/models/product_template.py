from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    attribute_ids = fields.Many2many(
        'product.attribute',
        string='Attributes',
        help='Attributes that will be automatically applied to products under this category.'
    )

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('categ_id')
    def _onchange_category_apply_attributes(self):
        """Automatically apply attributes based on the selected category."""
        if self.categ_id and self.categ_id.attribute_ids:
            # Merge existing attributes with category-specific attributes
            new_attributes = self.categ_id.attribute_ids - self.attribute_line_ids.mapped('attribute_id')
            for attribute in new_attributes:
                self.attribute_line_ids = [(0, 0, {'attribute_id': attribute.id})]