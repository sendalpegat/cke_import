{
    'name': 'Vendor Product Filter in Purchase Order',
    'version': '14.0.1.0.0',
    'summary': 'Filter products by vendor in Purchase Order',
    'category': 'Purchases',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'LGPL-3',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}