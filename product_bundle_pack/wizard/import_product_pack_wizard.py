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
            is_pack = self.B(first.get('Is Pack') or True)
            bundle_type = G(first, 'Type') or 'product'
            cal_pack_price = self.B(first.get('Cal Pack Price'))

            # cari / buat template
            prod = Product.search([('default_code', '=', bundle_code)], limit=1)
            if prod:
                tmpl = prod.product_tmpl_id
                updated_tmpl += 1
            else:
                tmpl = Template.create({
                    'name': bundle_name,
                    'type': bundle_type if bundle_type in ('product', 'consu', 'service') else 'product',
                    'is_pack': True,
                    'cal_pack_price': cal_pack_price,
                })
                prod = tmpl.product_variant_id
                prod.default_code = bundle_code
                created_tmpl += 1

            # update flags parent
            tmpl.is_pack = bool(is_pack)
            if tmpl.cal_pack_price != cal_pack_price:
                tmpl.cal_pack_price = cal_pack_price

            # === parent-only ===
            component_rows = [r for r in bundle_rows if self.S(r.get('Kode Part'))]

            if not component_rows:
                if self.allow_parent_only:
                    # cukup buat/update parent tanpa error
                    continue
                else:
                    raise UserError(_("Bundle %s has no components (no 'Kode Part').") % bundle_code)

            # hapus existing jika Replace All aktif
            if self.replace_all:
                tmpl.pack_ids.unlink()

            # mapping existing untuk Update Existing
            existing_map = {}
            if self.update_existing and not self.replace_all:
                for pl in tmpl.pack_ids:
                    existing_map[pl.product_id.id] = pl

            # proses komponen
            for r in component_rows:
                part_code = G(r, 'Kode Part')
                part_name = G(r, 'Deskripsi Part') or part_code
                qty = self.F(r.get('Quantity'))
                uom_name = G(r, 'UOM')
                cost = self.F(r.get('Part Cost'))

                if qty <= 0:
                    raise UserError(_("Bundle %s / Part %s has non-positive Quantity.") % (bundle_code, part_code))

                comp = Product.search([('default_code', '=', part_code)], limit=1)
                if not comp:
                    comp_tmpl = Template.create({
                        'name': part_name or part_code,
                        'type': 'product',
                    })
                    comp = comp_tmpl.product_variant_id
                    comp.default_code = part_code
                    if cost > 0:
                        comp.standard_price = cost

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
                        # 'uom_id': get_uom_id(uom_name) or comp.uom_id.id,
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