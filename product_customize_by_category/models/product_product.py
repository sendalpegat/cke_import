from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    spec_field_values = fields.One2many(
        'product.template.field.value',
        'product_product_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

    # motor_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Motor Type',
    #     domain=[('field_type', '=', 'motor')]
    # )

    # bearing_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Bearing Type',
    #     domain=[('field_type', '=', 'bearing')]
    # )

    # kss_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Knob Switch Speed',
    #     domain=[('field_type', '=', 'kss')]
    # )

    # cablespeed_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Cable Speed',
    #     domain=[('field_type', '=', 'cablespeed')]
    # )

    # remote_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Remote Control',
    #     domain=[('field_type', '=', 'remote')]
    # )

    # tou_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Therm of Use',
    #     domain=[('field_type', '=', 'tou')]
    # )

    # led_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='LED',
    #     domain=[('field_type', '=', 'led')]
    # )

    # book_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Manual Book',
    #     domain=[('field_type', '=', 'book')]
    # )

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

    is_locked = fields.Boolean(string='Locked', default=False)  # <-- Tambahkan ini

    # packing_field_values = fields.One2many(
    #     'product.template.field.value',
    #     'product_product_id',
    #     string='Packing Method',
    #     domain=[('field_type', '=', 'packing')]
    # )

    # Kembalikan field summary sebagai related ke template
    spec_field_summary = fields.Char(
        string="Specification Summary", 
        related='product_tmpl_id.spec_field_summary', 
        store=True
    )
    material_field_summary = fields.Char(
        string="Material Summary", 
        related='product_tmpl_id.material_field_summary', 
        store=True
    )
    cable_field_summary = fields.Char(
        string="Cable Summary", 
        related='product_tmpl_id.cable_field_summary', 
        store=True
    )
    color_field_summary = fields.Char(
        string="Color Summary", 
        related='product_tmpl_id.color_field_summary', 
        store=True
    )

    @api.model
    def create(self, vals):
        product = super(ProductProduct, self).create(vals)
        if 'product_tmpl_id' in vals:
            product._sync_from_template()
        return product

    def _sync_from_template(self):
        """Sinkronkan nilai dari template ke variant"""
        for product in self:
            if product.product_tmpl_id:
                # Ambil semua nilai dari template
                template_values = self.env['product.template.field.value'].search([
                    ('product_id', '=', product.product_tmpl_id.id)
                ])

                for tval in template_values:
                    # Cari atau buat record yang sesuai di variant
                    existing_value = self.env['product.template.field.value'].search([
                        ('field_definition_id', '=', tval.field_definition_id.id),
                        ('product_product_id', '=', product.id),
                        ('field_type', '=', tval.field_type)
                    ], limit=1)

                    if existing_value:
                        existing_value.write({'value': tval.value})
                    else:
                        self.env['product.template.field.value'].create({
                            'field_definition_id': tval.field_definition_id.id,
                            'product_product_id': product.id,
                            'field_type': tval.field_type,
                            'value': tval.value
                        })

    def update_from_template(self):
        """Update variant dengan nilai dari template"""
        self._sync_from_template()
        return True

    spec_field_summary = fields.Char(string="Specification Summary", related='product_tmpl_id.spec_field_summary', store=True)
    # motor_field_summary = fields.Char(string="Motor Summary", related='product_tmpl_id.motor_field_summary', store=True)
    # bearing_field_summary = fields.Char(string="Bearing Summary", related='product_tmpl_id.bearing_field_summary', store=True)
    # kss_field_summary = fields.Char(string="KSS Summary", related='product_tmpl_id.kss_field_summary', store=True)
    # cablespeed_field_summary = fields.Char(string="Cable Speed Summary", related='product_tmpl_id.cablespeed_field_summary', store=True)
    # remote_field_summary = fields.Char(string="Remote Summary", related='product_tmpl_id.remote_field_summary', store=True)
    # tou_field_summary = fields.Char(string="Tou Summary", related='product_tmpl_id.tou_field_summary', store=True)
    # led_field_summary = fields.Char(string="Motor Summary", related='product_tmpl_id.led_field_summary', store=True)
    # book_field_summary = fields.Char(string="Book Summary", related='product_tmpl_id.book_field_summary', store=True)
    material_field_summary = fields.Char(string="Material", related='product_tmpl_id.material_field_summary', store=True)
    cable_field_summary = fields.Char(string="Cable", related='product_tmpl_id.cable_field_summary', store=True)
    color_field_summary = fields.Char(string="Color", related='product_tmpl_id.color_field_summary', store=True)
    # packing_field_summary = fields.Char(string="Packing Summary", related='product_tmpl_id.packing_field_summary', store=True)