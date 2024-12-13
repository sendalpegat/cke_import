{
    'name': 'Item Count in Incoming shipment',
    'version': '14.0',
    'category': 'Inventory',
    'summery': 'Total Items Quantity for Delivery Order',
    'website': 'www.INKERP.com',
    'author': 'INKERP',
    'depends': ['stock'],
    
    'data': [
        'views/delivery_order_view.xml',
        'report/delivery_order_report.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
