from odoo import models, fields

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    vendor_product_code = fields.Char(string="Vendor Product Code", help="Code of the product provided by the vendor")