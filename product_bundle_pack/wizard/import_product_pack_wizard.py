# -*- coding: utf-8 -*-
# wizard/import_product_pack_wizard.py
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64, io, csv

try:
    import openpyxl
except Exception:
    openpyxl = None


class ImportProductPackWizard(models.TransientModel):
    _name = 'import.product.pack.wizard'
    _description = 'Import Product Pack Components'

    # --- Fields yang DIHARUSKAN oleh view XML ---
    import_type = fields.Selection(
        [('csv', 'CSV'), ('xlsx', 'Excel (.xlsx)')],
        string='Import Type',
        default='csv'
    )
    file_data = fields.Binary(string='File', required=True)
    file_name = fields.Char(string='Filename')
    update_existing = fields.Boolean(string='Update Existing Components')
    replace_all = fields.Boolean(string='Replace All Components')

    allow_parent_only = fields.Boolean(
        string='Allow Import Parent Without Components',
        default=True
    )

    # --- Helper casters aman ---
    @staticmethod
    def S(v):
        if v is None:
            return ''
        return v.strip() if isinstance(v, str) else str(v).strip()

    @staticmethod
    def F(v):
        if v is None or v == '':
            return 0.0
        if isinstance(v, (int, float)):
            return float(v)
        s = str(v).strip().replace(',', '')
        try:
            return float(s)
        except Exception:
            return 0.0

    @staticmethod
    def I(v):
        return int(ImportProductPackWizard.F(v))

    @staticmethod
    def B(v):
        if isinstance(v, bool):
            return v
        s = ImportProductPackWizard.S(v).lower()
        return s in ('1', 'true', 'yes', 'y', 't')

    # --- Tombol Download Template: lempar ke controller via act_url ---
    def download_excel_template(self):
        # /import_pack/excel_template sudah ada di controllers/template_download.py
        # Kembalikan action URL agar browser mendownload. 
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/excel_template',
            'target': 'self',
        }

    def download_csv_template(self):
        # /import_pack/csv_template sudah ada di controllers/template_download.py
        return {
            'type': 'ir.actions.act_url',
            'url': '/import_pack/csv_template',
            'target': 'self',
        }

    def action_show_manual_template(self):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Manual Template'),
                'message': _('Columns: Kode Unit, Deskripsi, Is Pack, Type, Category, Factory Model No, Product Brand, Cal Pack Price, Kode Part, Deskripsi Part, Quantity, UOM, Part Cost'),
                'sticky': False,
            }
        }

    def action_create_sample_file(self):
        sample = "BUNDLE001,Motor Package Set,TRUE,product,All / Saleable,MP-2024-001,Industrial Brand,TRUE,MOTOR001,Motor 1HP,1,Unit,1500000"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Sample Row'),
                'message': sample,
                'sticky': False,
            }
        }

    # --- Utilitas baca file ---
    def _read_rows(self):
        """Baca rows dari file CSV/XLSX, kembalikan list[dict]."""
        self.ensure_one()
        if not self.file_data:
            raise UserError(_("No file uploaded."))

        content = base64.b64decode(self.file_data or b'')
        rows = []

        # Pakai pilihan import_type jika ada; fallback dari ekstensi file_name
        ftype = self.import_type
        if not ftype and self.file_name:
            if self.file_name.lower().endswith('.xlsx'):
                ftype = 'xlsx'
            else:
                ftype = 'csv'

        if ftype == 'xlsx':
            if not openpyxl:
                raise UserError(_("openpyxl is not installed on the server."))
            wb = openpyxl.load_workbook(io.BytesIO(content), data_only=True)
            ws = wb.active
            header_cells = next(ws.iter_rows(min_row=1, max_row=1))
            header = [self.S(c.value) for c in header_cells]
            for r in ws.iter_rows(min_row=2, values_only=True):
                row = {header[i]: r[i] if i < len(r) else None for i in range(len(header))}
                rows.append(row)
        else:
            text = content.decode('utf-8-sig', errors='ignore')
            reader = csv.DictReader(io.StringIO(text))
            for row in reader:
                rows.append(row)

        return rows

    # --- Import utama (dipanggil tombol di view) ---
    def button_import(self):
        self.ensure_one()
        rows = self._read_rows()
        if not rows:
            raise UserError(_("No data rows detected."))

        def G(row, key):
            return self.S(row.get(key))

        Product = self.env['product.product']
        Template = self.env['product.template']
        Pack = self.env['product.pack']
        Uom = self.env['uom.uom']

        uom_cache = {}
        def get_uom_id(name):
            if not name:
                return False
            key = name.lower()
            if key in uom_cache:
                return uom_cache[key]
            rec = Uom.search([('name', 'ilike', name)], limit=1)
            uom_cache[key] = rec.id or False
            return uom_cache[key]

        by_bundle = {}
        for r in rows:
            bundle_code = G(r, 'Kode Unit') or G(r, 'Kode unit') or G(r, 'kode unit')
            if not bundle_code:
                raise UserError(_("Missing 'Kode Unit' on a row."))
            by_bundle.setdefault(bundle_code, []).append(r)

        created_tmpl = 0
        updated_tmpl = 0
        created_lines = 0
        updated_lines = 0

        for bundle_code, bundle_rows in by_bundle.items():
            first = bundle_rows[0]
            bundle_name = G(first, 'Deskripsi') or bundle_code
            is_pack_raw = first.get('Is Pack')
            if is_pack_raw is None or is_pack_raw == '':
                is_pack = True  # Default TRUE hanya jika kosong
            else:
                is_pack = self.B(is_pack_raw)  # Gunakan nilai asli dari file
            bundle_type = G(first, 'Type') or 'product'
            cal_pack_price = self.B(first.get('Cal Pack Price'))
            
            # Get Manufacture Code for PARENT product (Kode Unit)
            parent_mfg_code = G(first, 'Manufacture Code')
            parent_factory_model = G(first, 'Factory Model No')
            parent_brand = G(first, 'Product Brand')
            parent_category = G(first, 'Category')

            # Find or create template for parent/bundle
            prod = Product.search([('default_code', '=', bundle_code)], limit=1)
            if prod:
                tmpl = prod.product_tmpl_id
                updated_tmpl += 1
            else:
                # Set category for parent if provided
                parent_categ_id = False
                if parent_category:
                    categ = self.env['product.category'].search([('name', '=', parent_category)], limit=1)
                    if not categ:
                        categ = self.env['product.category'].create({'name': parent_category})
                    parent_categ_id = categ.id
                
                # Create template with Manufacture Code for PARENT
                tmpl = Template.create({
                    'name': bundle_name,
                    'type': bundle_type if bundle_type in ('product', 'consu', 'service') else 'product',
                    'is_pack': is_pack,
                    'cal_pack_price': cal_pack_price,
                    'manufacture_code': parent_mfg_code or False,  # Set manufacture code for parent
                    'factory_model_no': parent_factory_model or False,  # Set factory model for parent
                    'categ_id': parent_categ_id or self.env.ref('product.product_category_all').id,
                    'sale_ok': False,  # <-- HARDCODE: Can Be Sold = FALSE
                })
                prod = tmpl.product_variant_id
                prod.default_code = bundle_code
                created_tmpl += 1

            # Update parent product attributes if it already exists
            if prod:
                update_vals = {}
                if parent_mfg_code and not tmpl.manufacture_code:
                    update_vals['manufacture_code'] = parent_mfg_code
                if parent_factory_model and not tmpl.factory_model_no:
                    update_vals['factory_model_no'] = parent_factory_model
                if parent_category:
                    categ = self.env['product.category'].search([('name', '=', parent_category)], limit=1)
                    if not categ:
                        categ = self.env['product.category'].create({'name': parent_category})
                    if categ and tmpl.categ_id != categ:
                        update_vals['categ_id'] = categ.id
                if parent_brand:
                    try:
                        Brand = self.env['product.brand']
                        brand = Brand.search([('name', '=', parent_brand)], limit=1)
                        if not brand:
                            brand = Brand.create({'name': parent_brand})
                        
                        # Cek field brand yang ada dan update jika kosong
                        brand_fields = ['brand_id', 'product_brand_id', 'x_brand_id', 'brand']
                        for field_name in brand_fields:
                            if field_name in Template._fields:
                                current_brand = getattr(tmpl, field_name, False)
                                if not current_brand:  # Update hanya jika brand belum ada
                                    update_vals[field_name] = brand.id
                                break
                    except Exception:
                        # Skip jika model brand tidak ada
                        pass
                        
                if update_vals:
                    tmpl.write(update_vals)

            # Update flags parent
            tmpl.is_pack = bool(is_pack)
            if tmpl.cal_pack_price != cal_pack_price:
                tmpl.cal_pack_price = cal_pack_price

            # === parent-only ===
            component_rows = [r for r in bundle_rows if self.S(r.get('Kode Part'))]

            if not component_rows:
                if self.allow_parent_only:
                    # Just create/update parent without error
                    continue
                else:
                    raise UserError(_("Bundle %s has no components (no 'Kode Part').") % bundle_code)

            # Delete existing if Replace All is active
            if self.replace_all:
                tmpl.pack_ids.unlink()

            # Mapping existing for Update Existing
            existing_map = {}
            if self.update_existing and not self.replace_all:
                for pl in tmpl.pack_ids:
                    existing_map[pl.product_id.id] = pl

            # Process components
            for r in component_rows:
                part_code = G(r, 'Kode Part')
                part_name = G(r, 'Deskripsi Part') or part_code
                part_cat_name = G(r, 'Part Category')
                # Note: We DON'T use Manufacture Code here anymore as it belongs to parent
                qty = self.F(r.get('Quantity'))
                uom_name = G(r, 'UOM')
                cost = self.F(r.get('Part Cost'))

                if qty <= 0:
                    raise UserError(_("Bundle %s / Part %s has non-positive Quantity.") % (bundle_code, part_code))

                comp = Product.search([('default_code', '=', part_code)], limit=1)
                if not comp:
                    categ_id = False
                    if part_cat_name:
                        categ = self.env['product.category'].search([('name', '=', part_cat_name)], limit=1)
                        if not categ:
                            categ = self.env['product.category'].create({'name': part_cat_name})
                        categ_id = categ.id

                    # Create component WITHOUT manufacture_code (it belongs to parent)
                    comp_tmpl = Template.create({
                        'name': part_name or part_code,
                        'type': 'product',
                        'categ_id': categ_id or self.env.ref('product.product_category_all').id,
                        # NOT setting manufacture_code here - it's for parent only
                    })

                    comp = comp_tmpl.product_variant_id
                    comp.default_code = part_code
                    if cost > 0:
                        comp.standard_price = cost
                else:
                    # Update attributes if available in file
                    write_vals = {}
                    if part_cat_name:
                        categ = self.env['product.category'].search([('name', '=', part_cat_name)], limit=1)
                        if not categ:
                            categ = self.env['product.category'].create({'name': part_cat_name})
                        write_vals['categ_id'] = categ.id
                    if write_vals:
                        comp.product_tmpl_id.write(write_vals)

                if self.update_existing and comp.id in existing_map:
                    pl = existing_map[comp.id]
                    vals = {'qty_uom': qty}
                    if cost > 0 and not comp.standard_price:
                        vals['standard_price'] = cost
                    pl.write(vals)
                    updated_lines += 1
                else:
                    Pack.create({
                        'bi_product_template': tmpl.id,
                        'product_id': comp.id,
                        'qty_uom': qty,
                        'default_code': comp.default_code,
                        'name': comp.name,
                        'standard_price': comp.standard_price if comp.standard_price else cost,
                    })
                    created_lines += 1

            tmpl._recompute_pack_price()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Import Product Pack'),
                'message': _('Done. Template (new/updated): %s/%s | Lines (new/updated): %s/%s') %
                           (created_tmpl, updated_tmpl, created_lines, updated_lines),
                'sticky': False,
                'type': 'success',
            }
        }