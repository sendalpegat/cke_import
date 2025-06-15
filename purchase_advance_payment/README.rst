# Purchase Advance Payment - Custom Enhancement

Modul ini merupakan pengembangan dari sistem advance payment pada Purchase Order dan Vendor Bills di Odoo 14.0, yang memberikan fitur tambahan seperti pengelolaan pembayaran bertahap, validasi komersial invoice, dan ekspor laporan pembayaran.

## 🔧 Fitur Utama

### 1. Advance Payment via Purchase Order
- Wizard interaktif dengan input persentase atau nominal pembayaran.
- Validasi sisa jumlah (`residual`) sebelum membuat pembayaran.
- Pembayaran tercatat dalam tab *Payment Advances* di PO.

### 2. Advance Payment via Vendor Bills
- Wizard serupa seperti PO, dengan referensi ke faktur vendor.
- Pembayaran tercatat dalam tab *Payment Advances* di Vendor Bill.

### 3. Status dan Tracking
- `advance_payment_status` dan `payment_progress` otomatis dihitung.
- Tampilan badge pada tree dan form untuk status: `not_paid`, `partial`, `paid`, `down_payment`, `commercial_invoice`, dll.

### 4. Commercial Invoice State
- Tambahan state `commercial_invoice` pada `account.move`.
- Tombol `Validate` khusus untuk memindahkan draft menjadi `commercial_invoice`.
- Tombol **Cancel Commercial Invoice** disediakan untuk membatalkan dan mengembalikan ke draft.

### 5. Sequence Khusus Commercial Invoice
- Otomatis membuat penomoran dengan format: `CI/2025/00001`
- Kode sequence: `custom.commercial.invoice`

### 6. Export Payment Progress to XLSX
- Menu baru "Export Payment Progress" di modul Purchase.
- Menghasilkan file Excel berisi daftar PO beserta status pembayaran dan sisa tagihan.

---

## 📄 File yang Ditambahkan / Dimodifikasi

### Python
- `models/account_move.py`:
  - Tambahan field `container_number`, `receipt_date`
  - Tambahan logic: `_get_sequence()`, `action_post()`, `button_cancel_commercial_invoice()`

- `models/purchase_order.py`:
  - Perhitungan: `amount_residual`, `payment_progress`, `advance_payment_status`

- `wizard/purchase_advance_payment_wizard.py`:
  - Gabungan `check_amount()`
  - Ganti `child_contact_id` menjadi `display_child_name`

- `wizard/vendor_bill_advance_payment_wizard.py`:
  - Validasi advance payment vendor bill

- `report/purchase_payment_progress_report.py`: _(baru)_
  - Logic untuk generate report XLSX dari purchase.order

### XML
- `views/account_move_commercial_invoice_view.xml`
  - Tombol `Validate` & `Cancel Commercial Invoice`
  - Tambahan tab *Payment Advances*

- `views/account_move_tree_view.xml`
  - Badge untuk `commercial_invoice`, `cancel`

- `views/purchase_view.xml`
  - Tombol `Pay TT`, tab advance payment di PO

- `views/account_move_payment_advances.xml`: _(baru)_
  - Tab *Payment Advances* di vendor bill

- `views/report/purchase_payment_progress_report_view.xml`: _(baru)_
  - View dan menu untuk export XLSX

### Data
- `data/ir_sequence.xml`: _(baru)_
  - Sequence `custom.commercial.invoice`

---

## 📥 Instalasi

1. Pastikan dependensi `account`, `purchase`, dan `cke_vendor_child` sudah tersedia.
2. Pasang modul ini melalui Apps, atau upgrade jika sudah terpasang.
3. Akses melalui:
   - **Purchase Order**: tombol "Pay TT"
   - **Vendor Bill**: tombol "Pay Advance"
   - **Menu Purchase > Export Payment Progress**

---

## 📌 Catatan
- Modul ini sepenuhnya kompatibel dengan Odoo 14.0 EE.
- Disarankan untuk digunakan oleh user dengan akses grup: `Purchase User` dan `Account Invoice`.