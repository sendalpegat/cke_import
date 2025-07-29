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

from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    motor_type = fields.Text(string='Motor Type')
    bearing_type = fields.Text(string='Bearing Type')
    knob_switch_speed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Knob Switch Speed', default='no'
    )
    cable_speed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Cable Speed', default='no'
    )
    remote_control = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Remote Control', default='no'
    )
    tou = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Therm of Use', default='no'
    )
    led = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='LED', default='no'
    )
    manual_book = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')], string='Manual Book', default='no'
    )

    categories_template_summary = fields.Char(
        string="Categories Template Summary",
        compute="_compute_categories_template_summary",
        store=True
    )

    @api.depends(
        'motor_type',
        'bearing_type',
        'knob_switch_speed',
        'cable_speed',
        'remote_control',
        'tou',
        'led',
        'manual_book'
    )
    def _compute_categories_template_summary(self):
        for line in self:
            summary = []
            if line.motor_type:
                summary.append("Motor Type: %s" % line.motor_type)
            if line.bearing_type:
                summary.append("Bearing Type: %s" % line.bearing_type)
            if line.knob_switch_speed and line.knob_switch_speed != "no":
                summary.append("Knob Switch Speed: %s" % dict(line._fields['knob_switch_speed'].selection).get(line.knob_switch_speed))
            if line.cable_speed and line.cable_speed != "no":
                summary.append("Cable Speed: %s" % dict(line._fields['cable_speed'].selection).get(line.cable_speed))
            if line.remote_control and line.remote_control != "no":
                summary.append("Remote Control: %s" % dict(line._fields['remote_control'].selection).get(line.remote_control))
            if line.tou and line.tou != "no":
                summary.append("Therm of Use: %s" % dict(line._fields['tou'].selection).get(line.tou))
            if line.led and line.led != "no":
                summary.append("LED: %s" % dict(line._fields['led'].selection).get(line.led))
            if line.manual_book and line.manual_book != "no":
                summary.append("Manual Book: %s" % dict(line._fields['manual_book'].selection).get(line.manual_book))
            line.categories_template_summary = ", ".join(summary)

    @api.onchange('product_id')
    def _onchange_product_id_sync_custom_fields(self):
        if self.product_id:
            self.motor_type = self.product_id.motor_type
            self.bearing_type = self.product_id.bearing_type
            self.knob_switch_speed = self.product_id.knob_switch_speed
            self.cable_speed = self.product_id.cable_speed
            self.remote_control = self.product_id.remote_control
            self.tou = self.product_id.tou
            self.led = self.product_id.led
            self.manual_book = self.product_id.manual_book