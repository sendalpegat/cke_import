# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Daftar receipts (stock.picking) dan produk (stock.move) terkait bill
    picking_ids = fields.Many2many(
        'stock.picking',
        string='Receipts',
        compute='_compute_receipts_and_moves',
        readonly=True,
        copy=False,
    )
    receipt_move_ids = fields.Many2many(
        'stock.move',
        string='Receipt Products',
        compute='_compute_receipts_and_moves',
        readonly=True,
        copy=False,
    )
    receipt_product_count = fields.Integer(
        string='Receipt Product Count',
        compute='_compute_receipts_and_moves',
        readonly=True,
    )

    @api.depends('invoice_line_ids', 'invoice_line_ids.purchase_line_id',
                 'invoice_origin', 'company_id', 'state', 'move_type')
    def _compute_receipts_and_moves(self):
        Picking = self.env['stock.picking']
        PurchaseOrder = self.env['purchase.order']
        for move in self:
            picks = Picking.browse()

            # 1) Via purchase_line -> stock.move -> picking
            pols = move.invoice_line_ids.mapped('purchase_line_id')
            if pols:
                picks |= pols.mapped('move_ids').mapped('picking_id')

            # 2) Via PO dari purchase_line
            pos_from_line = pols.mapped('order_id')
            if pos_from_line:
                picks |= pos_from_line.mapped('picking_ids')

            # 3) Via invoice_origin (mis. "PO0001, PO0002")
            if move.invoice_origin:
                names = [s.strip() for s in re.split(r'[,;]+', move.invoice_origin) if s.strip()]
                if names:
                    pos_from_origin = PurchaseOrder.search([('name', 'in', names)])
                    if pos_from_origin:
                        picks |= pos_from_origin.mapped('picking_ids')

            # Filter receipts: incoming + company sama + DONE (sesuai alur auto-done Anda)
            picks = picks.filtered(
                lambda p: p.company_id == move.company_id
                and p.picking_type_id and p.picking_type_id.code == 'incoming'
                # and p.state == 'done' ## Tampilkan apabila hanya status done saja
            )
            move.picking_ids = picks.ids

            # Kumpulkan stock.move (produk) dari receipts
            receipt_moves = picks.mapped('move_lines').filtered(
                lambda sm: sm.product_id and sm.product_id.type in ('product', 'consu')
            )
            move.receipt_move_ids = receipt_moves.ids
            move.receipt_product_count = len(receipt_moves)

    def action_view_receipts(self):
        """Buka tree/form stock.picking untuk receipts terkait."""
        self.ensure_one()
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('id', 'in', self.picking_ids.ids)]
        if len(self.picking_ids) == 1:
            action.update({'view_mode': 'form', 'res_id': self.picking_ids.id})
        return action

    def action_view_receipt_products(self):
        """Buka list stock.move (produk) dari receipts terkait."""
        self.ensure_one()
        view = self.env.ref('cke_vendor_bill_receipts.view_receipt_move_tree', raise_if_not_found=False)
        action = {
            'type': 'ir.actions.act_window',
            'name': _('Picking List'),  # <- ganti judul action
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.receipt_move_ids.ids)],
            'context': {'search_default_group_by_picking': 1},
        }
        if view:
            action['views'] = [(view.id, 'tree'), (False, 'form')]
        return action