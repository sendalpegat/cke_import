# -*- encoding: utf-8 -*-
{
    'name': "Row Number in tree/list view",
    'version': '14.0.1.1',
    'summary': 'Show row number in tree/list view.',
    'category': 'Other',
    'description': """By installing this module, user can see row number in Odoo backend tree view.""",
    "depends" : ['web'],
    'data': [
             'views/listview_templates.xml',
             ],
    "images": ["static/description/rowno_tree-banner.png"],
    'license': 'LGPL-3',

    # Author
    'author': 'Synodica Solutions Pvt. Ltd.',
    'website': 'https://synodica.com',
    'maintainer': 'Synodica Solutions Pvt. Ltd.',

    'qweb': [
            ],  
    
    'installable': True,
    'application'   : True,
    'auto_install'  : False,
}
