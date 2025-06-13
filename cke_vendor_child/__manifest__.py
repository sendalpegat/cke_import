{
    'name': 'Vendor Child Contact View',
    'version': '14.0.1.0.0',
    'summary': 'Memisahkan Parent dan Child Contact di Tree View',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'category': 'Contacts',
    'depends': ['base', 'purchase'],
    'data': [
        'views/res_partner_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}