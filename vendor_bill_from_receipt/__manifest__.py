{
    'name': 'Manual Vendor Bill from Inventory Receipt',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Create Vendor Bills manually from Inventory Receipts',
    'description': """
        This module allows creating Vendor Bills manually from Inventory Receipts using a button or action.
    """,
    'author': 'Your Name',
<<<<<<< HEAD
    'depends': ['stock', 'account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml'
        # 'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
=======
    'depends': ['stock', 'account'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
}