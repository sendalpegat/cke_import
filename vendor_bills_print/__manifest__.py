{
    'name': 'Vendor Bills Print Button',
    'version': '14.0.1.0.0',
    'summary': 'Add Print button to Vendor Bills, depends on purchase_deposit module',
    'category': 'Accounting',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'AGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': [
        'account',
        'purchase_deposit'
    ],
    'data': [
        'views/account_move_view.xml',
        'report/vendor_bill_report.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}