{
    "name": "Product Bundle Invoice",
    "version": "14.0.1.0.0",
    "summary": "Generate vendor bills untuk komponen paket produk",
    "description": """
        Memastikan vendor bills dibuat berdasarkan komponen dalam paket produk.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    "depends": ["product_bundle_pack", "account"],
    "data": [
        "views/purchase_view.xml",
    ],
    'images': ['static/description/icon.png'],
    "installable": True,
    "application": True,
}