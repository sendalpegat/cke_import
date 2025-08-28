# product_bundle_pack/models/account_move.py
from odoo import models, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        res = super().action_post()

        for inv in self:
            if inv.move_type != 'in_invoice':
                continue

            # 1) Pastikan purchase_id terisi
            po = False
            # Dari invoice line → purchase_line_id.order_id (lebih akurat)
            pol_orders = inv.invoice_line_ids.mapped('purchase_line_id.order_id')
            if pol_orders:
                po = pol_orders[0]
            # Fallback dari invoice_origin jika itu PO
            if not po and inv.invoice_origin:
                po = self.env['purchase.order'].search([('name', '=', inv.invoice_origin)], limit=1)

            # Set purchase_id bila field tersedia dan belum terisi
            if hasattr(inv, 'purchase_id') and po and not inv.purchase_id:
                inv.purchase_id = po

            # 2) Kumpulkan pickings incoming yg belum done/cancel
            target_po = inv.purchase_id or po
            if not target_po:
                continue

            pickings = target_po.picking_ids.filtered(
                lambda p: p.picking_type_code == 'incoming' and p.state not in ('done', 'cancel')
            )
            if not pickings:
                continue

            # 3) Peta qty dari invoice per product
            inv_qty = {}
            for line in inv.invoice_line_ids:
                if line.product_id and line.quantity > 0:
                    inv_qty[line.product_id.id] = inv_qty.get(line.product_id.id, 0.0) + line.quantity

            if not inv_qty:
                continue

            # 4) Set quantity_done pada move yg match product
            for picking in pickings:
                # Assign dulu kalau perlu
                if picking.state in ('waiting', 'confirmed'):
                    picking.action_assign()

                updated = False
                for move in picking.move_ids_without_package:
                    qty = inv_qty.get(move.product_id.id)
                    if qty:
                        # Catatan: jika produk pakai lot/serial, kamu perlu set lot terlebih dulu
                        move.quantity_done = qty
                        updated = True

                if not updated:
                    continue

                # 5) Validate + backorder jika perlu
                try:
                    picking.button_validate()
                except Exception as e:
                    # Beri pesan jelas (misal produk tracing lot/serial)
                    raise UserError("Gagal memvalidasi Receipt %s: %s" % (picking.name, str(e)))

                # Otomatis backorder bila ada sisa
                remaining = picking.move_ids_without_package.filtered(
                    lambda m: m.product_uom_qty > m.quantity_done
                )
                if remaining:
                    wiz = self.env['stock.backorder.confirmation'].create({'picking_id': picking.id})
                    wiz.process()

        return res