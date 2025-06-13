from odoo import fields, models, api
from datetime import datetime


class StockPicking(models.Model):
    _inherit = "stock.picking"

    delivery_status_stamp_ids = fields.One2many(comodel_name="delivery.status.stamp", inverse_name="picking_id")

    @api.model
    def create(self, vals):
        res = super(StockPicking, self).create(vals)
        if not res.purchase_id:
            for picking_id in res.purchase_id.picking_ids:
                for stamp_id in picking_id.delivery_status_stamp_ids.filtered(lambda d: d.delivery_status in ['RFQ']):
                    self.env['delivery.status.stamp'].create({
                        'purchase_id': stamp_id.sale_id.id,
                        'picking_id': stamp_id.picking_id.id,
                        'delivery_status': stamp_id.delivery_status,
                        'created_date': stamp_id.created_date,
                        'created_uid': stamp_id.created_uid.id,
                    })
            res.purchase_id = res.purchase_id.id
        return res

    def action_cancel(self):
        res = super(StockPicking, self).action_cancel()
        self.env['delivery.status.stamp'].create({
            'purchase_id': self.purchase_id.id,
            'picking_id': self.id,
            'delivery_status': dict(self._fields['state'].selection).get(self.state),
            'created_date': datetime.now(),
            'created_uid': self.env.user.id,
        })
        return res

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        self.env['delivery.status.stamp'].create({
            'purchase_id': self.purchase_id.id,
            'picking_id': self.id,
            'delivery_status': 'Done',
            'created_date': datetime.now(),
            'created_uid': self.env.user.id,
        })
        return res

    