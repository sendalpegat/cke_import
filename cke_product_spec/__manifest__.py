{
    'name': 'Product Template by Category',
    'version': '1.0',
    'summary': 'Add product templates specifications based on category',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}