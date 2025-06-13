from odoo import api, fields, models

class ProductCategory(models.Model):
    _inherit = 'product.category'

    template_field_ids = fields.One2many(
        'product.template.field', 'category_id', string='Template Fields'
    )

class ProductTemplateField(models.Model):
    _name = 'product.template.field'
    _description = 'Product Template Field'

    name = fields.Char(string='Field Name', required=True)
    field_type = fields.Selection([
        ('char', 'Text'),
        ('integer', 'Integer'),
        ('boolean', 'Checkbox'),
    ], string='Field Type', required=True, default='char')
    category_id = fields.Many2one('product.category', string='Category', required=True)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dynamic_field_values = fields.One2many(
        'product.dynamic.field.value', 'product_id', string='Dynamic Field Values'
    )

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        if self.categ_id:
            template_fields = self.categ_id.template_field_ids
            self.dynamic_field_values = [(5, 0, 0)]  # Clear existing values
            for field in template_fields:
                self.dynamic_field_values = [(0, 0, {
                    'name': field.name,
                    'field_type': field.field_type,
                })]

class ProductDynamicFieldValue(models.Model):
    _name = 'product.dynamic.field.value'
    _description = 'Dynamic Field Value'

    name = fields.Char(string='Field Name')
    field_type = fields.Selection([
        ('char', 'Text'),
        ('integer', 'Integer'),
        ('boolean', 'Checkbox'),
    ], string='Field Type', readonly=True)
    value_char = fields.Char(string='Text Value')
    value_integer = fields.Integer(string='Integer Value')
    value_boolean = fields.Boolean(string='Checkbox Value')
    product_id = fields.Many2one('product.template', string='Product')

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    dynamic_field_values = fields.One2many(
        'purchase.dynamic.field.value', 'order_line_id', string='Dynamic Field Values'
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.dynamic_field_values = [(5, 0, 0)]  # Clear existing values
            for field_value in self.product_id.dynamic_field_values:
                self.dynamic_field_values = [(0, 0, {
                    'name': field_value.name,
                    'field_type': field_value.field_type,
                    'value_char': field_value.value_char,
                    'value_integer': field_value.value_integer,
                    'value_boolean': field_value.value_boolean,
                })]

class PurchaseDynamicFieldValue(models.Model):
    _name = 'purchase.dynamic.field.value'
    _description = 'Purchase Dynamic Field Value'

    name = fields.Char(string='Field Name')
    field_type = fields.Selection([
        ('char', 'Text'),
        ('integer', 'Integer'),
        ('boolean', 'Checkbox'),
    ], string='Field Type', readonly=True)
    value_char = fields.Char(string='Text Value')
    value_integer = fields.Integer(string='Integer Value')
    value_boolean = fields.Boolean(string='Checkbox Value')
    order_line_id = fields.Many2one('purchase.order.line', string='Purchase Order Line')