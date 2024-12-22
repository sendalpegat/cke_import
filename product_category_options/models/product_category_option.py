from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    product_options = fields.One2many(
        comodel_name='product.category.option',
        inverse_name='category_id',
        string='Product Options'
    )

class ProductCategoryOption(models.Model):
    _name = 'product.category.option'
    _description = 'Product Category Option'

    name = fields.Char(string='Option Name', required=True)
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Category',
        ondelete='cascade'
    )

# class ProductTemplate(models.Model):
#     _inherit = 'product.template'

#     product_options = fields.Many2many(
#         comodel_name='product.category.option',
#         string='Product Options',
#         compute='_compute_product_options',
#         store=True
#     )

#     @api.depends('categ_id')
#     def _compute_product_options(self):
#         for product in self:
#             product.product_options = product.categ_id.product_options if product.categ_id else False

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_options = fields.Char(
        string='Product Options',
        compute='_compute_product_options',
        store=True,
        readonly=True
    )

    @api.depends('categ_id')
    def _compute_product_options(self):
        for product in self:
            if product.categ_id:
                product.product_options = ", ".join(option.name for option in product.categ_id.product_options)
            else:
                product.product_options = False