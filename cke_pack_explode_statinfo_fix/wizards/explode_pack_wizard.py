# -*- coding: utf-8 -*-
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
            raise UserError(_("This wizard only works with Vendor Bills."))

        # Hindari menduplikasi komponen yang sudah ada di invoice
        exploded_product_ids = move.invoice_line_ids.mapped('product_id').ids
        pack_lines = []
        for line in move.invoice_line_ids:
            product = line.product_id
            if product and product.product_tmpl_id.is_pack:
                for pack in product.product_tmpl_id.pack_ids:
                    if pack.product_id.id not in exploded_product_ids:
                        account_id = line.account_id.id or \
                            pack.product_id.property_account_expense_id.id or \
                            pack.product_id.categ_id.property_account_expense_categ_id.id
                        if not account_id:
                            raise UserError(_("Missing expense account for product %s.") % pack.product_id.display_name)

                        pack_lines.append((0, 0, {
                            'product_id': pack.product_id.id,
                            'qty_uom': pack.qty_uom * line.quantity,
                            'price_unit': pack.product_id.standard_price,
                            'account_id': account_id,
                            'description': "%s (from %s)" % (pack.product_id.name, product.name),
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
        if move.move_type != 'in_invoice':
            raise UserError(_("This wizard only works with Vendor Bills."))

        # 1) Kumpulkan semua baris PACK asal (sebelum dihapus)
        src_pack_lines = move.invoice_line_ids.filtered(
            lambda l: l.product_id and l.product_id.product_tmpl_id.is_pack
        )
        if not src_pack_lines:
            # Tidak ada baris PACK di bill ini
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                'res_id': move.id,
                'view_mode': 'form',
                'target': 'current',
            }

        # 2) Ambil satu purchase_line_id rujukan dari pack asal (cukup 1 supaya PO→Bill terhitung)
        #    Jika ada banyak pack dari PO yang sama, ini aman.
        po_line_ref = src_pack_lines.mapped('purchase_line_id')[:1]
        po_line_ref = po_line_ref and po_line_ref[0] or False

        # 3) Jika move belum punya purchase_id tapi kita punya po_line_ref, set supaya relasi PO↔Bill kuat
        if not move.purchase_id and po_line_ref:
            move.purchase_id = po_line_ref.order_id

        order_ref = move.purchase_id.name if move.purchase_id else False

        # 4) Hapus pack asal
        #    (PENTING: dilakukan setelah kita simpan po_line_ref)
        src_pack_lines.unlink()

        # 5) Tambahkan komponen baru + wariskan purchase_line_id agar statinfo PO muncul
        for line in self.line_ids.filtered(lambda l: l.selected):
            self.env['account.move.line'].create({
                'move_id': move.id,
                'product_id': line.product_id.id,
                'quantity': line.qty_uom,
                'price_unit': line.price_unit,
                'account_id': line.account_id.id,
                'name': ("[%s] %s" % (order_ref, line.description)) if order_ref else line.description,
                'purchase_line_id': po_line_ref.id if po_line_ref else False,  # <<< kunci statinfo
                'is_exploded_component': True,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'res_id': move.id,
            'view_mode': 'form',
            'target': 'current',
        }