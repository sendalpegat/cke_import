{
    'name': 'Create Vendor Bill from Receipt',
    'version': '14.0.1.0.0',
    'summary': 'Create draft Vendor Bill from Stock Picking',
    'description': """
        This module allows creating draft Vendor Bills directly from Stock Picking (Receipts)
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['stock_account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}