# PROPOSAL BARU: Pelatihan Karyawan PT Asia Pramulia Tbk, Surabaya (2027)

> Aturan: `../ATURAN-PENULISAN.md` (cara menulis), `../ATURAN-PROPOSAL.md` (isi proposal, termasuk bagian 9 tentang alat bantu), `../FORMAT-STANDAR-PROPOSAL.md` (bentuk halaman, silabus memakai Tipe 4). Cek dengan `python3 ../tools/cek-gaya.py asia-pramulia`.
>
> Proyek ini terpisah dari `../tanoto/` dan `../slb-kaltim/`. Jangan mencampur aturan, aset, atau klaim antarproyek.

Dibuat: 10 November 2026. Status 12 November 2026: **silabus dan alat bantu disetujui tim. Deck silabus dan alat bantu sudah jadi. Anggaran belum dihitung.**

## 1. Ringkasan permintaan

Proposal penawaran pelatihan karyawan tahun 2027 untuk PT Asia Pramulia Tbk, Surabaya (manufaktur plastik). Delapan topik: Problem Solving dan RCA, Continuous Improvement Mindset, Gemba Walk, OEE, Budgeting dan Cost Control, Perencanaan dan Penjadwalan Produksi, Warehouse Management, Pengendalian Inventori. Tujuan menurut catatan klien: menutup kesenjangan kompetensi terhadap job specification.

Sumber: chat tim bertanggal 11/10/2026 (format tanggal sesuai aslinya). Bagian catatan di chat itu terpotong, jadi jumlah peserta dan lokasi belum diketahui.

## 2. Keputusan

1. 10 November 2026: alat kerja (kalkulator Excel dengan kasus contoh, templat, checklist) menjadi nilai jual Sanggabiz. LMS Sanggabiz ditawarkan sebagai lanjutan.
2. 12 November 2026: inhouse training satu hari. Delapan topik digabung menjadi empat sesi yang mengikuti alur kerja pabrik, dengan satu kasus sepanjang hari (order tutup botol 28 mm). Tiap topik berisi paparan singkat dan latihan kecil dengan alat.
3. 12 November 2026: bentuk silabus mengikuti standar baru (`../FORMAT-STANDAR-PROPOSAL.md` Tipe 4), dari proposal IHT PT BPR NBP 27.

## 3. Isi folder

| Berkas | Fungsi |
|---|---|
| `proposal/` | **Deck silabus dan alat bantu (pptx dan pdf), 11 halaman.** Dibuat oleh `_build/build_deck.py` |
| `01-SILABUS.md` | Isi silabus yang sama dengan deck, dalam teks |
| `01-SILABUS-DRAF-v1-modular.md` | Arsip: silabus modular dengan paket, sebelum keputusan satu hari |
| `02-TOOLKIT-DAN-LMS.md` | Daftar alat, kasus contoh, usul kalimat USP, dan tawaran LMS |
| `03-CATATAN-TIM.md` | **Mulai dari sini bila mau melanjutkan.** Daftar isian tim, pertanyaan ke klien, daftar cek sebelum kirim |
| `alat-bantu/` | Lima kalkulator Excel. Versi pertama disimpan di `alat-bantu/arsip-v1/` |
| `alat-bantu/_build/buat_kalkulator.py` | Skrip pembuat kalkulator. Versi pertama: `buat_kalkulator_v1.py` |
| `_build/build_deck.py` | Skrip pembuat deck. Memakai berkas rujukan standar dan tangkapan layar di `_build/assets/` |

## 4. Cara membuat ulang

1. Kalkulator: `python3 asia-pramulia/alat-bantu/_build/buat_kalkulator.py <folder keluaran>`, lalu buka dan simpan ulang di LibreOffice (`soffice --headless --convert-to xlsx`) supaya nilai hasil hitung ikut tersimpan.
2. Tangkapan layar untuk deck: ekspor kalkulator ke PDF dengan LibreOffice, render halaman lembar terkait ke PNG, potong sampai baris data terakhir, simpan ke `_build/assets/`.
3. Deck: `python3 asia-pramulia/_build/build_deck.py` dari akar repo.

## 5. Langkah berikutnya

1. Dapatkan lanjutan catatan klien yang terpotong: jumlah peserta, lokasi, jadwal.
2. Hitung anggaran mengikuti `../STANDAR-HARGA.md` dan `../ARAHAN-PRIYO.md`, lalu tambahkan halaman Rincian Anggaran ke deck.
3. Buat lima alat cetak dan formulir yang belum ada (lihat `03-CATATAN-TIM.md`).
