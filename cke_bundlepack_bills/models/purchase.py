from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_create_invoice(self):
        """
        Override untuk membuat vendor bill berdasarkan komponen paket,
        kompatibel dengan 'Ordered Quantities' (tanpa perlu penerimaan barang).
        """
        # Panggil fungsi asli untuk membuat invoice dasar
        result = super(PurchaseOrder, self).action_create_invoice()

        # Jika hasil bukan recordset invoice, kembalikan hasil asli (misal: wizard)
        if not isinstance(result, models.Model) or result._name != 'account.move':
            return result

        invoice = result

        # Hapus semua baris invoice untuk produk bertipe paket
        invoice.invoice_line_ids.filtered(
            lambda line: line.product_id.product_tmpl_id.is_pack
        ).unlink()

        # Tambahkan baris invoice berdasarkan komponen paket dari PO lines
        for line in self.order_line:
            if line.product_id.product_tmpl_id.is_pack:
                for component in line.product_id.product_tmpl_id.pack_ids:
                    # Hitung kuantitas komponen berdasarkan qty PO line
                    component_qty = component.qty_uom * line.product_qty
                    
                    # Ambil harga per unit (bisa dari PO line atau cost komponen)
                    price_unit = component.product_id.standard_price
                    
                    # Pastikan akun tersedia
                    account = invoice.invoice_line_ids[0].account_id if invoice.invoice_line_ids else component.product_id.property_account_expense_id

                    # Buat baris invoice untuk komponen
                    self.env["account.move.line"].create({
                        "move_id": invoice.id,
                        "product_id": component.product_id.id,
                        "quantity": component_qty,
                        "price_unit": price_unit,
                        "name": component.product_id.name,
                        "account_id": account.id,
                    })

        return invoice