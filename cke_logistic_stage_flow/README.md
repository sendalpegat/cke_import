# Logistic Stage Flow

Menambahkan alur status logistik dari Vendor Bill (posted):

Loaded → Boarded → Customs → Arrived → Gudang VSJ

Setiap perpindahan tahap membuat **Internal Transfer** dari lokasi tahap saat ini ke lokasi tahap berikut, dengan **input tanggal**.

## Cara Pakai
1. Pastikan Vendor Bill **posted**.
2. Di header, statusbar **Logistic Stage** terlihat (awal = *Loaded*).
3. Klik **Change Stage**, pilih **Target Stage** dan **Move Date**, lalu **Confirm**.
4. Sistem membuat **picking internal** & memvalidasi (default aktif). Status di bill ikut berubah.

## Lokasi
- Dibuat otomatis: *Boarded*, *Customs*, *Arrived*, *Gudang VSJ* di bawah *Logistics Transit* (internal).
- *Loaded* memakai lokasi stok hasil receipt (destination dari receipt pertama).