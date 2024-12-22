from odoo import api, fields, models
import math

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    hpp_factor = fields.Float(
        string="HPP Factor",
        default=1.45,
        help="The multiplier used to calculate HPP. Default is 1.45.",
    )

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    hpp = fields.Float(string="HPP IMF", compute="_compute_hpp", store=True, help="Calculated HPP value based on the configured currency and quantity.",)
    rest_po = fields.Float(string="Rest PO", compute="_compute_rest_po", store=True,)
    po_ita = fields.Char(string='PO ITA', store=True,)
    rest_po_total = fields.Float(string="Total CNY", compute="_compute_rest_po_total", store=True, help="Total value of rest_po multiplied by price_unit.",
    )

    @api.depends('price_unit', 'order_id.currency_id', 'rest_po')
    def _compute_hpp(self):
        for line in self:
            if line.price_unit:
                if line.order_id and line.order_id.currency_id:
                    # Ambil currency dari dokumen
                    currency = line.order_id.currency_id
                    # Ambil rate currency terbaru
                    latest_rate = currency.rate_ids.sorted('name', reverse=True)[:1]
                    if latest_rate:
                        hpp_factor = latest_rate.hpp_factor
                        currency_rate = latest_rate.rate
                    else:
                        hpp_factor = 1.45
                        currency_rate = 1.0

                    # Hitung HPP
                    hpp_value = math.ceil(line.price_unit * hpp_factor * currency_rate / 1000.0) * 1000.0
                    line.hpp = hpp_value
                else:
                    # Jika currency_id tidak ada, atur HPP ke 0
                    line.hpp = 0.0

    @api.depends('rest_po', 'price_unit')
    def _compute_rest_po_total(self):
        for line in self:
            if line.rest_po > 0 and line.price_unit > 0:
                line.rest_po_total = line.rest_po * line.price_unit
            else:
                line.rest_po_total = 0.0

    @api.depends('product_qty', 'qty_received')
    def _compute_rest_po(self):
        for line in self:
            if line.qty_received and line.qty_received > 0:
                # Hitung selisih jika qty_received memiliki nilai lebih dari 0
                line.rest_po = line.product_qty - line.qty_received
            else:
                # Jika qty_received belum ada atau 0, atur rest_po menjadi 0
                line.rest_po = 0.0