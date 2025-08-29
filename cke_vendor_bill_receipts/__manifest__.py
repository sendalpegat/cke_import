# -*- coding: utf-8 -*-
{
    "name": "Vendor Bill Receipts (Show Inventory Receipts After Posted)",
    "summary": "Tampilkan daftar Inventory Receipt (incoming pickings) di Vendor Bill setelah posted",
    "version": "14.0.1.0.0",
    "category": "Accounting/Stock",
    "author": "aRai + GPT",
    "website": "https://example.com",
    "license": "LGPL-3",
    "depends": ["account", "stock", "purchase", "product_bundle_pack", "purchase_advance_payment"],
    "data": [
        "views/account_move_receipts_button.xml",
        "views/receipt_move_tree.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}