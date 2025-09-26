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

    Extended Import Features:
    - Import product pack components from Excel/CSV files
    - Support for 13 fields including Type, Category, Factory Model No, Product Brand
    - Auto-create products if not exist
    - Flexible pack control (Is Pack field)
    - Calculate pack price option
    - Multiple download methods for templates
    - Comprehensive validation and error handling

    """,
    "sequence": 1,
    "author": "PT Industrial Multi Fan",
    "maintainer": "aRai",
    "website": "https://kipascke.co.id",
    "version": '14.0.15.09.25',
    "depends": ['sale','product','stock','sale_stock','sale_management','purchase','cke_product_model'],
    "data": [
        'views/product_view.xml',
        'views/purchase_order_pack_view.xml',
        'views/account_move_explode_button.xml',
        'views/account_move_line_view.xml',
        # 'views/stock_picking_view.xml',
        'wizard/product_bundle_wizard_view.xml',
        'wizard/explode_pack_wizard_view.xml',
        'wizard/import_product_pack_wizard_view.xml',        # Extended import wizard
        'views/dashboard_shortcuts_view.xml',                # Dashboard shortcuts & kanban
        'views/simple_import_menu.xml',                      # Minimal menu (cleaned)
        'security/ir.model.access.csv',
        'views/product_pack_view.xml',
    ],
    'external_dependencies': {
    'python': ['xlsxwriter']
    },
    "images": ['static/description/icon.png'],
    "installable": True,
    "application": True,
    "auto_install": False,
}