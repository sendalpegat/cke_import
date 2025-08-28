# Picking Stage Flow

- Tambah lokasi khusus: **Loaded**, serta **Boarded, Customs, Arrived, Gudang VSJ**.
- Pindah stage lewat menu **Action** di list `stock.move` (Picking List).

## Cara pakai
1. Buka **Picking List** (dari Vendor Bill → tab/aksi Picking List).
2. Centang baris produk yang mau dipindahkan.
3. Klik **Action → Change Logistic Stage**.
4. Pilih `From Stage` dan `Target Stage` (urutan satu langkah), set tanggal, lalu **Confirm**.
5. Sistem membuat **Internal Transfer** dari lokasi stage asal → tujuan dan (opsional) langsung memvalidasi.

> Catatan: Transisi hanya satu langkah (Loaded→Boarded→Customs→Arrived→Gudang VSJ) untuk menjamin jejak logistik yang rapi.