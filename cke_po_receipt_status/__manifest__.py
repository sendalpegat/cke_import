{
    'name': 'Receipt Status on Purchase order',
    'version': '14.0',
    'category': 'Purchase',
    'summery': 'Receipt Status on Purchase order',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': "https://kipascke.co.id",
    'depends': ['purchase', 'purchase_stock'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
