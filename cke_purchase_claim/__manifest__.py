{
    'name': 'Purchase Claim',
    'version': '14.0.1.0.0',
    'summary': 'Manage purchase claims to vendors',
    'description': """
        This module allows you to manage purchase claims to vendors.
        Key features include:
        - Creating, tracking, and managing purchase claims.
        - Workflow states for claim processing (draft, submitted, approved, rejected).
        - Integration with existing Odoo models such as purchase orders and vendors.
        - Security rules to manage access rights for different user roles.
    """,
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/purchase_claim_security.xml',
        'data/purchase_claim_data.xml',
        'views/purchase_claim_view.xml',
        'views/purchase_claim_menu.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}