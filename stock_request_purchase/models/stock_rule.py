# stock_request_purchase/models/stock_rule.py

from odoo import models, _
from odoo.exceptions import UserError


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _update_purchase_order_line(
        self, product_id, product_qty, product_uom, company_id, values, line
    ):
        vals = super()._update_purchase_order_line(
            product_id, product_qty, product_uom, company_id, values, line
        )
        if "stock_request_id" in values:
            vals["stock_request_ids"] = [(4, values["stock_request_id"])]
        return vals

    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values, po):
        """Override untuk handle stock request tanpa vendor price validation"""
        
        # Check jika ini dari stock request
        if values.get('stock_request_id'):
            # Buat supplier info sementara jika product tidak punya vendor
            if not product_id.seller_ids:
                self._ensure_product_has_supplier(product_id, company_id)
        
        # Panggil original method
        res = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, company_id, values, po
        )
        
        # Set default price jika dari stock request dan tidak ada price
        if values.get('stock_request_id') and not res.get('price_unit', 0):
            res['price_unit'] = 0.0
            
        return res

    def _ensure_product_has_supplier(self, product_id, company_id):
        """Ensure product has supplier untuk avoid procurement error"""
        
        # Check apakah sudah ada supplier
        if product_id.seller_ids:
            return
        
        # Get or create generic vendor
        generic_vendor = self._get_or_create_generic_vendor(company_id)
        
        # Create supplier info
        self.env['product.supplierinfo'].create({
            'name': generic_vendor.id,
            'product_tmpl_id': product_id.product_tmpl_id.id,
            'min_qty': 1.0,
            'price': 0.0,  # Default price
            'delay': 1,
            'company_id': company_id.id if company_id else False,
        })

    def _get_or_create_generic_vendor(self, company_id):
        """Get or create generic vendor untuk stock request"""
        partner_obj = self.env['res.partner']
        
        # Search existing generic vendor
        domain = [
            ('name', '=', 'Generic Vendor - Stock Request'),
            ('supplier_rank', '>', 0)
        ]
        if company_id:
            domain.append(('company_id', 'in', [company_id.id, False]))
            
        generic_vendor = partner_obj.search(domain, limit=1)
        
        if not generic_vendor:
            # Create generic vendor
            vendor_vals = {
                'name': 'Generic Vendor - Stock Request',
                'is_company': True,
                'supplier_rank': 1,
                'customer_rank': 0,
            }
            if company_id:
                vendor_vals['company_id'] = company_id.id
                
            generic_vendor = partner_obj.create(vendor_vals)
            
        return generic_vendor