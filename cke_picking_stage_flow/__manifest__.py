# -*- coding: utf-8 -*-
{
    "name": "Picking Stage Flow (Loaded → Boarded → Customs → Arrived → Gudang VSJ)",
    "summary": "Action untuk pindah stage logistik via Picking List (stock.move) + lokasi khusus Loaded",
    "version": "14.0.1.0.0",
    "category": "Inventory/Logistics",
    "author": "aRai + GPT",
    "license": "LGPL-3",
    "depends": [
        "stock",
        "purchase",
        "cke_vendor_bill_receipts",   # agar Picking List tersedia di Vendor Bill
        "product_bundle_pack"         # sesuai preferensi depend
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/stock_locations.xml",     # lokasi: Loaded, Boarded, Customs, Arrived, Gudang VSJ
        "data/actions.xml",             # binding action ke model stock.move (menu Action)
        "views/logistic_stage_move_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
}