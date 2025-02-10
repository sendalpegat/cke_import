class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_field_ids = fields.One2many(
        'product.category.custom.field',
        'category_id',
        string='Specification',
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

    @api.model
    def create(self, vals):
        # Tambahkan default value untuk custom_field_ids
        if 'custom_field_ids' not in vals:
            vals['custom_field_ids'] = [(0, 0, {
                'name': 'Default Name',
                'field_type': 'char',
            })]
        return super(ProductCategory, self).create(vals)

    def create(self, vals):
        # Tambahkan default value untuk custom_field_ids
        if 'custom_field2_ids' not in vals:
            vals['custom_field2_ids'] = [(0, 0, {
                'name': 'Default Name',
                'field_type': 'char',
            })]
        return super(ProductCategory, self).create(vals)

    def create(self, vals):
        # Tambahkan default value untuk custom_field_ids
        if 'custom_field3_ids' not in vals:
            vals['custom_field3_ids'] = [(0, 0, {
                'name': 'Default Name',
                'field_type': 'char',
            })]
        return super(ProductCategory, self).create(vals)

    def create(self, vals):
        # Tambahkan default value untuk custom_field_ids
        if 'custom_field4_ids' not in vals:
            vals['custom_field4_ids'] = [(0, 0, {
                'name': 'Default Name',
                'field_type': 'char',
            })]
        return super(ProductCategory, self).create(vals)