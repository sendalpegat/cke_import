from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    po_auto_receipt_date = fields.Selection([
        ('manual', 'Manual'),
        ('1_month', '1 Bulan'),
        ('2_month', '2 Bulan'),
        ('3_month', '3 Bulan'),
    ], string='Otomatis Receipt Date PO', default='manual',
        help='Pengaturan tanggal otomatis receipt PO untuk vendor ini.')