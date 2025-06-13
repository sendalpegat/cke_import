{
    'name': 'Product Custom Fields',
    'version': '14.0.1.0.0',
    'summary': 'Adds Factory Model No and Manufacture Code to Products',
    'description': """
        This module adds two custom fields to products:
        - Factory Model No
        - Manufacture Code
    """,
    'category': 'Inventory/Inventory',
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': [
        'views/product_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}