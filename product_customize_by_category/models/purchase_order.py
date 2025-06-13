from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    # def button_confirm(self):
    #     for order in self:
    #         for line in order.order_line:
    #             if line.product_id.product_tmpl_id:
    #                 template = line.product_id.product_tmpl_id
    #                 variant = line.product_id
    #                 template.write({'is_locked': True})
    #                 variant.write({'is_locked': True})
    #                 template.spec_field_values.write({'is_locked': True})
    #                 # template.motor_type.write({'is_locked': True})
    #                 # template.bearing_type.write({'is_locked': True})
    #                 # template.knob_switch_speed.write({'is_locked': True})
    #                 # template.cable_speed.write({'is_locked': True})
    #                 # template.remote_control.write({'is_locked': True})
    #                 # template.tou.write({'is_locked': True})
    #                 # template.led_field_values.write({'is_locked': True})
    #                 # template.manual_book.write({'is_locked': True})
    #                 template.material_field_values.write({'is_locked': True})
    #                 template.cable_field_values.write({'is_locked': True})
    #                 template.color_field_values.write({'is_locked': True})
    #                 # template.packing_field_values.write({'is_locked': True})
    #     return super(PurchaseOrder, self).button_confirm()
    #     
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