from odoo import api, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_invoice(self):
        self.ensure_one()
        
        # Pengecekan product pack yang ditambahkan setelah PO dibuat
        pack_lines = self.order_line.filtered(
            lambda l: l.product_id.is_pack and 
            l.create_date > self.create_date
        )
        
        if pack_lines:
            message = _("""
                Peringatan: Terdapat product pack yang ditambahkan 
                setelah Purchase Order dibuat. Silakan periksa kembali 
                daftar produk.
            """)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Peringatan Product Pack'),
                    'message': message,
                    'sticky': True,
                }
            }
        
        # Proses pembuatan invoice tetap berjalan
        return super(PurchaseOrder, self).action_create_invoice()