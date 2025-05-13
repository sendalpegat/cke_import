# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductBrand(models.Model):
    _name = "product.brand"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Product Brand"
    _order = "name"

    @api.depends("product_ids")
    def _compute_products_count(self):
        for rec in self:
            rec.products_count = len(rec.product_ids)

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        help="Select a partner for this brand if it exists",
        ondelete="restrict",
    )
    logo = fields.Binary(string="Logo File")
    product_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="product_brand_id",
        string="Brand Products",
    )
    products_count = fields.Integer(
        string="Number of products",
        compute="_compute_products_count",
    )
