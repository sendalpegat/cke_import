Purchase Order Due Date Tracking
================================

Modul ini menambahkan fitur pelacakan jatuh tempo invoice (Vendor Bill) pada dokumen Purchase Order, dengan pemisahan yang jelas antara estimasi internal dan data aktual dari invoice.

Fitur Utama
-----------

1. **Expected Invoice Due Date**
   - Dihitung otomatis berdasarkan `date_order` + 2 bulan.
   - Ditampilkan di header Purchase Order dan setiap baris order line.
   - Memberikan estimasi kapan invoice diharapkan jatuh tempo.

2. **Actual Invoice Due Date**
   - Diambil dari invoice (Vendor Bill) nyata yang masih belum lunas (`amount_residual > 0`).
   - Menampilkan tanggal jatuh tempo terbaru yang valid untuk setiap baris PO.

3. **Due Status dan Total Days**
   - Ditampilkan untuk **expected** dan **actual** due date.
   - Menggunakan widget **badge** berwarna:
     - 🟢 Not Due → Hijau
     - 🔴 Overdue → Merah
   - Dihitung selisih hari dari hari ini ke tanggal jatuh tempo.

4. **Visualisasi di Purchase Order**
   - Menampilkan informasi tersebut di bawah `product_id` pada tree view `order_line`.

Struktur Field
--------------

### Pada Purchase Order (`purchase.order`)
- `expected_invoice_due_date`: estimasi due date berdasarkan `date_order`.

### Pada Purchase Order Line (`purchase.order.line`)
- `expected_invoice_due_date`: dari `purchase.order`.
- `expected_due_status`: status overdue / not due berdasarkan estimasi.
- `expected_total_days`: selisih hari ke estimasi due date.
- `actual_invoice_due_date`: dari invoice nyata (unpaid).
- `actual_due_status`: status overdue / not due berdasarkan invoice.
- `actual_total_days`: selisih hari ke due date invoice nyata.

Dependensi
----------

- `purchase`
- `account`

Instalasi
---------

1. Salin file ke folder `addons/`.
2. Jalankan perintah upgrade:
3. Buka menu **Purchase > Orders > Purchase Orders**, dan lihat detail jatuh tempo di setiap baris.

Kontak
------

Modul dikembangkan oleh:

**PT Industrial Multi Fan**  
Website: https://kipascke.co.id  
Maintainer: aRai