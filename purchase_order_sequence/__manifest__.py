{
    'name': 'Custom Purchase Order Sequence',
    'version': '1.0',
    'summary': 'Generate custom sequence for Purchase Orders.',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'category': 'Purchases',
    'depends': ['purchase'],
    'data': [
            'views/purchase_order_view.xml',
    ],
    'images':['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}