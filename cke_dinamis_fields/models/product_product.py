from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.constrains('categ_id')
    def _check_categ_id(self):
        for product in self:
            if not product.categ_id:
                raise UserError("Setiap produk harus memiliki kategori.")

    import logging
    _logger = logging.getLogger(__name__)

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(ProductProduct, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        
        if view_type == 'form':
            _logger.info(f"Context: {self.env.context}")
            _logger.info(f"Current Record Categ ID: {self.categ_id and self.categ_id.id}")
            
            category_id = self.env.context.get('default_categ_id') or (self.categ_id and self.categ_id.id)
            if category_id:
                category = self.env['product.category'].browse(category_id)
                _logger.info(f"Category Dynamic Fields: {category.dynamic_field_ids}")
                
                for field in category.dynamic_field_ids:
                    if field.name not in res['fields']:
                        res['fields'][field.name] = {
                            'string': field.label,
                            'type': field.field_type,
                            'required': field.required,
                        }
                        res['arch'] = res['arch'].replace(
                            '</sheet>',
                            f'<field name="{field.name}"/>\n</sheet>'
                        )
        return res