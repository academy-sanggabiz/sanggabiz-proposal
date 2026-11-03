# IHT Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27 Bandung

> Aturan: `../ATURAN-PENULISAN.md`, `../ATURAN-PROPOSAL.md`, `../FORMAT-STANDAR-PROPOSAL.md`, `../STANDAR-HARGA.md`, `../ARAHAN-PRIYO.md`. Cek dengan `python3 ../tools/cek-gaya.py bpr-nbp27-bandung`.
>
> Proyek terpisah dari folder proyek lain. Jangan mencampur aturan, aset, atau klaim.

Dibuat: 3 November 2026. Tahap: **v4** silabus, contoh aset, dan anggaran dalam satu dokumen (versi yang dipakai). v1 sampai v3 disimpan sebagai arsip. Surat penawaran, profil, dan CV belum dibuat.

## Isi folder
| Berkas | Fungsi |
|---|---|
| `proposal/v4 Proposal Silabus, Contoh Aset, dan Anggaran - IHT Layanan Inklusif PT BPR NBP 27.pdf`, `.pptx`, dan `- rincian anggaran.xlsx` | **Versi yang dipakai.** 7 halaman: v3 ditambah rincian anggaran Rp 10.917.500 sudah termasuk pajak. Angka dari `_build/anggaran.py`, dibuat dengan `_build/build_v4.py` dan `_build/build_pptx_v4.py`. Excel memakai rumus |
| `proposal/v3 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pdf` dan `.pptx` | Arsip. Sama dengan v2, tetapi halaman contoh aset memakai kartu v4 (20 gambar contoh). Dibuat dengan `_build/build_v3.py` dan `_build/build_pptx_v3.py` |
| `proposal/v2 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pdf` dan `.pptx` | Arsip. 6 halaman berbahasa sehari-hari: jadwal satu hari, silabus per modul, yang didapat BPR, dan satu contoh aset (kartu saku isyarat). PPTX bisa diedit dan diunggah ke Canva |
| `kit/02 Kartu Saku Isyarat Perbankan v4 - foto contoh.pdf` dan `.pptx` | Kartu v2 dengan 20 gambar isyarat dari pengguna (3 November 2026). Gambar berlabel contoh, belum diperiksa pengguna Tuli. PPTX bisa diedit: teks, kotak, dan foto bisa diganti. Dibuat dengan `_build/potong_foto_contoh.py` lalu `_build/build_kartu_v4.py` |
| `kit/02 Kartu Saku Isyarat Perbankan v3 - belajar mandiri.pdf` | Kartu belajar di rumah: tiap kata punya kotak tempel foto atau gambar, catatan, centang hafal, dan cek pengajar. Sisi belakang kartu tunjuk. Dibuat dengan `_build/build_kartu_v3.py` |
| `kit/02 Kartu Saku Isyarat Perbankan v2.pdf` | Kartu saku desain ulang, dua sisi A5 siap cetak dan laminasi |
| `proposal/v1 ...pdf` (arsip) | 12 halaman 16:9: ringkasan silabus, tiga halaman kurikulum per modul, hasil dan evaluasi, isi kit, enam halaman aset |
| `proposal/v1 ...pptx` (arsip) | Isi yang sama dalam PPTX yang bisa diedit. Teks, tabel, dan bentuk berupa objek asli, jadi tetap bisa diubah setelah diunggah ke Canva atau dibuka di PowerPoint |
| `proposal/aset-slide/` | Gambar tiap aset yang dipakai di halaman proposal |
| `kit/` | Dokumen kerja tim dan bahan cetak pelatihan: 12 PDF dan 1 Excel. Tidak ditampilkan di proposal v2, kecuali kartu saku isyarat |
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
python3 build_pptx.py
# v2
python3 build_kartu.py && node render.js jobs_kartu.json
python3 build_v2.py && node render.js jobs_v2.json && python3 build_v2.py --gabung
python3 build_pptx_v2.py
# v3 (kartu v4 di halaman contoh aset)
python3 -I potong_foto_contoh.py && python3 build_kartu_v4.py
python3 build_v3.py && node render.js jobs_v3.json && python3 build_v3.py --gabung
python3 build_pptx_v3.py
# v4 (ditambah anggaran)
python3 build_v4.py && node render.js jobs_v4.json && python3 build_v4.py --gabung
python3 build_pptx_v4.py
```

## Mengunggah PPTX ke Canva
1. Di Canva pilih Unggah, lalu pilih berkas PPTX. Canva mengubahnya menjadi desain yang bisa diedit.
2. Font Montserrat dan Inter sudah ada di Canva. Bila ada teks yang bergeser, cek dulu tabel kurikulum di slide 2 sampai 4, karena isinya paling padat.
3. Gambar aset di slide 6 sampai 12 berupa gambar biasa. Untuk mengganti gambar, ambil berkas baru dari `proposal/aset-slide/`.

Isi v2 ada di `_build/silabus_v2.py`. Silabus v1 dan rincian menit untuk fasilitator ada di `_build/silabus.py` dan dipakai oleh halaman proposal dan Panduan Fasilitator, jadi perubahan cukup di satu tempat.
