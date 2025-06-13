{
    'name': 'Purchase Order History',
    'version': '14.0.1.0.0',
    'summary': 'View purchase order history per product and vendor',
    'description': 'Adds a dashboard menu to view purchase order history per product and vendor.',
    'category': 'Purchases',
    'author': 'PT Industrial Multi Fan',
    'website': 'https://kipascke.co.id',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/menus.xml',
        'views/purchase_order_history_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
}
