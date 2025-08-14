# models/account_move.py
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    fee_percentage = fields.Float(
        string='Fee (%)',
        digits=(16, 2),
        default=0.0,
        help="Fee percentage to be added to the bill amount"
    )
    
    fee_amount = fields.Monetary(
        string='Fee Amount',
        compute='_compute_fee_amount',
        store=True,
        help="Calculated fee amount"
    )
    
    subtotal_before_fee = fields.Monetary(
        string='Subtotal Before Fee',
        compute='_compute_fee_amount',
        store=True,
        help="Amount before fee calculation"
    )
    
    remaining_fee = fields.Monetary(
        string='Remaining Fee',
        compute='_compute_remaining_amounts',
        store=True,
        help="Remaining fee amount to be paid"
    )
    
    remaining_base = fields.Monetary(
        string='Remaining Base',
        compute='_compute_remaining_amounts',
        store=True,
        help="Remaining base amount to be paid"
    )

    @api.depends('invoice_line_ids.price_subtotal', 'fee_percentage')
    def _compute_fee_amount(self):
        for move in self:
            if move.move_type == 'in_invoice':
                # Calculate subtotal from all invoice lines
                subtotal = sum(line.price_subtotal for line in move.invoice_line_ids)
                move.subtotal_before_fee = subtotal
                move.fee_amount = subtotal * (move.fee_percentage / 100.0)
            else:
                move.subtotal_before_fee = 0.0
                move.fee_amount = 0.0

    @api.depends('invoice_line_ids.price_subtotal', 'fee_amount', 'invoice_line_ids.tax_ids', 'partner_id', 'currency_id')
    def _compute_amount(self):
        """Override to include fee in total amount calculation"""
        for move in self:
            if move.move_type == 'in_invoice' and move.fee_amount > 0:
                # Call parent method first to get standard calculations
                super(AccountMove, move)._compute_amount()
                # Add fee to amount_untaxed and amount_total
                move.amount_untaxed = move.amount_untaxed + move.fee_amount
                move.amount_total = move.amount_total + move.fee_amount
                # Adjust amount_residual to include fee for unpaid invoices
                if move.payment_state in ['not_paid', 'partial']:
                    move.amount_residual = move.amount_residual + move.fee_amount
            else:
                super(AccountMove, move)._compute_amount()

    @api.depends('amount_residual', 'fee_amount', 'subtotal_before_fee')
    def _compute_remaining_amounts(self):
        for move in self:
            if move.move_type == 'in_invoice' and move.fee_amount > 0:
                total_with_fee = move.subtotal_before_fee + move.fee_amount
                if total_with_fee > 0:
                    # Calculate proportional remaining amounts
                    paid_amount = total_with_fee - move.amount_residual
                    fee_ratio = move.fee_amount / total_with_fee
                    base_ratio = move.subtotal_before_fee / total_with_fee
                    
                    paid_fee = paid_amount * fee_ratio
                    paid_base = paid_amount * base_ratio
                    
                    move.remaining_fee = move.fee_amount - paid_fee
                    move.remaining_base = move.subtotal_before_fee - paid_base
                else:
                    move.remaining_fee = move.fee_amount
                    move.remaining_base = move.subtotal_before_fee
            else:
                move.remaining_fee = 0.0
                move.remaining_base = move.amount_residual

    @api.onchange('fee_percentage')
    def _onchange_fee_percentage(self):
        """Update fee calculation when fee percentage changes"""
        if self.move_type == 'in_invoice':
            # Just trigger recompute, no need to create fee line
            self._compute_fee_amount()
            self._compute_remaining_amounts()

    def _update_fee_line(self):
        """Create or update fee line"""
        # Remove existing fee line
        fee_lines = self.invoice_line_ids.filtered(lambda l: l.name and 'Fee' in l.name)
        if fee_lines:
            fee_lines.unlink()
        
        # Create new fee line if fee percentage > 0
        if self.fee_percentage > 0:
            subtotal = sum(line.price_subtotal for line in self.invoice_line_ids)
            fee_amount = subtotal * (self.fee_percentage / 100.0)
            
            if fee_amount > 0:
                # Get default expense account
                expense_account = self.env['account.account'].search([
                    ('user_type_id.type', '=', 'payable'),
                    ('company_id', '=', self.company_id.id)
                ], limit=1)
                
                if not expense_account:
                    expense_account = self.env['account.account'].search([
                        ('code', '=like', '2%'),
                        ('company_id', '=', self.company_id.id)
                    ], limit=1)
                
                self.invoice_line_ids = [(0, 0, {
                    'name': f'Fee {self.fee_percentage}%',
                    'quantity': 1,
                    'price_unit': fee_amount,
                    'account_id': expense_account.id if expense_account else False,
                })]

    def action_post(self):
        """Override to ensure fee line is created before posting"""
        for move in self:
            if move.move_type == 'in_invoice' and move.fee_percentage > 0:
                move._update_fee_line()
        return super(AccountMove, self).action_post()

    def action_refresh_fee(self):
        """Manual refresh fee calculation"""
        if self.move_type == 'in_invoice':
            self._update_fee_line()
            # Trigger recompute of all computed fields
            self._compute_fee_amount()
            self._compute_remaining_amounts()
        return True