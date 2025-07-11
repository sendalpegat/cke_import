from odoo import models, api, _
from odoo.exceptions import UserError

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def load(self, fields, data):
        try:
            default_code_idx = fields.index('default_code')
        except ValueError:
            return super(ProductProduct, self).load(fields, data)

        import_codes = [row[default_code_idx] for row in data if row[default_code_idx]]
        import_codes = list(set(import_codes))

        if import_codes:
            existing_products = self.env['product.product'].with_context(active_test=False).search([
                ('default_code', 'in', import_codes)
            ])
            if existing_products:
                dupe_codes = ', '.join(existing_products.mapped('default_code'))
                raise UserError(_(
                    "Import dibatalkan!\n\nTerdapat default_code yang sudah pernah ada: %s\n"
                    "Mohon hapus/mengganti kode tersebut sebelum import."
                ) % dupe_codes)

        return super(ProductProduct, self).load(fields, data)