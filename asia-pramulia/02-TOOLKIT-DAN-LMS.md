# TOOLKIT SANGGABIZ DAN TAWARAN LMS (PT ASIA PRAMULIA)

Arahan tim, 10 November 2026: pelatihan memberi peserta alat kerja yang siap pakai, selain materi. Alat itu dibuat sebagai nilai jual (USP) Sanggabiz dan membuka jalan menawarkan LMS Sanggabiz untuk materi lain.

## 1. Gagasan

1. Pekerjaan hitung yang berulang (OEE, varians anggaran, stok pengaman, beban mesin) dibuatkan alat. Peserta tidak menghabiskan waktu kelas untuk menghitung manual, dan waktunya dipakai untuk membaca hasil dan memutuskan tindakan.
2. Tiap alat membawa kasus contoh yang realistis. Peserta menjalankan kasus itu di kelas, lalu mengganti datanya dengan data pabrik sendiri.
3. Cara pakai tertulis di lembar Panduan pada tiap alat. Peserta mempelajari manualnya sendiri. Fasilitator tidak mengajarkan tombol dan rumus satu per satu.
4. Alat bukan hanya kalkulator. Templat, checklist, formulir, dan lembar kerja juga termasuk toolkit.
5. Materi lain yang tidak sempat dibahas di kelas bisa dipelajari mandiri di LMS Sanggabiz. Ini tawaran lanjutan.

## 2. Jujur soal data contoh

Semua angka di kalkulator adalah data rekaan fasilitator. Ini bukan data PT Asia Pramulia dan jangan ditulis sebagai data klien. Lembar Panduan di tiap berkas memuat pernyataan itu. Kasusnya dirancang meniru kejadian lazim di pabrik injeksi plastik (short shot, flashing, setup cetakan, resin lembap, sisa bahan di mesin).

Pilihan memakai data klien: bila PT Asia Pramulia mau memberi data yang sudah dianonimkan (misalnya data cacat dan downtime sebulan), kami ganti data contoh dengan data itu sebelum pelatihan. Itu membuat latihan lebih dekat ke pekerjaan peserta. `[ISI TIM: tanyakan ke klien]`

## 3. Alat yang sudah jadi

Folder `alat-bantu/`. Semua berupa berkas Excel dengan rumus hidup, lembar Panduan di depan, sel isian berwarna biru muda, dan sel hasil berwarna abu-abu. Skrip pembuatnya ada di `alat-bantu/_build/buat_kalkulator.py`.

| Berkas | Dipakai di sesi | Isi dan kasus contoh |
|---|---|---|
| `1-Kalkulator-OEE.xlsx` | 4 | OEE per shift per mesin, enam big losses, loss terbesar. Contoh: 8 shift dua mesin injeksi |
| `2-Pareto-5Why-CAPA.xlsx` | 1 | Pareto jenis cacat dengan grafik, formulir 5 Why, daftar CAPA dengan status dan penanda terlambat. Contoh: short shot akibat dryer tidak dinyalakan |
| `3-Anggaran-dan-Varians.xlsx` | 5 | Anggaran tahunan dari volume produksi, anggaran fleksibel, varians per akun dengan batas toleransi. Contoh: anggaran departemen produksi 2027 dan realisasi enam bulan |
| `4-Inventori-dan-Gudang.xlsx` | 7 dan 8 | Analisis ABC, stok pengaman dan titik pemesanan ulang dan EOQ, cycle count dengan akurasi stok, pelacakan sisa bahan baku per SPK. Contoh: 12 bahan baku, pembantu, pelengkap |
| `5-Kapasitas-dan-Jadwal.xlsx` | 6 | Beban jam mesin, kapasitas mingguan, urutan order, dan status terlambat. Contoh: 7 order tiga mesin, ada satu minggu yang kelebihan beban |

Pemeriksaan yang sudah dilakukan (10 November 2026): semua rumus dihitung ulang di LibreOffice tanpa galat, dan hasil contoh dicek dengan hitungan tangan untuk OEE, Pareto, anggaran fleksibel, kelas ABC, titik pemesanan ulang, dan beban mesin. Belum diuji di Excel desktop dan Google Sheets oleh anggota tim. `[ISI TIM: buka di Excel dan Google Sheets, catat bila ada yang berbeda]`

