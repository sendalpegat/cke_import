# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    # Menandai bahwa baris ini hasil explode pack (informasi saja)
    is_exploded_component = fields.Boolean(string="Exploded Component")

    # Opsional: referensi nomor PO untuk tampilan (tidak mempengaruhi statinfo)
    purchase_order_ref = fields.Char(
        string="PO Ref",
        compute="_compute_purchase_order_ref",
        store=True,
        readonly=True,
    )

    @api.depends("move_id.purchase_id")
    def _compute_purchase_order_ref(self):
        for line in self:
            line.purchase_order_ref = line.move_id.purchase_id.name if line.move_id and line.move_id.purchase_id else False