# models/report_excel_enhanced.py
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from ..exceptions.excel_exceptions import *
from ..utils.error_handler import handle_excel_errors, log_performance
from ..services.excel_generator import ExcelGeneratorService

_logger = logging.getLogger(__name__)

class ReportExcelEnhanced(models.Model):
    _inherit = 'report.excel'
    
    # Add new fields for better control
    max_records = fields.Integer(
        string="Maximum Records",
        default=10000,
        help="Maximum number of records to process in this report"
    )
    
    timeout_seconds = fields.Integer(
        string="Timeout (seconds)",
        default=300,
        help="Maximum execution time for report generation"
    )
    
    cache_enabled = fields.Boolean(
        string="Enable Caching",
        default=True,
        help="Cache report data for better performance"
    )
    
    @api.model
    @handle_excel_errors
    @log_performance
    def generate_excel_report(self, report_id, parameters=None, context=None):
        """
        Enhanced report generation with better error handling
        
        Args:
            report_id (int): Report configuration ID
            parameters (dict): Report parameters
            context (dict): Additional context
            
        Returns:
            dict: File action for download
        """
        # Validate inputs
        self._validate_report_generation_input(report_id, parameters)
        
        # Get report configuration
        report = self.browse(report_id)
        if not report.exists():
            raise TemplateNotFoundError(_("Report configuration not found"))
        
        # Check permissions
        self._check_report_access(report)
        
        # Initialize services
        excel_generator = ExcelGeneratorService(self.env)
        
        # Prepare configuration
        config = self._prepare_report_config(report, parameters)
        
        # Generate report
        try:
            result = excel_generator.generate_report(config, parameters)
            return self._create_download_action(result, report.name)
        except Exception as e:
            self._log_generation_error(report, parameters, e)
            raise
    
    def _validate_report_generation_input(self, report_id, parameters):
        """Validate input for report generation"""
        if not report_id:
            raise ValidationError(_("Report ID is required"))
        
        if not isinstance(report_id, int) or report_id <= 0:
            raise ValidationError(_("Invalid report ID"))
        
        if parameters is not None and not isinstance(parameters, dict):
            raise ValidationError(_("Parameters must be a dictionary"))
    
    def _check_report_access(self, report):
        """Check if user has access to generate this report"""
        if not report.active:
            raise UserError(_("This report is archived and cannot be generated"))
        
        # Add additional permission checks here
        try:
            report.check_access_rights('read')
        except Exception:
            raise UserError(_("You don't have permission to access this report"))
    
    def _prepare_report_config(self, report, parameters):
        """Prepare report configuration for generation"""
        return {
            'id': report.id,
            'name': report.name,
            'root_model_id': report.root_model_id.id,
            'root_model_name': report.root_model_id.model,
            'template_id': report.template_name_id.id if report.template_name_id else None,
            'sheet_reference': report.sheet_reference,
            'sections': self._get_sections_config(report),
            'parameters_config': self._get_parameters_config(report),
            'domain': report._get_base_domain(),
            'max_records': report.max_records,
            'timeout_seconds': report.timeout_seconds,
        }
    
    def _get_sections_config(self, report):
        """Get sections configuration"""
        sections = []
        for section in report.report_excel_section_ids:
            sections.append({
                'id': section.id,
                'name': section.name,
                'section_start': section.section_start,
                'section_end': section.section_end,
                'domain': section.domain,
                'fields': self._get_section_fields_config(section)
            })
        return sections
    
    def _get_section_fields_config(self, section):
        """Get section fields configuration"""
        fields = []
        for field in section.report_excel_fields_ids:
            fields.append({
                'id': field.id,
                'cell': field.cell,
                'model_field_selector': field.model_field_selector,
                'formula': field.formulas if field.formula else None,
                'aggregate': field.aggregate,
                'group_by': field.group_by,
            })
        return fields
    
    def _get_parameters_config(self, report):
        """Get parameters configuration"""
        params = {}
        for param in report.report_excel_param_ids:
            params[param.code] = {
                'name': param.name,
                'type': param.type_param,
                'required': param.param_required,
                'model_id': param.param_ir_model_id.id if param.param_ir_model_id else None,
            }
        return params
    
    def _create_download_action(self, excel_content, report_name):
        """Create download action for generated report"""
        import base64
        from datetime import datetime
        
        # Create attachment
        filename = f"{report_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': base64.b64encode(excel_content),
            'res_model': 'report.excel',
            'res_id': 0,
            'type': 'binary',
        })
        
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
    
    def _log_generation_error(self, report, parameters, error):
        """Log report generation error"""
        _logger.error(
            "Report generation failed - Report: %s (ID: %s), Parameters: %s, Error: %s",
            report.name, report.id, parameters, str(error)
        )