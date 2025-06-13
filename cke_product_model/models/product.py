from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    factory_model_no = fields.Char(
        string='Factory Model No',
        help='Factory model number of the product'
    )
    manufacture_code = fields.Char(
        string='Manufacture Code',
        help='Manufacturer code for the product'
    )

class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    factory_model_no = fields.Char(
        string='Factory Model No',
        related='product_tmpl_id.factory_model_no',
        readonly=False,
        store=True,
        help='Factory model number of the product'
    )
    manufacture_code = fields.Char(
        string='Manufacture Code',
        related='product_tmpl_id.manufacture_code',
        readonly=False,
        store=True,
        help='Manufacturer code for the product'
    )