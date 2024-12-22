from odoo import models, fields

class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    supplier_product_code = fields.Char(
        string='Supplier Product Code',
        help='Code used by the supplier for this product'
    )