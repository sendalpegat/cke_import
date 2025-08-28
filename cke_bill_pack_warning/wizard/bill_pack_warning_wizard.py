# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class BillPackWarningWizard(models.TransientModel):
    _name = "bill.pack.warning.wizard"
    _description = "Warning: Bill contains PACK products"

    move_id = fields.Many2one("account.move", string="Vendor Bill", required=True, ondelete="cascade")
    message = fields.Html(readonly=True, default=lambda self: self._default_message())

    def _default_message(self):
        return _(
            "<p><b>Bill ini berisi produk PACK (memiliki part).</b></p>"
            "<p>Jalankan <i>Explode Packs</i> sehingga part ditambahkan sebagai baris invoice dengan link ke PO line.</p>"
        )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        move_id = self._context.get("default_move_id")
        if not move_id:
            raise UserError(_("Tidak ada Bill aktif."))
        res["move_id"] = move_id
        return res

    def action_open_bill(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "res_id": self.move_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_try_open_explode(self):
        """
        Coba buka wizard explode packs.
        Kita deteksi beberapa nama model wizard yang umum dipakai.
        Jika tidak ditemukan, tampilkan error agar user jalankan manual.
        """
        self.ensure_one()
        env = self.env
        candidates = [
            "product.bundle.explode.wizard",
            "purchase.explode.pack.wizard",
            "account.move.explode.pack.wizard",
            "explode.pack.wizard",  # yang Anda pakai sebelumnya
        ]
        wizard_model = next((m for m in candidates if m in env), None)
        if not wizard_model:
            raise UserError(_(
                "Wizard Explode Packs tidak ditemukan.\n"
                "Buka Bill lalu jalankan fitur explode packs secara manual."
            ))

        # Buat record wizard. Banyak wizard cukup butuh context active_id/ids.
        ctx = dict(
            env.context,
            active_model="account.move",
            active_id=self.move_id.id,
            active_ids=[self.move_id.id],
        )

        # Coba cari view form untuk wizard tsb
        View = env["ir.ui.view"]
        view = View.search([("model", "=", wizard_model), ("type", "=", "form")], limit=1)

        # Beberapa wizard tidak butuh create() lebih dulu, cukup open action; namun agar aman, buat kosong.
        wiz_rec = env[wizard_model].with_context(ctx).create({})

        return {
            "type": "ir.actions.act_window",
            "res_model": wizard_model,
            "view_mode": "form",
            "view_id": view.id if view else False,
            "res_id": wiz_rec.id,
            "target": "new",
            "context": ctx,
        }