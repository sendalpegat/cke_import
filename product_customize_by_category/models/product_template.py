from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    spec_field_values = fields.One2many(
        'product.template.field.value',
        'product_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

    # motor_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Motor Type',
    #     domain=[('field_type', '=', 'motor')]
    # )

    # bearing_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Bearing Type',
    #     domain=[('field_type', '=', 'bearing')]
    # )

    # kss_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Knob Switch Speed',
    #     domain=[('field_type', '=', 'kss')]
    # )

    # cablespeed_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Cable Speed',
    #     domain=[('field_type', '=', 'cablespeed')]
    # )

    # remote_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Remote Control',
    #     domain=[('field_type', '=', 'remote')]
    # )

    # tou_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Therm of Use',
    #     domain=[('field_type', '=', 'tou')]
    # )

    # led_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='LED',
    #     domain=[('field_type', '=', 'led')]
    # )

    # book_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Manual Book',
    #     domain=[('field_type', '=', 'book')]
    # )

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
        [('yes', 'Yes - Reset Thermal Protector'), ('no', 'No')],
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

    # packing_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_id',
    #     string='Packing Method',
    #     domain=[('field_type', '=', 'packing')]
    # )
    is_locked = fields.Boolean(string='Locked', default=False)  # <-- Tambahkan ini

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
                # product.motor_field_values = [(5, 0, 0)]
                # product.bearing_field_values = [(5, 0, 0)]
                # product.kss_field_values = [(5, 0, 0)]
                # product.cablespeed_field_values = [(5, 0, 0)]
                # product.remote_field_values = [(5, 0, 0)]
                # product.tou_field_values = [(5, 0, 0)]
                # product.led_field_values = [(5, 0, 0)]
                # product.book_field_values = [(5, 0, 0)]
                product.material_field_values = [(5, 0, 0)]
                product.cable_field_values = [(5, 0, 0)]
                product.color_field_values = [(5, 0, 0)]
                # product.packing_field_values = [(5, 0, 0)]
                continue

            self._sync_field_type(product, 'spec')
            # self._sync_field_type(product, 'motor')
            # self._sync_field_type(product, 'bearing')
            # self._sync_field_type(product, 'kss')
            # self._sync_field_type(product, 'cablespeed')
            # self._sync_field_type(product, 'remote')
            # self._sync_field_type(product, 'tou')
            # self._sync_field_type(product, 'led')
            # self._sync_field_type(product, 'book') 
            self._sync_field_type(product, 'material')
            self._sync_field_type(product, 'cable')
            self._sync_field_type(product, 'color')
            # self._sync_field_type(product, 'packing')

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

    def update_all_variants(self):
        """Update semua variant dengan nilai dari template"""
        for template in self:
            for variant in template.product_variant_ids:
                variant._sync_from_template()
        return True

# Field Summary untuk Semua Grup
    spec_field_summary = fields.Char(string="Specification Summary", compute="_compute_field_summaries", store=True)
    # motor_field_summary = fields.Char(string="Motor Summary", compute="_compute_field_summaries", store=True)
    # bearing_field_summary = fields.Char(string="Bearing Summary", compute="_compute_field_summaries", store=True)
    # kss_field_summary = fields.Char(string="KSS Summary", compute="_compute_field_summaries", store=True)
    # cablespeed_field_summary = fields.Char(string="Cable Speed Summary", compute="_compute_field_summaries", store=True)
    # remote_field_summary = fields.Char(string="Remote Summary", compute="_compute_field_summaries", store=True)
    # tou_field_summary = fields.Char(string="Therm of Use Summary", compute="_compute_field_summaries", store=True)
    # led_field_summary = fields.Char(string="LED Summary", compute="_compute_field_summaries", store=True)
    # book_field_summary = fields.Char(string="Manual Book Summary", compute="_compute_field_summaries", store=True)
    material_field_summary = fields.Char(string="Material Summary", compute="_compute_field_summaries", store=True)
    cable_field_summary = fields.Char(string="Cable Summary", compute="_compute_field_summaries", store=True)
    color_field_summary = fields.Char(string="Color Summary", compute="_compute_field_summaries", store=True)
    # packing_field_summary = fields.Char(string="Packing Summary", compute="_compute_field_summaries", store=True)

    @api.depends(
        'spec_field_values', 'spec_field_values.value',
        # 'motor_field_values', 'motor_field_values.value',
        # 'bearing_field_values', 'bearing_field_values.value',
        # 'kss_field_values', 'kss_field_values.value',
        # 'cablespeed_field_values', 'cablespeed_field_values.value',
        # 'remote_field_values', 'remote_field_values.value',
        # 'tou_field_values', 'tou_field_values.value',
        # 'led_field_values', 'led_field_values.value',
        # 'book_field_values', 'book_field_values.value',
        'material_field_values', 'material_field_values.value',
        'cable_field_values', 'cable_field_values.value',
        'color_field_values', 'color_field_values.value',
        'product_variant_ids.spec_field_values.value',  # Tambahkan dependensi ke Variant
        'product_variant_ids.material_field_values.value',
        'product_variant_ids.cable_field_values.value',
        'product_variant_ids.color_field_values.value'
        # 'packing_field_values', 'packing_field_values.value'
    )
    # def _compute_field_summaries(self):
    #     """Menghitung ringkasan untuk semua grup field"""
    #     for product in self:
    #         # Specification
    #         spec_summary = [
    #             f"{field.name}: {field.value}" 
    #             for field in product.spec_field_values 
    #             if field.value.strip()
    #         ]
    #         product.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""

    #         # Motor Type
    #         # motor_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.motor_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.motor_field_summary = ", ".join(motor_summary) if motor_summary else ""

    #         # Bearing Type
    #         # bearing_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.bearing_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.bearing_field_summary = ", ".join(bearing_summary) if bearing_summary else ""

    #         # kss_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.kss_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.kss_field_summary = ", ".join(kss_summary) if kss_summary else ""


    #         # cablespeed_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.cablespeed_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.cablespeed_field_summary = ", ".join(cablespeed_summary) if cablespeed_summary else ""

    #         # remote_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.remote_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.remote_field_summary = ", ".join(remote_summary) if remote_summary else ""

    #         # tou_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.tou_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.tou_field_summary = ", ".join(tou_summary) if tou_summary else ""

    #         # led_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.led_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.led_field_summary = ", ".join(led_summary) if led_summary else ""

    #         # book_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.book_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.book_field_summary = ", ".join(book_summary) if book_summary else ""

    #         material_summary = [
    #             f"{field.name}: {field.value}" 
    #             for field in product.material_field_values 
    #             if field.value.strip()
    #         ]
    #         product.material_field_summary = ", ".join(material_summary) if material_summary else ""

    #         cable_summary = [
    #             f"{field.name}: {field.value}" 
    #             for field in product.cable_field_values 
    #             if field.value.strip()
    #         ]
    #         product.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""

    #         color_summary = [
    #             f"{field.name}: {field.value}" 
    #             for field in product.color_field_values 
    #             if field.value.strip()
    #         ]
    #         product.color_field_summary = ", ".join(color_summary) if color_summary else ""

    #         # packing_summary = [
    #         #     f"{field.name}: {field.value}" 
    #         #     for field in product.packing_field_values 
    #         #     if field.value.strip()
    #         # ]
    #         # product.packing_field_summary = ", ".join(packing_summary) if packing_summary else ""

    def _compute_field_summaries(self):
        """Hitung summary dari nilai Template DAN Variant"""
        for template in self:
            # Ambil semua nilai dari Template dan Variant
            all_spec_values = template.spec_field_values + template.product_variant_ids.mapped('spec_field_values')
            all_material_values = template.material_field_values + template.product_variant_ids.mapped('material_field_values')
            all_cable_values = template.cable_field_values + template.product_variant_ids.mapped('cable_field_values')
            all_color_values = template.color_field_values + template.product_variant_ids.mapped('color_field_values')

            # Hitung summary
            spec_summary = [f"{v.name}: {v.value}" for v in all_spec_values if v.value.strip()]
            material_summary = [f"{v.name}: {v.value}" for v in all_material_values if v.value.strip()]
            cable_summary = [f"{v.name}: {v.value}" for v in all_cable_values if v.value.strip()]
            color_summary = [f"{v.name}: {v.value}" for v in all_color_values if v.value.strip()]

            template.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""
            template.material_field_summary = ", ".join(material_summary) if material_summary else ""
            template.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""
            template.color_field_summary = ", ".join(color_summary) if color_summary else ""

    def action_unlock_custom_fields(self):
        """Unlock all custom field values so they can be edited again."""
        for rec in self:
            rec.is_locked = False
            # Unlock semua custom field values
            all_field_lines = (
                rec.spec_field_values +
                rec.material_field_values +
                rec.cable_field_values +
                rec.color_field_values
            )
            for field_val in all_field_lines:
                field_val.is_locked = False
        return True

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
        # ('motor', 'Motor type'),
        # ('bearing', 'Bearing Type'),
        # ('kss', 'Knob Switch Speed'),
        # ('cablespeed', 'Cable Speed'),
        # ('remote', 'Remote Control'),
        # ('tou', 'Therm of Use'),
        # ('led', 'LED'),
        # ('book', 'Manual Book'),
        ('material', 'Material'),
        ('cable', 'Cable'),
        ('color', 'Color')],
        # ('packing', 'Packing Method')],
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
        if 'value' in vals and any(rec.is_locked for rec in self):
            for rec in self:
                if rec.is_locked:
                    vals['original_value'] = vals.get('value', rec.value)
                    vals['value'] = rec.value
        return super(ProductTemplateFieldValue, self).write(vals)

    @api.model
    def create(self, vals):
        record = super(ProductTemplateFieldValue, self).create(vals)
        record._sync_to_variants()
        return record

    def write(self, vals):
        res = super(ProductTemplateFieldValue, self).write(vals)
        if 'value' in vals:
            self._sync_to_variants()
        return res

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

    def write(self, vals):
        # Jika nilai diubah di variant, update nilai di template
        res = super(ProductTemplateFieldValue, self).write(vals)
        for record in self:
            if record.product_product_id and 'value' in vals:
                # Cari field yang sama di Template
                template_value = self.env['product.template.field.value'].search([
                    ('field_definition_id', '=', record.field_definition_id.id),
                    ('product_id', '=', record.product_product_id.product_tmpl_id.id),
                ], limit=1)
                if template_value:
                    template_value.write({'value': vals['value']})
        return res