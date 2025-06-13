from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    category_custom_fields = fields.Many2many(
        'product.category.field', 
        string="Custom Fields", 
        compute="_compute_category_custom_fields", 
        store=True)

    @api.depends('categ_id')
    def _compute_category_custom_fields(self):
        for product in self:
            product.category_custom_fields = product.categ_id.custom_field_ids

    def _get_custom_field_values(self):
        """Mengembalikan nilai default untuk field kustom di kategori."""
        return {field.name: False for field in self.category_custom_fields}