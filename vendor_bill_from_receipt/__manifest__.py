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
=======
<<<<<<< HEAD
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
    'depends': ['stock', 'account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml'
        # 'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
<<<<<<< HEAD
=======
=======
    'depends': ['stock', 'account'],
    'data': [
        'views/stock_picking_views.xml',
    ],
    'installable': True,
    'application': False,
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
}