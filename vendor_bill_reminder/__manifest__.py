{
    'name': 'Vendor Bill Reminder for Purchase Orders',
    'version': '14.0.1.0.0',
    'summary': 'Remind users if PO has no Vendor Bill within 7 days',
    'category': 'Purchases',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'depends': ['purchase', 'account'],
    'data': [
        'data/reminder_cron.xml',
        'data/email_template.xml',
        'views/reminder_view.xml',
    ],
    'installable': True,
    'application': False,
}