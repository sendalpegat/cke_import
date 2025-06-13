{
    'name': 'Vendor Invoice with Product Pack',
    'version': '14.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Menambahkan tombol Commercial Invoice dan pengecekan product pack',
    'description': """
        Modul ini menambahkan fitur:
        1. Tombol Commercial Invoice di Purchase Order
        2. Pengecekan product pack yang ditambahkan setelah PO dibuat
        3. Peringatan saat membuat invoice jika ada product pack yang ditambahkan belakangan
    """,
    'depends': ['purchase', 'product_bundle_pack'],
    'data': [
        'views/purchase.xml',
    ],
    'installable': True,
    'application': False,
}