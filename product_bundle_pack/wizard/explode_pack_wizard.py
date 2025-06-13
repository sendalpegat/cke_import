# File: wizard/explode_pack_wizard.py
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

        # Hapus invoice line pack
        lines_to_remove = move.invoice_line_ids.filtered(lambda l: l.product_id.product_tmpl_id.is_pack)
        lines_to_remove.unlink()

        total_debit = 0.0

        # Tambahkan komponen baru
        for line in self.line_ids:
            if line.price_unit <= 0:
                raise UserError(
                    f"Komponen \"{line.product_id.display_name}\" memiliki harga 0.\n"
                    "Silakan isi Standard Price terlebih dahulu untuk menghindari jurnal tidak seimbang."
                )

            if line.qty_uom <= 0:
                raise UserError(
                    f"Kuantitas tidak valid untuk komponen \"{line.product_id.display_name}\"."
                )

            account_id = line.account_id.id
            total = line.qty_uom * line.price_unit
            total_debit += total

            self.env['account.move.line'].create({
                'move_id': move.id,
                'product_id': line.product_id.id,
                'quantity': line.qty_uom,
                'price_unit': line.price_unit,
                'account_id': account_id,
                'debit': total,
                'name': line.description,
            })

        # Tambahkan baris hutang vendor (credit)
        partner = move.partner_id
        payable_account = partner.property_account_payable_id
        if not payable_account:
            raise UserError("Vendor tidak memiliki akun hutang yang disetel. Periksa 'Account Payable' di form vendor.")

        self.env['account.move.line'].create({
            'move_id': move.id,
            'account_id': payable_account.id,
            'partner_id': partner.id,
            'credit': total_debit,
            'name': 'Hutang dari komponen produk bundle',
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

    def _check_balanced(self):
        return True