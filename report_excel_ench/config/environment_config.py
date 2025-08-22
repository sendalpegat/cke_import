# config/environment_config.py
import os
from odoo import api, fields, models, tools

class ReportExcelEnvironmentConfig(models.Model):
    _name = 'report.excel.config'
    _description = 'Report Excel Environment Configuration'
    _rec_name = 'key'
    
    key = fields.Char(string='Configuration Key', required=True, index=True)
    value = fields.Text(string='Configuration Value')
    description = fields.Text(string='Description')
    config_type = fields.Selection([
        ('string', 'String'),
        ('integer', 'Integer'),
        ('float', 'Float'),
        ('boolean', 'Boolean'),
        ('json', 'JSON'),
    ], string='Type', default='string', required=True)
    
    environment = fields.Selection([
        ('development', 'Development'),
        ('testing', 'Testing'),
        ('staging', 'Staging'),
        ('production', 'Production'),
    ], string='Environment', default='production')
    
    active = fields.Boolean(string='Active', default=True)
    
    @api.model
    def get_config_value(self, key, default=None, config_type='string'):
        """Get configuration value with type conversion"""
        config = self.search([
            ('key', '=', key),
            ('active', '=', True),
            ('environment', '=', self._get_current_environment())
        ], limit=1)
        
        if not config:
            return default
        
        value = config.value
        
        # Type conversion
        if config_type == 'integer':
            try:
                return int(value)
            except (ValueError, TypeError):
                return default
        elif config_type == 'float':
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        elif config_type == 'boolean':
            return value.lower() in ('true', '1', 'yes', 'on')
        elif config_type == 'json':
            try:
                import json
                return json.loads(value)
            except (ValueError, TypeError):
                return default
        
        return value
    
    def _get_current_environment(self):
        """Get current environment from system"""
        return os.environ.get('ODOO_ENVIRONMENT', 'production')
    
    @api.model
    def initialize_default_configs(self):
        """Initialize default configuration values"""
        default_configs = [
            {
                'key': 'excel.max_records_per_report',
                'value': '10000',
                'description': 'Maximum number of records per report',
                'config_type': 'integer'
            },
            {
                'key': 'excel.max_execution_time',
                'value': '300',
                'description': 'Maximum execution time in seconds',
                'config_type': 'integer'
            },
            {
                'key': 'excel.cache_enabled',
                'value': 'true',
                'description': 'Enable caching for better performance',
                'config_type': 'boolean'
            },
            {
                'key': 'excel.temp_directory',
                'value': '/tmp/odoo_excel_reports',
                'description': 'Temporary directory for Excel processing',
                'config_type': 'string'
            },
            {
                'key': 'excel.allowed_file_formats',
                'value': '["xlsx", "xlsm"]',
                'description': 'Allowed Excel file formats',
                'config_type': 'json'
            },
            {
                'key': 'excel.max_file_size_mb',
                'value': '50',
                'description': 'Maximum file size in MB',
                'config_type': 'integer'
            },
        ]
        
        for config_data in default_configs:
            existing = self.search([('key', '=', config_data['key'])])
            if not existing:
                self.create(config_data)

# Usage example in services
class ConfigurableExcelService:
    """Excel service with configuration management"""
    
    def __init__(self, env):
        self.env = env
        self.config = env['report.excel.config']
    
    def get_max_records(self):
        """Get maximum records limit from configuration"""
        return self.config.get_config_value(
            'excel.max_records_per_report', 
            default=10000, 
            config_type='integer'
        )
    
    def get_max_execution_time(self):
        """Get maximum execution time from configuration"""
        return self.config.get_config_value(
            'excel.max_execution_time',
            default=300,
            config_type='integer'
        )
    
    def is_cache_enabled(self):
        """Check if caching is enabled"""
        return self.config.get_config_value(
            'excel.cache_enabled',
            default=True,
            config_type='boolean'
        )