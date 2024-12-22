from odoo import models, fields, api

class ProductTemplateSpecification(models.Model):
    _name = 'product.template.specification'
    _description = 'Product Template Specification'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Category')
    product_id = fields.Many2one('product.template', string='Product Template')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    specification_ids = fields.One2many(
        'product.template.specification', 'product_id', string='Specifications'
    )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        """Copy default specifications from the category to the product"""
        if self.categ_id and self.categ_id.default_specifications:
            self.specification_ids = [(5, 0, 0)]  # Clear existing specifications
            self.specification_ids = [
                (0, 0, {'name': spec.name, 'value': spec.value})
                for spec in self.categ_id.default_specifications
            ]