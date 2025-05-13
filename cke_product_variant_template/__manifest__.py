{
    'name': 'Product Variant Template',
    'version': '1.0',
    'summary': 'Define product variants as templates in product categories',
    'description': """
        This module allows you to define product variants as templates in product categories.
        Variants will be inherited from the category to the product.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['product'],
    'data': [
        'views/product_category_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
}