from odoo import models, fields, api
import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default='New')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            supplier = self.env['res.partner'].browse(vals.get('partner_id'))
            supplier_code = supplier.ref or 'XX'  # Gunakan kode supplier atau 'XX' jika tidak ada
            current_date = datetime.datetime.now()
            month_roman = self._get_roman_month(current_date.month)
            year_short = str(current_date.year)[-2:]
            month_code = str(current_date.month).zfill(3)

            # # Generate yearly counter (can be reset yearly)
            # self.env.cr.execute("""
            #     SELECT COUNT(*) + 1 FROM purchase_order
            #     WHERE EXTRACT(YEAR FROM create_date) = %s
            # """, (current_date.year,))
            # yearly_counter = self.env.cr.fetchone()[0]

            # Generate yearly counter per supplier
            supplier_id = vals.get('partner_id')
            self.env.cr.execute("""
               SELECT COUNT(*) + 1 FROM purchase_order
              WHERE EXTRACT(YEAR FROM create_date) = %s
               AND partner_id = %s
            """, (current_date.year, supplier_id))
            yearly_counter = self.env.cr.fetchone()[0]            

            # Hitung jumlah Purchase Order dalam bulan ini untuk supplier
            start_date = current_date.replace(day=1)
            end_date = current_date.replace(day=28) + datetime.timedelta(days=4)
            end_date = end_date - datetime.timedelta(days=end_date.day)
            count = self.search_count([
                ('partner_id', '=', vals.get('partner_id')),
                ('date_order', '>=', start_date.strftime('%Y-%m-%d')),
                ('date_order', '<=', end_date.strftime('%Y-%m-%d')),
            ]) + 1  # Tambahkan 1 untuk PO baru

            vals['name'] = f"{yearly_counter:03}/{supplier_code}/{month_roman}-{str(count).zfill(2)}/{year_short}"
        return super(PurchaseOrder, self).create(vals)

    @staticmethod
    def _get_roman_month(month):
        """Convert bulan menjadi angka Romawi."""
        roman_months = [
            "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"
        ]
        return roman_months[month - 1]