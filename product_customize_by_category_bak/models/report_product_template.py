from odoo import models

class ReportProductTemplate(models.AbstractModel):
    _name = 'report.module_name.report_product_template_pdf'
    _description = 'Report Product Template PDF'

    def _get_report_values(self, docids, data=None):
        # Ambil record product.template berdasarkan docids
        products = self.env['product.template'].browse(docids)
        
        # Kembalikan data yang dibutuhkan untuk report
        return {
            'doc_ids': docids,
            'doc_model': 'product.template',
            'docs': products,
        }