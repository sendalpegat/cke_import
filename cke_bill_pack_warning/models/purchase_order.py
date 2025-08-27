# -*- coding: utf-8 -*-
from odoo import models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_view_invoice(self, invoices=False):
        """
        memanggil method ini kadang dengan argumen 'invoices' (recordset account.move).
        Pertahankan signature aslinya, lalu intercept hasil action untuk
        menampilkan warning jika bill berisi produk PACK.
        """
        # Panggil bawaan dengan argumen asli
        action = super().action_view_invoice(invoices)

        Move = self.env["account.move"]
        move = False

        # 1) Jika caller memberikan 'invoices' (recordset atau ids), utamakan itu
        if invoices:
            try:
                # invoices biasanya recordset; ambil 1 saja
                move = invoices[:1]
            except Exception:
                try:
                    # fallback jika invoices berupa id/ids
                    move = Move.browse(invoices)[:1]
                except Exception:
                    move = False

        # 2) Jika action punya res_id langsung, pakai itu
        if (not move) and isinstance(action, dict) and action.get("res_id"):
            move = Move.browse(action["res_id"])

        # 3) Jika action hanya domain (misal tree view), ambil 1 terbaru
        if (not move) and isinstance(action, dict) and action.get("domain"):
            try:
                domain = action["domain"]
                move = Move.search(domain, limit=1, order="id desc")
            except Exception:
                move = False

        # 4) Fallback: ambil 1 invoice terkait PO ini (yang terbaru)
        if (not move) and self:
            invs = self.mapped("invoice_ids")
            move = invs.sorted("id", reverse=True)[:1] if invs else Move.browse()

        if not move or not move.exists():
            return action

        # Hanya untuk Vendor Bills
        if move.move_type in ("in_invoice", "in_refund"):
            # Deteksi produk PACK (sesuaikan flag bila modul Anda pakai nama lain)
            has_pack = any(
                l.product_id and getattr(l.product_id.product_tmpl_id, "is_pack", False)
                for l in move.invoice_line_ids
            )
            if has_pack:
                # Tampilkan wizard warning
                wiz_action = self.env.ref(
                    "cke_bill_pack_warning.action_bill_pack_warning_wizard"
                ).read()[0]
                ctx = dict(self.env.context, default_move_id=move.id)
                wiz_action["context"] = ctx
                return wiz_action

        # Jika tidak ada PACK, kembalikan action asli
        return action