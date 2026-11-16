# Rekomendasi pelaksanaan: pelatihan AI Agent MyFundAction

Ditulis 16 November 2026 untuk tim Sanggabiz yang menyiapkan penawaran ke Arief (Assistant CMO MyFundAction). Dasar: notulen 14 November 2026 (`sumber/mom-14-nov-2026.md`) dan riset di `01-RISET-MATERI.md`. Bagian ini tafsiran dan usulan kami, bukan keputusan klien.

## 1. Pilih Skema B, 4 sesi x 2 jam

Isi kedua skema sama: 7 modul, 390 menit tatap muka inti. Yang berbeda hanya cara membaginya. Kami merekomendasikan Skema B karena empat alasan.

1. **Instalasi Hermes butuh jeda.** Peserta bukan programmer. Masalah instalasi (hak admin, WSL2, jaringan kantor) jarang selesai dalam satu sesi. Di Skema B, peserta yang tertahan dibantu di klinik 30 menit sebelum sesi 4. Di Skema A, peserta yang tertahan setelah pukul 14.55 kehilangan seluruh praktik Modul 7 di laptopnya sendiri.
2. **Tim lintas negara bisa ikut semua modul.** Sesi 09.00 - 11.00 WIB jatuh pukul 10.00 - 12.00 di Kuala Lumpur dan 13.00 - 15.00 di Sydney. Di Skema A, peserta Sydney hanya terjangkau sampai sekitar 13.00 WIB, padahal modul Hermes berlangsung siang hari.
3. **Standar prompt diuji di pekerjaan nyata.** Peserta memakai templat dari sesi 2 di pekerjaannya selama beberapa hari, lalu membawa hasilnya ke sesi 4. Ini yang paling dekat dengan tujuan penyelarasan kualitas antarnegara.
4. **Beban belajar.** Delapan jam materi baru dan praktik terminal dalam satu hari berat untuk peserta pemula.

Skema A tetap layak bila MFA hanya bisa mengumpulkan peserta satu hari. Syaratnya ada di bagian 3.

## 2. Jadwal usulan

Notulen mengusulkan Selasa, 17 November 2026, saat Dr Ghofur ada di Indonesia. Tanggal itu besok dari hari dokumen ini ditulis, dan penawaran belum disetujui HR Manager.

| Sesi | Tanggal usulan | Isi | Bentuk |
|---|---|---|---|
| 1 | Selasa, 17 November 2026 | M1 Introduction to AI, M2 Claude AI Utilization, pre-test | Luring di kantor MFA Jakarta |
| 2 | Kamis, 19 November 2026 | M3 Prompt Engineering, Standar Prompt MFA, cek perangkat | Hibrida |
| 3 | Selasa, 24 November 2026 | M4 AI Agent, M5 Hermes, M6 setup | Luring, peserta luar negeri daring |
| Klinik | Rabu, 25 November 2026 | Instalasi yang belum selesai, 30 menit | Daring |
| 4 | Kamis, 26 November 2026 | M7 penerapan, rencana 30 hari, post-test | Hibrida |
| Klinik pasca | Pekan pertama Desember 2026 | Agen pertama di pekerjaan nyata, 60 menit | Daring |

Sesi 1 tidak membutuhkan instalasi apa pun, jadi bisa tetap digelar 17 November bila MFA ingin memanfaatkan kehadiran Dr Ghofur. Peserta cukup punya akun Claude.

## 3. Bila MFA memilih Skema A

1. Tanggal paling cepat 3 hari kerja setelah konfirmasi, supaya cek perangkat H-2 sempat dikerjakan bersama tim IT MFA. Skema A pada 17 November berarti instalasi di laptop peserta tanpa cek perangkat. Risikonya kami tanggung dengan server latihan: peserta yang laptopnya belum siap tetap praktik lewat akun di server, lalu memasang di laptopnya saat klinik.
2. Ada satu asisten teknis selain trainer selama Modul 6.
3. Klinik pasca pelatihan 60 menit wajib, bukan pilihan.
4. Peserta Australia diarahkan ke sesi rekaman dan klinik terpisah, karena modul Hermes jatuh di luar jam kerja mereka.

## 4. Lingkungan Hermes

1. **Untuk belajar: laptop peserta.** Klien meminta peserta bisa memasang sendiri, jadi instalasi dipraktikkan di laptop masing-masing. Windows memakai WSL2 karena paling teruji. Pemasang Windows asli masih tahap awal menurut dokumentasi.
2. **Untuk demo dan cadangan: satu server latihan** yang disiapkan trainer, berisi 3 profil agen (CRM, Iklan, Analis) di satu grup Telegram. Ini memperlihatkan fitur agen saling berkomunikasi yang dilihat tim di workshop sebelumnya.
3. **Untuk pemakaian rutin setelah pelatihan: satu server milik MFA**, dikelola satu orang yang ditunjuk, bukan agen di laptop tiap orang. Agen di laptop mati saat laptop ditutup, dan kunci API tersebar di banyak perangkat. Ini dibahas di klinik pasca.

## 5. Akun dan biaya pemakaian

1. **Claude untuk Modul 1 sampai 3.** Akun Free cukup untuk mencoba, tetapi batas pesannya bisa habis di tengah praktik. Usul: peserta memakai Claude Pro minimal selama pelatihan. Bila MFA ingin satu Project bersama untuk Standar Prompt MFA lintas negara, paket Team lebih tepat. Harga dan fitur per paket perlu dicek di claude.com/pricing sebelum masuk penawaran.
2. **Model untuk Hermes.** Langganan Claude Pro tidak otomatis bisa dipakai di Hermes. Menurut panduan publik, login Claude di Hermes hanya untuk paket Max dengan kredit tambahan. Jadi Hermes memakai kunci API (OpenRouter atau Anthropic) per peserta dengan batas belanja. Pemakaian latihan diperkirakan beberapa dolar per peserta [E].
3. **Batas belanja dipasang sejak awal.** Penyedia model tidak membatasi biaya secara bawaan.

## 6. Data dan keamanan

1. Selama pelatihan hanya data rekaan (`aset/data-latihan/`).
2. Data donatur adalah data pribadi menurut UU 27 Tahun 2022. Kami sarankan MFA menetapkan kebijakan pemakaian AI untuk data donatur sebelum agen menyentuh data asli. Draf kebijakan bisa menjadi pekerjaan lanjutan.
3. Lima pengaturan aman diajarkan dan diperiksa di Modul 6: persetujuan perintah aktif, allowlist pengguna Telegram, batas belanja, data rekaan, dan pemeriksaan manusia sebelum pesan keluar.

## 7. Tim pengajar

Satu trainer utama dan satu asisten teknis. Asisten diperlukan karena instalasi dikerjakan di laptop tiap peserta dan sebagian peserta ikut daring. Untuk kurang dari 10 peserta, tidak perlu lebih dari dua orang.

## 8. Bahasa

Materi utama berbahasa Indonesia. Bila tim Malaysia dan Australia ikut, slide inti dan semua templat prompt tersedia dalam bahasa Inggris (pustaka prompt sudah dua bahasa), dan trainer perlu nyaman mengajar dua bahasa.

## 9. Langkah berikut

1. Kirim slide kurikulum dan ringkasan rekomendasi ini ke Arief hari ini, supaya bisa dibawa ke HR Manager.
2. Tanyakan lima hal di `03-CATATAN-TIM.md` bagian 2.
3. Susun quotation dua skema mengikuti proses bisnis di silabus (tab Alur program) dan `../STANDAR-HARGA.md`. Komponen yang perlu dihitung ada di `03-CATATAN-TIM.md` bagian 4.
