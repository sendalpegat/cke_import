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

        # List product_id yang sudah ada di invoice lines
        exploded_product_ids = move.invoice_line_ids.mapped('product_id').ids
        pack_lines = []

        for line in move.invoice_line_ids:
            product = line.product_id
            if product and product.product_tmpl_id.is_pack:
                # Komponen bundle yang BELUM ada di invoice lines
                for pack in product.product_tmpl_id.pack_ids:
                    if pack.product_id.id not in exploded_product_ids:
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
                            'selected': True,
                        }))

        res.update({
            'move_id': active_id,
            'line_ids': pack_lines,
        })
        return res

    def button_confirm(self):
        self.ensure_one()
        move = self.move_id
        order_ref = move.purchase_id.name

        # Selalu hapus SEMUA invoice line dengan is_pack=True (tidak peduli sudah partial atau belum)
        pack_lines = move.invoice_line_ids.filtered(lambda l: l.product_id and l.product_id.product_tmpl_id.is_pack)
        pack_lines.unlink()

        # Tambahkan komponen baru yang dipilih (selected)
        for line in self.line_ids.filtered(lambda l: l.selected):
            self.env['account.move.line'].create({
                'move_id': move.id,
                'product_id': line.product_id.id,
                'quantity': line.qty_uom,
                'price_unit': line.price_unit,
                'account_id': line.account_id.id,
                'name': f"[{order_ref}] {line.description}" if order_ref else line.description,
                'is_exploded_component': True,  # flag strict jika dipakai
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # @api.model
    # def default_get(self, fields_list):
    #     res = super().default_get(fields_list)
    #     active_id = self.env.context.get('active_id')
    #     move = self.env['account.move'].browse(active_id)
    #     if not move or move.move_type != 'in_invoice':
    #         raise UserError("This wizard only works with Vendor Bills.")

    #     pack_lines = []
    #     for line in move.invoice_line_ids:
    #         product = line.product_id
    #         if product and product.product_tmpl_id.is_pack:
    #             for pack in product.product_tmpl_id.pack_ids:
    #                 account_id = line.account_id.id or \
    #                     pack.product_id.property_account_expense_id.id or \
    #                     pack.product_id.categ_id.property_account_expense_categ_id.id
    #                 if not account_id:
    #                     raise UserError(f"Missing expense account for product {pack.product_id.display_name}.")

    #                 pack_lines.append((0, 0, {
    #                     'product_id': pack.product_id.id,
    #                     'qty_uom': pack.qty_uom * line.quantity,
    #                     'price_unit': pack.product_id.standard_price,
    #                     'account_id': account_id,
    #                     'description': f"{pack.product_id.name} (from {product.name})",
    #                 }))
    #     res.update({
    #         'move_id': active_id,
    #         'line_ids': pack_lines,
    #     })
    #     return res

    # def button_confirm(self):
    #     self.ensure_one()
    #     move = self.move_id
    #     order_ref = move.purchase_id.name  # Ambil referensi PO

    #     # Hapus invoice line pack
    #     lines_to_remove = move.invoice_line_ids.filtered(lambda l: l.product_id.product_tmpl_id.is_pack)
    #     lines_to_remove.unlink()

    #     # # Tambahkan komponen baru
    #     # for line in self.line_ids:
    #     # Tambahkan komponen baru yang selected saja
    #     for line in self.line_ids.filtered(lambda l: l.selected):
    #         self.env['account.move.line'].create({
    #             'move_id': move.id,
    #             'product_id': line.product_id.id,        
    #             'quantity': line.qty_uom,
    #             'price_unit': line.price_unit,
    #             'account_id': line.account_id.id,
    #             'name': f"[{order_ref}] {line.description}" if order_ref else line.description,
    #         })

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.move',
    #         'res_id': move.id,
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }


class ExplodePackLine(models.TransientModel):
    _name = 'explode.pack.line'
    _description = 'Pack Component Line'

    wizard_id = fields.Many2one('explode.pack.wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Component", required=True)
    qty_uom = fields.Float("Quantity", required=True)
    price_unit = fields.Float("Cost", required=True)
    account_id = fields.Many2one('account.account', string="Expense Account", required=True)
    description = fields.Char("Description")
    selected = fields.Boolean(string='Select', default=True)


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

    def action_post(self):
        res = super().action_post()
        # Lakukan otomatisasi hanya untuk vendor bill hasil explode packs
        for move in self:
            if move.move_type == 'in_invoice' and move.purchase_id:
                # Cari semua picking yang terkait PO
                pickings = move.purchase_id.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel'])
                for picking in pickings:
                    for move_line in move.invoice_line_ids:
                        # Cek apakah product_id dari komponen ada di picking move
                        pick_move = picking.move_lines.filtered(lambda m: m.product_id == move_line.product_id)
                        for sm in pick_move:
                            # Set qty_done = qty (atau sesuai invoice qty)
                            sm.quantity_done = move_line.quantity
                    # Validasi picking, ini akan otomatis bikin backorder jika qty kurang
                    if picking.state not in ['done', 'cancel']:
                        picking.button_validate()
        return res