from odoo import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    receipt_date_type = fields.Selection([
        ('1_month', '1 Bulan'),
        ('2_month', '2 Bulan'), 
        ('3_month', '3 Bulan'),
        ('manual', 'Manual')
    ], string='Tipe Receipt Date', default='2_month',  # Changed from '1_month' to '2_month'
       help='Menentukan cara perhitungan receipt date untuk PO')
    
    manual_receipt_date = fields.Date(
        string='Manual Receipt Date',
        help='Tanggal receipt yang akan digunakan jika tipe adalah manual'
    )
    
    def get_receipt_date(self, order_date=None):
        """
        Menghitung receipt date berdasarkan konfigurasi vendor
        """
        self.ensure_one()
        if not order_date:
            order_date = fields.Date.today()
        
        if isinstance(order_date, str):
            order_date = datetime.strptime(order_date, '%Y-%m-%d').date()
        elif isinstance(order_date, datetime):
            order_date = order_date.date()
            
        if self.receipt_date_type == '1_month':
            return order_date + relativedelta(months=1)
        elif self.receipt_date_type == '2_month':
            return order_date + relativedelta(months=2)
        elif self.receipt_date_type == '3_month':
            return order_date + relativedelta(months=3)
        elif self.receipt_date_type == 'manual' and self.manual_receipt_date:
            return self.manual_receipt_date
        else:
            # Default ke 2 bulan jika tidak ada konfigurasi (changed from 1 month to 2 months)
            return order_date + relativedelta(months=2)