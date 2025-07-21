from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

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

    @api.depends(
        'spec_field_values', 'spec_field_values.value',
        'material_field_values', 'material_field_values.value',
        'cable_field_values', 'cable_field_values.value',
        'color_field_values', 'color_field_values.value',
    )
    def _compute_field_summaries(self):
        for variant in self:
            # Specification
            spec_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.spec_field_values 
                if field.value and field.value.strip()
            ]
            variant.spec_field_summary = ", ".join(spec_summary) if spec_summary else ""

            material_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.material_field_values 
                if field.value and field.value.strip()
            ]
            variant.material_field_summary = ", ".join(material_summary) if material_summary else ""

            cable_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.cable_field_values 
                if field.value and field.value.strip()
            ]
            variant.cable_field_summary = ", ".join(cable_summary) if cable_summary else ""

            color_summary = [
                f"{field.name}: {field.value}" 
                for field in variant.color_field_values 
                if field.value and field.value.strip()
            ]
            variant.color_field_summary = ", ".join(color_summary) if color_summary else ""


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
        product = super(ProductProduct, self).create(vals)
        if 'product_tmpl_id' in vals:
            product._sync_from_template()
        return product

    def update_from_template(self):
        """Update variant dengan nilai dari template"""
        self._sync_from_template()
        return True

    # spec_field_summary = fields.Char(string="Specification Summary", related='product_tmpl_id.spec_field_summary', store=True)
    # cable_field_summary = fields.Char(string="Cable", related='product_tmpl_id.cable_field_summary', store=True)
    # color_field_summary = fields.Char(string="Color", related='product_tmpl_id.color_field_summary', store=True)