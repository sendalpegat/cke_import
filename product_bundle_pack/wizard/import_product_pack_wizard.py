# wizard/import_product_pack_wizard.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import base64
import io
import csv
import logging

_logger = logging.getLogger(__name__)

class ImportProductPackWizard(models.TransientModel):
    _name = 'import.product.pack.wizard'
    _description = 'Import Product Pack Components'

    file_data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='File Name')
    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File (.xls/.xlsx)')
    ], string='File Type', default='excel', required=True)
    
    update_existing = fields.Boolean(
        string='Update Existing Components', 
        default=True,
        help="If checked, existing pack components will be updated. If unchecked, only new components will be added."
    )
    
    replace_all = fields.Boolean(
        string='Replace All Components',
        default=False,
        help="If checked, all existing components will be removed and replaced with imported data."
    )

    # Remove problematic binary fields
    # sample_file_excel = fields.Binary(
    #     string='Excel Template',
    #     readonly=True
    # )
    
    # sample_file_csv = fields.Binary(
    #     string='CSV Template', 
    #     readonly=True
    # )
    
    # excel_filename = fields.Char(string='Excel Filename', default='product_pack_template.xlsx')
    # csv_filename = fields.Char(string='CSV Filename', default='product_pack_template.csv')

    def generate_excel_template(self):
        """Generate Excel template file"""
        try:
            import xlsxwriter
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Product Pack Import')
            
            # Header format
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D7E4BC',
                'border': 1
            })
            
            # Headers
            headers = [
                'Kode Unit', 'Deskripsi', 'Is Pack', 'Type', 'Category', 
                'Factory Model No', 'Product Brand', 'Cal Pack Price', 'Kode Part', 
                'Deskripsi Part', 'Quantity', 'UOM', 'Part Cost'
            ]
            
            for col, header in enumerate(headers):
                worksheet.write(0, col, header, header_format)
            
            # Sample data
            sample_data = [
                ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'MOTOR001', 'Motor 1HP', '1', 'Unit', '1500000'],
                ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'CABLE001', 'Power Cable 5m', '1', 'Unit', '150000'],
                ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'SWITCH001', 'On/Off Switch', '1', 'Unit', '75000'],
                ['BUNDLE002', 'Fan Complete Set', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'FAN001', 'Industrial Fan 16"', '1', 'Unit', '800000'],
                ['BUNDLE002', 'Fan Complete Set', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'STAND001', 'Fan Stand', '1', 'Unit', '200000'],
            ]
            
            for row, data in enumerate(sample_data, 1):
                for col, value in enumerate(data):
                    worksheet.write(row, col, value)
            
            # Auto-fit columns
            for col in range(len(headers)):
                worksheet.set_column(col, col, 20)
            
            workbook.close()
            output.seek(0)
            
            return base64.b64encode(output.read())
            
        except ImportError:
            # Fallback to CSV if xlsxwriter not available
            _logger.warning("xlsxwriter not available, generating CSV template instead")
            return self.generate_csv_template()
        except Exception as e:
            _logger.error(f"Error generating Excel template: {e}")
            # Fallback to CSV
            return self.generate_csv_template()

    def generate_csv_template(self):
        """Generate CSV template file"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Headers
        headers = [
            'Kode Unit', 'Deskripsi', 'Is Pack', 'Type', 'Category',
            'Factory Model No', 'Product Brand', 'Cal Pack Price', 'Kode Part',
            'Deskripsi Part', 'Quantity', 'UOM', 'Part Cost'
        ]
        writer.writerow(headers)
        
        # Sample data
        sample_data = [
            ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'MOTOR001', 'Motor 1HP', '1', 'Unit', '1500000'],
            ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'CABLE001', 'Power Cable 5m', '1', 'Unit', '150000'],
            ['BUNDLE001', 'Motor Package Set', 'TRUE', 'product', 'All / Saleable', 'MP-2024-001', 'Industrial Brand', 'TRUE', 'SWITCH001', 'On/Off Switch', '1', 'Unit', '75000'],
            ['BUNDLE002', 'Fan Complete Set', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'FAN001', 'Industrial Fan 16"', '1', 'Unit', '800000'],
            ['BUNDLE002', 'Fan Complete Set', 'TRUE', 'product', 'All / Saleable', 'FC-2024-002', 'Fan Pro', 'TRUE', 'STAND001', 'Fan Stand', '1', 'Unit', '200000'],
        ]
        
        for data in sample_data:
            writer.writerow(data)
        
        return base64.b64encode(output.getvalue().encode('utf-8'))

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Remove binary field defaults that cause issues
        return res

    def download_excel_template(self):
        """Download Excel template - Direct to HTTP controller"""
        try:
            return {
                'type': 'ir.actions.act_url',
                'url': '/import_pack/excel_template',
                'target': 'new',
            }
        except Exception as e:
            _logger.error(f"Excel download failed: {e}")
            return self.action_show_manual_template()

    def download_csv_template(self):
        """Download CSV template - Direct to HTTP controller"""
        try:
            return {
                'type': 'ir.actions.act_url',
                'url': '/import_pack/csv_template', 
                'target': 'new',
            }
        except Exception as e:
            _logger.error(f"CSV download failed: {e}")
            return self.action_show_manual_template()

    def action_download_excel_template(self):
        """Alternative method for downloading Excel template - Method 2"""
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/excel_template',
            'target': 'new',
        }

    def action_download_csv_template(self):
        """Alternative method for downloading CSV template - Method 2"""
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/csv_template',
            'target': 'new',
        }

    def action_create_sample_file(self):
        """Create sample file content for manual creation"""
        sample_content = """Kode Unit,Deskripsi,Is Pack,Type,Category,Factory Model No,Product Brand,Cal Pack Price,Kode Part,Deskripsi Part,Quantity,UOM,Part Cost
BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,MOTOR001,Motor 1HP,1,Unit,1500000
BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,CABLE001,Power Cable 5m,1,Unit,150000
BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,SWITCH001,On/Off Switch,1,Unit,75000
BUNDLE002,Fan Complete Set,TRUE,product,All / Saleable,FC-2024-002,Fan Pro,TRUE,FAN001,Industrial Fan 16",1,Unit,800000
BUNDLE002,Fan Complete Set,TRUE,product,All / Saleable,FC-2024-002,Fan Pro,TRUE,STAND001,Fan Stand,1,Unit,200000"""
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'title': 'Sample File Content',
                'message': f'''
Copy this content to Excel/CSV file:

{sample_content}

Instructions:
1. Create new Excel or CSV file
2. Copy the content above
3. Paste into first sheet starting from A1
4. Save file
5. Upload in import wizard
                ''',
                'sticky': True,
            }
        }
        """Method 3: Same as HTTP controller"""
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/excel_template',
            'target': 'new',
        }

    def action_generate_csv_manual(self):
        """Method 3: Same as HTTP controller"""
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/csv_template',
            'target': 'new',
        }

    def action_show_manual_template(self):
        """Show manual template creation instructions"""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'info',
                'title': 'Manual Template Creation',
                'message': '''
Create Excel/CSV file with these exact column headers:
1. Kode Unit (Required)
2. Deskripsi (Optional)
3. Is Pack (TRUE/FALSE, YES/NO, 1/0, Y/N - defaults to TRUE)
4. Type (product/consu/service - defaults to product)
5. Category (Optional - category name)
6. Factory Model No (Optional)
7. Product Brand (Optional - brand name)
8. Cal Pack Price (TRUE/FALSE - defaults to FALSE)
9. Kode Part (Required)
10. Deskripsi Part (Optional)
11. Quantity (Required, must be > 0)
12. UOM (Optional, defaults to Unit)
13. Part Cost (Optional)

Sample rows:
BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,MOTOR001,Motor 1HP,1,Unit,1500000
BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,CABLE001,Power Cable 5m,1,Unit,150000
PRODUCT001,Regular Product,FALSE,product,All / Saleable,REG-001,Standard Brand,FALSE,,,,,

Field Details:
- Type: product (stockable), consu (consumable), service
- Is Pack: TRUE = bundle product, FALSE = regular product  
- Cal Pack Price: TRUE = auto-calculate from components
- Category: match by name (e.g., "All / Saleable")
- Brand: requires product.brand model (custom field)
                ''',
                'sticky': True,
            }
        }

    def _parse_csv_file(self, file_data):
        """Parse CSV file and return data"""
        try:
            csv_data = base64.b64decode(file_data).decode('utf-8')
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            return list(csv_reader)
        except Exception as e:
            raise UserError(_("Error reading CSV file: %s") % str(e))

    def _parse_excel_file(self, file_data):
        """Parse Excel file and return data"""
        try:
            # Try xlrd first
            import xlrd
            excel_data = base64.b64decode(file_data)
            workbook = xlrd.open_workbook(file_contents=excel_data)
            sheet = workbook.sheet_by_index(0)
            
            # Get headers from first row
            headers = [sheet.cell_value(0, col) for col in range(sheet.ncols)]
            
            # Get data rows
            data = []
            for row in range(1, sheet.nrows):
                row_data = {}
                for col in range(sheet.ncols):
                    row_data[headers[col]] = sheet.cell_value(row, col)
                data.append(row_data)
            
            return data
            
        except ImportError:
            try:
                # Try openpyxl as fallback
                import openpyxl
                excel_data = base64.b64decode(file_data)
                workbook = openpyxl.load_workbook(io.BytesIO(excel_data))
                sheet = workbook.active
                
                # Get headers from first row
                headers = [cell.value for cell in sheet[1]]
                
                # Get data rows
                data = []
                for row in sheet.iter_rows(min_row=2, values_only=True):
                    row_data = {}
                    for col, value in enumerate(row):
                        if col < len(headers):
                            row_data[headers[col]] = value
                    data.append(row_data)
                
                return data
                
            except ImportError:
                raise UserError(_("Excel parsing requires xlrd or openpyxl library. Please install: pip install xlrd openpyxl"))
        except Exception as e:
            raise UserError(_("Error reading Excel file: %s\n\nTry saving as CSV format instead.") % str(e))

    def _validate_row_data(self, row):
        """Validate individual row data"""
        errors = []
        
        # Required fields
        required_fields = ['Kode Unit', 'Kode Part', 'Quantity']
        for field in required_fields:
            if not row.get(field):
                errors.append(_("Missing required field: %s") % field)
        
        # Validate quantity
        try:
            qty = float(row.get('Quantity', 0))
            if qty <= 0:
                errors.append(_("Quantity must be greater than 0"))
        except (ValueError, TypeError):
            errors.append(_("Invalid quantity value: %s") % row.get('Quantity'))
        
        # Validate Is Pack field
        is_pack_value = row.get('Is Pack', '').strip().upper()
        if is_pack_value and is_pack_value not in ['TRUE', 'FALSE', 'YES', 'NO', '1', '0', 'Y', 'N']:
            errors.append(_("Invalid 'Is Pack' value: %s. Use TRUE/FALSE, YES/NO, 1/0, or Y/N") % row.get('Is Pack'))
        
        # Validate Type field
        type_value = row.get('Type', '').strip().lower()
        if type_value and type_value not in ['product', 'consu', 'service']:
            errors.append(_("Invalid 'Type' value: %s. Use 'product', 'consu', or 'service'") % row.get('Type'))
        
        # Validate Cal Pack Price field
        cal_pack_price = row.get('Cal Pack Price', '').strip().upper()
        if cal_pack_price and cal_pack_price not in ['TRUE', 'FALSE', 'YES', 'NO', '1', '0', 'Y', 'N']:
            errors.append(_("Invalid 'Cal Pack Price' value: %s. Use TRUE/FALSE, YES/NO, 1/0, or Y/N") % row.get('Cal Pack Price'))
        
        return errors

    def _find_category(self, category_name):
        """Find product category by name"""
        if not category_name:
            return None
        
        # Search by name or complete_name
        category = self.env['product.category'].search([
            '|', ('name', 'ilike', category_name), ('complete_name', 'ilike', category_name)
        ], limit=1)
        
        if not category:
            # Try to find by partial match
            category = self.env['product.category'].search([
                ('complete_name', 'ilike', category_name)
            ], limit=1)
        
        return category

    def _find_brand(self, brand_name):
        """Find product brand by name"""
        if not brand_name:
            return None
        
        # Check if product_brand_id field exists (might be custom field)
        try:
            brand = self.env['product.brand'].search([('name', 'ilike', brand_name)], limit=1)
            return brand
        except:
            # If product.brand model doesn't exist, return None
            _logger.warning(f"Product brand model not found, skipping brand: {brand_name}")
            return None

    def _parse_product_type(self, type_value):
        """Parse product type value"""
        if not type_value:
            return 'product'  # Default
        
        type_str = str(type_value).strip().lower()
        if type_str in ['product', 'consu', 'service']:
            return type_str
        else:
            return 'product'  # Default fallback

    def _parse_cal_pack_price(self, value):
        """Parse Cal Pack Price field value to boolean"""
        if not value:
            return False  # Default to False if not specified
        
        value_str = str(value).strip().upper()
        
        # True values
        if value_str in ['TRUE', 'YES', '1', 'Y', 'T']:
            return True
        # False values  
        elif value_str in ['FALSE', 'NO', '0', 'N', 'F']:
            return False
        else:
            return False  # Default to False for unknown values

    def _parse_is_pack_value(self, value):
        """Parse Is Pack field value to boolean"""
        if not value:
            return True  # Default to True if not specified
        
        value_str = str(value).strip().upper()
        
        # True values
        if value_str in ['TRUE', 'YES', '1', 'Y', 'T']:
            return True
        # False values  
        elif value_str in ['FALSE', 'NO', '0', 'N', 'F']:
            return False
        else:
            return True  # Default to True for unknown values

    def _find_or_create_product(self, product_code, product_name=None, product_type=None, category_id=None, factory_model_no=None, brand_id=None):
        """Find product by code or create if not exists with extended fields"""
        if not product_code:
            return None
            
        # Search by default_code first
        product = self.env['product.product'].search([('default_code', '=', product_code)], limit=1)
        
        if not product and product_name:
            # Prepare product values
            product_vals = {
                'name': product_name,
                'default_code': product_code,
                'type': product_type or 'product',
                'purchase_ok': True,
                'sale_ok': True,
            }
            
            # Add category if found
            if category_id:
                product_vals['categ_id'] = category_id
            
            # Add factory model no if provided
            if factory_model_no:
                # Check if field exists
                if 'factory_model_no' in self.env['product.template']._fields:
                    product_vals['factory_model_no'] = factory_model_no
            
            # Add brand if found
            if brand_id:
                # Check if field exists
                if 'product_brand_id' in self.env['product.template']._fields:
                    product_vals['product_brand_id'] = brand_id
            
            # If not found and name provided, create new product
            product = self.env['product.product'].create(product_vals)
            _logger.info(f"Created new product: {product_code} - {product_name}")
        
        elif product:
            # Update existing product if fields provided
            update_vals = {}
            
            # Update type if provided
            if product_type and product.type != product_type:
                update_vals['type'] = product_type
            
            # Update category if provided
            if category_id and product.categ_id.id != category_id:
                update_vals['categ_id'] = category_id
            
            # Update factory model no if provided
            if factory_model_no and 'factory_model_no' in self.env['product.template']._fields:
                if getattr(product, 'factory_model_no', None) != factory_model_no:
                    update_vals['factory_model_no'] = factory_model_no
            
            # Update brand if provided
            if brand_id and 'product_brand_id' in self.env['product.template']._fields:
                current_brand_id = getattr(product, 'product_brand_id', None)
                if current_brand_id and current_brand_id.id != brand_id:
                    update_vals['product_brand_id'] = brand_id
                elif not current_brand_id:
                    update_vals['product_brand_id'] = brand_id
            
            # Apply updates if any
            if update_vals:
                product.write(update_vals)
                _logger.info(f"Updated product fields for: {product_code}")
        
        return product

    def _find_uom(self, uom_name):
        """Find UOM by name"""
        if not uom_name:
            return self.env.ref('uom.product_uom_unit')  # Default to Unit
        
        uom = self.env['uom.uom'].search([
            '|', ('name', 'ilike', uom_name), ('category_id.name', 'ilike', uom_name)
        ], limit=1)
        
        return uom if uom else self.env.ref('uom.product_uom_unit')

    def button_import(self):
        """Main import function"""
        if not self.file_data:
            raise UserError(_("Please select a file to import"))

        try:
            # Parse file based on type
            if self.import_type == 'csv':
                data = self._parse_csv_file(self.file_data)
            else:
                data = self._parse_excel_file(self.file_data)

            if not data:
                raise UserError(_("No data found in the file"))

            # Validate data
            errors = []
            for i, row in enumerate(data, 1):
                row_errors = self._validate_row_data(row)
                if row_errors:
                    errors.extend([f"Row {i}: {error}" for error in row_errors])

            if errors:
                raise ValidationError(_("Data validation errors:\n%s") % "\n".join(errors))

            # Process import
            result = self._process_import(data)

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'success',
                    'message': _('Product pack components imported successfully!'),
                    'next': {'type': 'ir.actions.act_window_close'},
                }
            }
        except Exception as e:
            _logger.error(f"Import error: {e}")
            raise UserError(_("Import failed: %s") % str(e))

    def _process_import(self, data):
        """Process the import data"""
        processed_parents = {}
        created_count = 0
        updated_count = 0
        
        for row in data:
            parent_code = row.get('Kode Unit', '').strip()
            parent_name = row.get('Deskripsi', '').strip()
            is_pack_value = self._parse_is_pack_value(row.get('Is Pack', ''))
            product_type = self._parse_product_type(row.get('Type', ''))
            category_name = row.get('Category', '').strip()
            factory_model_no = row.get('Factory Model No', '').strip()
            brand_name = row.get('Product Brand', '').strip()
            cal_pack_price = self._parse_cal_pack_price(row.get('Cal Pack Price', ''))
            component_code = row.get('Kode Part', '').strip()
            component_name = row.get('Deskripsi Part', '').strip()
            quantity = float(row.get('Quantity', 1))
            uom_name = row.get('UOM', 'Unit').strip()
            component_cost = float(row.get('Part Cost', 0)) if row.get('Part Cost') else 0
            
            # Find related records
            category_id = None
            if category_name:
                category = self._find_category(category_name)
                category_id = category.id if category else None
            
            brand_id = None
            if brand_name:
                brand = self._find_brand(brand_name)
                brand_id = brand.id if brand else None
            
            # Find or create parent product with extended fields
            parent_product = self._find_or_create_product(
                parent_code, parent_name, product_type, category_id, factory_model_no, brand_id
            )
            if not parent_product:
                _logger.warning(f"Parent product not found: {parent_code}")
                continue
            
            # Set parent as pack based on Is Pack field and Cal Pack Price
            update_vals = {}
            current_is_pack = parent_product.product_tmpl_id.is_pack
            current_cal_pack_price = getattr(parent_product.product_tmpl_id, 'cal_pack_price', False)
            
            if is_pack_value != current_is_pack:
                update_vals['is_pack'] = is_pack_value
                if is_pack_value:
                    _logger.info(f"Set product {parent_code} as pack")
                else:
                    _logger.info(f"Unset product {parent_code} as pack")
            
            # Set cal_pack_price to TRUE if product becomes a pack, or use provided value
            if is_pack_value and cal_pack_price != current_cal_pack_price:
                update_vals['cal_pack_price'] = cal_pack_price
                _logger.info(f"Set cal_pack_price for {parent_code} to {cal_pack_price}")
            
            # Apply updates if any
            if update_vals:
                parent_product.product_tmpl_id.write(update_vals)
            
            # Find or create component product
            component_product = self._find_or_create_product(component_code, component_name)
            if not component_product:
                _logger.warning(f"Component product not found: {component_code}")
                continue
            
            # Update Part Cost if provided
            if component_cost > 0 and component_product.standard_price != component_cost:
                component_product.write({'standard_price': component_cost})
            
            # Find UOM
            uom = self._find_uom(uom_name)
            
            # Track processed parents for replacement logic
            if parent_product.id not in processed_parents:
                processed_parents[parent_product.id] = {
                    'product': parent_product,
                    'new_components': []
                }
                
                # If replace_all is True, clear existing components
                if self.replace_all:
                    existing_packs = self.env['product.pack'].search([
                        ('bi_product_template', '=', parent_product.product_tmpl_id.id)
                    ])
                    existing_packs.unlink()
            
            processed_parents[parent_product.id]['new_components'].append({
                'product': component_product,
                'quantity': quantity,
                'uom': uom
            })
        
        # Create/update pack components
        for parent_id, parent_data in processed_parents.items():
            parent_product = parent_data['product']
            
            for comp_data in parent_data['new_components']:
                component_product = comp_data['product']
                quantity = comp_data['quantity']
                uom = comp_data['uom']
                
                # Check if component already exists
                existing_pack = self.env['product.pack'].search([
                    ('bi_product_template', '=', parent_product.product_tmpl_id.id),
                    ('product_id', '=', component_product.id)
                ], limit=1)
                
                if existing_pack:
                    if self.update_existing:
                        existing_pack.write({
                            'qty_uom': quantity,
                        })
                        updated_count += 1
                else:
                    # Create new pack component
                    self.env['product.pack'].create({
                        'bi_product_template': parent_product.product_tmpl_id.id,
                        'product_id': component_product.id,
                        'qty_uom': quantity,
                    })
                    created_count += 1
        
        _logger.info(f"Import completed: {created_count} created, {updated_count} updated")
        
        # Show summary
        message = _("Import Summary:\n- Created: %d components\n- Updated: %d components") % (created_count, updated_count)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'message': message,
                'sticky': True,
            }
        }