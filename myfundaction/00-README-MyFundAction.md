# MyFundAction: pelatihan AI Agent untuk tim CRM dan marketing

Folder kerja penawaran pelatihan AI Agent (Claude, prompt engineering, Hermes) untuk MyFundAction Jakarta, dengan kemungkinan peserta daring dari Malaysia dan Australia. Sumber: rapat Gmeet 14 November 2026 dengan Arief, Assistant CMO.

## Isi folder

| Berkas | Isi |
|---|---|
| `sumber/mom-14-nov-2026.md` | Notulen rapat, apa adanya |
| `01-RISET-MATERI.md` | Riset Hermes Agent, Claude, prompt engineering, keamanan, biaya, zona waktu, beserta sumber |
| `02-REKOMENDASI.md` | Rekomendasi skema, jadwal, lingkungan Hermes, akun, data, tim pengajar |
| `03-CATATAN-TIM.md` | Isian, pertanyaan ke klien, cek klaim, bahan quotation |
| `silabus/v1 Silabus Pelatihan AI Agent - MyFundAction.xlsx` | Silabus lengkap: ringkasan, silabus per topik, rundown Skema A dan B, hasil dibawa pulang, evaluasi, persiapan teknis, alur program |
| `proposal/v1 Kurikulum dan Silabus - Pelatihan AI Agent MyFundAction.pptx` | 14 slide untuk proposal (format standar tipe 1, keluarga teal) |
| `aset/v1 Materi Pelatihan AI Agent - MyFundAction.pptx` | 67 slide materi untuk dipresentasikan trainer di kelas, per modul dan aktivitas, dengan catatan trainer di speaker notes |
| `preview/` | PDF slide kurikulum dan slide materi, PNG slide kurikulum |
| `aset/v1 Panduan Setup Hermes untuk Non-Programmer.docx` | Langkah instalasi macOS dan Windows (WSL2), setup, SOUL.md, Telegram, keamanan, masalah umum |
| `aset/v1 Pustaka Prompt dan Standar Prompt MFA.docx` | Rubrik 6 unsur, aturan etika, glosarium tiga bahasa, 10 templat dua bahasa |
| `aset/v1 Lembar Kerja Peserta.docx` | Halaman 1 sampai 10 sesuai rujukan di silabus, plus lampiran bahan |
| `aset/v1 Pre-test dan Post-test.docx` | 10 soal pilihan ganda dan 1 tugas prompt |
| `aset/v1 Kunci Jawaban dan Panduan Penilaian - untuk Trainer.docx` | Kunci, contoh jawaban skor 12, kunci segmen donatur dan analisis kampanye |
| `aset/hermes-templat/` | Templat SOUL.md untuk Agen CRM, Iklan, Analis |
| `aset/data-latihan/` | Data donatur dan kampanye **rekaan** |
| `_build/` | Skrip pembuat semua berkas di atas |

## Ringkas program

- 7 modul sesuai notulen, 390 menit tatap muka inti.
- Skema A: 1 hari, 08.30 - 17.00 WIB. Skema B (rekomendasi): 4 sesi x 2 jam, 09.00 - 11.00 WIB.
- Metode: ADDIE (alur program), andragogi (aktivitas), Bloom (tujuan), Kirkpatrick level 1 sampai 3 (evaluasi).
- Penyelarasan antarnegara diukur dengan rubrik 6 unsur prompt (skor 0 sampai 12) di pre-test dan post-test.

## Membuat ulang berkas

Isi silabus ada di satu tempat, `_build/silabus_data.py`. Templat prompt di `_build/prompt_data.py`. Setelah mengubah isi, jalankan:

```bash
cd myfundaction/_build
python3 build_data.py
python3 build_silabus_xlsx.py
python3 build_deck.py
python3 build_materi.py
python3 build_panduan_hermes.py
python3 build_aset_docx.py
```

Lalu periksa gaya dari akar repo: `python3 tools/cek-gaya.py myfundaction/`.

Folder ini milik proyek MyFundAction. Jangan mencampur aset atau klaim dari proyek lain.
