# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ExplodePackWizard(models.TransientModel):
    _inherit = "explode.pack.wizard"  # <<< GANTI sesuai model wizard Anda

    move_id = fields.Many2one("account.move", string="Vendor Bill", readonly=True)
    line_ids = fields.One2many("explode.pack.line", "wizard_id", string="Lines")  # ADJUST IF DIFFERENT

    # --------- Helpers ----------
    def _match_po_line_by_product(self, po, product):
        """Cari 1 PO line yang product_id = product pada PO tersebut."""
        if not po or not product:
            return False
        return po.order_line.filtered(lambda l: l.product_id.id == product.id)[:1] or False

    def _ensure_move_vendor_bill(self):
        for wiz in self:
            if not wiz.move_id or wiz.move_id.move_type not in ("in_invoice", "in_refund"):
                raise UserError(_("Wizard ini hanya untuk Vendor Bill (in_invoice/in_refund)."))

    # --------- Core ----------
    def button_confirm(self):
        """
        Perbaikan utama link ke PO:
        - Untuk SETIAP baris PACK asal (src), simpan purchase_line_id (po_line_asal).
        - Buat komponen dari src dgn purchase_line_id = po_line_asal (per-line, bukan global).
        - Jika move.purchase_id kosong, set dari po_line_asal.order_id.
        - Fallback: jika po_line_asal kosong -> cari PO line berdasarkan produk di move.purchase_id.
        - Unlink baris PACK asal di akhir tiap iterasi.
        """
        self.ensure_one()
        self._ensure_move_vendor_bill()
        move = self.move_id

        # Ambil SEMUA baris PACK asal di bill ini
        pack_src_lines = move.invoice_line_ids.filtered(
            lambda l: l.product_id and getattr(l.product_id.product_tmpl_id, "is_pack", False)
        )
        if not pack_src_lines:
            # Tidak ada yang perlu diexplode
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "res_id": move.id,
                "view_mode": "form",
                "target": "current",
            }

        # Jika bill belum punya purchase_id, kita akan coba set dari line pertama yang punya po_line
        po_set = False

        # --- LOOP per sumber pack line (agar link PO tetap sesuai sumbernya) ---
        for src in pack_src_lines:
            po_line_asal = src.purchase_line_id  # bisa False kalau awalnya tidak dibuat dari PO
            if po_line_asal and not move.purchase_id and not po_set:
                move.purchase_id = po_line_asal.order_id
                po_set = True

            # Siapkan ref nama PO untuk mem-percantik kolom 'name'
            order_ref = move.purchase_id.name if move.purchase_id else False

            # Ambil baris komponen yang dipilih di wizard (kalau wizard Anda memang pakai baris)
            # Jika wizard Anda tidak punya relasi ke 'src', kita pakai seluruh line_ids yang selected.
            # ADJUST IF DIFFERENT: sesuaikan cara memilih komponen untuk 'src' tertentu.
            selected_lines = self.line_ids.filtered(lambda l: getattr(l, "selected", True))

            # --- Buat komponen untuk SRC ini ---
            for wline in selected_lines:
                product = wline.product_id
                qty = getattr(wline, "qty_uom", False) or getattr(wline, "quantity", 1.0)  # ADJUST IF DIFFERENT
                price_unit = getattr(wline, "price_unit", 0.0)
                account_id = getattr(wline, "account_id", False) and wline.account_id.id or False
                description = getattr(wline, "description", False) or getattr(wline, "name", "")  # ADJUST IF DIFFERENT

                # Tentukan PO line target:
                # 1) Pakai po_line_asal jika ada
                # 2) Kalau tidak ada, fallback cari berdasarkan product di move.purchase_id
                po_line_target = po_line_asal
                if not po_line_target and move.purchase_id:
                    po_line_target = self._match_po_line_by_product(move.purchase_id, product)
                    if not po_line_target:
                        _logger.warning(
                            "Tidak menemukan PO line untuk product %s pada PO %s saat explode; komponen tetap dibuat tanpa purchase_line_id.",
                            product.display_name, move.purchase_id.name
                        )

                name_val = "[%s] %s" % (order_ref, description) if order_ref else description

                self.env["account.move.line"].create({
                    "move_id": move.id,
                    "product_id": product.id,
                    "quantity": qty,
                    "price_unit": price_unit,
                    "account_id": account_id,
                    "name": name_val,
                    # KUNCI: linkkan ke PO line yang tepat
                    "purchase_line_id": po_line_target.id if po_line_target else False,
                    "is_exploded_component": True,
                })

            # Hapus baris pack asal (setelah komponen untuk SRC ini dibuat)
            src.unlink()

        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": move.id,
            "view_mode": "form",
            "target": "current",
        }