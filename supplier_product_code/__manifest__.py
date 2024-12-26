{
    'name': 'Supplier Product Code',
    'version': '14.0.1.0.0',
    'summary': 'Add supplier-specific product codes to the product form',
    'category': 'Purchases',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'depends': ['product', 'purchase'],
    'data': [
        'views/product_supplierinfo_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}