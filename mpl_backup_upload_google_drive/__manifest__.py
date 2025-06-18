# -*- coding: utf-8 -*-
###############################################################################
#
#    Meghsundar Private Limited(<https://www.meghsundar.com>).
#
###############################################################################
{
    'name': 'Database Backup Upload Local and GDrive',
    'version': '14.0.1',
    'summary': 'Database Backup Upload Local and GDrive',
    'description': 'Database Backup Upload Local and GDrive',
    'license': 'AGPL-3',
    'author': 'Meghsundar Private Limited',
    'website': 'https://www.meghsundar.com',
    'category': 'Administration',
    'depends': ['base', 'mail', 'google_drive'],
    'data': [
        'security/ir.model.access.csv',
        'views/backup_view.xml',
        'data/backup_scheduled_action_data.xml',
        'data/auto_backup_mail.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
