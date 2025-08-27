# -*- coding: utf-8 -*-
{
    "name": "Explode Pack: Fix PO Statinfo on Bills",
    "summary": "Propagasi purchase_line_id ke komponen hasil Explode agar statinfo PO muncul.",
    "version": "14.0.1.0.0",
    "author": "aRai",
    "license": "LGPL-3",
    "depends": [
        "purchase",
        "account",
        # Tambahkan modul pack Anda jika perlu, contoh:
        "product_bundle_pack",
    ],
    "data": [
        "views/account_move_views.xml",
    ],
    "application": True,
    "installable": True,
}