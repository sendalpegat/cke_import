from . import test_excel_generator
from . import test_formula_security
from . import test_performance
from . import test_integration
from . import test_api

# Test suite configuration
TEST_MODULES = [
    'test_excel_generator',
    'test_formula_security', 
    'test_performance',
    'test_integration',
    'test_api',
]

def run_all_tests():
    """Run all test modules"""
    import unittest
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for module_name in TEST_MODULES:
        module = __import__(f'tests.{module_name}', fromlist=[module_name])
        suite.addTests(loader.loadTestsFromModule(module))
    
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)