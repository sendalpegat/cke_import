# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Custom field values untuk variants
    spec_field_values = fields.One2many(
        'product.template.field.value',
        'product_product_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

    material_field_values = fields.One2many(
        'product.template.field.value',
        'product_product_id',
        string='Material',
        domain=[('field_type', '=', 'material')]
    )

    cable_field_values = fields.One2many(
        'product.template.field.value',
        'product_product_id',
        string='Cable',
        domain=[('field_type', '=', 'cable')]
    )

    color_field_values = fields.One2many(
        'product.template.field.value',
        'product_product_id',
        string='Color',
        domain=[('field_type', '=', 'color')]
    )

    # Additional attributes
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
        string='Thrmofuse',
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

    is_locked = fields.Boolean(
        string='Locked',
        default=False,
        help="When locked, custom fields cannot be modified"
    )

    # Computed summaries
    spec_field_summary = fields.Char(
        string="Specification Summary",
        compute="_compute_field_summaries",
        store=True
    )
    material_field_summary = fields.Char(
        string="Material Summary",
        compute="_compute_field_summaries",
        store=True
    )
    cable_field_summary = fields.Char(
        string="Cable Summary",
        compute="_compute_field_summaries",
        store=True
    )
    color_field_summary = fields.Char(
        string="Color Summary",
        compute="_compute_field_summaries",
        store=True
    )

    @api.depends(
        'spec_field_values', 'spec_field_values.value',
        'material_field_values', 'material_field_values.value',
        'cable_field_values', 'cable_field_values.value',
        'color_field_values', 'color_field_values.value',
    )
    def _compute_field_summaries(self):
        """
        IMPROVED: Compute summaries dengan None check
        """
        for variant in self:
            # Specification
            spec_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.spec_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            variant.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""

            # Material
            material_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.material_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            variant.material_field_summary = ", ".join(material_summary) if material_summary else ""

            # Cable
            cable_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.cable_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            variant.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""

            # Color
            color_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.color_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            variant.color_field_summary = ", ".join(color_summary) if color_summary else ""

    @api.model
    def create(self, vals):
        """
        Override create untuk auto-sync dari template
        """
        product = super(ProductProduct, self).create(vals)
        if 'product_tmpl_id' in vals:
            product._sync_from_template()
        return product

    def write(self, vals):
        """
        IMPROVED: Handle sync dengan proper context management
        """
        sync_fields = [
            'motor_type', 'bearing_type', 'knob_switch_speed', 'cable_speed',
            'remote_control', 'tou', 'led', 'manual_book'
        ]
        
        # Deteksi perubahan sync fields
        is_sync = any(f in vals for f in sync_fields)
        
        res = super(ProductProduct, self).write(vals)
        
        # Jika tidak dari template dan ada perubahan sync fields,
        # update template untuk maintain consistency
        if is_sync and not self.env.context.get('sync_from_template'):
            for variant in self:
                if variant.product_tmpl_id:
                    _logger.debug(
                        "Syncing fields from variant %s to template",
                        variant.display_name
                    )
                    variant.product_tmpl_id.sync_fields_from_variant(variant)
        
        return res

    def _sync_from_template(self):
        """
        OPTIMIZED: Sinkronkan nilai dari template ke variant dengan batch operations
        """
        FieldValue = self.env['product.template.field.value']
        
        for product in self:
            if not product.product_tmpl_id:
                continue
            
            try:
                template = product.product_tmpl_id
                
                # Batch query untuk template values
                template_values = FieldValue.search([
                    ('product_id', '=', template.id)
                ])
                
                if not template_values:
                    continue
                
                # Batch query untuk existing variant values
                existing_values = FieldValue.search([
                    ('product_product_id', '=', product.id)
                ])
                
                # Create mapping untuk quick lookup
                existing_map = {}
                for ev in existing_values:
                    key = (ev.field_definition_id.id, ev.field_type)
                    existing_map[key] = ev
                
                # Prepare batch operations
                records_to_update = FieldValue.browse()
                update_value = None
                to_create = []
                
                for tval in template_values:
                    key = (tval.field_definition_id.id, tval.field_type)
                    
                    if key in existing_map:
                        # Collect records untuk batch update
                        existing_record = existing_map[key]
                        # Update satu per satu karena value mungkin berbeda
                        existing_record.with_context(skip_variant_sync=True).write({
                            'value': tval.value
                        })
                    else:
                        # Prepare untuk batch create
                        to_create.append({
                            'field_definition_id': tval.field_definition_id.id,
                            'product_product_id': product.id,
                            'field_type': tval.field_type,
                            'value': tval.value
                        })
                
                # Batch create
                if to_create:
                    FieldValue.with_context(skip_variant_sync=True).create(to_create)
                
                _logger.debug(
                    "Synced %d fields from template to variant %s (created: %d)",
                    len(template_values),
                    product.display_name,
                    len(to_create)
                )
                
            except Exception as e:
                _logger.error(
                    "Error syncing variant %s from template: %s",
                    product.display_name,
                    str(e)
                )
                raise

    def sync_fields_from_template(self, template):
        """
        Sync specific fields dari template dengan context untuk prevent loop
        """
        sync_fields = [
            'motor_type', 'bearing_type', 'knob_switch_speed', 'cable_speed',
            'remote_control', 'tou', 'led', 'manual_book'
        ]
        update_vals = {f: getattr(template, f) for f in sync_fields}
        self.with_context(sync_from_template=True).write(update_vals)

    def update_from_template(self):
        """
        Manual action untuk update dari template
        """
        self._sync_from_template()
        return True

    def action_sync_variant_fields(self):
        """
        Action button untuk sync dari UI
        """
        self.update_from_template()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sync Complete',
                'message': 'Variant fields updated from template.',
                'type': 'success',
                'sticky': False,
            }
        }