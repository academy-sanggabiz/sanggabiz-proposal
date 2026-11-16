# Catatan tim: pelatihan AI Agent MyFundAction

Dibuat 16 November 2026. Berisi isian, pertanyaan ke klien, cek klaim, dan bahan quotation. Tidak untuk dikirim ke klien.

## 1. Isian sebelum dokumen dikirim

| No | Isian | Ada di |
|---|---|---|
| 1 | Siapa Dr Ghofur dan perannya di pelatihan (pimpinan MFA yang membuka acara, atau trainer yang diharapkan klien). Notulen tidak menjelaskan | Rekomendasi bagian 2 |
| 2 | Nama trainer utama dan asisten teknis, beserta pengalaman AI Agent dan Hermes | Penawaran |
| 3 | Penyedia dan model yang dipakai Hermes saat latihan (OpenRouter atau Anthropic) | Panduan Setup Hermes langkah 5 |
| 4 | Tanggal dan versi Hermes saat perintah dicocokkan dengan dokumentasi resmi | Panduan Setup Hermes, catatan trainer |
| 5 | Cocokkan istilah Melayu dan Inggris di glosarium dengan tim MFA Malaysia dan Australia | Pustaka prompt bagian 5 |
| 6 | Penanggung jawab templat di tiap negara | Pustaka prompt bagian 7 |
| 7 | Logo MFA bila klien mengizinkan dipasang di slide | Slide kurikulum |

## 2. Pertanyaan untuk Arief

1. Skema mana yang condong dipilih, dan apakah Sesi 1 tetap bisa 17 November bila memilih Skema B?
2. Apakah tim Malaysia dan Australia ikut? Berapa orang, dan kota mana di Australia (Sydney dan Melbourne berbeda 3 jam dengan Perth)?
3. Laptop peserta Windows atau macOS, dan apakah peserta punya hak admin? Apakah IT MFA bisa hadir H-2?
4. Akun Claude apa yang sudah dimiliki tim (Free, Pro, Team)? Apakah MFA bersedia membiayai akun Pro atau Team selama pelatihan?
5. Hermes versi apa yang dipakai di workshop dua minggu lalu, dan siapa penyelenggaranya? Kami perlu tahu agar tidak mengulang materi dan memakai versi yang sama.

## 3. Cek klaim

| Klaim | Status | Sumber |
|---|---|---|
| Hermes Agent buatan Nous Research, MIT, rilis Februari 2026 | Dari ringkasan pencarian, belum dibaca di dokumentasi resmi | `01-RISET-MATERI.md` bagian 2 |
| Bot Mode di v0.21 (31 Agustus 2026) | Dari blog pihak ketiga | Idem |
| Perintah `hermes setup`, `hermes gateway setup`, `hermes profile create`, `hermes doctor`, `hermes model` | Dari ringkasan dokumentasi dan cheat sheet. Trainer mencocokkan H-1 | Idem |
| Perintah `hermes gateway start` tanpa `-p` dan `hermes cron --help` | Diturunkan dari contoh `hermes -p <profil> gateway start` dan deskripsi `hermes cron`. Paling perlu dicek | Idem |
| Login Claude di Hermes hanya untuk Max dengan kredit tambahan | Satu panduan pihak ketiga | Idem |
| Harga paket Claude | Ringkasan situs pihak ketiga, angka Team berbeda antarsumber | `01-RISET-MATERI.md` bagian 4 |
| Program masjid lebih tinggi responsnya di Australia | Notulen klien | `sumber/mom-14-nov-2026.md` |
| Data latihan | Rekaan, ditulis jelas di semua tempat | `aset/data-latihan/README.md` |

Situs dokumentasi Hermes tidak bisa dibuka dari sesi kerja Claude karena jaringan sesi dibatasi. Siapa pun di tim bisa membukanya dari peramban biasa.

## 4. Bahan quotation (belum dihitung)

Belum ada angka di dokumen ini. Harga disusun mengikuti `../STANDAR-HARGA.md` dan `../ARAHAN-PRIYO.md`: rincian per baris, fee 10 persen sebagai baris sendiri, honor pembicara yang bisa dibela. Klien meminta dua skema, jadi penawaran menampilkan keduanya (pengecualian `../ATURAN-PROPOSAL.md` bagian 4 butir 1).

| Tahap proses bisnis | Komponen | Skema A | Skema B |
|---|---|---|---|
| 1. Asesmen dan cek perangkat | Formulir, wawancara singkat, cek perangkat H-2 bersama IT | sama | sama |
| 2. Penyesuaian modul | Silabus, slide, lembar kerja, pustaka prompt dua bahasa, panduan Hermes, tes, data latihan | sama | sama |
| 3. Persiapan teknis | Server latihan 1 bulan, kredit API latihan per peserta, bot Telegram latihan | sama | sama |
| 4. Pelaksanaan | Honor trainer per jam tatap muka | 7,25 jam tatap muka dalam 1 hari (390 menit inti, ditambah pembukaan, tes, dan penutup) | 8 jam tatap muka dalam 4 sesi |
| 4. Pelaksanaan | Asisten teknis | 1 hari | 4 sesi dan klinik 30 menit |
| 4. Pelaksanaan | Konsumsi bila di kantor MFA | 2 rehat dan makan siang | snack di sesi luring |
| 4. Pelaksanaan | Cetak lembar kerja dan kit peserta | per peserta | per peserta |
| 5. Klinik pendampingan | 1 sesi daring 60 menit | sama | sama |
| 6. Evaluasi dan laporan | Analisis pre-test dan post-test per negara, laporan akhir | sama | sama |
| | Fee 10 persen | | |

Catatan harga:
1. Rentang honor di `STANDAR-HARGA.md` bagian 4A disusun untuk acara setengah hari di Kalimantan Timur. Untuk trainer AI di Jakarta perlu dua pembanding pasar. [ISI TIM: tarif pembanding trainer AI Agent Jakarta]
2. Tempat diasumsikan kantor MFA. Bila MFA meminta tempat lain, tambahkan baris tempat.
3. Biaya akun Claude Pro atau Team dan kunci API setelah pelatihan ditanggung MFA langsung dan tidak masuk quotation, kecuali kredit latihan.

## 5. Status berkas

| Berkas | Status |
|---|---|
| `silabus/v1 Silabus Pelatihan AI Agent - MyFundAction.xlsx` | Siap ditinjau trainer |
| `proposal/v1 Kurikulum dan Silabus - Pelatihan AI Agent MyFundAction.pptx` | Siap dikirim setelah isian bagian 1 nomor 7 |
| `aset/` | Siap ditinjau trainer. Panduan Hermes wajib dicocokkan H-1 |
| Quotation | Belum dibuat |
