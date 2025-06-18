# -*- coding: utf-8 -*-
from odoo import models

class Payment(models.Model):
    _inherit = 'account.payment'

    def action_payment_cancel(self):
        for rec in self:
            lines = rec.sudo().move_id.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            lines.unlink()
            rec.sudo().move_id.write({'state': 'draft', 'name': '/'})
            rec.write({'state': 'cancel'})

    def action_payment_cancel_draft(self):
        for rec in self:
            lines = rec.sudo().move_id.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            rec.sudo().move_id.write({'state': 'draft', 'name': '/'})
            rec.write({'state': 'draft'})

    def action_payment_cancel_delete(self):
        for rec in self:
            lines = rec.sudo().move_id.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            lines.unlink()
            rec.sudo().move_id.write({'state': 'draft', 'name': '/'})
            rec.unlink()

class Invoice(models.Model):
    _inherit = 'account.move'

    def action_invoice_cancel(self):
        for rec in self:
            lines = rec.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            lines.unlink()
            rec.write({'state': 'draft', 'name': '/'})
            rec.write({'state': 'cancel'})

    def action_invoice_cancel_draft(self):
        for rec in self:
            lines = rec.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            rec.write({'state': 'draft', 'name': '/'})

    def action_invoice_cancel_delete(self):
        for rec in self:
            lines = rec.line_ids
            reconcile_lines = self.env['account.partial.reconcile'].sudo().search([
                '|', ('credit_move_id', 'in', lines.ids), ('debit_move_id', 'in', lines.ids)])
            reconcile_lines.unlink()
            lines.unlink()
            rec.write({'state': 'draft', 'name': '/'})
            rec.unlink()