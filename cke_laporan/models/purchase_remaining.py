from odoo import models, fields, api
from datetime import date

class PurchaseRemainingLine(models.Model):
    _name = 'purchase.remaining.line'
    _description = 'Remaining PO Line'
    _auto = False

    order_id = fields.Many2one('purchase.order', string='Order Reference')
    date_approve = fields.Datetime(string='Order Date')
    date_order = fields.Datetime(string='Order Deadline')
    partner_ref = fields.Char(string='Vendor Reference')
    product_id = fields.Many2one('product.product', string='Product')
    product_name = fields.Char(string='Product Name')
    quantity = fields.Float(string='Quantity Ordered')
    received = fields.Float(string='Received Quantity')
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal')
    due_date = fields.Date(string='Due Date')
    overdue = fields.Boolean(string='Overdue')
    po_ita = fields.Char(string='PO ITA')  # Optional field, you can customize logic
    hpp = fields.Float(string='HPP')       # Optional field, you can customize logic

    def _select(self):
        return """
            SELECT
                pol.id as id,
                po.id as order_id,
                po.partner_ref,
                po.date_approve,
                po.date_order,
                pol.product_id,
                pt.name as product_name,
                pol.product_qty as quantity,
                pol.qty_received as received,
                pol.price_unit,
                (pol.product_qty - pol.qty_received) * pol.price_unit as subtotal,
                pol.date_planned::date as due_date,
                CASE WHEN pol.date_planned::date < CURRENT_DATE THEN TRUE ELSE FALSE END as overdue,
                po.po_ita,
                pt.standard_price as hpp
        """

    def _from(self):
        return """
            FROM purchase_order_line pol
            JOIN purchase_order po ON pol.order_id = po.id
            JOIN product_product pp ON pol.product_id = pp.id
            JOIN product_template pt ON pp.product_tmpl_id = pt.id
        """

    def _where(self):
        return """
            WHERE pol.product_qty > pol.qty_received
        """

def init(self):
    self.env.cr.execute("""
        CREATE OR REPLACE VIEW purchase_remaining_line AS (
            {select}
            {from_clause}
            {where}
        )
    """.format(
        select=self._select(),
        from_clause=self._from(),
        where=self._where(),
    ))