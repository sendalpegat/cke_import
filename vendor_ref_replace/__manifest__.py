{
    'name': 'Vendor Reference Reposition',
    'version': '14.0.1.0.0',
    'summary': 'Memindahkan field ref ke bawah field name pada form vendor',
    'description': """
        Modul ini memindahkan field reference (ref) dari tab Sales & Purchase 
        ke bawah field name pada form vendor.
    """,
<<<<<<< HEAD
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
=======
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Purchases',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'depends': ['base', 'purchase'],
    'data': [
        'views/res_partner_views.xml',
    ],
<<<<<<< HEAD
    'images': ['static/description/icon.png'],
=======
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
    'installable': True,
    'application': False,
    'auto_install': False,
}