# -*- coding: utf-8 -*-
##############################################################################
#
#    PT Industrial Multi Fan.
#    Copyright (C) 2025-TODAY iWesabe (<httpss://kipascke.co.id>).
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Hide Product Cost',
    'version': '1.0',
    'author': 'aRai',
    'summary': 'Hide Product Standard Price',
    'description': """This module helps to hide product cost for specific group of users.""",
    'category': 'Human Resources',
    'website': 'httpss://kipascke.co.id',
    'license': 'AGPL-3',
    'depends': ['product'],
    'data': [
        'security/security.xml',
        'views/product_views.xml',
        'views/product_template_views.xml',
    ],
    'qweb': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
