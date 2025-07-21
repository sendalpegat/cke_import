from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
     
    def write(self, vals):
        # Jalankan logika penguncian sebelum menyimpan perubahan
        for order in self:
            if order.state in ['draft', 'sent']:  # Sesuaikan kondisi sesuai kebutuhan
                for line in order.order_line:
                    if line.product_id.product_tmpl_id:
                        template = line.product_id.product_tmpl_id
                        variant = line.product_id
                        template.write({'is_locked': True})
                        variant.write({'is_locked': True})
                        template.spec_field_values.write({'is_locked': True})
                        template.material_field_values.write({'is_locked': True})
                        template.cable_field_values.write({'is_locked': True})
                        template.color_field_values.write({'is_locked': True})
        # Panggil method write() asli untuk menyimpan data
        return super(PurchaseOrder, self).write(vals)