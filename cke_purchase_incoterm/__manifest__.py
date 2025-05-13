{
    'name': 'Purchase Incoterm Selection',
    'version': '14.0.1.0.0',
    'summary': 'Add FOB and CIF selection field to Purchase Orders',
    'description': """
        This module adds a selection field for FOB and CIF incoterms
        to purchase orders, displayed below the vendor name.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_views.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}