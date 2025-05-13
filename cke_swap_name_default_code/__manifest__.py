{
    'name': 'Swap Name and Default Code',
    'version': '14.0.1.0.0',
    'summary': 'Swaps the positions of the name and default_code fields in product.product and product.template models',
    'description': """
        This module swaps the positions of the 'name' and 'default_code' fields in the 'product.product' and 'product.template' models.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['base', 'product'],
    'data': [
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}