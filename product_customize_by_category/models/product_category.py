from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    spec_field_ids = fields.One2many(
        'product.category.field.definition',
        'category_id',
        string='Specification',
        domain=[('field_type', '=', 'spec')]
    )

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

class ProductCategoryFieldDefinition(models.Model):
    _name = 'product.category.field.definition'
    _description = 'Product Category'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    field_type = fields.Selection([
        ('spec', 'Specification'),
        ('material', 'Material'),
        ('cable', 'Cable'),
        ('color', 'Color'),
        ('motor_type', 'Motor Type'),
        ('bearing_type', 'Bearing Type'),
        ('knob_switch_speed', 'Knob Switch Speed'),
        ('cable_speed', 'Cable Speed'),
        ('remote_control', 'Remote Control'),
        ('tou', 'Therm of Use'),
        ('led', 'LED'),
        ('manual_book', 'Manual Book')],
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