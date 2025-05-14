# Swap Name and Default Code Module

## Overview
This module swaps the positions of the 'name' and 'default_code' fields in the 'product.product' and 'product.template' models.

## Installation
1. Place the module folder in the `addons` directory of your Odoo installation.
2. Update the app list in Odoo.
3. Install the module from the Apps menu.

## Features
- Swaps the positions of the 'name' and 'default_code' fields in product forms.
- Ensures form rendering and data consistency.
- Adheres to Odoo's best practices and coding standards.

## Testing
- Test the creation, modification, and display of product records to verify the field order is correctly swapped in both the product template and product forms.

## Maintenance
- The module is designed to be easily maintainable and extensible in the future.
- It avoids unnecessary overhead or resource consumption.
- It is compatible with Odoo 14.0 and should not introduce any regressions or unexpected behavior.
