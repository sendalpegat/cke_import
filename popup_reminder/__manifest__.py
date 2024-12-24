# See LICENSE file for full copyright and licensing details.
{
    'name': 'Pop-up Reminder',
    'version': '14.0.1.0.0',
    'category': 'Web',
    'license': 'LGPL-3',
    'summary': """Dynamic reminder of different models.
    popup reminder""",
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'description': ''' Popup reminder is helps to notify all your important
        records as per your configuration.You can set reminders
        of any model
        popup reminder
        popup notification
        notification alert
        notification box
        reminders''',
    'website': 'https://kipascke.co.id',
    'depends': ['base', 'web', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'views/popup_reminder_view.xml',
        'views/popup_views.xml'
    ],
    'qweb': ['static/src/xml/view.xml'],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
