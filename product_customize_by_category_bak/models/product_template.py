# models/product_template.py
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    custom_field_data = fields.One2many(
        'product.template.custom.field',
        'product_id',
        string='Custom Fields'
    )
    
    spec_field_summary = fields.Text(
        compute='_compute_field_summaries',
        store=True
    )
    material_field_summary = fields.Text(
        compute='_compute_field_summaries',
        store=True
    )
    cable_field_summary = fields.Text(
        compute='_compute_field_summaries',
        store=True
    )
    color_field_summary = fields.Text(
        compute='_compute_field_summaries',
        store=True
    )

    def action_sync_custom_fields(self):
        for product in self:
            product._update_custom_fields()

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        self._update_custom_fields()

    def _update_custom_fields(self):
        for product in self:
            existing_fields = product.custom_field_data.mapped('field_id')
            new_fields = product.categ_id.custom_field_ids.filtered(
                lambda f: f not in existing_fields
            )
            
            product.custom_field_data = [
                (0, 0, {
                    'field_id': field.id,
                    'field_name': field.name,
                    'field_type': field.field_type,
                    'value': ''
                }) for field in new_fields
            ]

    @api.depends('custom_field_data.value')
    def _compute_field_summaries(self):
        for product in self:
            summaries = {'spec': [], 'material': [], 'cable': [], 'color': []}
            
            for data in product.custom_field_data:
                summaries[data.field_type].append(
                    f"{data.field_name}: {data.value}"
                )
            
            product.spec_field_summary = ", ".join(summaries['spec'])
            product.material_field_summary = ", ".join(summaries['material'])
            product.cable_field_summary = ", ".join(summaries['cable'])
            product.color_field_summary = ", ".join(summaries['color'])

class ProductTemplateCustomField(models.Model):
    _name = 'product.template.custom.field'
    _description = 'Custom Field Data for Product'
    
    field_id = fields.Many2one(
        'product.category.custom.field',
        required=True,
        ondelete='cascade'
    )
    field_name = fields.Char(related='field_id.name', store=True)
    field_type = fields.Selection(related='field_id.field_type', store=True)
    value = fields.Char()
    product_id = fields.Many2one('product.template', ondelete='cascade')