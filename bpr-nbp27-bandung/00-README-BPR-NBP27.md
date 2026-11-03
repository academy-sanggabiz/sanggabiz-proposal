# IHT Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27 Bandung

> Aturan: `../ATURAN-PENULISAN.md`, `../ATURAN-PROPOSAL.md`, `../FORMAT-STANDAR-PROPOSAL.md`, `../STANDAR-HARGA.md`, `../ARAHAN-PRIYO.md`. Cek dengan `python3 ../tools/cek-gaya.py bpr-nbp27-bandung`.
>
> Proyek terpisah dari folder proyek lain. Jangan mencampur aturan, aset, atau klaim.

Dibuat: 3 November 2026. Tahap: draf v1 bagian silabus dan aset pelatihan. Anggaran, surat penawaran, profil, dan CV belum dibuat.

## Isi folder
| Berkas | Fungsi |
|---|---|
| `proposal/v1 Silabus dan Aset Pelatihan - IHT Layanan Inklusif PT BPR NBP 27.pdf` | 12 halaman 16:9: ringkasan silabus, tiga halaman kurikulum per modul, hasil dan evaluasi, isi kit, enam halaman aset |
| `proposal/aset-slide/` | Gambar tiap aset yang dipakai di halaman proposal |
| `kit/` | Isi kit pelatihan yang bisa langsung dicetak: 11 PDF dan 1 Excel |
| `preview/` | Gambar tiap halaman proposal, bisa dilihat di GitHub |
| `01-RINGKASAN-TOR.md` | Isi TOR yang dipakai, kutipan dan tafsiran dipisah |
| `08-CATATAN-TIM.md` | Mulai dari sini: keputusan yang perlu dikonfirmasi, isian tim, daftar cek klaim |
| `sumber/` | TOR asli dari BPR NBP 27 |
| `_build/` | Skrip pembuat. Isi silabus ada di `silabus.py`, isi kit di `build_kit.py` |

## Membuat ulang
Butuh Python 3 (openpyxl, Pillow), Node dengan Playwright, dan poppler (`pdftoppm`, `pdfunite`). Dari folder `_build`:

```bash
python3 build_kit.py && node render.js jobs_kit.json
python3 build_rekap.py
python3 build_proposal.py && node render.js jobs_proposal.json && python3 build_proposal.py --gabung
```

Silabus ditulis sekali di `_build/silabus.py` dan dipakai oleh halaman proposal dan Panduan Fasilitator, jadi perubahan cukup di satu tempat.
