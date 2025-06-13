{
    "name": "Custom Picking Stages",
    "version": "14.0.1.0.0",
    "category": "Warehouse",
    "summary": "Menambahkan status tambahan untuk stock picking",
    "description": """
        Modul ini menambahkan status Loaded, Boarded, Customs, Arrived sebelum Done.
        Memungkinkan input tanggal manual dan mencatat perubahan di log.
    """,
    "depends": ["product_bundle_pack", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_picking_views.xml",
        "wizard/date_input_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}