# Vendor Bill Picking (Create Picking After Posted)

Modul Odoo 14.0 untuk membuat **Incoming Picking** dari Vendor Bill (tipe `in_invoice`)
menggunakan tombol **Create Picking** yang **hanya tampil ketika bill sudah posted**.

## Fitur
- Tombol **Create Picking** muncul saat `state=posted` dan `move_type='in_invoice'`.
- Membuat `stock.picking` bertipe **incoming** berisi baris product (`product`, `consu`) dari bill.
- Konversi UoM invoice line → UoM produk.
- Smart button **Receipts** untuk membuka daftar picking yang terhubung.
- Jika bill terkait PO dan masih ada picking open dari PO (jika ada custom relasi `purchase_id`), modul akan **mengaitkan** ke picking tersebut agar tidak dobel.

## Dependensi
- `account`, `stock` (modul `purchase` opsional; tidak diwajibkan).

## Instalasi
1. Copy folder `cke_vendor_bill_picking` ke `addons` Anda.
2. **Apps** → Update App List.
3. Install modul **Vendor Bill Picking (Create Picking After Posted)**.

## Cara Pakai
1. Buka Vendor Bill yang **sudah posted**.
2. Klik tombol **Create Picking**.
3. Buka smart button **Receipts** untuk melihat picking yang dibuat.

## Catatan
- Sumber lokasi: `partner.property_stock_supplier`.
- Tujuan lokasi: `default_location_dest_id` dari picking type incoming; fallback ke `lot_stock_id` warehouse.
- Ingin auto-validate? Tambahkan logika set `quantity_done = product_uom_qty` lalu panggil `button_validate()` sesuai kebutuhan Anda.