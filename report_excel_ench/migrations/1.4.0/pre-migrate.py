# migrations/1.4.0/pre-migrate.py
import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def migrate(cr, version):
    """Migration script for version 1.4.0"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    _logger.info("Starting migration to version 1.4.0")
    
    # Step 1: Update existing reports
    _update_existing_reports(env)
    
    # Step 2: Initialize new configuration
    _initialize_configurations(env)
    
    # Step 3: Update security rules
    _update_security_rules(env)
    
    # Step 4: Clean up old data
    _cleanup_old_data(env)
    
    _logger.info("Migration to version 1.4.0 completed successfully")

def _update_existing_reports(env):
    """Update existing reports with new fields"""
    _logger.info("Updating existing reports...")
    
    reports = env['report.excel'].search([])
    for report in reports:
        # Set default values for new fields
        if not report.max_records:
            report.max_records = 10000
        
        if not report.timeout_seconds:
            report.timeout_seconds = 300
        
        # Enable caching by default
        report.cache_enabled = True
    
    _logger.info(f"Updated {len(reports)} reports")

def _initialize_configurations(env):
    """Initialize default configurations"""
    _logger.info("Initializing configurations...")
    
    try:
        config_model = env['report.excel.config']
        config_model.initialize_default_configs()
        _logger.info("Configurations initialized successfully")
    except Exception as e:
        _logger.error(f"Failed to initialize configurations: {e}")

def _update_security_rules(env):
    """Update security rules"""
    _logger.info("Updating security rules...")
    
    # Add any security rule updates here
    pass

def _cleanup_old_data(env):
    """Clean up old/unused data"""
    _logger.info("Cleaning up old data...")
    
    # Remove old temporary files
    try:
        import os
        import tempfile
        temp_dir = tempfile.gettempdir()
        for filename in os.listdir(temp_dir):
            if filename.startswith('excel_report_') and filename.endswith('.tmp'):
                try:
                    os.remove(os.path.join(temp_dir, filename))
                except OSError:
                    pass
        
        _logger.info("Temporary files cleaned up")
    except Exception as e:
        _logger.warning(f"Failed to clean up temporary files: {e}")