# Copyright 2024 OpenSynergy Indonesia
# Copyright 2024 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import ast

from odoo import api, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.depends("item_ids")
    def _compute_item_count(self):
        for rec in self:
            rec.item_count = len(rec.item_ids)

    item_count = fields.Integer(string="Item Count", compute="_compute_item_count")

    def action_view_price_rules(self):
        self.ensure_one()
        action = self.env.ref("product.product_pricelist_item_action").read()[0]
        action["domain"] = [("pricelist_id", "=", self.id)]
        context = action.get("context", {})
        if isinstance(context, str):
            context = ast.literal_eval(context)
        context.update(
            {
                "default_pricelist_id": self.id,
            }
        )
        action["context"] = context
        return action
