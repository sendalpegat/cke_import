{
    'name': 'Product Template by Category',
    'version': '1.0',
    'summary': 'Add product templates specifications based on category',
    'author': 'Your Name',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
    ],
    'installable': True,
    'application': False,
}