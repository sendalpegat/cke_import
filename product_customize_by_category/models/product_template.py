# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Custom field values untuk setiap kategori
    spec_field_values = fields.One2many(
        'product.template.field.value',
        'product_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

    material_field_values = fields.One2many(
        'product.template.field.value',
        'product_id',
        string='Material',
        domain=[('field_type', '=', 'material')]
    )

    cable_field_values = fields.One2many(
        'product.template.field.value',
        'product_id',
        string='Cable',
        domain=[('field_type', '=', 'cable')]
    )

    color_field_values = fields.One2many(
        'product.template.field.value',
        'product_id',
        string='Color',
        domain=[('field_type', '=', 'color')]
    )

    # Additional product attributes
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

    is_locked = fields.Boolean(
        string='Locked',
        default=False,
        help="When locked, custom fields cannot be modified"
    )

    # Field summaries - computed fields untuk preview
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
        IMPROVED: Menghitung ringkasan dengan pengecekan None
        Menghindari error saat value kosong atau None
        """
        for product in self:
            # Specification summary
            spec_summary = [
                f"{field.name}: {field.value}" 
                for field in product.spec_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            product.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""

            # Material summary
            material_summary = [
                f"{field.name}: {field.value}" 
                for field in product.material_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            product.material_field_summary = ", ".join(material_summary) if material_summary else ""

            # Cable summary
            cable_summary = [
                f"{field.name}: {field.value}" 
                for field in product.cable_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            product.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""

            # Color summary
            color_summary = [
                f"{field.name}: {field.value}" 
                for field in product.color_field_values 
                if field.value and field.value.strip()  # FIXED: Added None check
            ]
            product.color_field_summary = ", ".join(color_summary) if color_summary else ""

    @api.model
    def create(self, vals):
        """
        Override create untuk auto-generate custom fields berdasarkan kategori
        """
        product = super(ProductTemplate, self).create(vals)
        if 'categ_id' in vals:
            product._update_custom_fields()
        return product

    def write(self, vals):
        """
        FIXED: Consolidated duplicate write methods
        Handle category changes dan field synchronization dalam satu method
        """
        res = super(ProductTemplate, self).write(vals)
        
        # Handle category change - regenerate custom fields
        if 'categ_id' in vals:
            _logger.info("Category changed for products: %s", self.ids)
            self._update_custom_fields()
        
        # Handle sync fields - hanya jika tidak dari variant (prevent loop)
        if not self.env.context.get('sync_from_variant'):
            sync_fields = [
                'motor_type', 'bearing_type', 'knob_switch_speed', 'cable_speed',
                'remote_control', 'tou', 'led', 'manual_book'
            ]
            if any(f in vals for f in sync_fields):
                _logger.info("Syncing fields to variants for products: %s", self.ids)
                self._sync_fields_to_variants(sync_fields)
        
        return res

    @api.onchange('categ_id')
    def _onchange_categ_id_update_fields(self):
        """
        Update custom fields saat kategori berubah di form view
        """
        self._update_custom_fields()

    def _update_custom_fields(self):
        """
        IMPROVED: Update custom fields berdasarkan kategori produk
        dengan better error handling
        """
        for product in self:
            try:
                # Clear all fields jika tidak ada kategori
                if not product.categ_id:
                    product.spec_field_values = [(5, 0, 0)]
                    product.material_field_values = [(5, 0, 0)]
                    product.cable_field_values = [(5, 0, 0)]
                    product.color_field_values = [(5, 0, 0)]
                    continue

                # Sync semua field types
                self._sync_field_type(product, 'spec') 
                self._sync_field_type(product, 'material')
                self._sync_field_type(product, 'cable')
                self._sync_field_type(product, 'color')

                # Sinkronkan ke semua variant yang sudah ada
                if product.product_variant_ids:
                    _logger.info(
                        "Syncing %d variants for product %s",
                        len(product.product_variant_ids),
                        product.name
                    )
                    for variant in product.product_variant_ids:
                        variant._sync_from_template()
                        
            except Exception as e:
                _logger.error(
                    "Error updating custom fields for product %s: %s",
                    product.name,
                    str(e)
                )
                raise

    def _sync_field_type(self, product, field_type):
        """
        IMPROVED: Sinkronisasi field definitions dengan values
        dengan batch operations untuk performance
        """
        FieldDefinition = self.env['product.category.field.definition']
        FieldValue = self.env['product.template.field.value']
        
        # Dapatkan field definitions dari kategori
        definitions = FieldDefinition.search([
            ('category_id', '=', product.categ_id.id),
            ('field_type', '=', field_type)
        ])
        
        # Dapatkan existing values
        existing_values = product[f"{field_type}_field_values"]
        existing_def_ids = existing_values.mapped('field_definition_id.id')
        
        # IMPROVED: Batch create untuk definitions baru
        to_create = []
        for definition in definitions:
            if definition.id not in existing_def_ids:
                to_create.append({
                    'field_definition_id': definition.id,
                    'product_id': product.id,
                    'field_type': field_type,
                    'value': '',
                })
        
        if to_create:
            FieldValue.create(to_create)
        
        # Hapus values yang tidak ada di definitions
        to_remove = existing_values.filtered(
            lambda v: v.field_definition_id.id not in definitions.ids
        )
        
        # IMPROVED: Batch delete di variant juga
        if to_remove and product.product_variant_ids:
            variant_values_to_remove = FieldValue.search([
                ('field_definition_id', 'in', to_remove.mapped('field_definition_id.id')),
                ('product_product_id', 'in', product.product_variant_ids.ids)
            ])
            if variant_values_to_remove:
                variant_values_to_remove.unlink()
        
        to_remove.unlink()

    def _sync_fields_to_variants(self, fields_to_sync):
        """
        IMPROVED: Sinkronisasi fields ke variants dengan context untuk prevent loop
        """
        for template in self:
            if not template.product_variant_ids:
                continue
                
            for variant in template.product_variant_ids:
                update_vals = {f: getattr(template, f) for f in fields_to_sync}
                # Use context untuk prevent infinite loop
                variant.with_context(sync_from_template=True).write(update_vals)

    def sync_fields_from_variant(self, variant):
        """
        Sync fields dari variant ke template (reverse sync)
        Digunakan saat user update variant directly
        """
        sync_fields = [
            'motor_type', 'bearing_type', 'knob_switch_speed', 'cable_speed',
            'remote_control', 'tou', 'led', 'manual_book'
        ]
        update_vals = {f: getattr(variant, f) for f in sync_fields}
        # Use context untuk prevent infinite loop
        self.with_context(sync_from_variant=True).write(update_vals)

    def update_all_variants(self):
        """
        Manual action untuk update semua variant dengan nilai dari template
        """
        for template in self:
            _logger.info("Manually syncing all variants for template: %s", template.name)
            for variant in template.product_variant_ids:
                variant._sync_from_template()
        return True

    def action_sync_variant_fields(self):
        """
        Action button untuk sync variants dari UI
        """
        self.update_all_variants()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Sync Complete',
                'message': 'All variant fields updated from template.',
                'type': 'success',
                'sticky': False,
            }
        }


class ProductTemplateFieldValue(models.Model):
    _name = 'product.template.field.value'
    _description = 'Product Template Field Value'
    _order = 'sequence, id'

    field_definition_id = fields.Many2one(
        'product.category.field.definition',
        string='Definition',
        required=True,
        ondelete='cascade',
        index=True  # ADDED: Index untuk performance
    )
    
    name = fields.Char(
        string='Name',
        related='field_definition_id.name',
        readonly=True,
        store=True
    )
    
    sequence = fields.Integer(
        string='Sequence',
        related='field_definition_id.sequence',
        readonly=True,
        store=True
    )
    
    field_type = fields.Selection([
        ('spec', 'Specification'),
        ('material', 'Material'),
        ('cable', 'Cable'),
        ('color', 'Color')],
        string='Field Type',
        required=True,
        index=True  # ADDED: Index untuk performance
    )
    
    value = fields.Char(string='Value')
    
    original_value = fields.Char(
        string='Last Value',
        copy=True,
        help="Stores the original value before locking"
    )
    
    is_locked = fields.Boolean(
        string='Locked',
        default=False,
        help="If checked, value cannot be changed when used in PO"
    )
    
    product_id = fields.Many2one(
        'product.template',
        string='Product Template',
        ondelete='cascade',
        index=True  # ADDED: Index untuk performance
    )
    
    product_product_id = fields.Many2one(
        'product.product',
        string='Product Variant',
        ondelete='cascade',
        index=True  # ADDED: Index untuk performance
    )

    # ADDED: SQL constraints
    _sql_constraints = [
        ('unique_field_per_template',
         'unique(field_definition_id, product_id)',
         'Field definition must be unique per product template!'),
        ('unique_field_per_variant',
         'unique(field_definition_id, product_product_id)',
         'Field definition must be unique per product variant!'),
    ]

    @api.constrains('value', 'is_locked')
    def _check_locked_value(self):
        """
        ADDED: Validation untuk prevent modifikasi locked fields
        """
        for record in self:
            if record.is_locked and record.value != record.original_value:
                # Allow unlock via special context
                if not self.env.context.get('force_unlock'):
                    raise ValidationError(
                        "Cannot modify locked field '%s'.\n"
                        "Original value: %s\n"
                        "Please unlock the field first." % (
                            record.name,
                            record.original_value or '(empty)'
                        )
                    )

    @api.model
    def create(self, vals):
        """
        Override create untuk auto-sync ke variants
        """
        # Skip sync jika sudah dalam context sync
        if self.env.context.get('skip_variant_sync'):
            return super(ProductTemplateFieldValue, self).create(vals)
            
        record = super(ProductTemplateFieldValue, self).create(vals)
        record._sync_to_variants()
        return record

    def write(self, vals):
        """
        IMPROVED: Override write dengan lock validation dan efficient sync
        """
        # Skip sync jika sudah dalam context sync
        if self.env.context.get('skip_variant_sync'):
            return super(ProductTemplateFieldValue, self).write(vals)
        
        # Handle locked fields
        if 'value' in vals:
            for rec in self:
                if rec.is_locked and not self.env.context.get('force_unlock'):
                    # Store original value tapi tidak ubah value
                    vals['original_value'] = vals.get('value', rec.value)
                    vals['value'] = rec.value
                    _logger.warning(
                        "Attempted to modify locked field %s for product %s",
                        rec.name,
                        rec.product_id.name if rec.product_id else rec.product_product_id.name
                    )
        
        res = super(ProductTemplateFieldValue, self).write(vals)
        
        # Sync to variants jika value berubah
        if 'value' in vals:
            self._sync_to_variants()
        
        return res

    def _sync_to_variants(self):
        """
        IMPROVED: Sinkronkan nilai ke semua variant dengan batch operations
        Menghindari multiple queries dalam loop
        """
        for record in self:
            # Skip jika ini adalah variant value (bukan template value)
            if not record.product_id or record.product_product_id:
                continue
            
            try:
                # Get all variants untuk template ini
                variants = self.env['product.product'].search([
                    ('product_tmpl_id', '=', record.product_id.id)
                ])
                
                if not variants:
                    continue
                
                # IMPROVED: Batch query untuk existing values
                existing_values = self.search([
                    ('field_definition_id', '=', record.field_definition_id.id),
                    ('product_product_id', 'in', variants.ids),
                    ('field_type', '=', record.field_type)
                ])
                
                # Create mapping untuk quick lookup
                existing_map = {ev.product_product_id.id: ev for ev in existing_values}
                
                # Prepare batch operations
                to_create = []
                to_update = self.env['product.template.field.value']
                
                for variant in variants:
                    if variant.id in existing_map:
                        # Update existing
                        to_update |= existing_map[variant.id]
                    else:
                        # Create new
                        to_create.append({
                            'field_definition_id': record.field_definition_id.id,
                            'product_product_id': variant.id,
                            'field_type': record.field_type,
                            'value': record.value
                        })
                
                # IMPROVED: Batch operations
                if to_update:
                    to_update.with_context(skip_variant_sync=True).write({
                        'value': record.value
                    })
                
                if to_create:
                    self.with_context(skip_variant_sync=True).create(to_create)
                
                _logger.debug(
                    "Synced field %s to %d variants (updated: %d, created: %d)",
                    record.name,
                    len(variants),
                    len(to_update),
                    len(to_create)
                )
                
            except Exception as e:
                _logger.error(
                    "Error syncing field %s to variants: %s",
                    record.name,
                    str(e)
                )
                # Don't raise to avoid blocking the operation
                # raise