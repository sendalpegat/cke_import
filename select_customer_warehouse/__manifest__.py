# -*- coding: utf-8 -*-
{
    'name': "Sales Customer Warehouse",
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'category': 'Sales',
    'summary': """Select Warehouse on the Sales order automatically based on Warehouse set on the Customer""",
    'description': """
""",
    'version': '14.0.1.0',
    'depends': ['base','stock','sale_management'],
    'data': ['views/customer_warehouse.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
