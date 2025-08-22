from odoo import api, fields, models

class ReportExcelSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    excel_max_records = fields.Integer(
        string="Maximum Records per Report",
        default=10000,
        config_parameter='report_excel.max_records_per_report'
    )
    
    excel_temp_directory = fields.Char(
        string="Temporary Directory",
        default='/tmp/odoo_excel_reports',
        config_parameter='report_excel.temp_directory'
    )
    
    excel_cache_enabled = fields.Boolean(
        string="Enable Caching",
        default=True,
        config_parameter='report_excel.cache_enabled'
    )
    
    excel_debug_mode = fields.Boolean(
        string="Debug Mode",
        default=False,
        config_parameter='report_excel.debug_mode'
    )