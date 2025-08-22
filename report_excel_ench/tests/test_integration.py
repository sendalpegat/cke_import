# tests/test_integration.py
class TestIntegration(TransactionCase):
    """Integration tests for the complete flow"""
    
    def setUp(self):
        super().setUp()
        # Create comprehensive test setup
        self.report = self.env['report.excel'].create({
            'name': 'Integration Test Report',
            'root_model_id': self.env.ref('base.model_res_partner').id,
            'sheet_reference': 'Sheet1'
        })
        
        # Add parameters
        self.param = self.env['report.excel.param'].create({
            'report_excel_id': self.report.id,
            'name': 'Partner Type',
            'code': 'partner_type',
            'type_param': 'char'
        })
        
        # Add section
        self.section = self.env['report.excel.section'].create({
            'report_excel_id': self.report.id,
            'name': 'Partner Data',
            'section_start': 'A1',
            'section_end': 'C10',
            'root_model_id': self.env.ref('base.model_res_partner').id
        })
        
        # Add field
        self.field = self.env['report.excel.fields'].create({
            'report_excel_section_id': self.section.id,
            'cell': 'A1',
            'model_field_selector': 'name'
        })
    
    def test_complete_report_generation_flow(self):
        """Test complete report generation flow"""
        parameters = {
            'partner_type': 'customer'
        }
        
        # Test report generation
        result = self.report.generate_excel_report(
            self.report.id,
            parameters
        )
        
        self.assertIn('type', result)
        self.assertEqual(result['type'], 'ir.actions.act_url')
        self.assertIn('url', result)
    
    @patch('odoo.addons.report_excel.services.excel_generator.ExcelGeneratorService')
    def test_error_handling_in_flow(self, mock_service):
        """Test error handling in complete flow"""
        # Mock service to raise exception
        mock_service.return_value.generate_report.side_effect = Exception("Test error")
        
        with self.assertRaises(UserError):
            self.report.generate_excel_report(self.report.id, {})