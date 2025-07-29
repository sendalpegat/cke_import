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
    'name': 'Purchase Order HPP',
    'version': '14.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Module to calculate HPP based on purchase order currency.',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'license': 'AGPL-3',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}