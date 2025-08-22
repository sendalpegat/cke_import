# tests/test_excel_generator.py
import unittest
from unittest.mock import patch, MagicMock
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError, ValidationError
from ..services.excel_generator import ExcelGeneratorService
from ..exceptions.excel_exceptions import *

class TestExcelGenerator(TransactionCase):
    """Test Excel Generator Service"""
    
    def setUp(self):
        super().setUp()
        self.excel_service = ExcelGeneratorService(self.env)
        
        # Create test data
        self.test_report = self.env['report.excel'].create({
            'name': 'Test Report',
            'root_model_id': self.env.ref('base.model_res_partner').id,
            'sheet_reference': 'Sheet1'
        })
        
        self.test_parameters = {
            'date_from': '2023-01-01',
            'date_to': '2023-12-31',
            'partner_ids': [1, 2, 3]
        }
    
    def test_generate_report_success(self):
        """Test successful report generation"""
        config = {
            'id': self.test_report.id,
            'name': 'Test Report',
            'root_model_name': 'res.partner',
            'template_id': None,
            'sections': [],
            'max_records': 1000
        }
        
        with patch.object(self.excel_service, '_create_excel_file') as mock_create:
            mock_create.return_value = b'fake_excel_content'
            
            result = self.excel_service.generate_report(config, self.test_parameters)
            
            self.assertEqual(result, b'fake_excel_content')
            mock_create.assert_called_once()
    
    def test_validate_configuration_missing_field(self):
        """Test configuration validation with missing field"""
        config = {
            'name': 'Test Report',
            # Missing root_model_id
            'sheet_reference': 'Sheet1'
        }
        
        with self.assertRaises(ValidationError):
            self.excel_service._validate_configuration(config)
    
    def test_validate_parameters_invalid_type(self):
        """Test parameter validation with invalid type"""
        invalid_parameters = "not_a_dict"
        
        with self.assertRaises(ValidationError):
            self.excel_service._validate_parameters(invalid_parameters)
    
    def test_generate_report_with_template_error(self):
        """Test report generation with template error"""
        config = {
            'id': self.test_report.id,
            'name': 'Test Report',
            'root_model_name': 'res.partner',
            'template_id': 999,  # Non-existent template
            'sections': [],
        }
        
        with self.assertRaises(TemplateNotFoundError):
            self.excel_service.generate_report(config, self.test_parameters)