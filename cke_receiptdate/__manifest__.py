{
    'name': 'Purchase Auto Receipt Date by Vendor',
    'version': '14.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Atur receipt date otomatis di PO berdasarkan konfigurasi vendor',
    'depends': ['purchase'],
    'author': 'aRai',
    'data': [
        'views/res_partner_view.xml',
        'views/purchase_order_view.xml',
    ],
    'installable': True,
}