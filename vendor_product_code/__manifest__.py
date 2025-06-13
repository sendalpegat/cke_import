{
    'name': 'Vendor Product Code',
    'version': '14.0.1.0.0',
    'summary': 'Add vendor product code field to product supplier information',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': [
        'views/product_supplierinfo_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}