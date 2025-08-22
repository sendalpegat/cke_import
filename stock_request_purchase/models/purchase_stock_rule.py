# stock_request_purchase/models/purchase_stock_rule.py (file baru)

from odoo import models, _
from odoo.exceptions import UserError


class PurchaseRule(models.Model):
    _inherit = "stock.rule"
    
    def _run_buy(self, procurements):
        """Override _run_buy untuk handle stock request tanpa vendor"""
        # Filter procurement yang dari stock request
        stock_request_procurements = []
        normal_procurements = []
        
        for procurement in procurements:
            if procurement.values.get('stock_request_id'):
                stock_request_procurements.append(procurement)
            else:
                normal_procurements.append(procurement)
        
        # Process normal procurements dengan validation biasa
        if normal_procurements:
            super()._run_buy(normal_procurements)
        
        # Process stock request procurements tanpa vendor validation
        if stock_request_procurements:
            self._run_buy_stock_request(stock_request_procurements)
    
    def _run_buy_stock_request(self, procurements):
        """Special handling untuk stock request procurement"""
        for procurement in procurements:
            params = procurement.values
            product = procurement.product_id
            
            # Get or create generic supplier
            supplier = self._get_stock_request_supplier(product, params)
            
            # Create supplier info jika belum ada
            if supplier and not product.seller_ids.filtered(lambda s: s.name == supplier):
                self.env['product.supplierinfo'].create({
                    'name': supplier.id,
                    'product_tmpl_id': product.product_tmpl_id.id,
                    'min_qty': 1.0,
                    'price': 0.0,  # Default price 0
                    'delay': 1,
                })
            
            # Update procurement values dengan supplier
            params['supplier'] = supplier
            
        # Panggil original method dengan supplier yang sudah di-set
        return super()._run_buy(procurements)
    
    def _get_stock_request_supplier(self, product, params):
        """Get supplier untuk stock request"""
        # Cari existing supplier untuk product
        if product.seller_ids:
            return product.seller_ids[0].name
        
        # Jika tidak ada, buat/gunakan generic supplier
        return self._get_or_create_generic_vendor(self.company_id)
    
    def _get_or_create_generic_vendor(self, company_id):
        """Get or create generic vendor"""
        partner_obj = self.env['res.partner']
        
        generic_vendor = partner_obj.search([
            ('name', '=', 'Generic Vendor - Stock Request'),
            ('is_company', '=', True),
            ('supplier_rank', '>', 0)
        ], limit=1)
        
        if not generic_vendor:
            generic_vendor = partner_obj.create({
                'name': 'Generic Vendor - Stock Request',
                'is_company': True,
                'supplier_rank': 1,
                'customer_rank': 0,
                'company_id': company_id.id if company_id else False,
            })
            
        return generic_vendor