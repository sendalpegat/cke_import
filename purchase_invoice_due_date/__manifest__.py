{
    'name': 'Purchase Order Due Date',
    'version': '14.0.1.0.0',
    'summary': 'Display Due Date from Account Move in Purchase Order',
    'description': 'Adds a field to display the due date from related invoices in the Purchase Order form view.',
    'category': 'Purchases',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'depends': ['purchase', 'account'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}