{
    'name': 'Purchase Order Timeline',
    'version': '14.0.1.0.0',
    'description': 'Purchase Order Timeline',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
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
