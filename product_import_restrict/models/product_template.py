from odoo import models, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def load(self, fields, data):
        # Cari index kolom default_code di import
        try:
            default_code_idx = fields.index('default_code')
        except ValueError:
            # Tidak ada kolom default_code, lanjut import biasa
            return super(ProductTemplate, self).load(fields, data)

        # Kumpulkan semua default_code yang di-import
        import_codes = [row[default_code_idx] for row in data if row[default_code_idx]]
        import_codes = list(set(import_codes))  # Hilangkan duplikat di list import

        # Cek ke database apakah sudah ada
        if import_codes:
            # Cari ke product.product (bukan hanya template, agar lebih aman)
            ProductProduct = self.env['product.product'].with_context(active_test=False)
            existing_products = ProductProduct.search([('default_code', 'in', import_codes)])
            if existing_products:
                dupe_codes = ', '.join(existing_products.mapped('default_code'))
                raise UserError(_(
                    "Import dibatalkan!\n\nTerdapat default_code yang sudah pernah ada: %s\n"
                    "Mohon hapus/mengganti kode tersebut sebelum import."
                ) % dupe_codes)

        # Lanjutkan import jika tidak ada duplikat
        return super(ProductTemplate, self).load(fields, data)