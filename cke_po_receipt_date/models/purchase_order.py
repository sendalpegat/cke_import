from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    computed_receipt_date = fields.Date(
        string='Computed Receipt Date',
        compute='_compute_receipt_date',
        store=False,
        help='Receipt date yang dihitung berdasarkan konfigurasi vendor atau default 2 bulan'
    )
    
    @api.depends('partner_id', 'date_order', 'partner_id.receipt_date_type', 'partner_id.manual_receipt_date')
    def _compute_receipt_date(self):
        """Compute receipt date berdasarkan konfigurasi vendor atau default 2 bulan"""
        for order in self:
            if not order.date_order:
                order.computed_receipt_date = False
                continue
                
            order_date = order.date_order
            if isinstance(order_date, str):
                try:
                    order_date = datetime.strptime(order_date, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    order_date = datetime.strptime(order_date, '%Y-%m-%d')
            
            # Cek konfigurasi vendor
            if (order.partner_id and 
                order.partner_id.is_company and 
                order.partner_id.supplier_rank > 0 and
                hasattr(order.partner_id, 'receipt_date_type') and
                order.partner_id.receipt_date_type):
                # Gunakan konfigurasi vendor
                order.computed_receipt_date = order.partner_id.get_receipt_date(order_date)
            else:
                # Default 2 bulan
                order.computed_receipt_date = order_date.date() + relativedelta(months=2)
    
    @api.onchange('partner_id', 'date_order')
    def _onchange_partner_receipt_date(self):
        """Update receipt date untuk semua order lines"""
        if self.computed_receipt_date:
            for line in self.order_line:
                line.date_planned = self.computed_receipt_date
    
    @api.model
    def create(self, vals):
        """Override create untuk set receipt date saat membuat PO"""
        po = super(PurchaseOrder, self).create(vals)
        # Trigger compute dan update lines
        po._compute_receipt_date()
        if po.computed_receipt_date:
            for line in po.order_line:
                line.date_planned = po.computed_receipt_date
        return po

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.model
    def create(self, vals):
        """Override create untuk set receipt date saat membuat line baru"""
        line = super(PurchaseOrderLine, self).create(vals)
        
        # Set receipt date berdasarkan computed field dari order
        if line.order_id:
            line.order_id._compute_receipt_date()
            if line.order_id.computed_receipt_date:
                line.date_planned = line.order_id.computed_receipt_date
                
        return line
    
    @api.model
    def default_get(self, fields_list):
        """Set default date_planned berdasarkan order"""
        defaults = super(PurchaseOrderLine, self).default_get(fields_list)
        
        if self.env.context.get('default_order_id'):
            order = self.env['purchase.order'].browse(self.env.context['default_order_id'])
            if order:
                order._compute_receipt_date()
                if order.computed_receipt_date:
                    defaults['date_planned'] = order.computed_receipt_date
        
        return defaults