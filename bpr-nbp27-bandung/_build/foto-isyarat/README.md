# Foto isyarat untuk Kartu Saku Isyarat Perbankan

Folder ini menampung foto peragaan isyarat BISINDO dari co-trainer Tuli. Selama foto belum ada, kotak di kartu berisi ikon tangan. Foto tidak dibuat atau digambar oleh tim, karena isyarat yang dikarang bisa keliru dan membingungkan nasabah Tuli.

## Cara memasang
1. Simpan foto di folder ini dengan nama persis seperti tabel di bawah (jpg, png, atau webp).
2. Dari folder `_build`, jalankan:

```bash
python3 build_kartu.py && node render.js jobs_kartu.json
python3 build_v2.py && node render.js jobs_v2.json && python3 build_v2.py --gabung
python3 build_pptx_v2.py
```

Foto otomatis masuk ke kartu cetak, halaman proposal PDF, dan PPTX.

## Ketentuan foto
1. Satu foto untuk satu isyarat, posisi tangan di titik paling jelas. Isyarat yang bergerak difoto di posisi akhir, atau dibuat dua foto lalu digabung oleh desainer.
2. Format mendatar (landscape). Kotak di kartu lebar dan pendek, jadi bingkai foto dari kepala sampai dada, tangan di depan dada, ada ruang kosong di kiri dan kanan.
3. Latar polos terang, satu warna untuk semua foto. Baju polos gelap supaya tangan terlihat jelas.
4. Cahaya dari depan, wajah terlihat. Ekspresi wajah bagian dari isyarat.
5. Resolusi minimal 1200 piksel di sisi panjang.
6. Izin tertulis dari co-trainer untuk memakai foto di kartu, proposal, dan bahan pelatihan.

## Daftar foto
| No | Kata | Kelompok | Nama berkas |
|---|---|---|---|
| 01 | Selamat pagi | Salam | `01-selamat-pagi.jpg` |
| 02 | Terima kasih | Salam | `02-terima-kasih.jpg` |
| 03 | Silakan duduk | Salam | `03-silakan-duduk.jpg` |
| 04 | Tunggu sebentar | Salam | `04-tunggu-sebentar.jpg` |
| 05 | Setor | Transaksi | `05-setor.jpg` |
| 06 | Tarik | Transaksi | `06-tarik.jpg` |
| 07 | Rekening | Transaksi | `07-rekening.jpg` |
| 08 | Kartu ATM | Transaksi | `08-kartu-atm.jpg` |
| 09 | Uang | Nominal | `09-uang.jpg` |
| 10 | Ribu | Nominal | `10-ribu.jpg` |
| 11 | Juta | Nominal | `11-juta.jpg` |
| 12 | Nomor | Nominal | `12-nomor.jpg` |
| 13 | Formulir | Dokumen | `13-formulir.jpg` |
| 14 | Tanda tangan | Dokumen | `14-tanda-tangan.jpg` |
| 15 | Cap jempol | Dokumen | `15-cap-jempol.jpg` |
| 16 | KTP | Dokumen | `16-ktp.jpg` |
| 17 | Nama | Konfirmasi | `17-nama.jpg` |
| 18 | Benar? | Konfirmasi | `18-benar.jpg` |
| 19 | Ulangi | Konfirmasi | `19-ulangi.jpg` |
| 20 | Selesai | Konfirmasi | `20-selesai.jpg` |

Sebelum sesi foto, minta co-trainer memeriksa daftar kata ini. Bila ada kata yang di Bandung memakai isyarat berbeda dari yang dikenal tim, ikuti co-trainer.
