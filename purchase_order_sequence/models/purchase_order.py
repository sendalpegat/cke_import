from odoo import models, fields, api
import datetime

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=False, index=True, default='New')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            # Ambil atau buat date_order jika belum ada
            if 'date_order' in vals:
                date_order = fields.Datetime.from_string(vals['date_order'])
            else:
                date_order = datetime.datetime.now()
                vals['date_order'] = fields.Datetime.to_string(date_order)

            # Dapatkan informasi supplier
            supplier = self.env['res.partner'].browse(vals.get('partner_id'))
            supplier_code = supplier.ref or 'XX'

            # Ekstrak informasi dari date_order
            year = date_order.year
            month = date_order.month
            month_roman = self._get_roman_month(month)
            year_short = str(year)[-2:]

            # Hitung counter tahunan per supplier berdasarkan date_order
            supplier_id = vals.get('partner_id')
            self.env.cr.execute("""
                SELECT COUNT(*) + 1 FROM purchase_order
                WHERE EXTRACT(YEAR FROM date_order) = %s
                AND partner_id = %s
            """, (year, supplier_id))
            yearly_counter = self.env.cr.fetchone()[0]

            # Hitung jumlah PO dalam bulan yang sama dari date_order
            start_month = date_order.replace(day=1)
            if month == 12:
                next_month = date_order.replace(year=year + 1, month=1, day=1)
            else:
                next_month = date_order.replace(month=month + 1, day=1)
            end_month = next_month - datetime.timedelta(days=1)

            count = self.search_count([
                ('partner_id', '=', vals.get('partner_id')),
                ('date_order', '>=', fields.Datetime.to_string(start_month)),
                ('date_order', '<=', fields.Datetime.to_string(end_month)),
            ]) + 1

            # Format sequence name
            vals['name'] = f"{yearly_counter:03}/{supplier_code}/{month_roman}-{str(count).zfill(2)}/{year_short}"

        return super(PurchaseOrder, self).create(vals)

    @staticmethod
    def _get_roman_month(month):
        """Convert bulan menjadi angka Romawi."""
        roman_months = [
            "I", "II", "III", "IV", "V", "VI",
            "VII", "VIII", "IX", "X", "XI", "XII"
        ]
        return roman_months[month - 1]