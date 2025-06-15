# Purchase Invoice Due Date

Modul ini memperluas fitur Purchase Order dan Vendor Bills di Odoo 14.0 dengan menambahkan informasi tanggal jatuh tempo invoice, status overdue, dan keterkaitannya dengan Purchase Order Line serta Invoice Line.

## 📦 Fitur Utama

### 1. Purchase Order
- Menambahkan field:
  - `invoice_date_due`: dihitung otomatis 2 bulan dari `date_order` atau dari invoice terkait
  - `today_date`: tanggal hari ini
  - `total_days`: selisih hari dari `today_date` ke `invoice_date_due`
- Ditampilkan langsung di form Purchase Order.
- Field-field ini juga **diturunkan ke setiap `purchase.order.line`** untuk keperluan laporan per-produk.

### 2. Purchase Order Line
- Menambahkan:
  - `invoice_date_due` (related dari PO)
  - `due_status` (related dari invoice PO)
  - `total_days` (komputasi dari `invoice_date_due`)
- Ditampilkan di tree view lines PO.

### 3. Vendor Bill (`account.move`)
- Menambahkan:
  - `due_status`: otomatis terisi berdasarkan `invoice_date_due`
  - `today_date` dan `total_days`
  - `purchase_order_id`: secara otomatis terisi dari invoice line berdasarkan `invoice_origin`

### 4. Invoice Line (`account.move.line`)
- Menambahkan:
  - `purchase_line_id`: otomatis dicari berdasarkan `invoice_origin`, `product_id`, dan `price_unit` dari `purchase.order.line`.

## ⚠️ Validasi Tambahan
- Mencegah error pada proses *Create Bill* dengan mengecek ketersediaan `product_id`, `price_unit`, dan `invoice_origin` sebelum menjalankan pencarian relasi PO Line.

## 📂 File yang Dimodifikasi / Ditambahkan

- `models/purchase_order.py`:
  - Penambahan field di `purchase.order` dan `purchase.order.line`
- `models/account_move.py`:
  - Penambahan field dan logic untuk `account.move` dan `account.move.line`
- `views/purchase_order_view.xml`:
  - Tampilan field baru di form dan tree view PO
- `views/account_move_view.xml`:
  - Tampilan field baru di form vendor bill
- `__manifest__.py`:
  - Pastikan view yang relevan sudah aktif
