# Silabus Customer Retention dan Sales Leadership, klien pest control

> Aturan: `../ATURAN-PENULISAN.md`, `../ATURAN-PROPOSAL.md`, `../FORMAT-STANDAR-PROPOSAL.md` (tipe 4).
>
> Proyek terpisah dari folder proyek lain. Jangan mencampur aturan, aset, atau klaim.

Dibuat: 12 November 2026. Permintaan asli: `sumber/permintaan-12-nov-2026.md`.

## Isi folder
| Berkas | Fungsi |
|---|---|
| `proposal/v1 Silabus dan Alat Bantu - ... - Pest Control.pptx` | Deck 19 slide, siap tempel ke proposal |
| `preview/v1 ... .pdf` | Pratinjau PDF deck |
| `alat-bantu/Alat Bantu Customer Retention - Pest Control.xlsx` | Skor Kesehatan Pelanggan, Kalkulator Retensi, Log Keluhan |
| `alat-bantu/Alat Bantu Sales Leadership - Pest Control.xlsx` | Dasbor Tim, Target ke Aktivitas, Rencana Coaching GROW |
| `08-CATATAN-TIM.md` | Mulai dari sini: isian tim, asumsi, daftar cek klaim |
| `_build/` | Skrip pembuat. Urutan: `build_alat_bantu.py`, `render_gambar.py`, `build_deck.py` |

## Membuat ulang
Jalankan dari akar repo:
```
python3 pest-control/_build/build_alat_bantu.py
python3 pest-control/_build/render_gambar.py
python3 pest-control/_build/build_deck.py
```
`render_gambar.py` butuh LibreOffice dan pdftoppm. Huruf Montserrat ada di `../tanoto/fonts/`, Inter perlu terpasang agar pratinjau sama dengan PowerPoint.

## Susunan deck
| Slide | Isi |
|---|---|
| 1 | Ringkasan dua pelatihan dan persiapan kelas Zoom |
| 2 sampai 8 | Customer Retention: ringkasan dan rundown, alur empat sesi, empat slide silabus per sesi, hasil |
| 9 sampai 15 | Sales Leadership: susunan sama |
| 16 | Toolkit alat bantu |
| 17 sampai 19 | Contoh alat bantu: Skor Kesehatan Pelanggan, Log Keluhan, Dasbor Tim dan Target ke Aktivitas |
