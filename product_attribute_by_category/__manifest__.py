{
    'name': 'Product Attribute by Category',
    'version': '1.0',
    'summary': 'Automatically apply product attributes based on category.',
    'category': 'Product',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['product'],
    'data': [
        'views/product_template_views.xml',
        'views/product_category_views.xml',
    ],    
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}