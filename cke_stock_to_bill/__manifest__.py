{
    'name': 'Create Vendor Bill from Receipt',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Create draft Vendor Bill from Stock Picking',
    'description': """
        This module allows creating draft Vendor Bills directly from Stock Picking (Receipts)
    """,
    'author': 'Your Name',
    'website': 'https://www.yourcompany.com',
    'depends': ['stock_account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}