{
    'name': 'Product Variant by Category',
    'version': '14.0.1.0.0',
    'summary': 'Add product variant fields based on category',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'depends': ['product'],
    'data': [
        # Jika Anda menambahkan view, tambahkan XML-nya di sini
        'views/product_category_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}