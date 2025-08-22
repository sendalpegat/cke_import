# migrations/1.4.0/post-migrate.py
def migrate(cr, version):
    """Post-migration script"""
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    _logger.info("Starting post-migration tasks")
    
    # Rebuild caches
    _rebuild_caches(env)
    
    # Update database indexes
    _update_indexes(cr)
    
    # Validate configurations
    _validate_configurations(env)
    
    _logger.info("Post-migration tasks completed")

def _rebuild_caches(env):
    """Rebuild application caches"""
    _logger.info("Rebuilding caches...")
    
    try:
        from ..services.cache_service import report_cache
        report_cache.invalidate()
        _logger.info("Caches rebuilt successfully")
    except Exception as e:
        _logger.error(f"Failed to rebuild caches: {e}")

def _update_indexes(cr):
    """Update database indexes for better performance"""
    _logger.info("Updating database indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_report_excel_active ON report_excel(active)",
        "CREATE INDEX IF NOT EXISTS idx_report_excel_root_model ON report_excel(root_model_id)",
        "CREATE INDEX IF NOT EXISTS idx_report_excel_section_report ON report_excel_section(report_excel_id)",
    ]
    
    for index_sql in indexes:
        try:
            cr.execute(index_sql)
            _logger.info(f"Created index: {index_sql}")
        except Exception as e:
            _logger.warning(f"Failed to create index: {e}")

def _validate_configurations(env):
    """Validate system configurations"""
    _logger.info("Validating configurations...")
    
    try:
        config_model = env['report.excel.config']
        
        # Check required configurations
        required_configs = [
            'excel.max_records_per_report',
            'excel.max_execution_time',
            'excel.cache_enabled'
        ]
        
        for config_key in required_configs:
            if not config_model.search([('key', '=', config_key)]):
                _logger.warning(f"Missing required configuration: {config_key}")
        
        _logger.info("Configuration validation completed")
    except Exception as e:
        _logger.error(f"Configuration validation failed: {e}")