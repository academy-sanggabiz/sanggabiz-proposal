# Pelatihan Online AR dan Income Audit Hotel: Hotel Vila Lumbung

> Aturan: `../ATURAN-PENULISAN.md`, `../ATURAN-PROPOSAL.md`, `../FORMAT-STANDAR-PROPOSAL.md`, `../STANDAR-HARGA.md`. Cek gaya dengan `python3 ../tools/cek-gaya.py hotel-vila-lumbung`.

Dibuat 19 November 2026. Status: silabus dan berkas pendamping selesai dibuat, belum ada anggaran dan belum dikirim. **Mulai dari `08-CATATAN-TIM.md`.**

## Isi folder
| Berkas atau folder | Fungsi |
|---|---|
| `08-CATATAN-TIM.md` | Isian tim, hal yang perlu dicek, soal anggaran, hitungan internal |
| `sumber/01-BRIEF-KLIEN.md` | Brief klien 15 butir apa adanya, ditambah tafsiran |
| `silabus/Silabus Pelatihan Online AR dan Income Audit Hotel - Hotel Vila Lumbung.docx` | Silabus untuk klien, 3 sesi x 3 jam, per topik dengan tujuan, outline, aktivitas, output, ukuran |
| `assets/1 Modul Peserta ...docx` | Modul 8 bab dan 6 lampiran |
| `assets/2 Workbook ... (peserta).xlsx` | Enam lembar latihan dengan sel isian kuning |
| `assets/3 Workbook ... (kunci pengajar).xlsx` | Isi sama dengan jawaban dan rumus. Jangan dibagikan ke peserta |
| `assets/4 Instrumen Evaluasi ...docx` | Pre-test, post-test, rubrik hasil kerja, survei |
| `assets/5 Kunci dan Pembahasan (pengajar).docx` | Kunci soal dan kunci latihan modul |
| `assets/6 Contoh Sertifikat.docx` | Rancangan sertifikat dengan kolom isian |
| `assets/7 Slide Pelatihan ... (Sesi 1 sampai 3).pptx` | 40 slide siap pakai untuk ketiga sesi |
| `assets/7 Slide Sesi 1 ...pptx` | Versi awal, hanya sesi 1 (arsip, diganti deck lengkap) |
| `_build/` | Skrip pembuat semua berkas (node dan python). Jalankan ulang bila isi diubah |

## Cara membuat ulang
```bash
cd hotel-vila-lumbung/_build
NODE_PATH=$(npm root -g) node build_silabus.js
NODE_PATH=$(npm root -g) node build_modul.js
NODE_PATH=$(npm root -g) node build_evaluasi.js
NODE_PATH=$(npm root -g) node build_sertifikat.js
python3 build_workbook.py
python3 build_slide_lengkap.py
python3 build_slide.py   # versi awal sesi 1
```
