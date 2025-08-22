from odoo.exceptions import UserError, ValidationError

class ExcelReportError(UserError):
    """Base exception for Excel report errors"""
    pass

class TemplateError(ExcelReportError):
    """Template-related errors"""
    pass

class TemplateNotFoundError(TemplateError):
    """Template file not found"""
    pass

class InvalidTemplateFormatError(TemplateError):
    """Invalid template format"""
    pass

class TemplateCorruptedError(TemplateError):
    """Template file is corrupted"""
    pass

class DataProcessingError(ExcelReportError):
    """Data processing errors"""
    pass

class FormulaError(ExcelReportError):
    """Formula evaluation errors"""
    pass

class InvalidFormulaError(FormulaError):
    """Invalid formula syntax"""
    pass

class FormulaSecurityError(FormulaError):
    """Formula contains unsafe operations"""
    pass

class ParameterError(ExcelReportError):
    """Parameter-related errors"""
    pass

class MissingParameterError(ParameterError):
    """Required parameter is missing"""
    pass

class InvalidParameterError(ParameterError):
    """Parameter value is invalid"""
    pass