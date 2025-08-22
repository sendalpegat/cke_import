class ExcelConfig:
    """Excel module configuration constants"""
    
    # File format support
    SUPPORTED_FORMATS = ('.xlsx', '.xlsm')
    SUPPORTED_MIMETYPES = [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/vnd.ms-excel.sheet.macroEnabled.12'
    ]
    
    # Excel limits
    MAX_COLUMN_INDEX = 18278
    MAX_ROW_INDEX = 1048576
    MAX_SHEET_NAME_LENGTH = 31
    
    # Performance limits
    DEFAULT_BATCH_SIZE = 1000
    MAX_RECORDS_PER_REPORT = 100000
    MAX_FORMULA_LENGTH = 1000
    
    # File size limits (in bytes)
    MAX_TEMPLATE_SIZE = 50 * 1024 * 1024  # 50MB
    MAX_OUTPUT_SIZE = 100 * 1024 * 1024   # 100MB
    
    # Cache settings
    TEMPLATE_CACHE_SIZE = 100
    DATA_CACHE_TTL = 3600  # 1 hour
    
    # Security settings
    ALLOWED_FORMULA_FUNCTIONS = [
        'sum', 'avg', 'count', 'min', 'max',
        'len', 'str', 'int', 'float', 'bool',
        'datetime', 'date'
    ]
    
    # Default values
    DEFAULT_SHEET_NAME = 'Sheet1'
    DEFAULT_CELL_FORMAT = 'General'
    
    @classmethod
    def get_temp_directory(cls):
        """Get temporary directory for Excel processing"""
        import tempfile
        return tempfile.gettempdir()
    
    @classmethod
    def validate_file_size(cls, file_size, file_type='output'):
        """Validate file size against limits"""
        if file_type == 'template':
            max_size = cls.MAX_TEMPLATE_SIZE
        else:
            max_size = cls.MAX_OUTPUT_SIZE
        
        if file_size > max_size:
            from odoo.exceptions import ValidationError
            from odoo import _
            raise ValidationError(
                _("File size (%s MB) exceeds limit (%s MB)") % (
                    round(file_size / 1024 / 1024, 2),
                    round(max_size / 1024 / 1024, 2)
                )
            )