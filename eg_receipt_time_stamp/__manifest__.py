{
    'name': 'Purchase Order Timeline',
    'version': '14.0.1.0.0',
    'description': 'Purchase Order Timeline',
    'author': 'INKERP',
    'website': 'www.INKERP.com',
    'depends': ['purchase', 'stock', 'mail'],
    
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
