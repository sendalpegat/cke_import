{
    'name': 'Report Designer (XLSX, XLSM) - Enhanced',
    'version': '1.4.0',
    'category': 'Extra Tools',
    'summary': 'Enhanced Excel Report Designer with Security, Performance & API',
    'description': """
Enhanced Report Designer for Odoo
================================
- Secure formula evaluation
- Performance optimizations
- RESTful API endpoints
- Comprehensive monitoring
- Enhanced error handling
- Advanced caching mechanisms
    """,
    'author': 'Enhanced by AI Assistant',
    'depends': [
        'base',
        'web', 
        'attachment_indexation',
        'mail',
        'base_sparse_field'
    ],
    'external_dependencies': {
        'python': [
            'openpyxl',
            'xlsxwriter', 
            'pillow',
            'psutil'
        ]
    },
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'security/api_security.xml',
        
        # Data
        'data/aggregate_data.xml',
        'data/ir_sequence_data.xml',
        'data/default_configs.xml',
        'data/security_groups.xml',
        
        # Views
        'views/report_excel_views.xml',
        'views/monitoring_views.xml',
        'views/configuration_views.xml',
        'views/menuitem.xml',
        
        # Wizards
        'wizard/report_excel_wizard_view.xml',
        'wizard/report_excel_export_import_wizard_view.xml',
        'wizard/report_performance_wizard_view.xml',
        
        # Assets
        'static/src/xml/assets.xml',
    ],
    'qweb': [
        'static/src/xml/templates.xml',
        'static/src/xml/monitoring_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'pre_init_hook': 'pre_init_check',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}