from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    advance_payment_ids = fields.One2many(
        'account.payment', 'invoice_id', string="Advance Payments"
    )
    advance_payment_status = fields.Selection(
        selection=[
            ("not_paid", "Not Paid"),
            ("paid", "Paid"),
            ("partial", "Partially Paid"),
        ],
        string="Advance Status",
        compute="_compute_advance_payment_status",
        store=True,
    )
    
    state = fields.Selection(
        selection_add=[('commercial_invoice', 'Commercial Invoice')],
        ondelete={'commercial_invoice': 'set default'}
    )

    container_number = fields.Char(
        string='Container Number',
        required=False,
        help="Required field to indicate the container number."
    )

    receipt_date = fields.Date(
        string="Receipt Date",
        compute="_compute_receipt_date",
        store=False,
    )

    outstanding_debit_line_ids = fields.One2many(
        'account.move.line',
        compute='_compute_outstanding_debits',
        string='Outstanding Debits',
        store=False,
    )

    @api.depends('invoice_origin')
    def _compute_receipt_date(self):
        for move in self:
            receipt_date = False
            if move.invoice_origin:
                po = self.env['purchase.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if po and po.order_line:
                    # Ambil tanggal paling awal dari semua line
                    receipt_date = min(po.order_line.mapped('date_planned'))
            move.receipt_date = receipt_date

    # def action_post(self):
    #     for move in self:
    #         if move.move_type == 'in_invoice' and move.state == 'draft':
    #             move.state = 'commercial_invoice'
    #         else:
    #             super(AccountMove, move).action_post()

    # def action_post(self):
    #     for move in self:
    #         if move.move_type == 'in_invoice' and move.state == 'draft':
    #             if not move.name or move.name == '/':
    #                 move.name = move._get_sequence()
    #             move.state = 'commercial_invoice'
    #         else:
    #             super(AccountMove, move).action_post()
    #             
    def action_post(self):
        for move in self:
            if move.move_type == 'in_invoice' and move.state == 'draft':
                # Tambahan: Link manual ke purchase jika belum ada
                if not move.purchase_id and move.invoice_origin:
                    po = self.env['purchase.order'].search([('name', '=', move.invoice_origin)], limit=1)
                    if po:
                        move.purchase_id = po

                if not move.name or move.name == '/':
                    move.name = move._get_sequence()
                move.state = 'commercial_invoice'
            else:
                super(AccountMove, move).action_post()

    def _get_sequence(self):
        self.ensure_one()
        prefix = 'CI/%(year)s/'
        seq_code = 'custom.commercial.invoice'

        # Cek apakah sequence sudah ada
        seq = self.env['ir.sequence'].search([('code', '=', seq_code)], limit=1)
        if not seq:
            seq = self.env['ir.sequence'].create({
                'name': 'Commercial Invoice Sequence',
                'code': seq_code,
                'implementation': 'no_gap',
                'prefix': prefix,
                'padding': 5,
                'number_next_actual': 1,
            })

        return seq.with_context(ir_sequence_date=self.date or fields.Date.today()).next_by_code(seq_code)

    def action_validate_commercial_invoice(self):
        for move in self:
            super(AccountMove, move).action_post()

    def button_cancel_commercial_invoice(self):
        for move in self:
            if move.state == 'commercial_invoice':
                move.state = 'draft'
                move.line_ids.remove_move_reconcile()
                move.button_cancel()  # jika perlu batalkan invoice sepenuhnya


    @api.depends("advance_payment_ids.state", "amount_total", "amount_residual")
    def _compute_advance_payment_status(self):
        for inv in self:
            if not inv.advance_payment_ids:
                inv.advance_payment_status = "not_paid"
            else:
                if inv.amount_residual == 0.0:
                    inv.advance_payment_status = "paid"
                elif inv.amount_residual < inv.amount_total:
                    inv.advance_payment_status = "partial"
                else:
                    inv.advance_payment_status = "not_paid"

    @api.depends('partner_id')
    def _compute_outstanding_debits(self):
        for move in self:
            if move.partner_id:
                move.outstanding_debit_line_ids = self.env['account.move.line'].search([
                    ('partner_id', '=', move.partner_id.id),
                    ('account_id.internal_type', '=', 'payable'),
                    ('reconciled', '=', False),
                    ('debit', '>', 0),
                    ('company_id', '=', move.company_id.id)
                ])
            else:
                move.outstanding_debit_line_ids = False