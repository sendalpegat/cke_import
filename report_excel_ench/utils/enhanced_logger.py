# utils/enhanced_logger.py
import logging
import json
import time
from functools import wraps
from odoo import http

class ReportExcelLogger:
    """Enhanced logger for Excel reports"""
    
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Add custom formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - '
            '[%(user_id)s] - %(message)s'
        )
        
        # Add console handler if not exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def log_report_generation(self, report_id, user_id, parameters, 
                            execution_time, success=True, error=None):
        """Log report generation event"""
        log_data = {
            'event': 'report_generation',
            'report_id': report_id,
            'user_id': user_id,
            'parameters': parameters,
            'execution_time': execution_time,
            'success': success,
            'error': str(error) if error else None,
            'timestamp': time.time()
        }
        
        if success:
            self.logger.info("Report generated successfully: %s", 
                           json.dumps(log_data))
        else:
            self.logger.error("Report generation failed: %s", 
                            json.dumps(log_data))
    
    def log_performance_metric(self, metric_name, value, context=None):
        """Log performance metric"""
        log_data = {
            'event': 'performance_metric',
            'metric': metric_name,
            'value': value,
            'context': context or {},
            'timestamp': time.time()
        }
        
        self.logger.info("Performance metric: %s", json.dumps(log_data))
    
    def log_security_event(self, event_type, details, user_id=None):
        """Log security-related event"""
        log_data = {
            'event': 'security_event',
            'type': event_type,
            'details': details,
            'user_id': user_id,
            'timestamp': time.time()
        }
        
        self.logger.warning("Security event: %s", json.dumps(log_data))

# Decorator for automatic logging
def log_report_operation(operation_name):
    """Decorator to automatically log report operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = ReportExcelLogger(f"report_excel.{operation_name}")
            start_time = time.time()
            
            # Extract user ID if available
            user_id = None
            if hasattr(http.request, 'env') and http.request.env:
                user_id = http.request.env.uid
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.log_report_generation(
                    report_id=kwargs.get('report_id', 'unknown'),
                    user_id=user_id,
                    parameters=kwargs.get('parameters', {}),
                    execution_time=execution_time,
                    success=True
                )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                logger.log_report_generation(
                    report_id=kwargs.get('report_id', 'unknown'),
                    user_id=user_id,
                    parameters=kwargs.get('parameters', {}),
                    execution_time=execution_time,
                    success=False,
                    error=e
                )
                
                raise
        
        return wrapper
    return decorator