from odoo import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # Custom note field yang tidak terikat validasi akuntansi
    custom_note = fields.Text(
        string='Additional Notes',
        help='Custom notes for this purchase order line'
    )
    
    # Atau bisa juga menggunakan Html field untuk rich text
    custom_note_html = fields.Html(
        string='Detailed Notes',
        help='Detailed notes with formatting support'
    )

    # Override method _check_accountable jika perlu
    # untuk bypass validasi tertentu pada custom field
    @api.constrains('custom_note', 'custom_note_html')
    def _check_custom_note(self):
        # Custom validation jika diperlukan
        # Method ini tidak akan terpengaruh validasi accountable
        pass