# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        """
        IMPROVED: Lock fields hanya saat PO confirmed, bukan saat draft
        Ini lebih reasonable karena draft bisa diubah
        """
        res = super(PurchaseOrder, self).button_confirm()
        
        # Lock product fields setelah PO confirmed
        for order in self:
            try:
                for line in order.order_line:
                    if not line.product_id or not line.product_id.product_tmpl_id:
                        continue
                    
                    template = line.product_id.product_tmpl_id
                    variant = line.product_id
                    
                    # IMPROVED: Lock dengan context untuk bypass validations
                    _logger.info(
                        "Locking product %s due to PO %s confirmation",
                        variant.display_name,
                        order.name
                    )
                    
                    # Lock template dan variant
                    template.with_context(tracking_disable=True).write({
                        'is_locked': True
                    })
                    variant.with_context(tracking_disable=True).write({
                        'is_locked': True
                    })
                    
                    # Lock semua field values
                for field_value in template.spec_field_values:
                    field_value.with_context(force_unlock=True).write({
                        'is_locked': True,
                        'original_value': field_value.value
                    })
                    template.material_field_values.with_context(force_unlock=True).write({
                        'is_locked': True
                    })
                    template.cable_field_values.with_context(force_unlock=True).write({
                        'is_locked': True
                    })
                    template.color_field_values.with_context(force_unlock=True).write({
                        'is_locked': True
                    })
                    
            except Exception as e:
                _logger.error(
                    "Error locking products for PO %s: %s",
                    order.name,
                    str(e)
                )
                # Don't block PO confirmation jika ada error
                
        return res

    def button_cancel(self):
        """
        ADDED: Unlock products saat PO dibatalkan
        """
        res = super(PurchaseOrder, self).button_cancel()
        
        for order in self:
            for line in order.order_line:
                if not line.product_id or not line.product_id.product_tmpl_id:
                    continue
                
                template = line.product_id.product_tmpl_id
                variant = line.product_id
                
                _logger.info(
                    "Unlocking product %s due to PO %s cancellation",
                    variant.display_name,
                    order.name
                )
                
                # Unlock dengan context
                template.with_context(tracking_disable=True).write({
                    'is_locked': False
                })
                variant.with_context(tracking_disable=True).write({
                    'is_locked': False
                })
                
                # Unlock field values
                all_field_values = (
                    template.spec_field_values |
                    template.material_field_values |
                    template.cable_field_values |
                    template.color_field_values
                )
                all_field_values.with_context(force_unlock=True).write({
                    'is_locked': False
                })
        
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Custom fields di PO line
    motor_type = fields.Text(string='Motor Type')
    bearing_type = fields.Text(string='Bearing Type')
    
    knob_switch_speed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Knob Switch Speed',
        default='no'
    )
    
    cable_speed = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Cable Speed',
        default='no'
    )
    
    remote_control = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Remote Control',
        default='no'
    )
    
    tou = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Thermofuse',
        default='no'
    )
    
    led = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='LED',
        default='no'
    )
    
    manual_book = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Manual Book',
        default='no'
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
        """
        IMPROVED: Compute summary dengan better formatting
        """
        for line in self:
            summary = []
            
            # Text fields
            if line.motor_type:
                summary.append(f"Motor Type: {line.motor_type}")
            if line.bearing_type:
                summary.append(f"Bearing Type: {line.bearing_type}")
            
            # Selection fields - hanya tampilkan yang 'yes'
            selection_fields = [
                ('knob_switch_speed', 'Knob Switch Speed'),
                ('cable_speed', 'Cable Speed'),
                ('remote_control', 'Remote Control'),
                ('tou', 'Thermofuse'),
                ('led', 'LED'),
                ('manual_book', 'Manual Book'),
            ]
            
            for field_name, field_label in selection_fields:
                field_value = getattr(line, field_name)
                if field_value and field_value != 'no':
                    # Get human-readable label
                    selection_dict = dict(
                        line._fields[field_name].selection
                    )
                    summary.append(
                        f"{field_label}: {selection_dict.get(field_value, field_value)}"
                    )
            
            line.categories_template_summary = ", ".join(summary) if summary else ""

    @api.onchange('product_id')
    def _onchange_product_id_sync_custom_fields(self):
        """
        IMPROVED: Sync custom fields dari product saat product berubah
        """
        if self.product_id:
            _logger.debug(
                "Syncing custom fields for PO line with product %s",
                self.product_id.display_name
            )
            
            self.motor_type = self.product_id.motor_type
            self.bearing_type = self.product_id.bearing_type
            self.knob_switch_speed = self.product_id.knob_switch_speed
            self.cable_speed = self.product_id.cable_speed
            self.remote_control = self.product_id.remote_control
            self.tou = self.product_id.tou
            self.led = self.product_id.led
            self.manual_book = self.product_id.manual_book