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

    today_date = fields.Date(
        string="Today",
        compute="_compute_today_date",
        store=False
    )

    total_days = fields.Integer(
        string="Total Days",
        compute="_compute_total_days",
        store=False
    )

    purchase_order_id = fields.Many2one(
        'purchase.order',
        string="Purchase Order",
        compute="_compute_purchase_order_id",
        store=True,
        readonly=True
    )

    @api.depends('invoice_date_due')
    def _compute_due_status(self):
        today = fields.Date.today()  # Gunakan fields.Date.today() untuk menjaga kompatibilitas timezone
        for move in self:
            if move.invoice_date_due:
                move.due_status = 'overdue' if move.invoice_date_due < today else 'not_due'
            else:
                move.due_status = False

    @api.depends('invoice_line_ids.purchase_line_id')
    def _compute_purchase_order_id(self):
        for move in self:
            po_ids = move.invoice_line_ids.mapped('purchase_line_id.order_id')
            move.purchase_order_id = po_ids[0] if po_ids else False


    @api.depends()
    def _compute_today_date(self):
        today = fields.Date.context_today(self)
        for move in self:
            move.today_date = today

    @api.depends('invoice_date_due')
    def _compute_total_days(self):
        today = fields.Date.context_today(self)
        for move in self:
            if move.invoice_date_due:
                move.total_days = (move.invoice_date_due - today).days
            else:
                move.total_days = 0

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    purchase_line_id = fields.Many2one(
        'purchase.order.line',
        string="Purchase Order Line",
        compute='_compute_purchase_line_id',
        store=True,
        readonly=True
    )

    @api.depends('move_id.invoice_origin', 'product_id')
    def _compute_purchase_line_id(self):
        for line in self:
            po_line = False
            if line.move_id.invoice_origin and line.product_id and line.price_unit:
                domain = [
                    ('order_id.name', '=', line.move_id.invoice_origin),
                    ('product_id', '=', line.product_id.id),
                    ('price_unit', '=', line.price_unit),
                ]
                po_line = self.env['purchase.order.line'].search(domain, limit=1)
            line.purchase_line_id = po_line

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

