from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    spec_field_ids = fields.One2many(
        'product.category.field.definition',
        'category_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

    # motor_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Motor Type',
    #     domain=[('field_type', '=', 'motor')]
    # )

    # bearing_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='bearing Type',
    #     domain=[('field_type', '=', 'bearing')]
    # )

    # kss_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Knob Switch Speed',
    #     domain=[('field_type', '=', 'kss')]
    # )

    # cablespeed_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Cable Speed',
    #     domain=[('field_type', '=', 'cablespeed')]
    # )

    # remote_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Remote Control',
    #     domain=[('field_type', '=', 'remote')]
    # )

    # tou_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Therm of Use',
    #     domain=[('field_type', '=', 'tou')]
    # )

    # led_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='LED',
    #     domain=[('field_type', '=', 'led')]
    # )

    # book_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Manual Book',
    #     domain=[('field_type', '=', 'book')]
    # )

    material_field_ids = fields.One2many(
        'product.category.field.definition',
        'category_id',
        string='Material',
        domain=[('field_type', '=', 'material')]
    )

    cable_field_ids = fields.One2many(
        'product.category.field.definition',
        'category_id',
        string='Cable',
        domain=[('field_type', '=', 'cable')]
    )

    color_field_ids = fields.One2many(
        'product.category.field.definition',
        'category_id',
        string='Color',
        domain=[('field_type', '=', 'color')]
    )

    # packing_field_ids = fields.One2many(
    #     'product.category.field.definition',
    #     'category_id',
    #     string='Packing Method',
    #     domain=[('field_type', '=', 'packing')]
    # )

class ProductCategoryFieldDefinition(models.Model):
    _name = 'product.category.field.definition'
    _description = 'Product Category'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
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
        string='Type',
        required=True,
        default='spec'
    )
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        ondelete='cascade'
    )

    @api.model
    def create(self, vals):
        if 'field_type' not in vals:
            if self.env.context.get('default_field_type'):
                vals['field_type'] = self.env.context.get('default_field_type')
            else:
                vals['field_type'] = 'spec'
        return super(ProductCategoryFieldDefinition, self).create(vals)