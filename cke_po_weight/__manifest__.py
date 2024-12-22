{
    'name': 'Product weight in purchase Order',
    'version': '14.0.1.0.0',
    'category': 'Purchase',
    'summery': 'Total Weight of the Purchase Order Products',
    'author': 'INKERP',
    'website': 'www.inkerp.com',
    'depends': ['purchase'],
    
    'data': [
        'reports/purchase_quotation_template.xml',
        'reports/purchase_order_template.xml',
        'views/purchase_order_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
