from odoo import api, models, _, fields
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID

class PurchaseOrderLine(models.Model):
	_inherit = 'purchase.order.line'

	def _prepare_stock_moves(self, picking):
		""" Prepare the stock moves data for one order line. This function returns a list of
		dictionary ready to be used in stock.move's create()
		"""
		res = super(PurchaseOrderLine, self)._prepare_stock_moves(picking=picking)
		config_id = self.env['res.config.settings'].sudo().search([],limit=1,order='id desc')
		if config_id.allow_bundle == True:

			self.ensure_one()
			res = []
			if self.product_id.type not in ['product', 'consu']:
				return res
			qty = 0.0
			price_unit = self._get_stock_move_price_unit()
			for move in self.move_ids.filtered(lambda x: x.state != 'cancel' and not x.location_dest_id.usage == "supplier"):
				qty += move.product_qty
			if  self.product_id.pack_ids:
				for item in self.product_id.pack_ids:
					template = {
						'name': item.product_id.name or '',
						'product_id': item.product_id.id,
						'product_uom': item.uom_id.id,
						'date': self.order_id.date_order,
						'date_deadline': self.date_planned,
						'location_id': self.order_id.partner_id.property_stock_supplier.id,
						'location_dest_id': self.order_id._get_destination_location(),
						'picking_id': picking.id,
						'partner_id': self.order_id.dest_address_id.id,
						'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
						'state': 'draft',
						'purchase_line_id': self.id,
						'company_id': self.order_id.company_id.id,
						'price_unit': price_unit,
						'picking_type_id': self.order_id.picking_type_id.id,
						'group_id': self.order_id.group_id.id,
						'origin': self.order_id.name,
						'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
						'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
						'pack_id' : item.id,
					}
					diff_quantity = item.qty_uom
					if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
						template['product_uom_qty'] = diff_quantity * self.product_qty
						res.append(template)
				return res
			else:
				template = {
				'name': self.name or '',
				'product_id': self.product_id.id,
				'product_uom': self.product_uom.id,
				'date': self.order_id.date_order,
				'location_id': self.order_id.partner_id.property_stock_supplier.id,
				'location_dest_id': self.order_id._get_destination_location(),
				'picking_id': picking.id,
				'partner_id': self.order_id.dest_address_id.id,
				'move_dest_ids': [(4, x) for x in self.move_dest_ids.ids],
				'state': 'draft',
				'purchase_line_id': self.id,
				'company_id': self.order_id.company_id.id,
				'price_unit': price_unit,
				'picking_type_id': self.order_id.picking_type_id.id,
				'group_id': self.order_id.group_id.id,
				'origin': self.order_id.name,
				'route_ids': self.order_id.picking_type_id.warehouse_id and [(6, 0, [x.id for x in self.order_id.picking_type_id.warehouse_id.route_ids])] or [],
				'warehouse_id': self.order_id.picking_type_id.warehouse_id.id,
			}
				diff_quantity = self.product_qty - qty
				if float_compare(diff_quantity, 0.0,  precision_rounding=self.product_uom.rounding) > 0:
					template['product_uom_qty'] = diff_quantity
					res.append(template)
			return res
		else:
			return res

	@api.depends('move_ids.state', 'move_ids.product_uom_qty', 'move_ids.product_uom')
	def _compute_qty_received(self):
		super(PurchaseOrderLine, self)._compute_qty_received()
		config_id = self.env['res.config.settings'].sudo().search([],limit=1,order='id desc')
		for line in self:
			total = 0.0
			if line.qty_received_method == 'stock_moves':
				def check_product(x):
					for rec in line.product_id.pack_ids:
						if x == rec.product_id:
							return x
				qty = 0.0
				flag = False
				count = 0
				done_list = [] 
				deliver_list = []
				move_list = []
				products = []
				filtered = []
				vals_list = []
				picking_ids = self.env['stock.picking'].search([('origin','=',line.order_id.name)])
				for pick in picking_ids:
					for move_is in pick.move_ids_without_package:
						if move_is.product_id not in products:
							products.append(move_is.product_id)
		
				pro = filter(check_product,products)
				for product in pro:
					filtered.append(product)
				for pick in picking_ids:
					for move_is in pick.move_ids_without_package:
						if move_is.product_id in filtered:
							if move_is.pack_id in line.product_id.pack_ids:
								if move_is.quantity_done >0:
									quantity = move_is.pack_id.qty_uom / move_is.quantity_done
									vals_list.append(quantity)
								move_list.append(move_is.product_uom_qty)
								done_list.append(move_is.quantity_done)				
				stock_move = self.env['stock.move'].search([('origin','=',line.order_id.name)])
				vals = []
				if line.product_id.is_pack == True and config_id.allow_bundle == True:
					list_of_sub_product = []
					for product_item in line.product_id.pack_ids:
						list_of_sub_product.append(product_item.product_id)
					for move in stock_move:
						if count == 0:
							if move.state == 'done' and move.product_uom_qty == move.quantity_done:
								flag = True
								for picking in picking_ids:
									for move_is in picking.move_ids_without_package:
										if sum(move_list) == 0:
											pass
										else:
											deliver_qty =(line.product_qty*sum(done_list))/sum(move_list)
											line.qty_received = int(deliver_qty)
											deliver_list.append(line.qty_received)           
						elif move.state == 'confirmed':
							flag = 'confirmed'
							count = count+1
							done_list.append(move.quantity_done)
							for picking in picking_ids:
								for move_is in picking.move_ids_without_package:

									if sum(move_list) == 0:
										pass
									else:
										deliver_qty =(line.product_qty*sum(done_list))/sum(move_list)
										line.qty_received = int(deliver_qty)
										deliver_list.append(line.qty_received)  
				
					print(line.qty_received)                        
				else:
											
					# In case of a BOM in kit, the products delivered do not correspond to the products in
					# the PO. Therefore, we can skip them since they will be handled later on.
					for move in line.move_ids.filtered(lambda m: m.product_id == line.product_id):
						if move.state == 'done':
							if move.location_dest_id.usage == "supplier":
								if move.to_refund:
									total -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
							elif move.origin_returned_move_id and move.origin_returned_move_id._is_dropshipped() and not move._is_dropshipped_returned():
								# Edge case: the dropship is returned to the stock, no to the supplier.
								# In this case, the received quantity on the PO is set although we didn't
								# receive the product physically in our stock. To avoid counting the
								# quantity twice, we do nothing.
								pass
							elif (
								move.location_dest_id.usage == "internal"
								and move.to_refund
								and move.location_dest_id
								not in self.env["stock.location"].search(
									[("id", "child_of", move.warehouse_id.view_location_id.id)]
								)
							):
								total -= move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
							else:
								total += move.product_uom._compute_quantity(move.product_uom_qty, line.product_uom)
					line.qty_received = total
  #untuk cek product pack sebelum di simpan  
	# @api.constrains('product_id', 'pack_ids')
	# def _check_pack_components(self):
	# 	for line in self:
	# 		if line.product_id.is_pack and not line.product_id.pack_ids:
	# 			raise UserError(
	# 				f"Product {line.product_id.name} is marked as pack but has no components!"
	# 			)   
    # Hapus @api.constrains dan ganti dengan @api.onchange
	@api.onchange('product_id')
	def _onchange_product_id_check_pack(self):
		"""Memberikan warning jika produk pack tidak memiliki komponen"""
		if self.product_id.product_tmpl_id.is_pack and not self.product_id.product_tmpl_id.pack_ids:
			return {
				'warning': {
					'title': _("Warning"),
					'message': _(
						"Product %s is marked as a bundle but has no components!\n"
						"You can save this record, but please configure components later."
					) % self.product_id.default_code
				}
			}

	# def write(self, vals):
	# 	res = super().write(vals)
	# 	for line in self:
	# 		if line.product_id.product_tmpl_id.is_pack and not line.product_id.product_tmpl_id.pack_ids:
	# 			_logger.warning(
    #                 "Bundle Product %s has no components (Purchase Line ID: %s)", 
    #                 line.product_id.name, line.id
    #             )
	# 	return res
# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
    
#     def action_recheck_bundle(self):
#         """Tombol Re-check untuk validasi bundle di Purchase Order."""
#         warning_messages = []
#         for order in self:
#             for line in order.order_line:
#                 if line.product_id.is_pack:
#                     # Cek apakah produk bundle memiliki komponen pack_ids
#                     if not line.product_id.pack_ids:
#                         warning_messages.append(
#                             f"⚠️ Produk {line.product_id.name} adalah bundle, tetapi tidak memiliki komponen pack!"
#                         )
#                     else:
#                         # Cek apakah semua komponen pack tercatat di receipt
#                         moves = line.move_ids.filtered(lambda m: m.state != 'cancel')
#                         pack_products = line.product_id.pack_ids.mapped('product_id')
#                         received_products = moves.mapped('product_id')
                        
#                         missing_products = pack_products - received_products
#                         if missing_products:
#                             warning_messages.append(
#                                 f"⚠️ Produk {line.product_id.name} memiliki komponen yang belum diterima: {', '.join(missing_products.mapped('name'))}"
#                             )
#         if warning_messages:
#             raise UserError("\n".join(warning_messages))
#         else:
#             return {
#                 'type': 'ir.actions.client',
#                 'tag': 'display_notification',
#                 'params': {
#                     'type': 'success',
#                     'message': '✅ Semua bundle dan komponennya valid!',
#                 }
#             }       

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    pack_line_ids = fields.One2many(
        'product.pack',
        compute='_compute_pack_lines',
        string="Pack Components",
        store=False
    )
  
    def action_validate_product_packs(self):
        error_messages = []
        for order in self:
            for line in order.order_line:
                if line.product_id.is_pack:
                    # Check pack components
                    if not line.product_id.pack_ids:
                        error_messages.append(
                            f"Product {line.product_id.default_code} is a pack but has no components!"
                        )
                    
                    # Check stock moves
                    for move in line.move_ids:
                        if not move.pack_id:
                            error_messages.append(
                                f"Stock move for {line.product_id.default_code} is missing pack components!"
                            )
        
        if error_messages:
            return {
                'warning': {
                    'title': 'Validation Error',
                    'message': '\n'.join(error_messages)
                }
            }
        else:
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'All pack products are validated successfully!',
                    'type': 'rainbow_man'
                }
            }

    @api.depends('order_line.product_id')
    def _compute_pack_lines(self):
        for order in self:
            packs = self.env['product.pack']
            for line in order.order_line:
                if line.product_id and line.product_id.product_tmpl_id.is_pack:
                    packs |= line.product_id.product_tmpl_id.pack_ids
            # order.pack_line_ids = packs ## sebelum menghitung pack qty po
            order.pack_line_ids = packs.with_context(po_id=order.id)

    # def action_create_invoice(self):
    #     invoices = self.env['account.move']
    #     for order in self:
    #         invoice_vals = order._prepare_invoice()
    #         invoice = self.env['account.move'].create(invoice_vals)

    #         for line in order.order_line:
    #             if line.product_id.product_tmpl_id.is_pack:
    #                 for pack in line.product_id.product_tmpl_id.pack_ids:
    #                     # ✅ Validasi: standard_price wajib
    #                     if not pack.product_id.standard_price or pack.product_id.standard_price <= 0:
    #                         raise UserError(
    #                             f"Produk komponen \"{pack.product_id.display_name}\" dari bundle \"{line.product_id.display_name}\" "
    #                             f"belum memiliki Standard Price!\n\n"
    #                             "Silakan isi terlebih dahulu di Master Produk untuk menghindari jurnal tidak seimbang."
    #                         )

    #                     # Buat PO line virtual
    #                     fake_line = self.env['purchase.order.line'].new({
    #                         'product_id': pack.product_id.id,
    #                         'product_uom_qty': pack.qty_uom * line.product_qty,
    #                         'product_uom': pack.uom_id.id,
    #                         'price_unit': pack.product_id.standard_price,
    #                         'order_id': order.id,
    #                         'name': f"{pack.product_id.display_name} (from {line.product_id.display_name})"
    #                     })

    #                     # Buat invoice line dari PO line virtual
    #                     invoice_line_vals = fake_line._prepare_account_move_line()

    #                     # ✅ Fallback account_id ke akun hardcoded [69000000] jika kosong
    #                     if not invoice_line_vals.get('account_id'):
    #                         fallback_account = self.env['account.account'].search([('code', '=', '69000000')], limit=1)
    #                         if not fallback_account:
    #                             raise UserError(
    #                                 "Akun fallback [69000000] belum ditemukan.\n"
    #                                 "Silakan buat akun dengan kode '69000000' dan tipe 'Expenses'."
    #                             )
    #                         invoice_line_vals['account_id'] = fallback_account.id

    #                     invoice_line_vals.update({'move_id': invoice.id})
    #                     self.env['account.move.line'].create(invoice_line_vals)
    #             else:
    #                 # Produk biasa, gunakan standar
    #                 invoice_line_vals = line._prepare_account_move_line()
    #                 invoice_line_vals.update({'move_id': invoice.id})
    #                 self.env['account.move.line'].create(invoice_line_vals)

    #         invoices += invoice

    #     # ✅ Return action vendor bill (tanpa external ID)
    #     if invoices:
    #         if len(invoices) == 1:
    #             return {
    #                 'name': 'Vendor Bill',
    #                 'type': 'ir.actions.act_window',
    #                 'view_mode': 'form',
    #                 'res_model': 'account.move',
    #                 'res_id': invoices.id,
    #                 'target': 'current',
    #             }
    #         else:
    #             return {
    #                 'name': 'Vendor Bills',
    #                 'type': 'ir.actions.act_window',
    #                 'view_mode': 'tree,form',
    #                 'res_model': 'account.move',
    #                 'domain': [('id', 'in', invoices.ids)],
    #             }
    #     return True

class StockPickingInherit(models.Model):
	_inherit = 'stock.picking'

class StockMoveInherit(models.Model):
	_inherit = 'stock.move'

	pack_id = fields.Many2one('product.pack',string="PACK")

	# purchase_order_ref = fields.Char(
    #     string='PO Reference',
    #     compute='_compute_purchase_order_ref',
    #     store=True
    # )

	# @api.depends('origin')
	# def _compute_purchase_order_ref(self):
	# 	for move in self:
	# 		move.purchase_order_ref = move.origin

class StockMoveLineInherit(models.Model):
	_inherit = 'stock.move.line'

	pack_id = fields.Many2one('product.pack',string="PACK")