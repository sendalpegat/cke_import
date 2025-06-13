{
    'name': 'Manual Vendor Bill from Inventory Receipt',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Create Vendor Bills manually from Inventory Receipts',
    'description': """
        This module allows creating Vendor Bills manually from Inventory Receipts using a button or action.
    """,
    'author': 'Your Name',
    'depends': ['stock', 'account', 'purchase'],
    'data': [
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml'
        # 'views/account_move_views.xml',
    ],
    'installable': True,
    'application': True,
}