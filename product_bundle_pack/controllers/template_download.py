# controllers/template_download.py
from odoo import http
from odoo.http import request
import base64
import io
import csv
import logging

_logger = logging.getLogger(__name__)

class TemplateDownloadController(http.Controller):

    @http.route('/import_pack/excel_template', type='http', auth='user', methods=['GET'])
    def download_excel_template(self, wizard_id=None):
        """HTTP controller for Excel template download"""
        try:
            # Generate Excel template
            import xlsxwriter
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Product Pack Import')
            
            # Header format
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D7E4BC',
                'border': 1
            })
            
            # Headers
            headers = [
                'Kode Unit', 'Deskripsi', 'Manufacture Code', 'Is Pack', 'Type', 'Category',
                'Factory Model No', 'Product Brand', 'Cal Pack Price', 'Kode Part',
                'Deskripsi Part', 'Part Category', 'Quantity', 'UOM', 'Part Cost'
            ]
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            # Sample data
            sample_data = [
                #  Kode Unit, Deskripsi, Manufacture Code, Is Pack, Type, Category,
                #  Factory Model No, Product Brand, Cal Pack Price, Kode Part,
                #  Deskripsi Part, Part Category, Quantity, UOM, Part Cost
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'MOTOR001', 'Motor 1HP', 'Motor', 1, 'Unit', 1500000],
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'CABLE001', 'Power Cable 5m', 'Cable', 1, 'Unit', 150000],
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'SWITCH001', 'On/Off Switch', 'Switch', 1, 'Unit', 75000],
                ['BUNDLE002', 'Fan Complete Set', 'MFG-BND-002', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'FAN001', 'Industrial Fan 16\"', 'Fan', 1, 'Unit', 800000],
                ['BUNDLE002', 'Fan Complete Set', 'MFG-BND-002', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'STAND001', 'Fan Stand', 'Stand', 1, 'Unit', 200000],
            ]
            
            for row, data in enumerate(sample_data, 1):
                for col, value in enumerate(data):
                    worksheet.write(row, col, value)
            
            # Auto-fit columns
            for col in range(len(headers)):
                worksheet.set_column(col, col, 20)
            
            workbook.close()
            output.seek(0)
            
            # Return file
            return request.make_response(
                output.getvalue(),
                headers=[
                    ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                    ('Content-Disposition', 'attachment; filename="product_pack_template.xlsx"')
                ]
            )
            
        except ImportError:
            # Fallback to CSV if xlsxwriter not available
            return self.download_csv_template()
        except Exception as e:
            _logger.error(f"Excel template generation failed: {e}")
            return request.make_response(
                f"Error generating Excel template: {e}",
                headers=[('Content-Type', 'text/plain')]
            )

    @http.route('/import_pack/csv_template', type='http', auth='user', methods=['GET'])
    def download_csv_template(self, wizard_id=None):
        """HTTP controller for CSV template download"""
        try:
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Headers
            headers = [
                'Kode Unit', 'Deskripsi', 'Manufacture Code', 'Is Pack', 'Type', 'Category',
                'Factory Model No', 'Product Brand', 'Cal Pack Price', 'Kode Part',
                'Deskripsi Part', 'Part Category', 'Quantity', 'UOM', 'Part Cost'
            ]
            writer.writerow(headers)
            
            # Sample data
            sample_data = [
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'MOTOR001', 'Motor 1HP', 'Motor', '1', 'Unit', '1500000'],
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'CABLE001', 'Power Cable 5m', 'Cable', '1', 'Unit', '150000'],
                ['BUNDLE001', 'Motor Package Set', 'MFG-BND-001', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'SWITCH001', 'On/Off Switch', 'Switch', '1', 'Unit', '75000'],
                ['BUNDLE002', 'Fan Complete Set', 'MFG-BND-002', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'FAN001', 'Industrial Fan 16\"', 'Fan', '1', 'Unit', '800000'],
                ['BUNDLE002', 'Fan Complete Set', 'MFG-BND-002', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'STAND001', 'Fan Stand', 'Stand', '1', 'Unit', '200000'],
            ]
            
            for data in sample_data:
                writer.writerow(data)
            
            csv_content = output.getvalue()
            
            return request.make_response(
                csv_content,
                headers=[
                    ('Content-Type', 'text/csv'),
                    ('Content-Disposition', 'attachment; filename="product_pack_template.csv"')
                ]
            )
            
        except Exception as e:
            _logger.error(f"CSV template generation failed: {e}")
            return request.make_response(
                f"Error generating CSV template: {e}",
                headers=[('Content-Type', 'text/plain')]
            )