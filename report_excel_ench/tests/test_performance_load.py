# tests/test_performance_load.py
import time
import threading
from odoo.tests.common import TransactionCase

class TestPerformanceLoad(TransactionCase):
    """Load testing for performance validation"""
    
    def setUp(self):
        super().setUp()
        # Create large dataset for testing
        self.create_test_data()
    
    def create_test_data(self):
        """Create test data for performance testing"""
        # Create 1000 test partners
        partners_data = [
            {
                'name': f'Performance Test Partner {i}',
                'email': f'perf_test_{i}@example.com',
                'phone': f'+1-555-{i:04d}',
                'street': f'{i} Test Street',
                'city': f'Test City {i % 10}',
                'zip': f'{i:05d}',
            }
            for i in range(1000)
        ]
        
        self.test_partners = self.env['res.partner'].create(partners_data)
        
        # Create report configuration
        self.performance_report = self.env['report.excel'].create({
            'name': 'Performance Test Report',
            'root_model_id': self.env.ref('base.model_res_partner').id,
            'sheet_reference': 'Sheet1',
            'max_records': 1000
        })
    
    def test_large_dataset_performance(self):
        """Test performance with large dataset"""
        start_time = time.time()
        
        # Generate report with large dataset
        parameters = {}
        result = self.performance_report.generate_excel_report(
            self.performance_report.id,
            parameters
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert reasonable execution time (adjust threshold as needed)
        self.assertLess(execution_time, 30.0, 
                       "Report generation took too long")
        
        # Assert successful result
        self.assertIn('type', result)
    
    def test_concurrent_report_generation(self):
        """Test concurrent report generation"""
        results = []
        errors = []
        
        def generate_report():
            try:
                result = self.performance_report.generate_excel_report(
                    self.performance_report.id,
                    {}
                )
                results.append(result)
            except Exception as e:
                errors.append(str(e))
        
        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=generate_report)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join(timeout=60)  # 60 second timeout
        
        # Check results
        self.assertEqual(len(errors), 0, f"Errors occurred: {errors}")
        self.assertEqual(len(results), 5, "Not all reports generated")
    
    def test_memory_usage_large_report(self):
        """Test memory usage with large report"""
        from ..utils.memory_manager import MemoryManager
        
        initial_memory = MemoryManager.get_memory_usage()
        
        # Generate report
        with MemoryManager.memory_monitor("large_report_test"):
            result = self.performance_report.generate_excel_report(
                self.performance_report.id,
                {}
            )
        
        final_memory = MemoryManager.get_memory_usage()
        memory_increase = final_memory - initial_memory
        
        # Assert memory increase is reasonable (adjust threshold as needed)
        self.assertLess(memory_increase, 500,  # 500MB threshold
                       f"Memory increase too high: {memory_increase:.2f} MB")