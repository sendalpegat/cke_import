{
    'name': 'Dynamic Product Templates',
    'version': '14.0.1.0.0',
    'summary': 'Dynamic product templates based on product categories',
    'description': 'This module adds dynamic templates to products based on categories and displays them in product forms and purchase orders.',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['base', 'product', 'purchase'],
    'data': [
        'views/product_template_views.xml',
        'views/purchase_order_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': true,
    'auto_install': False,
}