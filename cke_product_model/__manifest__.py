{
    'name': 'Product Custom Fields',
    'version': '14.0.1.0.0',
    'summary': 'Adds Factory Model No and Manufacture Code to Products',
    'description': """
        This module adds two custom fields to products:
        - Factory Model No
        - Manufacture Code
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['product'],
    'data': [
        'views/product_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}