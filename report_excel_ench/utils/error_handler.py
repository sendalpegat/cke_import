import logging
import traceback
from functools import wraps
from odoo import _

_logger = logging.getLogger(__name__)

def handle_excel_errors(func):
    """Decorator for handling Excel-related errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TemplateNotFoundError as e:
            _logger.error("Template not found: %s", str(e))
            raise UserError(_("Template file not found. Please check template configuration."))
        except InvalidTemplateFormatError as e:
            _logger.error("Invalid template format: %s", str(e))
            raise UserError(_("Template format is not supported. Please use .xlsx or .xlsm format."))
        except FormulaSecurityError as e:
            _logger.error("Formula security violation: %s", str(e))
            raise UserError(_("Formula contains unsafe operations. Please contact administrator."))
        except Exception as e:
            _logger.error("Unexpected error in %s: %s\n%s", 
                         func.__name__, str(e), traceback.format_exc())
            raise UserError(_("An unexpected error occurred. Please contact administrator."))
    return wrapper

def log_performance(func):
    """Decorator for logging performance metrics"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            _logger.info("Method %s.%s executed successfully in %.2f seconds", 
                        args[0].__class__.__name__ if args else 'Unknown',
                        func.__name__, 
                        execution_time)
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            _logger.error("Method %s.%s failed after %.2f seconds: %s", 
                         args[0].__class__.__name__ if args else 'Unknown',
                         func.__name__, 
                         execution_time, 
                         str(e))
            raise
    return wrapper