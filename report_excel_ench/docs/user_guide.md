This guide covers how to use the Excel Report Designer module
to create and generate custom Excel reports in Odoo.
"""

getting_started = """
Getting Started
===============

1. Access the Report Designer:
   - Go to Settings > Technical > Reports > Report Excel
   - Or use the search bar to find "Report Excel"

2. Create Your First Report:
   - Click "Create" button
   - Fill in basic information:
     * Name: Give your report a descriptive name
     * Root Model: Select the main data source
     * Template: Upload an Excel template (optional)
     * Sheet Reference: Specify sheet name (default: Sheet1)

3. Add Parameters (Optional):
   - Parameters allow users to filter data when generating reports
   - Click "Add a line" in Report Parameters section
   - Configure parameter type and requirements

4. Configure Sections:
   - Sections define where data appears in your Excel file
   - Set section start and end cells (e.g., A1:C10)
   - Add fields to map data to specific cells

5. Generate Report:
   - Save your configuration
   - Use "Create a Menu" or "Add to Print menu" for easy access
   - Generate reports from the source records
"""

advanced_features = """
Advanced Features
================

1. Formula Fields:
   - Use Python expressions for calculated fields
   - Access other cell values: cell(A1)
   - Use parameters: param(parameter_code)
   - Available functions: sum, avg, count, min, max, datetime

Example Formula:
```python
# Calculate total with tax
base_amount = cell(B7)
tax_rate = param(tax_rate) / 100
result = base_amount * (1 + tax_rate)
```

2. Aggregation Functions:
   - SUM: Total of numeric values
   - AVG: Average of numeric values
   - COUNT: Count of records
   - MIN/MAX: Minimum/Maximum values

3. Grouping:
   - Group data by field values
   - Combine with aggregation for summary reports
   - Use having clauses for filtered aggregation

4. Hierarchical Sections:
   - Create parent-child relationships
   - Build master-detail reports
   - Support multiple nesting levels

5. Image Fields:
   - Display images in Excel cells
   - Configure image position and size
   - Support common image formats
"""

best_practices = """
Best Practices
==============

1. Template Design:
   - Use Excel templates for complex formatting
   - Keep templates simple and maintainable
   - Test templates with sample data

2. Performance Optimization:
   - Limit record count for large datasets
   - Use appropriate filters and domains
   - Avoid complex formulas in loops

3. Security Considerations:
   - Validate all user inputs
   - Use safe formula expressions only
   - Restrict access to sensitive data

4. Error Handling:
   - Test reports with various data conditions
   - Handle empty datasets gracefully
   - Provide meaningful error messages

5. Maintenance:
   - Document report purposes and usage
   - Keep templates in version control
   - Regular testing after system updates
"""

troubleshooting = """
Troubleshooting
==============

Common Issues and Solutions:

1. "Template not found" error:
   - Verify template file is uploaded
   - Check file format (.xlsx or .xlsm)
   - Ensure file is not corrupted

2. "Invalid cell coordinates" error:
   - Use proper Excel cell notation (A1, B2, etc.)
   - Ensure start cell comes before end cell
   - Check section boundaries don't overlap

3. "Formula error" messages:
   - Review formula syntax
   - Use only allowed functions
   - Check parameter references

4. Slow report generation:
   - Reduce number of records
   - Optimize filters and domains
   - Consider using data streaming

5. Memory errors:
   - Reduce report complexity
   - Process data in smaller batches
   - Contact administrator for memory limits

6. Access denied errors:
   - Check user permissions on source models
   - Verify report access rights
   - Contact administrator for access issues
"""