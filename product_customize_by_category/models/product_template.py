from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

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
        string='Therm of Use',
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

    is_locked = fields.Boolean(string='Locked', default=False)  # <-- Tambahkan ini

    def update_all_variants(self):
        """Update semua variant dengan nilai dari template"""
        for template in self:
            for variant in template.product_variant_ids:
                variant._sync_from_template()
        return True

    def action_sync_variant_fields(self):
        self.update_all_variants()
        # Optional: message popup
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': ('Sync Complete'),
                'message': ('All variant fields updated from template.'),
                'sticky': False,
            }
        }

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        if 'categ_id' in vals:
            product._update_custom_fields()
        return product

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'categ_id' in vals:
            self._update_custom_fields()
        return res

    @api.onchange('categ_id')
    def _onchange_categ_id_update_fields(self):
        self._update_custom_fields()

    def _update_custom_fields(self):
        FieldDefinition = self.env['product.category.field.definition']
        FieldValue = self.env['product.template.field.value']
        
        for product in self:
            if not product.categ_id:
                product.spec_field_values = [(5, 0, 0)]
                product.material_field_values = [(5, 0, 0)]
                product.cable_field_values = [(5, 0, 0)]
                product.color_field_values = [(5, 0, 0)]
                continue

            self._sync_field_type(product, 'spec') 
            self._sync_field_type(product, 'material')
            self._sync_field_type(product, 'cable')
            self._sync_field_type(product, 'color')

            # Sinkronkan ke semua variant yang sudah ada
            if product.product_variant_ids:
                for variant in product.product_variant_ids:
                    variant._sync_from_template()

    def _sync_field_type(self, product, field_type):
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
        
        # Buat values untuk definitions baru
        for definition in definitions:
            if definition.id not in existing_def_ids:
                FieldValue.create({
                    'field_definition_id': definition.id,
                    'product_id': product.id,
                    'field_type': field_type,
                    'value': '',
                })
        
        # Hapus values yang tidak ada di definitions
        to_remove = existing_values.filtered(
            lambda v: v.field_definition_id.id not in definitions.ids
        )
        # Hapus juga di variant
        if to_remove and product.product_variant_ids:
            variant_values_to_remove = FieldValue.search([
                ('field_definition_id', 'in', to_remove.mapped('field_definition_id.id')),
                ('product_product_id', 'in', product.product_variant_ids.ids)
            ])
            variant_values_to_remove.unlink()
        to_remove.unlink()


# Field Summary untuk Semua Grup
    spec_field_summary = fields.Char(string="Specification Summary", compute="_compute_field_summaries", store=True)
    material_field_summary = fields.Char(string="Material Summary", compute="_compute_field_summaries", store=True)
    cable_field_summary = fields.Char(string="Cable Summary", compute="_compute_field_summaries", store=True)
    color_field_summary = fields.Char(string="Color Summary", compute="_compute_field_summaries", store=True)

    @api.depends(
        'spec_field_values', 'spec_field_values.value',
        'material_field_values', 'material_field_values.value',
        'cable_field_values', 'cable_field_values.value',
        'color_field_values', 'color_field_values.value',
    )
    def _compute_field_summaries(self):
        """Menghitung ringkasan untuk semua grup field"""
        for product in self:
            # Specification
            spec_summary = [
                f"{field.name}: {field.value}" 
                for field in product.spec_field_values 
                if field.value.strip()
            ]
            product.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""

            material_summary = [
                f"{field.name}: {field.value}" 
                for field in product.material_field_values 
                if field.value.strip()
            ]
            product.material_field_summary = ", ".join(material_summary) if material_summary else ""

            cable_summary = [
                f"{field.name}: {field.value}" 
                for field in product.cable_field_values 
                if field.value.strip()
            ]
            product.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""

            color_summary = [
                f"{field.name}: {field.value}" 
                for field in product.color_field_values 
                if field.value.strip()
            ]
            product.color_field_summary = ", ".join(color_summary) if color_summary else ""

class ProductTemplateFieldValue(models.Model):
    _name = 'product.template.field.value'
    _description = 'Product Template Value'
    _order = 'sequence, id'

    field_definition_id = fields.Many2one(
        'product.category.field.definition',
        string='Definition',
        required=True,
        ondelete='cascade'
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
        required=True
    )
    value = fields.Char(string='Value')
    original_value = fields.Char(string='Last Value', copy=True)
    is_locked = fields.Boolean(string='Locked', default=False,
                             help="If checked, value cannot be changed when used in PO")
    product_id = fields.Many2one(
        'product.template',
        string='Product',
        ondelete='cascade'
    )
    product_product_id = fields.Many2one(
        'product.product',
        string='Product Variant',
        ondelete='cascade'
    )

    def write(self, vals):
        # Lock value jika field locked
        if 'value' in vals:
            for rec in self:
                if rec.is_locked:
                    vals['original_value'] = vals.get('value', rec.value)
                    vals['value'] = rec.value
        res = super(ProductTemplateFieldValue, self).write(vals)
        if 'value' in vals:
            self._sync_to_variants()
        return res

    @api.model
    def create(self, vals):
        record = super(ProductTemplateFieldValue, self).create(vals)
        record._sync_to_variants()
        return record

    def _sync_to_variants(self):
        """Sinkronkan nilai ke semua variant produk"""
        for record in self:
            if record.product_id:
                # Update semua variant dari template ini
                variants = self.env['product.product'].search([
                    ('product_tmpl_id', '=', record.product_id.id)
                ])
                for variant in variants:
                    # Cari atau buat record yang sesuai di variant
                    existing_value = self.search([
                        ('field_definition_id', '=', record.field_definition_id.id),
                        ('product_product_id', '=', variant.id),
                        ('field_type', '=', record.field_type)
                    ], limit=1)

                    if existing_value:
                        existing_value.write({'value': record.value})
                    else:
                        self.create({
                            'field_definition_id': record.field_definition_id.id,
                            'product_product_id': variant.id,
                            'field_type': record.field_type,
                            'value': record.value
                        })