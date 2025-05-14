# models/product_category.py
from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'
    
    custom_field_ids = fields.One2many(
        'product.category.custom.field',
        'category_id',
        string='Custom Fields'
    )

    @api.model
    def create(self, vals):
        # Hapus inisialisasi default yang tidak diperlukan
        return super().create(vals)

class ProductCategoryCustomField(models.Model):
    _name = 'product.category.custom.field'
    _description = 'Custom Field for Category'
    
    name = fields.Char(required=True)
    category_id = fields.Many2one('product.category', ondelete='cascade')
    field_type = fields.Selection([
        ('spec', 'Specification'),
        ('material', 'Material'),
        ('cable', 'Cable'),
        ('color', 'Color'),
    ], required=True, string='Field Type')