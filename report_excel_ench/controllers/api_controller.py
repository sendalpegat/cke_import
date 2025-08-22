# controllers/api_controller.py
import json
import logging
from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)

class ReportExcelAPIController(http.Controller):
    """RESTful API for Excel Report Generation"""
    
    @http.route('/api/v1/reports/excel', type='json', auth='user', 
                methods=['GET'], csrf=False)
    def list_reports(self, **kwargs):
        """List available Excel reports"""
        try:
            domain = [('active', '=', True)]
            
            # Apply filters
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs['name']))
            
            reports = request.env['report.excel'].search(domain)
            
            result = []
            for report in reports:
                result.append({
                    'id': report.id,
                    'name': report.name,
                    'description': report.description,
                    'root_model': report.root_model_id.model,
                    'parameters': self._get_report_parameters(report),
                    'created_date': report.create_date.isoformat() if report.create_date else None,
                })
            
            return {
                'success': True,
                'data': result,
                'count': len(result)
            }
            
        except Exception as e:
            _logger.error("API error in list_reports: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'code': 500
            }
    
    @http.route('/api/v1/reports/excel/<int:report_id>', type='json', 
                auth='user', methods=['GET'], csrf=False)
    def get_report(self, report_id, **kwargs):
        """Get specific report details"""
        try:
            report = request.env['report.excel'].browse(report_id)
            
            if not report.exists():
                return {
                    'success': False,
                    'error': 'Report not found',
                    'code': 404
                }
            
            return {
                'success': True,
                'data': {
                    'id': report.id,
                    'name': report.name,
                    'description': report.description,
                    'root_model': report.root_model_id.model,
                    'sheet_reference': report.sheet_reference,
                    'parameters': self._get_report_parameters(report),
                    'sections': self._get_report_sections(report),
                    'created_date': report.create_date.isoformat() if report.create_date else None,
                    'updated_date': report.write_date.isoformat() if report.write_date else None,
                }
            }
            
        except AccessError:
            return {
                'success': False,
                'error': 'Access denied',
                'code': 403
            }
        except Exception as e:
            _logger.error("API error in get_report: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'code': 500
            }
    
    @http.route('/api/v1/reports/excel/<int:report_id>/generate', 
                type='json', auth='user', methods=['POST'], csrf=False)
    def generate_report(self, report_id, **kwargs):
        """Generate Excel report"""
        try:
            report = request.env['report.excel'].browse(report_id)
            
            if not report.exists():
                return {
                    'success': False,
                    'error': 'Report not found',
                    'code': 404
                }
            
            # Validate parameters
            parameters = kwargs.get('parameters', {})
            validation_result = self._validate_parameters(report, parameters)
            if not validation_result['valid']:
                return {
                    'success': False,
                    'error': validation_result['message'],
                    'code': 400
                }
            
            # Generate report
            result = report.generate_excel_report(report_id, parameters)
            
            # Extract download URL from result
            if result.get('type') == 'ir.actions.act_url':
                return {
                    'success': True,
                    'data': {
                        'download_url': result['url'],
                        'report_name': report.name,
                        'generated_at': http.request.env.cr.now().isoformat()
                    }
                }
            else:
                return {
                    'success': False,
                    'error': 'Report generation failed',
                    'code': 500
                }
                
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e),
                'code': 400
            }
        except AccessError:
            return {
                'success': False,
                'error': 'Access denied',
                'code': 403
            }
        except Exception as e:
            _logger.error("API error in generate_report: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'code': 500
            }
    
    @http.route('/api/v1/reports/excel/<int:report_id>/validate', 
                type='json', auth='user', methods=['POST'], csrf=False)
    def validate_parameters(self, report_id, **kwargs):
        """Validate report parameters"""
        try:
            report = request.env['report.excel'].browse(report_id)
            
            if not report.exists():
                return {
                    'success': False,
                    'error': 'Report not found',
                    'code': 404
                }
            
            parameters = kwargs.get('parameters', {})
            validation_result = self._validate_parameters(report, parameters)
            
            return {
                'success': True,
                'data': validation_result
            }
            
        except Exception as e:
            _logger.error("API error in validate_parameters: %s", str(e))
            return {
                'success': False,
                'error': str(e),
                'code': 500
            }
    
    def _get_report_parameters(self, report):
        """Get report parameters configuration"""
        parameters = []
        for param in report.report_excel_param_ids:
            param_info = {
                'code': param.code,
                'name': param.name,
                'type': param.type_param,
                'required': param.param_required,
            }
            
            if param.param_ir_model_id:
                param_info['model'] = param.param_ir_model_id.model
                param_info['model_name'] = param.param_ir_model_id.name
            
            parameters.append(param_info)
        
        return parameters
    
    def _get_report_sections(self, report):
        """Get report sections configuration"""
        sections = []
        for section in report.report_excel_section_ids:
            sections.append({
                'id': section.id,
                'name': section.name,
                'section_start': section.section_start,
                'section_end': section.section_end,
                'domain': section.domain,
                'fields_count': len(section.report_excel_fields_ids),
            })
        
        return sections
    
    def _validate_parameters(self, report, parameters):
        """Validate report parameters"""
        errors = []
        
        for param in report.report_excel_param_ids:
            if param.param_required and param.code not in parameters:
                errors.append(f"Required parameter '{param.code}' is missing")
                continue
            
            if param.code in parameters:
                value = parameters[param.code]
                
                # Type validation
                if param.type_param == 'integer' and not isinstance(value, int):
                    errors.append(f"Parameter '{param.code}' must be an integer")
                elif param.type_param == 'float' and not isinstance(value, (int, float)):
                    errors.append(f"Parameter '{param.code}' must be a number")
                elif param.type_param == 'boolean' and not isinstance(value, bool):
                    errors.append(f"Parameter '{param.code}' must be a boolean")
                elif param.type_param in ['date', 'datetime'] and not isinstance(value, str):
                    errors.append(f"Parameter '{param.code}' must be a date string")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'message': '; '.join(errors) if errors else 'All parameters are valid'
        }

# OpenAPI Documentation
class ReportExcelAPIDocumentation:
    """OpenAPI/Swagger documentation for Report Excel API"""
    
    openapi_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Report Excel API",
            "version": "1.0.0",
            "description": "API for generating Excel reports in Odoo",
        },
        "servers": [
            {
                "url": "/api/v1",
                "description": "Report Excel API v1"
            }
        ],
        "paths": {
            "/reports/excel": {
                "get": {
                    "summary": "List all available Excel reports",
                    "parameters": [
                        {
                            "name": "name",
                            "in": "query",
                            "description": "Filter by report name",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "List of reports",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/ReportSummary"}
                                            },
                                            "count": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/reports/excel/{report_id}": {
                "get": {
                    "summary": "Get specific report details",
                    "parameters": [
                        {
                            "name": "report_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Report details",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {"$ref": "#/components/schemas/ReportDetail"}
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Report not found"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "ReportSummary": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "root_model": {"type": "string"},
                        "parameters": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Parameter"}
                        }
                    }
                },
                "Parameter": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "required": {"type": "boolean"}
                    }
                }
            }
        }
    }