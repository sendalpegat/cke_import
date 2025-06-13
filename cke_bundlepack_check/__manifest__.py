{
    "name": "Purchase Bundle Validation",
    "version": "14.0.1.0.0",
    "category": "Purchase",
    "summary": "Add validation for product bundles in purchase orders",
    "description": "Validate product packs in purchase orders and receipts",
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    "depends": ["product_bundle_pack", "purchase"],
    "data": [
        "views/purchase_views.xml",
    ],
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
}