{
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
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
<<<<<<< HEAD
=======
=======
    'name': 'Inventory Receipt Status',
    'version': '14.0.1.0.0',
    'summary': 'Menambahkan status pada Inventory Receipt',
    'category': 'Inventory',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['product_bundle_pack', 'stock'],
    'data': [
        'views/stock_picking_view.xml',
        'views/date_input_wizard_views.xml',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "license": "LGPL-3",
}