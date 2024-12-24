{
    'name': 'Item Count in Incoming shipment',
    'version': '14.0',
    'category': 'Inventory',
    'summery': 'Total Items Quantity for Delivery Order',
    'website': 'https://kipascke.co.id',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'depends': ['stock'],
    
    'data': [
        'views/delivery_order_view.xml',
        'report/delivery_order_report.xml',
    ],
    
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
