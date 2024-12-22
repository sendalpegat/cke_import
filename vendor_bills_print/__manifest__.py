{
    'name': 'Vendor Bills Print Button',
    'version': '14.0.1.0.0',
    'summary': 'Add Print button to Vendor Bills, depends on purchase_deposit module',
    'category': 'Accounting',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
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
    'installable': True,
    'application': False,
    'auto_install': False,
}