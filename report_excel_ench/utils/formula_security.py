# utils/formula_security.py
import ast
import re
from odoo import _
from odoo.exceptions import ValidationError

class SecureFormulaValidator:
    """Advanced formula security validation"""
    
    # Dangerous patterns to block
    DANGEROUS_PATTERNS = [
        r'__\w+__',  # Dunder methods
        r'\.mro\(',  # Method resolution order
        r'\.bases',  # Class bases
        r'\.globals',  # Global namespace
        r'\.locals',  # Local namespace
        r'eval\s*\(',  # eval function
        r'exec\s*\(',  # exec function
        r'compile\s*\(',  # compile function
        r'open\s*\(',  # file operations
        r'import\s+',  # import statements
        r'from\s+\w+\s+import',  # from import
        r'\.system\s*\(',  # system calls
        r'\.popen\s*\(',  # process operations
        r'\.subprocess',  # subprocess module
    ]
    
    # Allowed built-in functions
    SAFE_BUILTINS = {
        'abs', 'all', 'any', 'bool', 'dict', 'float', 'int', 'len', 
        'list', 'max', 'min', 'round', 'str', 'sum', 'tuple', 'type'
    }
    
    @classmethod
    def validate_formula(cls, formula):
        """Comprehensive formula validation"""
        if not formula or not formula.strip():
            return True
        
        # Check for dangerous patterns
        cls._check_dangerous_patterns(formula)
        
        # Parse and analyze AST
        try:
            tree = ast.parse(formula, mode='exec')
            cls._analyze_ast(tree)
        except SyntaxError as e:
            raise ValidationError(_("Formula syntax error: %s") % str(e))
        
        return True
    
    @classmethod
    def _check_dangerous_patterns(cls, formula):
        """Check for dangerous regex patterns"""
        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, formula, re.IGNORECASE):
                raise ValidationError(
                    _("Formula contains forbidden pattern: %s") % pattern
                )
    
    @classmethod
    def _analyze_ast(cls, node):
        """Analyze AST for security violations"""
        for child in ast.walk(node):
            cls._check_node_security(child)
    
    @classmethod
    def _check_node_security(cls, node):
        """Check individual AST node for security"""
        # Block dangerous node types
        forbidden_nodes = {
            ast.Import: "Import statements not allowed",
            ast.ImportFrom: "Import statements not allowed", 
            ast.Exec: "Exec statements not allowed",
            ast.Global: "Global statements not allowed",
            ast.Nonlocal: "Nonlocal statements not allowed",
        }
        
        node_type = type(node)
        if node_type in forbidden_nodes:
            raise ValidationError(
                _("Forbidden operation: %s") % forbidden_nodes[node_type]
            )
        
        # Check function calls
        if isinstance(node, ast.Call):
            cls._check_function_call(node)
        
        # Check attribute access
        if isinstance(node, ast.Attribute):
            cls._check_attribute_access(node)
    
    @classmethod
    def _check_function_call(cls, node):
        """Check function call security"""
        if hasattr(node.func, 'id'):
            func_name = node.func.id
            if func_name not in cls.SAFE_BUILTINS:
                # Check if it's an allowed custom function
                allowed_custom = [
                    'datetime', 'date', 'cell', 'param'
                ]
                if func_name not in allowed_custom:
                    raise ValidationError(
                        _("Function '%s' not allowed in formulas") % func_name
                    )
    
    @classmethod
    def _check_attribute_access(cls, node):
        """Check attribute access security"""
        dangerous_attrs = [
            '__class__', '__bases__', '__mro__', '__globals__',
            '__locals__', '__dict__', '__code__', '__closure__'
        ]
        
        if hasattr(node, 'attr') and node.attr in dangerous_attrs:
            raise ValidationError(
                _("Attribute '%s' access not allowed") % node.attr
            )