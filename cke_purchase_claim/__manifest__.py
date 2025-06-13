{
    'name': 'Purchase Claim',
    'version': '14.0.1.0.0',
<<<<<<< HEAD
    'category': 'Purchases',
=======
<<<<<<< HEAD
    'category': 'Purchases',
=======
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
    'summary': 'Manage purchase claims to vendors',
    'description': """
        This module allows you to manage purchase claims to vendors.
        Key features include:
        - Creating, tracking, and managing purchase claims.
        - Workflow states for claim processing (draft, submitted, approved, rejected).
        - Integration with existing Odoo models such as purchase orders and vendors.
        - Security rules to manage access rights for different user roles.
    """,
<<<<<<< HEAD
    'author': 'Your Name',
=======
<<<<<<< HEAD
    'author': 'Your Name',
=======
    'category': 'Custom',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'license': 'LGPL-3',
    'website': 'https://kipascke.co.id',
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
    'depends': ['base', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/purchase_claim_security.xml',
        'data/purchase_claim_data.xml',
        'views/purchase_claim_view.xml',
        'views/purchase_claim_menu.xml',
    ],
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    'images': ['static/description/icon.png'],
>>>>>>> 14235b34476058108377e4dd1d0e42c42ff8007c
>>>>>>> 96b28c2cf3b83a317a773c01125a88ce0c9038de
    'installable': True,
    'application': True,
    'auto_install': False,
}