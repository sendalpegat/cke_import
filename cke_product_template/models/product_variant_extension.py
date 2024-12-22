from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    has_variant_field = fields.Boolean(string='Has Variant Field', default=False)
    variant_field_name = fields.Char(string='Variant Field Name')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        # Jika kategori memiliki field tambahan, tambahkan logika
        category = self.env['product.category'].browse(vals.get('categ_id'))
        if category.has_variant_field and category.variant_field_name:
            vals[category.variant_field_name] = "Default Value"
        return super(ProductTemplate, self).create(vals)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Menambahkan field secara dinamis berdasarkan kategori
    def _compute_dynamic_fields(self):
        for record in self:
            category = record.categ_id
            if category.has_variant_field and category.variant_field_name:
                record[category.variant_field_name] = "Computed Value"

    # Contoh field dummy; sesuaikan sesuai kebutuhan
    dynamic_field = fields.Char(string='Dynamic Field', compute='_compute_dynamic_fields')