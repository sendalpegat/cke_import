from odoo import models, fields, api

class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_field_ids = fields.One2many(
        'product.category.custom.field',
        'category_id',
        string='Specification',
        help='Fields to be dynamically added to products under this category.'
    )

    custom_field2_ids = fields.One2many(
        'product.category.custom.field2',
        'category_id',
        string='Material',
        help='Additional fields to be dynamically added to products under this category.'
    )

    custom_field3_ids = fields.One2many(
        'product.category.custom.field3',
        'category_id',
        string='Cable',
        help='Additional fields to be dynamically added to products under this category.'
    )

    custom_field4_ids = fields.One2many(
        'product.category.custom.field4',
        'category_id',
        string='Color',
        help='Additional fields to be dynamically added to products under this category.'
    )

class ProductCategoryCustomField(models.Model):
    _name = 'product.category.custom.field'
    _description = 'Custom Field for Product Specification'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Specification', ondelete='cascade')

class ProductCategoryCustomField2(models.Model):
    _name = 'product.category.custom.field2'
    _description = 'Custom Field for Product Material'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Material', ondelete='cascade')

class ProductCategoryCustomField3(models.Model):
    _name = 'product.category.custom.field3'
    _description = 'Custom Field for Product Cable'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Cable', ondelete='cascade')

class ProductCategoryCustomField4(models.Model):
    _name = 'product.category.custom.field4'
    _description = 'Custom Field for Product Color'

    name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    category_id = fields.Many2one('product.category', string='Color', ondelete='cascade')

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    custom_field_data = fields.One2many(
        'product.template.custom.field',
        'product_id',
        string='Specification',
        compute='_compute_custom_field_data',
        store=True
    )

    custom_field_data2 = fields.One2many(
        'product.template.custom.field2',
        'product_id',
        string='Material',
        compute='_compute_custom_field_data',
        store=True
    )

    custom_field_data3 = fields.One2many(
        'product.template.custom.field3',
        'product_id',
        string='Cable',
        compute='_compute_custom_field_data',
        store=True
    )

    custom_field_data4 = fields.One2many(
        'product.template.custom.field4',
        'product_id',
        string='Color',
        compute='_compute_custom_field_data',
        store=True
    )

    @api.depends('categ_id', 'categ_id.custom_field_ids', 'categ_id.custom_field_ids.name', 'categ_id.custom_field_ids.value',
                 'categ_id.custom_field2_ids', 'categ_id.custom_field2_ids.name', 'categ_id.custom_field2_ids.value', 'categ_id.custom_field3_ids', 'categ_id.custom_field3_ids.name', 'categ_id.custom_field3_ids.value', 'categ_id.custom_field4_ids', 'categ_id.custom_field4_ids.name', 'categ_id.custom_field4_ids.value')
    # @api.depends('categ_id')
    def _compute_custom_field_data(self):
        for product in self:
            if product.categ_id:
                # Specification
                field_data1 = [
                    (0, 0, {'field_name': field.name, 'value': field.value, 'product_id': product.id})
                    for field in product.categ_id.custom_field_ids
                ]
                product.custom_field_data = field_data1

                # Material
                field_data2 = [
                    (0, 0, {'field_name': field.name, 'value': field.value, 'product_id': product.id})
                    for field in product.categ_id.custom_field2_ids
                ]
                product.custom_field_data2 = field_data2

                # Cable
                field_data3 = [
                    (0, 0, {'field_name': field.name, 'value': field.value, 'product_id': product.id})
                    for field in product.categ_id.custom_field3_ids
                ]
                product.custom_field_data3 = field_data3

                # Color
                field_data4 = [
                    (0, 0, {'field_name': field.name, 'value': field.value, 'product_id': product.id})
                    for field in product.categ_id.custom_field4_ids
                ]
                product.custom_field_data4 = field_data4

    # Field baru untuk menyimpan hasil penggabungan
    spec_field_summary = fields.Text(
        string='Specification Summary',
        compute='_compute_spec_field_summary',
        store=True
    )

    material_field_summary = fields.Text(
        string='Material Summary',
        compute='_compute_material_field_summary',
        store=True
    )

    cable_field_summary = fields.Text(
        string='Cable Summary',
        compute='_compute_cable_field_summary',
        store=True
    )

    color_field_summary = fields.Text(
        string='Color Summary',
        compute='_compute_color_field_summary',
        store=True
    )

    @api.depends('categ_id', 'categ_id.custom_field_ids')
    def _compute_spec_field_summary(self):
        for product in self:
            summary = []

            # Menggabungkan data dari custom_field_ids (Specification)
            for field in product.categ_id.custom_field_ids:
                summary.append(f"{field.name} : {field.value}")

            # Menggabungkan semua data menjadi satu string dengan pemisah koma
            product.spec_field_summary = ", ".join(summary) if summary else ""

    @api.depends('categ_id', 'categ_id.custom_field2_ids')
    def _compute_material_field_summary(self):
        for product in self:
            summary = []

            # Menggabungkan data dari custom_field_ids (Specification)
            for field in product.categ_id.custom_field2_ids:
                summary.append(f"{field.name} : {field.value}")

            # Menggabungkan semua data menjadi satu string dengan pemisah koma
            product.material_field_summary = ", ".join(summary) if summary else ""

    @api.depends('categ_id', 'categ_id.custom_field3_ids')
    def _compute_cable_field_summary(self):
        for product in self:
            summary = []

            # Menggabungkan data dari custom_field_ids (Specification)
            for field in product.categ_id.custom_field3_ids:
                summary.append(f"{field.name} : {field.value}")

            # Menggabungkan semua data menjadi satu string dengan pemisah koma
            product.cable_field_summary = ", ".join(summary) if summary else ""

    @api.depends('categ_id', 'categ_id.custom_field4_ids')
    def _compute_color_field_summary(self):
        for product in self:
            summary = []

            # Menggabungkan data dari custom_field_ids (Specification)
            for field in product.categ_id.custom_field4_ids:
                summary.append(f"{field.name} : {field.value}")

            # Menggabungkan semua data menjadi satu string dengan pemisah koma
            product.color_field_summary = ", ".join(summary) if summary else ""

class ProductTemplateCustomField(models.Model):
    _name = 'product.template.custom.field'
    _description = 'Custom Field Data for Product Template Specification'

    field_name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    product_id = fields.Many2one('product.template', string='Specification', ondelete='cascade')

class ProductTemplateCustomField2(models.Model):
    _name = 'product.template.custom.field2'
    _description = 'Custom Field Data for Product Template Material'

    field_name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    product_id = fields.Many2one('product.template', string='Material', ondelete='cascade')

class ProductTemplateCustomField3(models.Model):
    _name = 'product.template.custom.field3'
    _description = 'Custom Field Data for Product Template Cable'

    field_name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    product_id = fields.Many2one('product.template', string='Cable', ondelete='cascade')

class ProductTemplateCustomField4(models.Model):
    _name = 'product.template.custom.field4'
    _description = 'Custom Field Data for Product Template Color'

    field_name = fields.Char(string='Name', required=True)
    value = fields.Char(string='Value')
    product_id = fields.Many2one('product.template', string='Color', ondelete='cascade')