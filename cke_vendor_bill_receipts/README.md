# Vendor Bill Receipts (Show Inventory Receipts After Posted)

Modul Odoo 14.0 untuk menampilkan **Inventory Receipts (incoming pickings)** yang
berkaitan dengan **Vendor Bill**. Tombol hanya muncul ketika bill **sudah posted**.

## Cara Kerja
- Field `picking_ids` (computed) mengumpulkan receipts dari tiga sumber:
  1) `purchase_line_id` pada `account.move.line` → `stock.move` → `picking_id`
  2) `purchase.order` hasil mapping dari invoice lines → `po.picking_ids`
  3) `invoice_origin` (nama PO), misal: "PO0001, PO0002" → `po.picking_ids`
- Hanya receipts **tipe incoming** dan **state = done** (sesuai alur auto-done Anda).

## UI
- **Smart Button "Receipts"** (dengan counter) dan **tombol "View Receipts"**
  muncul di header Vendor Bill saat `state = posted` dan `picking_ids` tidak kosong.
- Klik tombol membuka daftar/fom `stock.picking` terkait.

## Dependensi
- `account`, `stock`, `purchase`

## Instalasi
1. Copy folder `cke_vendor_bill_receipts` ke path addons Anda.
2. Apps → Update App List.
3. Install **Vendor Bill Receipts (Show Inventory Receipts After Posted)**.

## Opsi Kustom
- Jika ingin menampilkan receipts yang belum `done` juga, hapus filter `p.state == 'done'`.
- Jika di sistem Anda relasi PO → Bill berbeda, sesuaikan logika compute pada
  `_compute_picking_ids_from_bill`.