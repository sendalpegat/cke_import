{
    'name': 'Item Count In Purchase Order',
    'version': '14.0',
    'category': 'Purchase',
    'summery': 'Total Items Quantity for Purchase Order',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['purchase'],
    
    'data': [
        'views/purchase_order_view.xml',
        'report/purchase_order_report.xml',
    ],
    
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
