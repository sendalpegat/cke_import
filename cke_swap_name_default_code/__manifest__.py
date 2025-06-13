{
    'name': 'Swap Name and Default Code',
    'version': '14.0.1.0.0',
<<<<<<< HEAD
    'category': 'Product',
=======
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'summary': 'Swaps the positions of the name and default_code fields in product.product and product.template models',
    'description': """
        This module swaps the positions of the 'name' and 'default_code' fields in the 'product.product' and 'product.template' models.
    """,
<<<<<<< HEAD
    'author': 'Your Name',
    'website': 'http://www.yourwebsite.com',
=======
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'depends': ['base', 'product'],
    'data': [
        'views/product_product_views.xml',
        'views/product_template_views.xml',
    ],
<<<<<<< HEAD
    'installable': True,
    'application': False,
=======
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
}