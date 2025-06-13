# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_brand_id = fields.Many2one(
        comodel_name="product.brand",
        string="Brand",
        help="Select a brand for this product",
    )

    def name_get(self):
        res = super(ProductTemplate, self).name_get()
        res2 = []
        for name_tuple in res:
            product = self.browse(name_tuple[0])
            if not product.product_brand_id:
                res2.append(name_tuple)
                continue
            res2.append(
                (
                    name_tuple[0],
                    "{} ({})".format(name_tuple[1], product.product_brand_id.name),
                )
            )
        return res2
