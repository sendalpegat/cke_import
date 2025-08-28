# -*- coding: utf-8 -*-
{
    "name": "Vendor Bill Picking (Create Picking After Posted)",
    "summary": "Tambah tombol Create Picking di Vendor Bill setelah posted",
    "version": "14.0.1.0.0",
    "category": "Accounting/Stock",
    "author": "aRai",
    "website": "https://kipascke.co.id",
    "license": "LGPL-3",
    "depends": ["account", "stock"],  # 'purchase' opsional; tidak wajib
    "data": [
        "views/account_move_picking_button.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}