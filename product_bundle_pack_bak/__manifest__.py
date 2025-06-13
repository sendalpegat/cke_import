# -*- coding: utf-8 -*-

{
    "name": "Product Bundle Pack",
    "category": 'Purchase',
    "summary": 'Combine two or more product pack product kit product bundle product pack item on product combo product',
    "description": """
	This module is use to 
    odoo create Product Bundle Product Pack Bundle Pack of Product Combined Product pack odoo
    odoo Product Pack Custom Combo Product Bundle Product Customized product Group product odoo
    odoo Custom product bundle Custom Product Pack odoo combo product pack combo product combo bundle pack combo bundle product pack 
    odoo combo product pack multiple product pack group product pack choice odoo
    odoo product Pack Price Product Bundle pack price product Bundle Discount product Bundle Offer bundle price

    """,
    "sequence": 1,
    "author": "PT Industrial Multi Fan",
    "maintainer": "aRai",
    "license": "LGPL-3",
    "website": "https://kipascke.co.id",
    "version": '14.0.0.1',
    "depends": ['sale','product','stock','sale_stock','sale_management','purchase'],
    "data": [
        'wizard/product_bundle_wizard_view.xml',
        'views/product_view.xml',
        'views/purchase_view.xml',
        'security/ir.model.access.csv'
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
     "images":['static/description/icon.png'],

}
