{
    'name': 'Custom Dynamic Fields',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Add dynamic fields to products based on product category',
    'author': 'Your Name',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_views.xml',
        'views/product_product_views.xml',
    ],
    'installable': True,
    'application': False,
}