Skenario latihan yang sudah tertanam di data contoh:
- OEE: loss terbesar adalah kecepatan turun, bukan kerusakan. Peserta diajak membaca dulu sebelum menebak.
- Jadwal: urutan awal membuat tiga order terlambat. Mengubah kolom Urutan mengubah hasil, sehingga peserta membandingkan FIFO, tenggat terdekat, dan waktu proses terpendek.
- Pesan Ulang: satu item (masterbatch putih) sudah di bawah titik pemesanan ulang.
- Cycle count: empat dari delapan item selisihnya melebihi toleransi 2 persen.
- Sisa bahan: dua dari empat SPK melebihi batas bahan tidak terlacak 1 persen.

## 4. Alat lain yang direncanakan (belum dibuat)

Alat ini non-hitung dan lebih cepat dibuat. Belum ada, ditandai rencana.

| Alat | Sesi | Fungsi |
|---|---|---|
| Templat usulan kaizen satu halaman | 2 | Kondisi sebelum, usulan, hasil yang diharapkan, PIC |
| Lembar pengamatan delapan pemborosan | 2 | Dipakai peserta saat menonton video atau berjalan di lini |
| Checklist Gemba Walk lima area | 3 | Keselamatan, 5S, aliran material, kondisi mesin, informasi visual |
| Lembar temuan dan jadwal Gemba rutin | 3 | Mencatat temuan, pertanyaan, dan tindak lanjut |
| Templat laporan A3 | 1 | Ringkasan masalah, akar penyebab, CAPA dalam satu lembar |
| Checklist awal shift injeksi | 1, 4 | Contoh checklist yang memuat langkah dryer dan cek cetakan |
| Templat rencana pengendalian stok | 8 | Siapa memeriksa apa, seberapa sering, batas selisih |
| SOP cycle count satu halaman | 7 | Langkah menghitung, mencatat, dan menelusuri selisih |

`[ISI TIM: tentukan mana yang masuk paket pelatihan dan mana yang dibuat bila klien memilih paket tertentu]`

## 5. Nilai jual di proposal

Usul kalimat untuk bagian keunggulan Sanggabiz, silakan ubah:

> Setiap peserta pulang membawa alat yang bisa langsung dipakai di pabriknya: kalkulator OEE, lembar anggaran dan varians, kalkulator stok pengaman dan titik pemesanan ulang, lembar kapasitas dan jadwal, serta templat RCA dan CAPA. Alat ini sudah berisi kasus contoh, panduan pemakaian, dan dapat diisi dengan data PT Asia Pramulia sendiri. Karena hitungan sudah dibantu alat, waktu pelatihan dipakai untuk membaca hasil dan mengambil keputusan.

Yang tidak boleh ditulis di proposal:
- Angka hasil (misalnya OEE naik sekian persen atau biaya turun sekian persen). Kami tidak punya data itu.
- Anggapan alat ini menggantikan sistem ERP atau MES klien. Alat ini lembar kerja Excel.

## 6. Tawaran LMS Sanggabiz

Arah dari tim: topik yang tidak sempat atau tidak dipilih klien bisa dipelajari mandiri di LMS Sanggabiz. Ini peluang penjualan lanjutan (upselling), tidak masuk paket inti.

Yang kami ketahui: tim sedang mengerjakan LMS akademik. Repo ini belum memuat spesifikasinya.

Yang belum ada dan harus diisi tim sebelum LMS ditulis di proposal:
- `[ISI TIM: fitur LMS yang sudah jalan: materi video, kuis, sertifikat, laporan kemajuan]`
- `[ISI TIM: materi yang sudah tersedia di LMS dan yang akan dibuat untuk delapan topik ini]`
- `[ISI TIM: model harga LMS (per peserta per bulan, per modul, atau paket) dan sumbernya, mengikuti STANDAR-HARGA.md]`
- `[ISI TIM: apakah LMS dibuat khusus PT Asia Pramulia atau memakai platform yang sama dengan klien lain]`

Cara menawarkannya di proposal (usul):
1. Letakkan sebagai opsi lanjutan di akhir, bukan di tabel anggaran inti.
2. Hubungkan dengan paket: klien yang memilih paket pengenalan satu hari mendapat jalur belajar mandiri untuk memperdalam modul yang belum dibahas praktik.
3. Tulis apa adanya soal batas: belajar mandiri tidak menggantikan sesi praktik dengan fasilitator, terutama untuk topik yang butuh latihan dengan data (OEE, penjadwalan, inventori).
4. Aturan anggaran di `ATURAN-PROPOSAL.md` bagian 4 meminta satu opsi saja di dokumen klien. Katalog paket dan opsi LMS adalah pengecualian karena klien sendiri belum tahu kebutuhannya. Minta konfirmasi Pak Priyo atau Muchson.
