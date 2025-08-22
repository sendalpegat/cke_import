# tests/test_formula_security.py
class TestFormulaSecurity(TransactionCase):
    """Test Formula Security"""
    
    def setUp(self):
        super().setUp()
        from ..utils.formula_security import SecureFormulaValidator
        self.validator = SecureFormulaValidator()
    
    def test_safe_formula(self):
        """Test safe formula validation"""
        safe_formula = """
result = sum([1, 2, 3, 4, 5])
"""
        # Should not raise exception
        self.validator.validate_formula(safe_formula)
    
    def test_dangerous_import(self):
        """Test dangerous import detection"""
        dangerous_formula = """
import os
result = os.system('rm -rf /')
"""
        with self.assertRaises(ValidationError):
            self.validator.validate_formula(dangerous_formula)
    
    def test_dangerous_eval(self):
        """Test dangerous eval detection"""
        dangerous_formula = """
result = eval('__import__("os").system("ls")')
"""
        with self.assertRaises(ValidationError):
            self.validator.validate_formula(dangerous_formula)
    
    def test_dangerous_attribute_access(self):
        """Test dangerous attribute access"""
        dangerous_formula = """
result = ().__class__.__bases__[0].__subclasses__()
"""
        with self.assertRaises(ValidationError):
            self.validator.validate_formula(dangerous_formula)