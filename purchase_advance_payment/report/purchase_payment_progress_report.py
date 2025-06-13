from odoo import models
from io import BytesIO
import xlsxwriter
import base64

class PurchaseOrderPaymentXLSX(models.TransientModel):
    _name = 'purchase.payment.progress.report'
    _description = 'Export Purchase Payment Progress XLSX'

    def export_xlsx(self):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Payment Progress")

        header = ['PO Number', 'Vendor', 'Total', 'Residual', 'Advance Status', 'Progress']
        for col, name in enumerate(header):
            sheet.write(0, col, name)

        orders = self.env['purchase.order'].search([])

        for row, po in enumerate(orders, start=1):
            sheet.write(row, 0, po.name)
            sheet.write(row, 1, po.partner_id.name)
            sheet.write(row, 2, po.amount_total)
            sheet.write(row, 3, po.amount_residual)
            sheet.write(row, 4, po.advance_payment_status)
            sheet.write(row, 5, po.payment_progress)

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'payment_progress_report.xlsx',
            'datas': base64.b64encode(output.read()),
            'res_model': 'purchase.payment.progress.report',
            'res_id': self.id,
            'type': 'binary',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }