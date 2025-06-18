Cancel Account Move
====================

Modul ini memungkinkan Anda untuk membatalkan (cancel), mengatur ulang ke draft (reset to draft), atau menghapus (delete) transaksi jurnal dan pembayaran di Odoo 14.0. Fitur ini cocok digunakan untuk akuntan atau pengguna yang membutuhkan fleksibilitas dalam koreksi jurnal.

Fitur Utama
-----------

- Cancel jurnal (account.move) secara massal.
- Reset jurnal ke status draft.
- Cancel dan delete jurnal.
- Cancel pembayaran (account.payment) termasuk reconciled entries.
- Reset pembayaran ke draft.
- Cancel dan delete pembayaran.
- Konfigurasi global untuk memilih perilaku default pada pembatalan invoice dan payment.
- Tombol tambahan di form invoice dan payment untuk pembatalan manual.

Instalasi
---------

1. Salin folder `cke_account_cancel` ke direktori `addons` Anda.
2. Jalankan perintah upgrade:
3. Aktifkan grup akses "Account Cancel Feature" pada pengguna yang membutuhkan fitur ini.

Konfigurasi
-----------

Masuk ke menu **Invoicing > Configuration > Settings**, lalu scroll ke bagian **Cancel Configuration**.

- **Invoice Operation Type**:
- Cancel Only
- Cancel and Reset to Draft
- Cancel and Delete

- **Payment Operation Type**:
- Cancel Only
- Cancel and Reset to Draft
- Cancel and Delete

Grup Akses
----------

Modul ini menambahkan satu grup akses:

- **Account Cancel Feature** (`group_sh_account_cancel_adv`)

Pastikan pengguna Anda termasuk dalam grup ini untuk dapat melihat dan menggunakan tombol cancel pada invoice dan pembayaran.

Dependensi
----------

- `account` (Odoo 14.0 core module)

Catatan Versi
-------------

**Versi:** 14.0.1.17062026

Lisensi
-------

OPL-1

Penulis
-------

aRai

