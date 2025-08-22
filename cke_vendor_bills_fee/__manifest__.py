# -*- coding: utf-8 -*-
{
    'name': 'Vendor Bills Fee',
    'version': '14.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Add fee calculation to vendor bills',
    'description': """
        This module adds fee functionality to vendor bills.
        Fee works like discount but as addition instead of reduction.
        When payment is made with different amount, fee is calculated proportionally.
    """,
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': "https://kipascke.co.id",
    'depends': ['account'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}