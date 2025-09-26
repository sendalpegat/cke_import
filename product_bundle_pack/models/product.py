from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID


# class ProductPack(models.Model):
# 	_name = 'product.pack'
# 	_description = "Product Pack"
	
# 	product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
# 	default_code = fields.Char(related='product_id.default_code', string="Product Code", store=True)
# 	standard_price = fields.Float(related='product_id.standard_price', string="Cost", store=True)
# 	qty_uom = fields.Float(string='Quantity', required=True, default=1.0)
# 	bi_product_template = fields.Many2one(comodel_name='product.template', string='Product pack')
# 	bi_image = fields.Binary(related='product_id.image_1920', string='Image', store=True)
# 	price = fields.Float(related='product_id.lst_price', string='Product Price')
# 	uom_id = fields.Many2one(related='product_id.uom_id' , string="Unit of Measure", readonly="1")
# 	name = fields.Char(related='product_id.name', readonly="1")

class ProductPack(models.Model):
    _name = 'product.pack'
    _description = "Product Pack"

    product_id = fields.Many2one('product.product', string='Product', required=True)
    default_code = fields.Char(string="Product Code")
    name = fields.Char(string="Product Name")
    standard_price = fields.Float(string="Cost")
    qty_uom = fields.Float(string='Quantity', required=True, default=1.0)
    uom_id = fields.Many2one(related='product_id.uom_id', string="Unit of Measure", readonly=True)
    bi_product_template = fields.Many2one('product.template', string='Parent Product')
    bi_image = fields.Binary(related='product_id.image_1920', string='Image', store=True)
    price = fields.Float(related='product_id.lst_price', string='Product Price')
    po_qty = fields.Float(string='PO Qty', compute='_compute_po_qty', digits='Product Unit of Measure', store=False)
    total_qty = fields.Float(string='Total Qty', compute='_compute_total_qty', digits='Product Unit of Measure', store=False)


    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.default_code = self.product_id.default_code
        self.name = self.product_id.name
        self.standard_price = self.product_id.standard_price

    @api.depends_context('po_id')
    def _compute_po_qty(self):
        """Jumlah kuantitas PO untuk template bundle yang sama di PO aktif."""
        PurchaseOrder = self.env['purchase.order']
        po_id = self.env.context.get('po_id')
        po = PurchaseOrder.browse(po_id) if po_id else PurchaseOrder.browse()
        for pack in self:
            qty = 0.0
            if po:
                # Akumulasi semua line PO yang produknya adalah template bundle ini
                for line in po.order_line:
                    if line.product_id and line.product_id.product_tmpl_id == pack.bi_product_template:
                        qty += line.product_qty
            pack.po_qty = qty

    @api.depends('qty_uom', 'po_qty')
    def _compute_total_qty(self):
        for pack in self:
            pack.total_qty = (pack.qty_uom or 0.0) * (pack.po_qty or 0.0)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_pack = fields.Boolean(string='Is Product Pack')
    cal_pack_price = fields.Boolean(string='Calculate Pack Price')
    pack_ids = fields.One2many('product.pack', 'bi_product_template', string='Product Components')

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            rec._recompute_pack_price()
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'pack_ids' in vals or 'cal_pack_price' in vals:
            for rec in self:
                rec._recompute_pack_price()
        return res

    def _recompute_pack_price(self):
        """Update standard_price jika cal_pack_price diaktifkan"""
        if self.cal_pack_price and self.pack_ids:
            total = sum(line.qty_uom * line.product_id.standard_price for line in self.pack_ids if line.product_id)
            if total > 0:
                self.standard_price = total

class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'		

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_bundle = fields.Boolean('Allow Manual Dropshipping Delivery')

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        allow_bundle = self.env['ir.config_parameter'].sudo().get_param('product_bundle_pack.allow_bundle')
        res.update(allow_bundle = allow_bundle)
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('product_bundle_pack.allow_bundle', self.allow_bundle)