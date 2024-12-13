{
    'name': 'Receipt Status on Purchase order',
    'version': '14.0',
    'category': 'Purchase',
    'summery': 'Receipt Status on Purchase order',
    'author': 'INKERP',
    'website': "https://www.inkerp.com",
    'depends': ['purchase', 'purchase_stock'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
