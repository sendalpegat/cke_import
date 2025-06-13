{
    'name': 'Purchase Incoterm Selection',
    'version': '14.0.1.0.0',
    'summary': 'Add FOB and CIF selection field to Purchase Orders',
    'description': """
        This module adds a selection field for FOB and CIF incoterms
        to purchase orders, displayed below the vendor name.
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'category': 'Purchases',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}