{
    "name": "Product Bundle Invoice",
    "version": "14.0.1.0.0",
    "summary": "Generate vendor bills untuk komponen paket produk",
    "description": """
        Memastikan vendor bills dibuat berdasarkan komponen dalam paket produk.
    """,
    "depends": ["product_bundle_pack", "account"],
    "data": [
        "views/purchase_view.xml",
    ],
    "installable": True,
    "application": False,
}