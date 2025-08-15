from odoo import models, fields, api
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    @api.onchange('partner_id', 'date_order')
    def _onchange_partner_receipt_date(self):
        """
        Otomatis mengisi receipt date berdasarkan konfigurasi vendor
        """
        if self.partner_id and self.partner_id.is_company and self.partner_id.supplier_rank > 0:
            # Hanya untuk vendor (supplier)
            order_date = self.date_order or fields.Datetime.now()
            receipt_date = self.partner_id.get_receipt_date(order_date)
            
            # Update semua purchase order lines
            for line in self.order_line:
                line.date_planned = receipt_date

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.model
    def create(self, vals):
        """
        Override create untuk mengisi receipt date saat membuat line baru
        """
        line = super(PurchaseOrderLine, self).create(vals)
        
        if line.order_id.partner_id and line.order_id.partner_id.supplier_rank > 0:
            order_date = line.order_id.date_order or fields.Datetime.now()
            receipt_date = line.order_id.partner_id.get_receipt_date(order_date)
            line.date_planned = receipt_date
            
        return line