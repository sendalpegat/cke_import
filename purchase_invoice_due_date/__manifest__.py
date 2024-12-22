{
    'name': 'Purchase Order Due Date',
    'version': '14.0.1.0.0',
    'summary': 'Display Due Date from Account Move in Purchase Order',
    'description': 'Adds a field to display the due date from related invoices in the Purchase Order form view.',
    'category': 'Purchases',
    'author': 'PT. Industrial Multi Fan',
    'website': 'https://kipascke.co.id',
    'maintainer': 'aRai',
    'depends': ['purchase', 'account'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}