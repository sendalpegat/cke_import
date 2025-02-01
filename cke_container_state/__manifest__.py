{
    'name': 'Inventory Receipt Status',
    'version': '14.0.1.0.0',
    'summary': 'Menambahkan status pada Inventory Receipt',
    'category': 'Inventory',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['stock'],
    'data': [
        'views/stock_picking_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}