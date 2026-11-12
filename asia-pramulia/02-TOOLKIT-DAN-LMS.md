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

| Berkas | Dipakai di | Isi dan kasus contoh |
|---|---|---|
| `1-Kalkulator-OEE.xlsx` | Sesi 3 | OEE per shift per mesin dengan cavity, enam big losses, loss terbesar. Contoh: 8 shift, IM-01 (tutup botol 28 mm, 8 cavity) dan IM-02 (ember, 1 cavity) |
| `2-Pareto-5Why-CAPA.xlsx` | Sesi 4 | Pareto jenis cacat dengan grafik, formulir 5 Why, daftar CAPA dengan status dan penanda terlambat. Contoh: short shot di IM-01 akibat dryer tidak dinyalakan |
| `3-Anggaran-dan-Varians.xlsx` | Sesi 1 dan 4 | Anggaran lini tutup botol dari volume produksi, anggaran fleksibel, varians per akun, dan lembar Dampak Perbaikan. Contoh: resin melewati anggaran fleksibel 6,7 persen |
| `4-Inventori-dan-Gudang.xlsx` | Sesi 2 | Analisis ABC, stok pengaman, titik pemesanan ulang dan EOQ, cycle count dengan akurasi stok, sisa bahan baku per SPK tutup botol |
| `5-Kapasitas-dan-Jadwal.xlsx` | Sesi 1 | Beban jam mesin, kapasitas mingguan, urutan order, status terlambat, dan lembar Kebutuhan Bahan. Contoh: 7 order tiga mesin |

Versi 12 November 2026 menyelaraskan data kelima berkas menjadi satu kasus (order tutup botol 28 mm di IM-01) dan menambah dua lembar: Kebutuhan Bahan dan Dampak Perbaikan. Versi pertama disimpan di `alat-bantu/arsip-v1/`.

Pemeriksaan (12 November 2026): semua rumus dihitung ulang di LibreOffice tanpa galat. Hasil contoh dicek dengan hitungan tangan untuk OEE, anggaran fleksibel, dampak perbaikan, kebutuhan bahan, dan sisa bahan. Belum diuji di Excel desktop dan Google Sheets oleh anggota tim. `[ISI TIM: buka di Excel dan Google Sheets, catat bila ada yang berbeda]`

Angka kasus yang tertanam:
- OEE gabungan 69,2 persen. Loss terbesar kecepatan turun (361 menit), bukan kerusakan. Operator memperlambat siklus karena short shot.
- Pareto: short shot 412 pcs, 39 persen dari cacat seminggu.
- Varians: resin melewati anggaran fleksibel 6,7 persen, lembur melewati lebih dari dua kali lipat, perawatan 22 persen.
- Dampak perbaikan: scrap turun dari 4 ke 1,5 persen dan lembur turun, perkiraan hemat Rp 70.665.000 per tahun atau 1,6 persen dari anggaran lini.
- Cycle count: resin PP selisih 2,8 persen karena sisa dari IM-01 belum dicatat. Empat dari delapan item perlu diselidiki.
- Sisa bahan: dua dari empat SPK tutup botol melewati batas bahan tidak terlacak 1 persen.
- Jadwal: urutan awal membuat tiga order terlambat. Resin HDPE kurang untuk jadwal minggu ini, resin PP cukup.
- Pesan Ulang: masterbatch putih di bawah titik pemesanan ulang.

## 4. Alat cetak dan formulir untuk pelatihan satu hari (belum dibuat)

| Alat | Fungsi |
|---|---|
| Buku kasus | Cerita pabrik contoh dan data awal setiap sesi, 4 sampai 6 halaman |
| Checklist Gemba Walk | Lima area amatan dan kolom temuan, 1 halaman |
| Kartu usulan kaizen | Kondisi sebelum, usulan, perkiraan hasil, penanggung jawab, setengah halaman |
| Lembar rencana tindak lanjut | Rencana 30 hari per peserta, 1 halaman |
| Pre-test, post-test, dan survei | Formulir daring, soal yang sama di awal dan akhir |

Rencana alat dari 10 November 2026 yang dicoret untuk pelatihan satu hari: lembar pengamatan delapan pemborosan (diganti foto lini di slide), lembar jadwal Gemba rutin, templat laporan A3, checklist awal shift injeksi, templat rencana pengendalian stok, dan SOP cycle count. Alat ini bisa dibuat untuk sesi lanjutan atau LMS.

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
4. Aturan anggaran di `ATURAN-PROPOSAL.md` bagian 4 meminta satu opsi saja di dokumen klien. Sejak 12 November 2026 deck hanya menawarkan satu program satu hari. LMS disebut sebagai materi lanjutan di halaman toolkit, tanpa harga. Bila LMS ditawarkan dengan harga terpisah, minta konfirmasi Pak Priyo atau Muchson.
