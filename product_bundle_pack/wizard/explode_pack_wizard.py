from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ExplodePackWizard(models.TransientModel):
    _name = 'explode.pack.wizard'
    _description = 'Explode Product Pack to Components'

    move_id = fields.Many2one('account.move', string="Vendor Bill", required=True)
    line_ids = fields.One2many('explode.pack.line', 'wizard_id', string="Pack Lines")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        move = self.env['account.move'].browse(active_id)
        if not move or move.move_type != 'in_invoice':
            raise UserError("This wizard only works with Vendor Bills.")

        pack_lines = []
        for line in move.invoice_line_ids:
            product = line.product_id
            if product and product.product_tmpl_id.is_pack:
                for pack in product.product_tmpl_id.pack_ids:
                    account_id = line.account_id.id or \
                        pack.product_id.property_account_expense_id.id or \
                        pack.product_id.categ_id.property_account_expense_categ_id.id
                    if not account_id:
                        raise UserError(f"Missing expense account for product {pack.product_id.display_name}.")

                    pack_lines.append((0, 0, {
                        'product_id': pack.product_id.id,
                        'qty_uom': pack.qty_uom * line.quantity,
                        'price_unit': pack.product_id.standard_price,
                        'account_id': account_id,
                        'description': f"{pack.product_id.name} (from {product.name})",
                    }))
        res.update({
            'move_id': active_id,
            'line_ids': pack_lines,
        })
        return res

    def button_confirm(self):
        self.ensure_one()
        move = self.move_id
        order_ref = move.purchase_id.name  # Ambil referensi PO

        # Hapus invoice line pack
        lines_to_remove = move.invoice_line_ids.filtered(lambda l: l.product_id.product_tmpl_id.is_pack)
        lines_to_remove.unlink()

        # Tambahkan komponen baru
        for line in self.line_ids:
            self.env['account.move.line'].create({
                'move_id': move.id,
                'product_id': line.product_id.id,
        
                'quantity': line.qty_uom,
                'price_unit': line.price_unit,
                'account_id': line.account_id.id,
                'name': f"[{order_ref}] {line.description}" if order_ref else line.description,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }


class ExplodePackLine(models.TransientModel):
    _name = 'explode.pack.line'
    _description = 'Pack Component Line'

    wizard_id = fields.Many2one('explode.pack.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Component", required=True)
    qty_uom = fields.Float("Quantity", required=True)
    price_unit = fields.Float("Cost", required=True)
    account_id = fields.Many2one('account.account', string="Expense Account", required=True)
    description = fields.Char("Description")


# OPTIONAL: Inject button into account.move via product_bundle_pack
class AccountMove(models.Model):
    _inherit = 'account.move'

    def explode_pack_button(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Explode Product Pack'),
            'res_model': 'explode.pack.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_move_id': self.id},
        }
    # Hiangkan jika Akunting dijalankan (module: account_accountant)
    def _check_balanced(self):
        return True