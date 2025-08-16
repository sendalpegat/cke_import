{
    'name': 'Vendor Receipt Date Setting',
    'version': '14.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Automatic receipt date setting based on vendor configuration',
    'description': """
        This module allows setting receipt date configuration on vendors and 
        automatically applies it to Purchase Orders.
        
        Features:
        - Vendor receipt date configuration (1 month, 2 months, 3 months, or manual date)
        - Automatic receipt date calculation in Purchase Orders (default 2 months)
        - Override option for manual adjustment
    """,
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': "https://kipascke.co.id",
    'depends': ['purchase'],
    'data': [
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
    ],
    'qweb': [
        'static/src/xml/purchase_order.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'static/src/js/purchase_order.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}