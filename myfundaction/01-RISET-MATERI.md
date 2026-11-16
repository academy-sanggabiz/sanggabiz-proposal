# Riset materi: pelatihan AI Agent untuk MyFundAction

Dikerjakan 16 November 2026 sebagai bahan silabus. Tanda sumber mengikuti `../STANDAR-HARGA.md` bagian 0: [R] dokumen resmi yang dibaca langsung, [P] publikasi atau ringkasan pencarian yang sumber aslinya belum dibuka, [E] estimasi kami.

Keterbatasan: situs dokumentasi resmi Hermes (hermes-agent.nousresearch.com) dan beberapa blog panduan tidak bisa dibuka dari sesi kerja ini karena jaringan dibatasi. Semua fakta Hermes di bawah berasal dari ringkasan hasil pencarian, jadi tingkatnya [P]. Trainer wajib mencocokkan perintah dan fitur dengan dokumentasi resmi sehari sebelum pelatihan, karena Hermes merilis versi baru hampir tiap minggu.

## 1. Siapa klien

1. MyFundAction (MFA) adalah organisasi nirlaba berbasis relawan muda yang berawal di Malaysia, dahulu bernama Yayasan Dana Kebajikan Muslim Malaysia, dengan cabang antara lain di Indonesia, Selandia Baru, dan Australia [P].
2. Cabang Indonesia tercatat di Jakarta Pusat dengan 11 sampai 50 karyawan (profil lowongan kerja) [P]. Kantor Australia berada di bawah cabang Selandia Baru dan merekrut relawan di Sydney dan Melbourne [P].
3. Program yang disebut di rapat: Palestina, pembangunan masjid, dan air bersih. Program masjid mendapat respons lebih tinggi di Australia (notulen 14 November 2026).
4. Kontak: Arief, Assistant CMO. Peserta dari tim CRM dan marketing, kurang dari 10 orang.

Akibatnya untuk silabus: contoh kasus memakai ketiga program itu, dengan audiens Indonesia, Malaysia, dan Australia. Materi dan templat prompt perlu tersedia dalam bahasa Inggris bila tim Malaysia dan Australia ikut.

## 2. Hermes yang dimaksud klien

Notulen menyebut Hermes sebagai alat yang "memungkinkan beberapa AI Agent saling berinteraksi dan berkomunikasi secara otomatis". Yang cocok dengan gambaran itu adalah **Hermes Agent** dari Nous Research.

