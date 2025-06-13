# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestProductBundle(TransactionCase):

    def setUp(self):
        super().setUp()

        # Buat dua produk komponen
        self.product_a = self.env['product.product'].create({
            'name': 'Component A',
            'standard_price': 100.0,
            'list_price': 150.0,
            'type': 'product',
            'uom_id': self.ref('uom.product_uom_unit'),
        })

        self.product_b = self.env['product.product'].create({
            'name': 'Component B',
            'standard_price': 50.0,
            'list_price': 100.0,
            'type': 'product',
            'uom_id': self.ref('uom.product_uom_unit'),
        })

        # Template bundle
        self.bundle_template = self.env['product.template'].create({
            'name': 'Bundle X',
            'type': 'product',
            'is_pack': True,
            'cal_pack_price': True,
            'uom_id': self.ref('uom.product_uom_unit'),
        })
        self.bundle = self.bundle_template.product_variant_id

        # Assign komponen ke bundle
        self.env['product.pack'].create({
            'product_id': self.product_a.id,
            'qty_uom': 2,
            'bi_product_template': self.bundle_template.id
        })
        self.env['product.pack'].create({
            'product_id': self.product_b.id,
            'qty_uom': 1,
            'bi_product_template': self.bundle_template.id
        })

    def test_pack_price_calculation(self):
        """Bundle standard_price dihitung otomatis dari komponen"""
        self.bundle_template._recompute_pack_price()
        self.assertEqual(self.bundle_template.standard_price, 2 * 100 + 1 * 50)

    def test_sale_order_bundle_line(self):
        """Bundle dapat ditambahkan ke SO"""
        partner = self.env['res.partner'].create({'name': 'Customer Test'})
        so = self.env['sale.order'].create({'partner_id': partner.id})
        line = self.env['sale.order.line'].create({
            'order_id': so.id,
            'product_id': self.bundle.id,
            'product_uom_qty': 1,
            'product_uom': self.bundle.uom_id.id
        })
        self.assertTrue(line.product_id.is_pack)
        self.assertEqual(len(line.product_id.pack_ids), 2)

    def test_purchase_order_invoice_with_bundle(self):
        """Invoice PO bundle harus terbentuk dan valid"""
        vendor = self.env['res.partner'].create({'name': 'Vendor Test', 'supplier_rank': 1})
        po = self.env['purchase.order'].create({'partner_id': vendor.id})
        po_line = self.env['purchase.order.line'].create({
            'order_id': po.id,
            'product_id': self.bundle.id,
            'product_uom_qty': 1,
            'product_uom': self.bundle.uom_id.id,
            'price_unit': 0.0,
            'date_planned': po.date_order,
            'name': self.bundle.name,
        })

        po.action_confirm()
        result = po.action_create_invoice()
        self.assertIn('account.move', result['res_model'])
        invoice = self.env['account.move'].browse(result['res_id'])
        self.assertGreater(len(invoice.invoice_line_ids), 0)

    def test_pack_without_component_warning(self):
        """Bundle tanpa komponen harus raise error saat dijual"""
        empty_template = self.env['product.template'].create({
            'name': 'Empty Pack',
            'type': 'product',
            'is_pack': True,
            'uom_id': self.ref('uom.product_uom_unit'),
        })
        empty_bundle = empty_template.product_variant_id
        partner = self.env['res.partner'].create({'name': 'Client X'})
        so = self.env['sale.order'].create({'partner_id': partner.id})

        with self.assertRaises(UserError):
            self.env['sale.order.line'].create({
                'order_id': so.id,
                'product_id': empty_bundle.id,
                'product_uom_qty': 1,
                'product_uom': empty_bundle.uom_id.id
            })