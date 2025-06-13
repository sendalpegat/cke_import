from odoo import fields, models, api


class DeliveryStatusStamp(models.Model):
    _name = "delivery.status.stamp"

    purchase_id = fields.Many2one(comodel_name="purchase.order")
    picking_id = fields.Many2one(comodel_name="stock.picking", string="picking")
    delivery_status = fields.Char(string="Status")
    created_date = fields.Datetime(string="Created on")
    created_uid = fields.Many2one(comodel_name="res.users")

    @api.model
    def create(self, vals):
        res = super(DeliveryStatusStamp, self).create(vals)
        if not res.purchase_id:
            res.purchase_id = res.picking_id.purchase_id.id
        return res