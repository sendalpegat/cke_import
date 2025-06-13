{
    'name': 'Custom Dynamic Fields',
    'version': '14.0.1.0.0',
    'summary': 'Add dynamic fields to products based on product category',
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_views.xml',
        'views/product_product_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}