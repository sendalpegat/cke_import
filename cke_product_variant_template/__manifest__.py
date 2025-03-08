{
    'name': 'Product Variant Template',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Define product variants as templates in product categories',
    'description': """
        This module allows you to define product variants as templates in product categories.
        Variants will be inherited from the category to the product.
    """,
    'author': 'Your Name',
    'depends': ['product'],
    'data': [
        'views/product_category_views.xml',
    ],
    'installable': True,
    'application': False,
}