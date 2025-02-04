# from odoo import api, fields, models
# from datetime import date

# class AccountMove(models.Model):
#     _inherit = 'account.move'

#     due_status = fields.Selection(
#         [('not_due', 'Not Due'), ('overdue', 'Overdue')],
#         string="Due Status",
#         compute="_compute_due_status",
#         store=True
#     )

#     @api.depends('invoice_date_due')
#     def _compute_due_status(self):
#         for move in self:
#             if move.invoice_date_due:
#                 today = date.today()
#                 if move.invoice_date_due < today:
#                     move.due_status = 'overdue'
#                 else:
#                     move.due_status = 'not_due'
#             else:
#                 move.due_status = False

# Perbaikan:
# Tambahkan compute_sudo=True pada field due_status agar komputasi bisa berjalan dengan akses superuser (menghindari masalah hak akses).
# Pastikan field invoice_date_due ada dengan menambah check if move.invoice_date_due sebelum mengaksesnya.
# Gunakan move.invoice_date_due and untuk memastikan tidak ada kesalahan jika field kosong.
# Tambahkan False sebagai default untuk due_status jika invoice_date_due tidak ada.
# Gunakan fields.Date.today() daripada date.today() untuk menjaga kompatibilitas dengan timezone Odoo.

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    due_status = fields.Selection(
        [('not_due', 'Not Due'), ('overdue', 'Overdue')],
        string="Due Status",
        compute="_compute_due_status",
        store=True,
        compute_sudo=True  # Menjalankan komputasi dengan hak akses superuser
    )

    @api.depends('invoice_date_due')
    def _compute_due_status(self):
        today = fields.Date.today()  # Gunakan fields.Date.today() untuk menjaga kompatibilitas timezone
        for move in self:
            if move.invoice_date_due:
                move.due_status = 'overdue' if move.invoice_date_due < today else 'not_due'
            else:
                move.due_status = False


# Perbaikan yang dilakukan:
# Tambahkan default=False pada field due_status

# Ini mencegah field memiliki nilai None, yang dapat menyebabkan masalah dalam tampilan atau penyimpanan data.
# Pastikan invoice_date_due memiliki nilai sebelum membandingkan dengan today

# Saat ini, Anda sudah melakukan pemeriksaan, tetapi kita bisa lebih eksplisit dalam memastikan bahwa nilai tidak kosong.
# Gunakan fields.Date.context_today(self) daripada date.today()

# Ini penting agar mempertimbangkan timezone dalam konteks Odoo.
# from odoo import api, fields, models

# class AccountMove(models.Model):
#     _inherit = 'account.move'

#     due_status = fields.Selection(
#         [('not_due', 'Not Due'), ('overdue', 'Overdue')],
#         string="Due Status",
#         compute="_compute_due_status",
#         store=True,
#         default=False  # Menambahkan default agar lebih aman
#     )

#     @api.depends('invoice_date_due')
#     def _compute_due_status(self):
#         today = fields.Date.context_today(self)  # Menggunakan context_today untuk mempertimbangkan timezone
#         for move in self:
#             if move.invoice_date_due:
#                 move.due_status = 'overdue' if move.invoice_date_due < today else 'not_due'
#             else:
#                 move.due_status = False

