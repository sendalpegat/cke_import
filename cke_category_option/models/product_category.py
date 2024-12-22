from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_option = fields.Char(string='Custom Option')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_option = fields.Char(string='Custom Option', compute='_compute_custom_option', store=True)

    @api.depends('categ_id')
    def _compute_custom_option(self):
        for product in self:
            product.custom_option = product.categ_id.custom_option if product.categ_id else False