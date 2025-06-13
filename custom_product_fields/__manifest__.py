{
    'name': 'Custom Product Fields',
    'version': '14.0.1.0.0',
    'summary': 'Menambahkan field kustom secara dinamis di kategori produk dan otomatis muncul di formulir produk',
    'category': 'Product',
    'author': 'Your Name',
    'depends': ['product'],
    'data': [
        'views/product_category_field_view.xml',
        'views/product_category_view.xml',
        'views/product_template_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}