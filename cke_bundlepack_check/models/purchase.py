from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    def action_validate_bundles(self):
        """ Tombol validasi utama """
        error_log = []
        for order in self:
            for line in order.order_line.filtered(lambda l: l.product_id.is_pack):
                # Validasi 1: Cek apakah pack memiliki komponen
                if not line.product_id.pack_ids:
                    error_log.append(
                        _("⚠️ Product [%s] is a bundle but has no components!") % 
                        line.product_id.name
                    )
                
                # Validasi 2: Cek apakah receipt sudah sesuai
                moves = line.move_ids.filtered(
                    lambda m: m.state not in ('done', 'cancel')
                )
                for move in moves:
                    if not move.pack_id:
                        error_log.append(
                            _("🚫 Missing bundle components in receipt for product [%s]!") % 
                            line.product_id.name
                        )
        
        if error_log:
            raise UserError("\n".join(error_log))
        
        return {
            'effect': {
                'fadeout': 'slow',
                'message': _('All bundles validated successfully!'),
                'type': 'rainbow_man'
            }
        }

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.constrains('product_id')
    def _check_bundle_components(self):
        """ Constraint untuk validasi pack """
        for line in self:
            if line.product_id.is_pack and not line.product_id.pack_ids:
                raise UserError(
                    _("Product %s is marked as bundle but has no components!") % 
                    line.product_id.name
                )