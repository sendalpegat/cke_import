{
    'name': 'Product Name and Internal Reference Swap',
    'version': '14.0.1.05052025',
    'category': 'Inventory',
    'summary': 'Swap the position of Product Name and Internal Reference in the Product Form',
    'description': """
        This module swaps the position of the Product Name and Internal Reference fields
        in the Product form view.
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'depends': ['product'],
    'data': [
        'views/product_template_views.xml',
    ],
    # 'post_init_hook': 'set_default_product_settings',
    'installable': True,
    'application': False,
    'auto_install': False,
}