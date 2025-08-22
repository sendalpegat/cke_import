# docs/technical_documentation.py
"""
Technical Documentation for Report Excel Module

This module provides comprehensive Excel reporting capabilities for Odoo 14.0
with enhanced security, performance, and maintainability features.

Architecture Overview:
=====================

1. Services Layer:
   - ExcelGeneratorService: Core report generation logic
   - TemplateProcessorService: Excel template handling
   - DataProcessorService: Data extraction and processing
   - FormulaEvaluatorService: Safe formula evaluation
   - CacheService: Performance caching

2. Security Layer:
   - SecureFileHandler: File operation security
   - SecureFormulaValidator: Formula security validation
   - ReportAccessControl: Access control utilities

3. Performance Layer:
   - QueryOptimizer: Database query optimization
   - MemoryManager: Memory usage monitoring
   - StreamingDataProcessor: Large dataset handling

4. API Layer:
   - RESTful API endpoints for external integration
   - Comprehensive error handling
   - Parameter validation

Usage Examples:
==============

Basic Report Generation:
```python
# Create report configuration
report = env['report.excel'].create({
    'name': 'Sales Report',
    'root_model_id': env.ref('sale.model_sale_order').id,
    'sheet_reference': 'Sheet1'
})

# Generate report
result = report.generate_excel_report(report.id, {
    'date_from': '2023-01-01',
    'date_to': '2023-12-31'
})