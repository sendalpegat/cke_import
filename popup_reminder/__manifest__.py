# See LICENSE file for full copyright and licensing details.
{
    'name': 'Pop-up Reminder',
    'version': '14.0.1.0.0',
    'category': 'Web',
    'live_test_url': 'https://www.youtube.com/watch?v=jgBcyyhU7KU',
    'license': 'LGPL-3',
    'summary': """Dynamic reminder of different models.
    popup reminder""",
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'maintainer': 'Serpent Consulting Services Pvt. Ltd.',
    'description': ''' Popup reminder is helps to notify all your important
        records as per your configuration.You can set reminders
        of any model (eg: CRM, HR, Project, Sales)
        popup reminder
        popup notification
        notification alert
        notification box
        reminders''',
    'website': 'https://www.serpentcs.com',
    'depends': ['base', 'web', 'bus'],
    'data': [
        'security/ir.model.access.csv',
        'views/popup_reminder_view.xml',
        'views/popup_views.xml'
    ],
    'qweb': ['static/src/xml/view.xml'],
    'images': ['static/description/Pop-UpReminder.png'],
    'installable': True,
    'application': True,
    'price': 45,
    'currency': 'EUR',
}
