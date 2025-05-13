# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ProductKey(models.Model):
    _name = "product.key"
    _inherit = [
        "mixin.master_data",
    ]
    _description = "Commodity Key"
    _order = "name"

    @api.depends("product_ids")
    def _compute_products_count(self):
        for rec in self:
            rec.products_count = len(rec.product_ids)

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        help="Select a partner for this commodity Key if it exists",
        ondelete="restrict",
    )
    logo = fields.Binary(string="Logo File")
    product_ids = fields.One2many(
        comodel_name="product.template",
        inverse_name="product_key_id",
        string="Commodity Key",
    )
    products_count = fields.Integer(
        string="Number of products",
        compute="_compute_products_count",
    )
