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

        id_idx = None
        if 'id' in fields:
            id_idx = fields.index('id')

        import_codes = {}
        for row in data:
            code = row[default_code_idx]
            if code:
                rec_id = row[id_idx] if id_idx is not None else False
                import_codes[code] = rec_id

        check_codes = list(import_codes.keys())
        if check_codes:
            existing_products = self.env['product.product'].with_context(active_test=False).search([('default_code', 'in', check_codes)])

            dupe_codes = []
            for prod in existing_products:
                rec_id = import_codes.get(prod.default_code)
                if not rec_id or str(prod.id) != str(rec_id):
                    dupe_codes.append(prod.default_code)

            if dupe_codes:
                raise UserError(_(
                    "Import dibatalkan!\n\nTerdapat default_code yang sudah pernah ada: %s\n"
                    "Mohon hapus/mengganti kode tersebut sebelum import."
                ) % ', '.join(dupe_codes))

        return super(ProductProduct, self).load(fields, data)