{
    'name': 'Product Customize by Category',
    'version': '1.0',
    'summary': 'Dynamically customize products based on product categories.',
    'category': 'Product',
    'author': 'PT Industrial Multi Fan',
    'maintainer': 'aRai',
    'website': 'https://kipascke.co.id',
    'depends': ['product', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
    ],
    'installable': True,
    'application': False,
}