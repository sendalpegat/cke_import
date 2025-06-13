{
    'name': 'Create Vendor Bill from Receipt',
    'version': '14.0.1.0.0',
<<<<<<< HEAD
    'category': 'Inventory',
=======
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'summary': 'Create draft Vendor Bill from Stock Picking',
    'description': """
        This module allows creating draft Vendor Bills directly from Stock Picking (Receipts)
    """,
<<<<<<< HEAD
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
=======
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'depends': ['stock_account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
    ],
<<<<<<< HEAD
    'installable': True,
    'application': False,
=======
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'auto_install': False,
}