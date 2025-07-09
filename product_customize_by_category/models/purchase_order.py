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
    
    # sementara di comment  
    # def write(self, vals):
    #     # Jalankan logika penguncian sebelum menyimpan perubahan
    #     for order in self:
    #         if order.state in ['draft', 'sent']:  # Sesuaikan kondisi sesuai kebutuhan
    #             for line in order.order_line:
    #                 if line.product_id.product_tmpl_id:
    #                     template = line.product_id.product_tmpl_id
    #                     variant = line.product_id
    #                     template.write({'is_locked': True})
    #                     variant.write({'is_locked': True})
    #                     template.spec_field_values.write({'is_locked': True})
    #                     template.material_field_values.write({'is_locked': True})
    #                     template.cable_field_values.write({'is_locked': True})
    #                     template.color_field_values.write({'is_locked': True})
    #     # Panggil method write() asli untuk menyimpan data
    #     return super(PurchaseOrder, self).write(vals)
    #     

    def button_confirm(self):
        """
        Ketika PO dikonfirmasi, lock semua field dynamic & selection
        di product.template dan product.product yang terkait di order_line.
        """
        for order in self:
            for line in order.order_line:
                template = line.product_id.product_tmpl_id
                variant = line.product_id
                if not template or not variant:
                    continue

                # 1. Lock semua field dynamic (One2many) yang sudah diaktifkan
                # Tambahkan sesuai group field yang kamu gunakan
                dynamic_fields = [
                    'spec_field_values',
                    # 'motor_field_values',
                    # 'bearing_field_values',
                    # 'kss_field_values',
                    # 'cablespeed_field_values',
                    # 'remote_field_values',
                    # 'tou_field_values',
                    # 'led_field_values',
                    # 'book_field_values',
                    'material_field_values',
                    'cable_field_values',
                    'color_field_values',
                ]
                for field in dynamic_fields:
                    getattr(template, field).write({'is_locked': True})
                    getattr(variant, field).write({'is_locked': True})

                # 2. Lock field selection
                selection_fields = [
                    'motor_type',
                    'bearing_type',
                    'knob_switch_speed',
                    'cable_speed',
                    'remote_control',
                    'tou',
                    'led',
                    'manual_book',
                ]
                vals_selection = {}
                for field in selection_fields:
                    # Sync value dari template ke variant, lalu lock
                    if hasattr(template, field):
                        value = getattr(template, field)
                        vals_selection[field] = value
                vals_selection['is_locked'] = True

                template.write(vals_selection)
                variant.write(vals_selection)

        return super(PurchaseOrder, self).button_confirm()