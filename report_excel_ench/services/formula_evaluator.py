import ast
from odoo import _
from odoo.exceptions import ValidationError

class FormulaEvaluatorService:
    """Safe formula evaluation service"""
    
    ALLOWED_FUNCTIONS = {
        # Math functions
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'len': len,
        
        # Date/time
        'datetime': __import__('datetime'),
        'date': __import__('datetime').date,
        
        # String functions
        'str': str,
        'float': float,
        'int': int,
        'bool': bool,
    }
    
    ALLOWED_MODULES = {
        'datetime', 'math'
    }
    
    def __init__(self, env):
        self.env = env
    
    def evaluate_formula(self, formula, context=None):
        """
        Safely evaluate formula
        
        Args:
            formula (str): Formula to evaluate
            context (dict): Evaluation context
            
        Returns:
            any: Formula result
        """
        if not formula or not formula.strip():
            return None
        
        context = context or {}
        
        # Parse and validate formula
        self._validate_formula_syntax(formula)
        
        # Prepare safe execution environment
        safe_globals = self.ALLOWED_FUNCTIONS.copy()
        safe_locals = context.copy()
        
        try:
            # Execute formula
            exec(formula, safe_globals, safe_locals)
            return safe_locals.get('result')
            
        except Exception as e:
            _logger.error("Formula evaluation failed: %s", str(e))
            raise ValidationError(_("Formula error: %s") % str(e))
    
    def _validate_formula_syntax(self, formula):
        """Validate formula syntax and security"""
        try:
            tree = ast.parse(formula)
            self._check_ast_security(tree)
        except SyntaxError as e:
            raise ValidationError(_("Formula syntax error: %s") % str(e))
    
    def _check_ast_security(self, node):
        """Check AST for security violations"""
        forbidden_nodes = {
            ast.Import, ast.ImportFrom, ast.Exec, ast.Eval,
            ast.Call  # We'll check calls separately
        }
        
        for child in ast.walk(node):
            if type(child) in forbidden_nodes:
                if isinstance(child, ast.Call):
                    self._check_function_call(child)
                else:
                    raise ValidationError(_("Forbidden operation in formula"))
    
    def _check_function_call(self, call_node):
        """Check if function call is allowed"""
        if hasattr(call_node.func, 'id'):
            func_name = call_node.func.id
            if func_name not in self.ALLOWED_FUNCTIONS:
                raise ValidationError(
                    _("Function '%s' not allowed in formulas") % func_name
                )