| Hal | Isi | Tingkat |
|---|---|---|
| Pembuat dan lisensi | Nous Research, sumber terbuka, lisensi MIT, rilis akhir Februari 2026 | [P] |
| Versi terakhir yang ditemukan | v0.21.5 (v2026.9.24), 24 September 2026. Versi Oktober dan November belum terlihat di indeks rilis | [P] |
| Rilis "Pantheon" v0.21.0 (31 Agustus 2026) | Menambah Bot Mode (beberapa agen bernama, masing-masing dengan model, memori, skill, dan chat sendiri), pesan antarbot di grup, dan persetujuan sebelum agen mengubah berkas instruksinya sendiri. Inilah fitur "agen saling berkomunikasi" yang kemungkinan dilihat klien di workshop | [P] |
| Memori | Dua berkas yang dikurasi: `MEMORY.md` dan `USER.md`. Agen juga bisa mencari percakapan lamanya | [P] |
| Identitas agen | Berkas `SOUL.md`, menempati urutan pertama di system prompt. Tiap profil punya `SOUL.md` sendiri | [P] |
| Skill | Prosedur yang disimpan agen dan dipakai ulang, dibuat dari pengalaman dan diperbaiki saat dipakai | [P] |
| Profil | Satu profil satu agen terpisah: config, kunci API, memori, sesi, skill, dan jadwal sendiri. Lokasi `~/.hermes/profiles/<nama>/`. Dibuat dengan `hermes profile create <nama>` | [P] |
| Gateway | Satu proses melayani Telegram, Discord, Slack, WhatsApp, Signal, dan CLI. Diatur dengan `hermes gateway setup`. Untuk beberapa profil di satu grup Telegram, tiap profil butuh token bot sendiri dan gateway sendiri (`hermes -p <profil> gateway start`) | [P] |
| Jadwal (cron) | Penjadwal bawaan, hasilnya bisa dikirim ke platform yang terhubung, misalnya laporan harian | [P] |
| Instalasi macOS, Linux, WSL2 | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash`. Satu-satunya prasyarat yang disebut dokumentasi adalah Git. Pemasang mengurus Python dan Node.js | [P] |
| Instalasi Windows | Ada pemasang PowerShell untuk Windows asli, disebut early beta. WSL2 dengan Ubuntu disebut jalur yang paling teruji. Sumber berbeda pendapat, jadi cek ulang | [P] |
| Setelah pasang | `hermes setup` (wizard: pilih penyedia model, masukkan kunci API atau login, pilih model), `hermes model` (tambah penyedia), `hermes doctor` (cek masalah) | [P] |
| Syarat model | Konteks minimal 64.000 token. Model yang lebih kecil ditolak saat start | [P] |
| Claude di Hermes | Lewat kunci API Anthropic, OpenRouter, atau login OAuth Anthropic. Satu panduan menyebut OAuth hanya untuk paket Max dengan kredit tambahan, paket Pro tidak bisa. Jadi langganan Claude Pro peserta tidak otomatis bisa dipakai di Hermes | [P] |
| Biaya pakai | Panduan vendor: sekitar USD 5 sampai 8 per bulan untuk pemakaian ringan lewat OpenRouter, USD 25 sampai 40 untuk pemakaian berat. Nous Portal Plus USD 20 per bulan berisi kredit USD 22. Tidak ada batas biaya bawaan, jadi pasang batas belanja di penyedia model | [P] |
| Jalur tanpa terminal | Hostinger menjual Hermes terkelola dan Hermes WebUI sekali klik. Ada juga Hermes Desktop yang tetap butuh pemasangan lewat terminal. Semua klaim dari vendor, belum diuji | [P] |

## 3. Keamanan Hermes yang wajib diajarkan

1. Hermes punya sistem persetujuan perintah berbahaya dengan mode manual, smart, dan off, diatur di `~/.hermes/config.yaml`. Ada daftar blokir untuk perintah yang merusak sistem [P].
2. Mode YOLO (`hermes --yolo`, `/yolo`, atau `HERMES_YOLO_MODE=1`) mematikan persetujuan. Peserta non-programmer tidak memakai mode ini [P].
3. Cloud Security Alliance mencatat 9 CVE dalam 4 hari pada Mei 2026, dengan perbaikan resmi di v0.9.0, dan menilai risiko terbesar ada di arsitekturnya. Adversa menilai konfigurasi bawaan membuka kredensial, berkas, dan jaringan komputer pemilik terhadap masukan dari luar [P].
4. Saran yang berulang di sumber: batasi siapa yang boleh mengirim pesan ke agen (allowlist dan pairing), periksa perintah yang di luar tugas, dan pasang batas belanja API [P].

Akibatnya untuk silabus: modul setup memuat satu topik keamanan. Latihan memakai data rekaan, bukan data donatur. Data donatur adalah data pribadi menurut UU 27 Tahun 2022 tentang Pelindungan Data Pribadi, dan untuk tim Malaysia dan Australia berlaku aturan negaranya masing-masing. Kebijakan pemakaian data asli diputuskan MFA setelah pelatihan.

## 4. Claude

| Hal | Isi | Tingkat |
|---|---|---|
| Paket | Free, Pro USD 20 per bulan (USD 17 bila tahunan), Max USD 100 dan USD 200, Team USD 25 per kursi per bulan (USD 20 bila tahunan) untuk 2 sampai 150 pengguna, Enterprise sesuai negosiasi. Angka Team berbeda antarsumber | [P] |
| Fitur yang relevan | Projects (ruang kerja dengan instruksi dan berkas pengetahuan tetap), Skills, Artifacts, konektor, dan Cowork. Ketersediaan per paket berbeda antarsumber dan perlu dicek di claude.com/pricing | [P] |
| Kegunaan untuk penyelarasan lintas negara | Satu Project bersama berisi Standar Prompt MFA, contoh hasil yang baik, dan glosarium istilah program. Project bersama tersedia di paket Team | [P] |

Catatan: akun Free cukup untuk latihan dasar, tetapi batas pesannya bisa habis di tengah sesi praktik. Rekomendasi akun ada di `02-REKOMENDASI.md`.

## 5. Prompt engineering

Prinsip yang kami pakai berasal dari panduan prompting resmi Anthropic (platform.claude.com, halaman Prompting best practices) [P]:
1. Jelas dan langsung. Tulis tugas seperti memberi arahan ke rekan baru yang belum tahu konteks.
2. Beri konteks dan alasan, bukan hanya perintah.
3. Pisahkan instruksi, bahan, dan contoh dengan tag XML seperti `<instruksi>`, `<data>`, `<contoh>`. Nama tag bebas asal masuk akal.
4. Beri 3 sampai 5 contoh yang beragam bila ingin gaya keluaran yang konsisten.
5. Minta AI berpikir dulu sebelum menjawab untuk tugas analisis.
6. Tentukan format keluaran.

Dari prinsip itu kami susun **6 unsur prompt** yang dipakai sebagai standar bersama tim Indonesia, Malaysia, dan Australia: Konteks, Tugas, Bahan, Aturan, Contoh, Format. Tiap unsur dinilai 0 sampai 2, jadi skor prompt 0 sampai 12. Skor ini dipakai di pre-test dan post-test untuk mengukur penyelarasan kualitas prompt antarnegara (lihat `aset/v1 Pustaka Prompt dan Standar Prompt MFA.docx`).

## 6. Standar kompetensi

1. SKKNI Kepmenaker 103 Tahun 2026 (6 April 2026) memperbarui standar kecerdasan artifisial subbidang Knowledge-Based System dan menggantikan Kepmenaker 123 Tahun 2021 [P]. Isi lampirannya belum dibaca.
2. Belum ditemukan unit SKKNI untuk pemakaian AI generatif atau prompt engineering sebagai alat kerja. Silabus ini tidak mengklaim rujukan SKKNI. Rujukannya adalah metode pelatihan di `../ATURAN-PROPOSAL.md` bagian 1.

## 7. Zona waktu peserta (November 2026)

| Lokasi | Zona | Selisih dari WIB | 09.00 WIB menjadi |
|---|---|---|---|
| Jakarta | WIB, UTC+7 | 0 | 09.00 |
| Kuala Lumpur | MYT, UTC+8 | +1 jam | 10.00 |
| Perth | AWST, UTC+8 | +1 jam | 10.00 |
| Sydney dan Melbourne | AEDT, UTC+11 (musim panas) | +4 jam | 13.00 |

Sesi daring yang mulai pukul 09.00 sampai 10.00 WIB dan selesai 2 jam kemudian masih jatuh di jam kerja ketiga negara. Sesi pukul 14.00 WIB sudah pukul 18.00 di Sydney.

## 8. Sumber

1. Hermes Agent, instalasi dan quickstart (dokumentasi resmi, tidak bisa dibuka dari sesi ini): https://hermes-agent.nousresearch.com/docs/getting-started/installation
2. Repositori resmi: https://github.com/NousResearch/hermes-agent
3. Profil dan Telegram (dokumentasi resmi): https://hermes-agent.nousresearch.com/docs/user-guide/profiles dan https://hermes-agent.nousresearch.com/docs/user-guide/messaging/telegram
4. Penyedia model dan FAQ (dokumentasi resmi): https://hermes-agent.nousresearch.com/docs/integrations/providers dan https://hermes-agent.nousresearch.com/docs/reference/faq
5. Ringkasan fitur: https://www.truefoundry.com/blog/what-is-hermes-agent dan https://userorbit.com/blog/getting-started-with-hermes-agent
6. Daftar rilis: https://releases.sh/nousresearch/hermes-agent.md dan https://newreleases.io/project/github/NousResearch/hermes-agent/release/v2026.9.7
7. Bot Mode v0.21: https://blog.meetneura.ai/hermes-agent-v0-21-bot-mode/ dan https://runtimewire.com/article/nous-research-hermes-agent-pantheon-bot-mode
8. Keamanan: https://www.hostinger.com/tutorials/hermes-agent-security/ , https://labs.cloudsecurityalliance.org/research/csa-research-note-hermes-agent-cves-20260504-csa-styled/ , https://airq.adversa.ai/agent/hermes-agent
9. Biaya: https://www.dreamhost.com/guides/hermes-agent/hermes-agent-monthly-cost/ dan https://www.fast.io/resources/hermes-agent-pricing.md
10. Jalur terkelola: https://www.hostinger.com/managed-hermes-agent
11. Prompting Claude: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
12. Paket Claude: https://claude.com/pricing (belum dibaca langsung), ringkasan di https://krater.ai/blog/claude-pricing
13. Profil MFA: https://glints.com/companies/myfundaction-indonesia/809ad27e-9f95-4f74-bfb1-8047c336c2f5 dan https://www.eventbrite.com.au/o/myfundaction-62715133253
14. SKKNI AI 2026: https://veritask.ai/id/artikel/keputusan-menteri-ketenagakerjaan-nomor-103-tahun-2026-menetapkan-standar-kompetensi-ai-generatif-dan-mewajibkan-penyesuaian-sertifikasi-kompetensi-dalam-6-bulan
