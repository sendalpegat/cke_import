# -*- coding: utf-8 -*-
{
    "name": "Logistic Stage Flow (Loaded → Boarded → Customs → Arrived → Gudang VSJ)",
    "summary": "Status logistik & internal transfer per tahap dari Vendor Bill (posted)",
    "version": "14.0.1.0.0",
    "category": "Inventory/Logistics",
    "author": "aRai + GPT",
    "license": "LGPL-3",
    "depends": [
        "account",
        "stock",
        "purchase",
        "cke_vendor_bill_receipts",   # ambil Picking List & relasi receipts
        "product_bundle_pack"         # sesuai permintaan, jadikan depend agar mudah
    ],
    "data": [
        "data/stock_locations.xml",
        "security/ir.model.access.csv",
        "views/account_move_logistic_views.xml",
    ],
    "installable": False,
    "application": False,
}