# Proposal Training CS Aqiqah Al Kautsar

Proposal pelatihan closing lewat WhatsApp untuk tim Customer Service Aqiqah Al Kautsar. Judul yang dipakai klien: Training CS for Improving Sales Closing Rate.

## Ringkasan program
| Hal | Isi |
|---|---|
| Peserta | 6 sampai 8 CS dan 1 Supervisor |
| Alur | Mengenal tim (9 sampai 13 November 2026), workshop 4 jam (pekan 16 sampai 21 November 2026), pendampingan WhatsApp 4 minggu, laporan akhir |
| Inti materi | Lima langkah chat closing: sapa, gali kebutuhan, rekomendasikan satu paket, jawab keraguan, ajak memesan. Ditambah follow-up dan target harian |
| Nilai | Nilai program Rp 7.500.000. Nilai kemitraan Rp 5.500.000, dibayar dengan konsumsi 50 orang untuk acara Sanggabiz 7 November 2026 senilai Rp 3.500.000 dan tunai Rp 2.000.000 dalam dua termin |

## Isi folder
| Berkas | Keterangan |
|---|---|
| `proposal/v1 Proposal Training CS Closing - Aqiqah Al Kautsar.docx` | Proposal untuk klien, versi pertama di repo ini |
| `proposal/v1 Proposal Training CS Closing - Aqiqah Al Kautsar.pptx` | Isi yang sama dalam 22 slide 16:9, untuk diunggah dan diedit di Canva |
| `aset/Kartu Saku CS - 5 Langkah Chat Closing (contoh).pdf` | Satu aset contoh, siap cetak ukuran A6, dua sisi |
| `arsip/` | Draf sebelum aturan bagian 0 berlaku: draf output dan evaluasi, proposal satu halaman revisi 5, dan framework teknis. Disimpan sebagai arsip |
| `_build/build_proposal.js` | Pembuat docx |
| `_build/build_pptx.py` | Pembuat pptx (python-pptx). Teks berupa kotak teks biasa dan tabel dibuat dari kotak, supaya rapi saat diimpor ke Canva |
| `_build/kartu_saku.html`, `_build/render_kartu.js` | Sumber dan pembuat kartu saku (PNG untuk proposal, PDF untuk cetak) |
| `08-CATATAN-TIM.md` | Isian yang belum lengkap, cek klaim, dan catatan anggaran |

## Cara membuat ulang
```
cd aqiqah-alkautsar/_build
NODE_PATH=$(npm root -g) node render_kartu.js
NODE_PATH=$(npm root -g) node build_proposal.js
python3 build_pptx.py
python3 ../../tools/cek-gaya.py "../proposal/v1 Proposal Training CS Closing - Aqiqah Al Kautsar.docx"
```
`render_kartu.js` memakai Playwright dan huruf Montserrat dari `tanoto/fonts/`.

## Riwayat
- Sebelum 3 November 2026: proposal disusun di luar repo, dari dua halaman sampai framework teknis 18 halaman. Acuan bentuk: proposal Boardriders (slide) dan proposal SLB Kaltim (docx).
- 3 November 2026: versi pptx ditambahkan atas permintaan tim agar bisa diunggah ke Canva.
- 3 November 2026: arahan tim agar proposal mudah dipahami dan meyakinkan, tanpa istilah akademik, dengan satu aset contoh. Arahan dicatat di `ATURAN-PROPOSAL.md` bagian 0. Proposal ditulis ulang menjadi v1 di folder ini.
