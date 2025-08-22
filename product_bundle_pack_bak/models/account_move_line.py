# from odoo import api, models, fields

# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'

#     purchase_order_ref = fields.Char(
#         string='PO Reference',
#         compute='_compute_purchase_order_ref',
#         store=True
#     )

#     # @api.depends('move_id.purchase_id')
#     # def _compute_purchase_order_ref(self):
#     #     for line in self:
#     #         line.purchase_order_ref = line.move_id.purchase_id.name if line.move_id.purchase_id else False

# @api.depends('move_id', 'purchase_line_id', 'move_id.purchase_id', 'purchase_line_id.order_id')
# def _compute_purchase_order_ref(self):
#     for line in self:
#         po = line.move_id.purchase_id

#         if not po and line.purchase_line_id:
#             po = line.purchase_line_id.order_id

#         if not po and line.move_id and line.move_id.picking_id and line.move_id.picking_id.origin:
#             po = self.env['purchase.order'].search([
#                 ('name', '=', line.move_id.picking_id.origin)
#             ], limit=1)

#         line.purchase_order_ref = po.name if po else False

from odoo import api, fields, models
from odoo.exceptions import UserError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    is_exploded_component = fields.Boolean(string='Exploded Component', default=False)

    @api.model
    def unlink(self):
        for line in self:
            if line.is_exploded_component:
                raise UserError("You cannot delete exploded pack components from invoice. Please manage pack from the wizard.")
        return super(AccountMoveLine, self).unlink()