# -*- coding: utf-8 -*-
{
    "name": "Purchase Bill Pack Warning",
    "summary": "Tampilkan warning setelah Create Bill jika ada produk PACK (dengan komponen) di invoice lines.",
    "version": "14.0.1.0.0",
    "author": "aRai",
    "license": "LGPL-3",
    "depends": ["purchase", "account", "product_bundle_pack", "cke_pack_explode_statinfo_fix"],
    "data": [
        "security/ir.model.access.csv",
        "views/bill_pack_warning_wizard_views.xml",
        "views/purchase_views.xml",
    ],
    "application": True,
    "installable": True,
}