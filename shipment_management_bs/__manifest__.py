# -*- coding: utf-8 -*-
{
    'name': 'Purchase Order Shipment',
    'summary': "Create Shipments of Purchase Order and align stock transfer as per shipments",
    'author': "PT Industrial Multi Fan",
    'maintainer': "aRai",
    'website': "https://kipascke.co.id",

    'license': 'OPL-1',
    'category': 'Purchase',
    'version': '14.0.0.1',

    'depends': ['base','purchase','stock'],
    'data': [
        'security/ir.model.access.csv',
        'security/purchase_order_shipment_security.xml',

        'data/data.xml',

        'views/purchase_order.xml',
        'views/purchase_order_shipment.xml',
        'views/stock_picking.xml',
    ],
    'images': ['/static/description/icon.png'],

    'application': True,
    'installable': True,
    'auto_install': False,
    'currency': 'USD'
}


