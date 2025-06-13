# -*- coding: utf-8 -*-
# Copyright 2024 Trackedge <https://trackedgetechnologies.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Product Multiple Images & Videos',
    'version': '1.0',
    'summary': """Add Multiple Images & YouTube into Your Products""",
    'description': """""",
    'category': 'Base',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'depends': ['base', 'product'],

    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
    ],
    'demo': [

    ],
    'images': ['static/description/icon.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
