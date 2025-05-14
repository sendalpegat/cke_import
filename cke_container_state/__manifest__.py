{
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
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}