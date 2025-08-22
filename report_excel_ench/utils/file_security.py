# utils/file_security.py
import os
import mimetypes
from pathlib import Path
from odoo import _
from odoo.exceptions import ValidationError
from ..config.excel_config import ExcelConfig

class SecureFileHandler:
    """Secure file handling utilities"""
    
    @staticmethod
    def validate_file_path(file_path):
        """Validate file path for security"""
        if not file_path:
            raise ValidationError(_("File path is required"))
        
        # Resolve path to prevent directory traversal
        resolved_path = Path(file_path).resolve()
        
        # Check if path is within allowed directories
        allowed_dirs = [
            Path(ExcelConfig.get_temp_directory()).resolve(),
            Path('/tmp').resolve(),
        ]
        
        if not any(str(resolved_path).startswith(str(allowed_dir)) 
                  for allowed_dir in allowed_dirs):
            raise ValidationError(_("File path not allowed"))
        
        return str(resolved_path)
    
    @staticmethod
    def validate_file_type(file_path, file_content=None):
        """Validate file type and content"""
        # Check file extension
        file_ext = Path(file_path).suffix.lower()
        if file_ext not in ExcelConfig.SUPPORTED_FORMATS:
            raise ValidationError(
                _("Unsupported file format: %s") % file_ext
            )
        
        # Check MIME type if content is provided
        if file_content:
            detected_type = mimetypes.guess_type(file_path)[0]
            if detected_type not in ExcelConfig.SUPPORTED_MIMETYPES:
                raise ValidationError(
                    _("File content doesn't match expected format")
                )
    
    @staticmethod
    def sanitize_filename(filename):
        """Sanitize filename for security"""
        if not filename:
            return "report.xlsx"
        
        # Remove dangerous characters
        dangerous_chars = ['/', '\\', '..', '<', '>', ':', '"', '|', '?', '*']
        sanitized = filename
        
        for char in dangerous_chars:
            sanitized = sanitized.replace(char, '_')
        
        # Limit length
        if len(sanitized) > 255:
            name, ext = os.path.splitext(sanitized)
            sanitized = name[:250] + ext
        
        return sanitized
    
    @staticmethod
    def create_secure_temp_file(prefix="excel_report_", suffix=".xlsx"):
        """Create secure temporary file"""
        import tempfile
        import os
        
        temp_dir = ExcelConfig.get_temp_directory()
        os.makedirs(temp_dir, exist_ok=True)
        
        fd, temp_path = tempfile.mkstemp(
            prefix=prefix,
            suffix=suffix,
            dir=temp_dir
        )
        
        os.close(fd)  # Close file descriptor
        return temp_path

# utils/access_control.py
from odoo import api, models
from odoo.exceptions import AccessError

class ReportAccessControl:
    """Access control utilities for reports"""
    
    @staticmethod
    def check_model_access(env, model_name, operation='read'):
        """Check if user has access to model"""
        try:
            Model = env[model_name]
            Model.check_access_rights(operation)
            return True
        except AccessError:
            return False
    
    @staticmethod
    def check_record_access(env, model_name, record_ids, operation='read'):
        """Check if user has access to specific records"""
        try:
            Model = env[model_name]
            records = Model.browse(record_ids)
            records.check_access_rights(operation)
            records.check_access_rule(operation)
            return True
        except AccessError:
            return False
    
    @staticmethod
    def filter_accessible_records(env, model_name, record_ids):
        """Filter records that user can access"""
        Model = env[model_name]
        try:
            records = Model.browse(record_ids)
            records.check_access_rule('read')
            return records.ids
        except AccessError:
            # Try individual records
            accessible_ids = []
            for record_id in record_ids:
                try:
                    record = Model.browse(record_id)
                    record.check_access_rule('read')
                    accessible_ids.append(record_id)
                except AccessError:
                    continue
            return accessible_ids