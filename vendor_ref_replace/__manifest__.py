{
    'name': 'Vendor Reference Reposition',
    'version': '14.0.1.0.0',
    'summary': 'Memindahkan field ref ke bawah field name pada form vendor',
    'description': """
        Modul ini memindahkan field reference (ref) dari tab Sales & Purchase 
        ke bawah field name pada form vendor.
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Purchases',
    'depends': ['base', 'purchase'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}