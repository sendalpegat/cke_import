from odoo import models, fields, api
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == 'New':
            # Generate custom sequence
            vals['name'] = self._generate_sequence(vals)
        return super(PurchaseOrder, self).create(vals)

    def _generate_sequence(self, vals):
        """Generate custom sequence for purchase order."""
        today = datetime.today()
        year = today.strftime('%y')  # 2-digit year
        month = today.strftime('%m')  # Month as number
        month_roman = self._to_roman(int(month))  # Convert to Roman numeral

        # Generate counter per month
        self.env.cr.execute("""
            SELECT COUNT(*) + 1 FROM purchase_order
            WHERE EXTRACT(YEAR FROM create_date) = %s AND EXTRACT(MONTH FROM create_date) = %s
        """, (today.year, int(month)))
        counter = self.env.cr.fetchone()[0]

        # Get Supplier Code (use the first partner as an example)
        supplier_code = ''
        if 'partner_id' in vals and vals['partner_id']:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            supplier_code = partner.ref or 'XX'  # Default to 'XX' if no code

        # Generate yearly counter (can be reset yearly)
        self.env.cr.execute("""
            SELECT COUNT(*) + 1 FROM purchase_order
            WHERE EXTRACT(YEAR FROM create_date) = %s
        """, (today.year,))
        yearly_counter = self.env.cr.fetchone()[0]

        # Format sequence
        sequence = f"{yearly_counter:03}/{supplier_code}/{month_roman}-{counter:02}/{year}"
        return sequence

    def _to_roman(self, num):
        """Convert integer to Roman numeral."""
        roman_map = {
            1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V',
            6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX', 10: 'X',
            11: 'XI', 12: 'XII'
        }
        return roman_map.get(num, '')

    def button_cancel(self):
        """Override cancel button to reset sequence if order is cancelled."""
        for order in self:
            if order.state != 'cancel':
                order.name = 'New'  # Reset sequence to default
        return super(PurchaseOrder, self).button_cancel()


# from odoo import models, fields, api
# import datetime

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'

#     name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default='New')

#     @api.model
#     def create(self, vals):
#         if vals.get('name', 'New') == 'New':
#             supplier = self.env['res.partner'].browse(vals.get('partner_id'))
#             supplier_code = supplier.ref or 'XX'  # Gunakan kode supplier atau 'XX' jika tidak ada
#             current_date = datetime.datetime.now()
#             month_roman = self._get_roman_month(current_date.month)
#             year_short = str(current_date.year)[-2:]
#             month_code = str(current_date.month).zfill(3)

#             # Hitung jumlah Purchase Order dalam bulan ini untuk supplier
#             start_date = current_date.replace(day=1)
#             end_date = current_date.replace(day=28) + datetime.timedelta(days=4)
#             end_date = end_date - datetime.timedelta(days=end_date.day)
#             count = self.search_count([
#                 ('partner_id', '=', vals.get('partner_id')),
#                 ('date_order', '>=', start_date.strftime('%Y-%m-%d')),
#                 ('date_order', '<=', end_date.strftime('%Y-%m-%d')),
#             ]) + 1  # Tambahkan 1 untuk PO baru

#             vals['name'] = f"{month_code}/{supplier_code}/{month_roman}-{str(count).zfill(2)}/{year_short}"
#         return super(PurchaseOrder, self).create(vals)

#     @staticmethod
#     def _get_roman_month(month):
#         """Convert bulan menjadi angka Romawi."""
#         roman_months = [
#             "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"
#         ]
#         return roman_months[month - 1]

# from odoo import models, fields, api
# from datetime import datetime

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'

#     @api.model
#     def create(self, vals):
#         # Dapatkan sequence nomor PO
#         vals['name'] = self._generate_custom_po_sequence(vals)
#         return super(PurchaseOrder, self).create(vals)

#     def _generate_custom_po_sequence(self, vals):
#         """
#         Generate custom sequence for Purchase Orders:
#         Format: 051/YL/XI-05/24
#         """
#         sequence = self.env['ir.sequence'].next_by_code('purchase.order') or '000'
        
#         # Ambil kode supplier
#         partner = self.env['res.partner'].browse(vals.get('partner_id'))
#         supplier_code = partner.ref or 'XX'  # Default kode jika tidak ada

#         # Ambil bulan dalam format Romawi
#         month_roman = self._get_roman_month(datetime.today().month)

#         # Ambil tahun dalam format dua digit
#         year = datetime.today().strftime('%y')

#         # Dapatkan nomor urut dalam 1 bulan per supplier
#         po_count = self.search_count([
#             ('partner_id', '=', partner.id),
#             ('create_date', '>=', datetime.today().replace(day=1).strftime('%Y-%m-%d')),
#             ('create_date', '<', datetime.today().replace(day=1).strftime('%Y-%m-%d') + ' +1 MONTH'),
#         ])
#         po_number = str(po_count + 1).zfill(2)

#         # Gabungkan semuanya
#         custom_sequence = f"{sequence}/{supplier_code}/{month_roman}-{po_number}/{year}"
#         return custom_sequence

#     def _get_roman_month(self, month):
#         roman_months = {
#             1: 'I', 2: 'II', 3: 'III', 4: 'IV',
#             5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII',
#             9: 'IX', 10: 'X', 11: 'XI', 12: 'XII',
#         }
#         return roman_months.get(month, 'XX')

#     # def _create_sequence(self):
#     # self.env['ir.sequence'].create({
#     #     'name': 'Purchase Order Sequence',
#     #     'code': 'purchase.order',
#     #     'prefix': '',
#     #     'padding': 3,
#     #     'number_increment': 1,
#     # })