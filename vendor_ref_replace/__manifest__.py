{
    'name': 'Vendor Reference Reposition',
    'version': '14.0.1.0.0',
    'summary': 'Memindahkan field ref ke bawah field name pada form vendor',
    'description': """
        Modul ini memindahkan field reference (ref) dari tab Sales & Purchase 
        ke bawah field name pada form vendor.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['base', 'purchase'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}