{
    'name': 'Swap Name and Default Code',
    'version': '14.0.1.0.0',
    'category': 'Product',
    'summary': 'Swaps the positions of the name and default_code fields in product.product and product.template models',
    'description': """
        This module swaps the positions of the 'name' and 'default_code' fields in the 'product.product' and 'product.template' models.
    """,
    'author': 'Your Name',
    'website': 'http://www.yourwebsite.com',
    'depends': ['base', 'product'],
    'data': [
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}