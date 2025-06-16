Purchase Advance Payment - Custom Enhancement
=============================================

Modul Odoo 14.0 ini menambahkan fitur advance payment dan pelacakan pembayaran PO & vendor bill.

-------------------------------------------------------
Fitur Utama
===========

💸 1. Advance Payment via Purchase Order
----------------------------------------
- Wizard interaktif dengan input persentase atau nominal.
- Validasi sisa tagihan (`residual`) otomatis.
- Pembayaran tampil di tab *Payment Advances* dalam PO.

💰 2. Advance Payment via Vendor Bill
-------------------------------------
- Wizard serupa, berbasis invoice.
- Pembayaran tercatat di tab *Payment Advances* di vendor bill.

📊 3. Tracking Status Pembayaran
--------------------------------
- Field `advance_payment_status`, `payment_progress` otomatis dihitung.
- Lencana (badge) untuk status seperti `not_paid`, `partial`, `paid`, `commercial_invoice`.

📄 4. Commercial Invoice State
------------------------------
- Tambahan state `commercial_invoice` untuk `account.move`.
- Tombol `Validate` & `Cancel Commercial Invoice`.
- Penomoran otomatis: `CI/2025/00001` (kode: `custom.commercial.invoice`).
- Otomatis **link ke PO** berdasarkan `invoice_origin` agar field `purchase_id` dan **PO Reference** terisi.

📤 5. Export Payment Progress (XLSX)
-----------------------------------
- Menu: *Purchase > Export Payment Progress*
- Menyediakan laporan Excel berisi daftar PO, status pembayaran, dan sisa tagihan.

-------------------------------------------------------
Integrasi dengan Bundle Pack
============================

- Jika digunakan bersama `product_bundle_pack`, field `PO Reference` di invoice line akan tetap muncul saat status `commercial_invoice`.
- Tidak perlu dependensi langsung, hanya perlu pastikan invoice memiliki `invoice_origin`.

-------------------------------------------------------
Instalasi
=========

1. Pastikan `purchase`, `account`, dan `cke_vendor_child` sudah tersedia.
2. Jalankan upgrade:

::

    odoo-bin -u purchase_advance_payment -d nama_database

3. Uji alur:
   - Buat PO > Pay Advance > Receipt > Vendor Bill
   - Validasi sebagai **Commercial Invoice**
   - Klik **Explode Packs** (jika aktif), cek PO Reference

-------------------------------------------------------
Informasi
=========

- Author: PT Industrial Multi Fan
- Maintainer: aRai
- Website: https://kipascke.co.id
- License: AGPL-3 (purchase_advance_payment), LGPL-3 (product_bundle_pack)