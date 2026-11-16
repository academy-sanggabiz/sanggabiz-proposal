"""Sumber tunggal isi silabus pelatihan AI Agent MyFundAction.

Dipakai oleh build_silabus_xlsx.py, build_deck.py, dan build_aset_docx.py
supaya isi xlsx, slide, dan docx selalu sama. Ubah isi di sini, lalu jalankan ulang
ketiga skrip.
"""

PROGRAM = {
    "judul": "Pelatihan AI Agent untuk Tim CRM dan Marketing",
    "klien": "MyFundAction",
    "kontak": "Arief, Assistant CMO",
    "peserta": "Tim CRM dan marketing MyFundAction Jakarta, kurang dari 10 orang. Tim Malaysia dan Australia dapat bergabung daring bila dikonfirmasi klien",
    "level": "Pemula. Tidak memerlukan kemampuan pemrograman",
    "bahasa": "Bahasa Indonesia. Templat prompt dan slide inti disiapkan juga dalam bahasa Inggris bila tim Malaysia dan Australia ikut",
    "versi": "v2, 16 November 2026",
}

METODE = [
    ("ADDIE", "Alur program dari asesmen kebutuhan sampai evaluasi (tahap 1 sampai 6 di alur program)"),
    ("Andragogi", "Peserta belajar dari pekerjaannya sendiri: latihan memakai kasus program Palestina, masjid, dan air bersih, trainer berperan sebagai fasilitator"),
    ("Taksonomi Bloom revisi", "Tujuan tiap topik ditulis dengan kata kerja terukur, kode C1 sampai C6"),
    ("Kirkpatrick", "Evaluasi level 1 sampai 3: survei kepuasan, pre-test dan post-test dengan rubrik prompt, dan pemantauan penerapan 30 hari"),
]

# Proses bisnis program (ATURAN-PROPOSAL bagian 4a)
ALUR = [
    ("1", "Asesmen kebutuhan dan cek perangkat", "Formulir daring untuk peserta: peran, tugas harian, pengalaman AI, jenis laptop, hak admin, akun Claude dan Telegram. Tiga contoh prompt yang biasa dipakai peserta dikumpulkan untuk pre-test", "Peta peserta dan daftar kesiapan perangkat"),
    ("2", "Penyesuaian modul dan studi kasus", "Contoh kasus disusun dari program Palestina, masjid, dan air bersih untuk audiens Indonesia, Malaysia, dan Australia. Data latihan rekaan dibuat", "Modul, lembar kerja, pustaka prompt, data latihan"),
    ("3", "Persiapan teknis", "Kunci API latihan dengan batas belanja, server latihan Hermes dengan 3 agen contoh, grup Telegram latihan, uji instalasi di laptop peserta H-2", "Lingkungan latihan siap dan teruji"),
    ("4", "Pelaksanaan pelatihan", "Skema A (1 hari) atau Skema B (4 sesi x 2 jam), luring di Jakarta dengan opsi daring untuk Malaysia dan Australia", "Hasil praktik peserta, skor pre-test dan post-test"),
    ("5", "Klinik pendampingan", "Satu sesi daring 60 menit sekitar 1 sampai 2 minggu setelah pelatihan untuk masalah instalasi dan penerapan agen pertama", "Agen pertama tiap tim berjalan"),
    ("6", "Evaluasi dan laporan", "Analisis pre-test dan post-test, rubrik prompt per negara, survei kepuasan, rekomendasi lanjutan", "Laporan akhir"),
]

# Rubrik 6 unsur prompt. Dipakai di M3, pre-test, post-test, dan pustaka prompt.
RUBRIK = [
    ("Konteks", "Context", "Siapa kita, untuk siapa hasilnya, dan mengapa tugas ini dikerjakan", "Tidak ada konteks", "Konteks umum, misalnya 'untuk donatur'", "Konteks lengkap: organisasi, program, negara audiens, tujuan"),
    ("Tugas", "Task", "Satu kalimat perintah yang jelas dengan kata kerja", "Tugas kabur atau lebih dari satu tanpa urutan", "Tugas jelas tetapi lingkupnya terbuka", "Tugas jelas, terukur, dan berurutan bila lebih dari satu"),
    ("Bahan", "Input", "Data, dokumen, atau fakta yang harus dipakai AI, dipisah dengan tag", "Tidak ada bahan, AI menebak", "Bahan ada tetapi bercampur dengan instruksi", "Bahan lengkap dan dipisah dengan tag seperti <data>"),
    ("Aturan", "Rules", "Batasan: nada, panjang, larangan, fakta yang tidak boleh dikarang", "Tidak ada aturan", "Satu atau dua aturan umum", "Aturan spesifik, termasuk larangan mengarang angka dampak"),
    ("Contoh", "Examples", "Satu sampai tiga contoh hasil yang baik", "Tidak ada contoh", "Satu contoh", "Dua atau tiga contoh beragam dalam tag <contoh>"),
    ("Format", "Output format", "Bentuk hasil: tabel, poin, panjang, bahasa", "Tidak disebut", "Disebut umum, misalnya 'singkat'", "Disebut rinci: bentuk, panjang, bahasa, kolom tabel"),
]

# Modul inti. Menit topik sama di Skema A dan Skema B.
# Tiap topik: kode, judul, menit, tujuan (Bloom), outline, aktivitas (menit, langkah), alat, output, ukuran, format
MODUL = [
    {
        "kode": "M1",
        "judul": "Introduction to AI",
        "judul_id": "Pengenalan AI",
        "fokus": "Peserta memahami apa yang bisa dan tidak bisa dikerjakan AI generatif di pekerjaan CRM dan marketing MFA.",
        "prasyarat": "Bisa memakai laptop dan peramban. Tidak perlu pengalaman AI",
        "topik": [
            {
                "kode": "1.1",
                "judul": "Cara kerja AI generatif",
                "menit": 15,
                "tujuan": "C2 Menjelaskan cara kerja model bahasa besar (LLM) dengan bahasa sendiri, termasuk alasan AI bisa salah dengan yakin",
                "outline": [
                    "AI, machine learning, dan AI generatif: perbedaannya dalam satu gambar",
                    "LLM menebak kata berikutnya dari pola, bukan mencari di basis data",
                    "Halusinasi: jawaban yakin yang salah, dan contohnya pada angka donasi",
                    "Perkembangan 2024 sampai 2026: dari chatbot ke agen yang memakai alat",
                ],
                "aktivitas": [
                    (5, "Trainer menampilkan dua jawaban AI atas pertanyaan yang sama, satu benar dan satu mengarang. Peserta menebak mana yang dikarang"),
                    (7, "Trainer menjelaskan cara kerja LLM dengan slide dan analogi pelengkap otomatis di ponsel"),
                    (3, "Peserta menulis satu kalimat di lembar kerja: 'AI bisa salah karena ...'"),
                ],
                "alat": "Slide, Claude di layar trainer, lembar kerja halaman 1",
                "output": "Kalimat penjelasan cara kerja AI di lembar kerja",
                "ukuran": "Minimal 80 persen peserta menulis penjelasan yang menyebut 'menebak pola' atau setara",
                "format": "Teori, Demo",
            },
            {
                "kode": "1.2",
                "judul": "Peta pemakaian AI di pekerjaan MFA",
                "menit": 20,
                "tujuan": "C4 Memilah tugas harian ke dalam tiga kelompok: cocok untuk AI, cocok dengan pemeriksaan manusia, dan tidak untuk AI",
                "outline": [
                    "Tugas CRM, iklan, marketing, dan analisis yang lazim dibantu AI",
                    "Batas: data pribadi donatur (UU 27 Tahun 2022 tentang Pelindungan Data Pribadi), angka dampak program, keputusan yang menyangkut uang",
                    "Aturan dasar: AI membuat draf, manusia memeriksa dan memutuskan",
                ],
                "aktivitas": [
                    (8, "Peserta menulis 5 tugas yang paling menyita waktu minggu lalu di kartu tempel, satu tugas satu kartu"),
                    (7, "Peserta menempel kartu di papan tiga kolom: hijau (AI), kuning (AI dengan pemeriksaan), merah (bukan untuk AI). Peserta daring memakai papan Miro atau Google Jamboard pengganti"),
                    (5, "Trainer membahas kartu yang diperdebatkan dan menandai 3 tugas yang dipakai sebagai latihan di Modul 7"),
                ],
                "alat": "Kartu tempel tiga warna, papan, papan daring, lembar kerja halaman 1",
                "output": "Peta tugas tim: daftar tugas per kolom hijau, kuning, merah",
                "ukuran": "Setiap peserta menempatkan minimal 5 tugas. Tidak ada tugas yang memuat data pribadi donatur di kolom hijau",
                "format": "Diskusi, Praktik kelompok",
            },
        ],
    },
    {
        "kode": "M2",
        "judul": "Claude AI Utilization",
        "judul_id": "Memakai Claude untuk pekerjaan",
        "fokus": "Peserta memakai Claude untuk tiga tugas nyata dan memeriksa hasilnya.",
        "prasyarat": "Akun Claude aktif sebelum sesi (lihat daftar persiapan)",
        "topik": [
            {
                "kode": "2.1",
                "judul": "Mengenal Claude dan fiturnya",
                "menit": 20,
                "tujuan": "C3 Menggunakan fitur dasar Claude: percakapan, unggah berkas, Projects, dan riwayat",
                "outline": [
                    "Antarmuka Claude di web, desktop, dan ponsel",
                    "Memilih model dan kapan memakai model yang lebih kuat",
                    "Unggah berkas: PDF, gambar, dan tabel",
                    "Projects: instruksi tetap dan berkas pengetahuan yang dipakai berulang",
                    "Pengaturan privasi akun dan apa yang tidak diunggah",
                ],
                "aktivitas": [
                    (8, "Trainer mendemonstrasikan percakapan, unggah PDF profil program air bersih, dan membuat Project 'Latihan MFA'"),
                    (10, "Peserta mengikuti langkah yang sama di laptop masing-masing dengan panduan di lembar kerja halaman 2"),
                    (2, "Peserta menandai checklist: akun aktif, berkas terunggah, Project terbuat"),
                ],
                "alat": "Laptop peserta, akun Claude, PDF profil program (bahan latihan), lembar kerja halaman 2",
                "output": "Project 'Latihan MFA' di akun Claude tiap peserta",
                "ukuran": "Semua peserta berhasil membuat Project dan mengunggah satu berkas",
                "format": "Demo, Praktik",
            },
            {
                "kode": "2.2",
                "judul": "Praktik Claude untuk tugas CRM dan marketing",
                "menit": 40,
                "tujuan": "C3 Menerapkan Claude untuk meringkas dokumen, menyusun draf pesan donatur, dan mengolah tabel. C5 Menilai hasilnya dengan daftar periksa",
                "outline": [
                    "Tugas A: ringkas laporan program Palestina menjadi 5 poin untuk donatur",
                    "Tugas B: draf pesan terima kasih donatur program masjid dalam bahasa Indonesia dan Inggris",
                    "Tugas C: unggah data kampanye rekaan, minta tabel ringkas per negara",
                    "Daftar periksa hasil AI: fakta, angka, nada, bahasa, data pribadi",
                ],
                "aktivitas": [
                    (5, "Trainer membagikan bahan tiga tugas di folder bersama dan menjelaskan daftar periksa"),
                    (25, "Peserta berpasangan mengerjakan tugas A, B, dan C di Claude. Trainer dan asisten berkeliling, peserta daring dibantu di ruang breakout"),
                    (10, "Dua pasangan menampilkan hasil. Kelas memeriksa dengan daftar periksa dan menunjukkan satu kesalahan AI yang ditemukan"),
                ],
                "alat": "Laptop, Claude, bahan latihan (laporan program rekaan, data-latihan/kampanye-iklan-rekaan.csv), daftar periksa di lembar kerja halaman 3",
                "output": "Tiga hasil kerja: ringkasan, draf pesan dua bahasa, tabel ringkas per negara",
                "ukuran": "Setiap pasangan menyelesaikan minimal 2 dari 3 tugas dan mengisi daftar periksa",
                "format": "Praktik berpasangan",
            },
        ],
    },
    {
        "kode": "M3",
        "judul": "Prompt Engineering",
        "judul_id": "Menyusun prompt dan Standar Prompt MFA",
        "fokus": "Peserta menulis prompt dengan 6 unsur yang sama di Indonesia, Malaysia, dan Australia, dan mengukurnya dengan rubrik.",
        "prasyarat": "Mengikuti Modul 2",
        "topik": [
            {
                "kode": "3.1",
                "judul": "Enam unsur prompt dan teknik dasar",
                "menit": 30,
                "tujuan": "C2 Menjelaskan enam unsur prompt (Konteks, Tugas, Bahan, Aturan, Contoh, Format). C3 Menerapkan tag XML, contoh, dan permintaan berpikir dulu",
                "outline": [
                    "Enam unsur prompt dan rubrik skor 0 sampai 12",
                    "Memisahkan bahan dengan tag, misalnya <data> dan <contoh>",
                    "Memberi 1 sampai 3 contoh agar gaya hasil konsisten",
                    "Meminta AI berpikir dulu untuk tugas analisis",
                    "Iterasi: memperbaiki prompt dari hasil, bukan mengulang pertanyaan yang sama",
                ],
                "aktivitas": [
                    (10, "Trainer menjalankan prompt satu baris dan prompt 6 unsur untuk tugas yang sama, lalu membandingkan hasilnya di layar"),
                    (10, "Trainer menjelaskan tiap unsur dengan contoh program air bersih"),
                    (10, "Peserta menulis ulang prompt tugas B dari Modul 2 memakai 6 unsur, lalu menjalankannya"),
                ],
                "alat": "Slide, Claude, kartu 6 unsur (pustaka prompt halaman 1), lembar kerja halaman 4",
                "output": "Satu prompt 6 unsur milik peserta dan hasilnya",
                "ukuran": "Prompt peserta memuat minimal 5 dari 6 unsur",
                "format": "Teori, Demo, Praktik",
            },
            {
                "kode": "3.2",
                "judul": "Bedah dan perbaiki prompt",
                "menit": 30,
                "tujuan": "C5 Menilai prompt dengan rubrik 6 unsur. C6 Menyusun versi perbaikan yang skornya naik",
                "outline": [
                    "Membaca rubrik: skor 0, 1, dan 2 per unsur",
                    "Kesalahan yang sering muncul: tanpa konteks negara, tanpa larangan mengarang angka, format tidak disebut",
                    "Mengukur perbaikan: skor sebelum dan sesudah, mutu hasil sebelum dan sesudah",
                ],
                "aktivitas": [
                    (5, "Trainer membagikan 3 prompt nyata peserta dari formulir asesmen tanpa nama"),
                    (15, "Kelompok 2 sampai 3 orang memberi skor tiap prompt dengan rubrik, lalu menulis versi perbaikan"),
                    (10, "Kelompok menjalankan prompt lama dan baru di Claude dan menampilkan perbedaan hasil"),
                ],
                "alat": "Rubrik cetak, prompt asesmen tanpa nama, Claude, lembar kerja halaman 5",
                "output": "Tiga prompt perbaikan dengan skor sebelum dan sesudah",
                "ukuran": "Rata-rata skor prompt perbaikan minimal 9 dari 12",
                "format": "Praktik kelompok",
            },
            {
                "kode": "3.3",
                "judul": "Standar Prompt MFA lintas negara",
                "menit": 30,
                "tujuan": "C6 Menyusun templat prompt bersama untuk tugas yang sering dipakai tim Indonesia, Malaysia, dan Australia",
                "outline": [
                    "Mengapa hasil AI berbeda antarnegara: prompt berbeda, konteks audiens berbeda, contoh berbeda",
                    "Isi standar: templat 6 unsur, glosarium nama program dalam tiga bahasa, aturan nada dan etika penggalangan dana",
                    "Tempat menyimpan: satu Claude Project bersama atau folder bersama yang dipakai ketiga tim",
                    "Lokalisasi: program masjid untuk audiens Australia berbeda nadanya dengan audiens Indonesia",
                ],
                "aktivitas": [
                    (5, "Trainer menunjukkan pustaka prompt contoh dan glosarium"),
                    (20, "Tiap kelompok memilih satu tugas dari peta tugas di Modul 1 dan menyusun templat dalam bahasa Indonesia dan Inggris, termasuk tempat isian {nama_program} dan {negara}"),
                    (5, "Templat dikumpulkan ke folder bersama dan menjadi draf Standar Prompt MFA"),
                ],
                "alat": "Pustaka prompt, glosarium, folder bersama atau Claude Project, lembar kerja halaman 6",
                "output": "Draf Standar Prompt MFA: minimal 3 templat dua bahasa",
                "ukuran": "Setiap templat lolos rubrik dengan skor minimal 10 dari 12",
                "format": "Praktik kelompok, Diskusi",
            },
        ],
    },
    {
        "kode": "M4",
        "judul": "Introduction to AI Agent",
        "judul_id": "Pengenalan AI Agent",
        "fokus": "Peserta membedakan chatbot dan AI Agent, dan memilih tugas yang layak dijadikan agen.",
        "prasyarat": "Mengikuti Modul 1 sampai 3",
        "topik": [
            {
                "kode": "4.1",
                "judul": "Chatbot dan AI Agent",
                "menit": 25,
                "tujuan": "C2 Membedakan chatbot dan AI Agent. C4 Menganalisis tugas yang cocok dijadikan agen dengan empat pertanyaan",
                "outline": [
                    "Chatbot menjawab satu permintaan. Agen bekerja dalam putaran: tujuan, rencana, memakai alat, memeriksa hasil, mengingat",
                    "Komponen agen: model, instruksi, alat, memori, jadwal, saluran komunikasi",
                    "Multi-agen: beberapa agen dengan peran berbeda saling mengirim hasil",
                    "Empat pertanyaan sebelum membuat agen: berulang, ada aturan jelas, ada data yang boleh dipakai, ada orang yang memeriksa",
                    "Risiko: agen bertindak tanpa diperiksa, biaya API, dan data bocor",
                ],
                "aktivitas": [
                    (8, "Trainer memperagakan tugas yang sama dua kali: lewat chat Claude dan lewat agen yang membaca berkas, menghitung, lalu mengirim ringkasan ke Telegram"),
                    (7, "Trainer menjelaskan komponen agen dengan diagram"),
                    (10, "Peserta menguji 3 tugas dari peta tugas Modul 1 dengan empat pertanyaan dan memilih satu calon agen"),
                ],
                "alat": "Slide diagram agen, Hermes di server latihan, Telegram, lembar kerja halaman 7",
                "output": "Satu calon agen per peserta dengan jawaban empat pertanyaan",
                "ukuran": "Setiap peserta memilih satu calon agen yang menjawab 'ya' pada keempat pertanyaan",
                "format": "Teori, Demo, Praktik",
            },
        ],
    },
    {
        "kode": "M5",
        "judul": "Introduction to Hermes",
        "judul_id": "Mengenal Hermes Agent",
        "fokus": "Peserta mengenali bagian-bagian Hermes Agent dan melihat tiga agen bekerja sama.",
        "prasyarat": "Mengikuti Modul 4",
        "topik": [
            {
                "kode": "5.1",
                "judul": "Bagian-bagian Hermes dan demo tiga agen",
                "menit": 25,
                "tujuan": "C2 Menjelaskan fungsi SOUL.md, memori, skill, profil, gateway, dan jadwal di Hermes. C4 Menelusuri alur kerja tiga agen dalam satu grup",
                "outline": [
                    "Hermes Agent dari Nous Research: sumber terbuka, berjalan di komputer atau server sendiri, memakai model pilihan",
                    "SOUL.md sebagai identitas dan aturan agen",
                    "Memori (MEMORY.md dan USER.md) dan skill yang dipakai ulang",
                    "Profil: satu profil satu agen. Gateway: agen menerima pesan dari Telegram, WhatsApp, atau Slack",
                    "Jadwal: agen bekerja otomatis, misalnya laporan tiap Senin",
                    "Bot Mode: beberapa agen bernama di satu grup dan saling mengirim pesan",
                ],
                "aktivitas": [
                    (10, "Trainer menampilkan grup Telegram latihan berisi 3 agen: Agen CRM, Agen Iklan, Agen Analis. Trainer meminta laporan kampanye, Agen Analis menghitung, Agen Iklan mengusulkan perbaikan iklan, Agen CRM menyusun draf pesan donatur"),
                    (10, "Trainer membuka folder profil tiap agen dan menunjukkan SOUL.md, skill, dan jadwalnya"),
                    (5, "Peserta menggambar alur pesan tiga agen di lembar kerja dan menandai titik pemeriksaan manusia"),
                ],
                "alat": "Server latihan Hermes, grup Telegram latihan, slide, lembar kerja halaman 8",
                "output": "Diagram alur tiga agen dengan titik pemeriksaan manusia",
                "ukuran": "Peserta menandai minimal satu titik pemeriksaan sebelum pesan dikirim ke donatur",
                "format": "Demo, Teori",
            },
        ],
    },
    {
        "kode": "M6",
        "judul": "Hermes Setup and Configuration",
        "judul_id": "Instalasi dan konfigurasi Hermes",
        "fokus": "Peserta memasang Hermes, menyambungkannya ke model, dan menjalankan agen pertamanya dengan pengaturan aman.",
        "prasyarat": "Cek perangkat H-2 selesai: laptop dengan hak admin, Git terpasang, WSL2 aktif untuk Windows, akun Telegram, kunci API latihan",
        "topik": [
            {
                "kode": "6.1",
                "judul": "Instalasi dan wizard setup",
                "menit": 30,
                "tujuan": "C3 Memasang Hermes dan menyelesaikan wizard setup sampai agen menjawab di terminal",
                "outline": [
                    "Mengenal terminal: membuka, menyalin perintah, membaca pesan galat",
                    "Instalasi macOS dan Windows (WSL2) dengan satu perintah",
                    "hermes setup: memilih penyedia model, memasukkan kunci API latihan, memilih model",
                    "hermes doctor untuk memeriksa masalah",
                ],
                "aktivitas": [
                    (5, "Trainer membuka terminal di layar dan menjelaskan tiga hal: tempel perintah, tekan Enter, baca baris terakhir"),
                    (20, "Peserta mengikuti Panduan Setup Hermes langkah 1 sampai 4. Trainer memandu di layar, asisten membantu peserta yang tertahan. Peserta yang laptopnya belum siap memakai akun di server latihan"),
                    (5, "Peserta mengetik 'halo, siapa kamu' dan menjalankan hermes doctor. Hasil ditandai di checklist"),
                ],
                "alat": "Laptop peserta, Panduan Setup Hermes, kunci API latihan dengan batas belanja, server latihan cadangan",
                "output": "Hermes terpasang dan menjawab di terminal",
                "ukuran": "Minimal 80 persen peserta selesai di laptop sendiri. Sisanya selesai di server latihan dan dijadwalkan di klinik",
                "format": "Demo, Praktik terbimbing",
            },
            {
                "kode": "6.2",
                "judul": "Agen pertama: SOUL.md, Telegram, dan pengaturan aman",
                "menit": 35,
                "tujuan": "C3 Mengonfigurasi identitas agen dan saluran Telegram. C5 Memeriksa pengaturan keamanan dengan daftar periksa",
                "outline": [
                    "Mengisi SOUL.md dari templat: peran, audiens, aturan, hal yang dilarang",
                    "Membuat bot Telegram lewat BotFather dan menghubungkannya dengan hermes gateway setup",
                    "Membatasi siapa yang boleh mengirim pesan ke agen",
                    "Persetujuan perintah tetap aktif, mode YOLO tidak dipakai",
                    "Batas belanja kunci API dan data rekaan untuk latihan",
                ],
                "aktivitas": [
                    (10, "Peserta menyalin templat SOUL agen sesuai calon agennya dari Modul 4 dan mengisi bagian bertanda"),
                    (15, "Peserta membuat bot Telegram dan menjalankan hermes gateway setup dengan panduan langkah 5 sampai 7"),
                    (10, "Peserta mengirim pesan dari Telegram, lalu memeriksa 5 butir daftar periksa keamanan bersama trainer"),
                ],
                "alat": "Templat SOUL (aset/hermes-templat), Telegram di ponsel, Panduan Setup Hermes, daftar periksa keamanan",
                "output": "Agen pertama yang menjawab lewat Telegram dengan SOUL.md sendiri",
                "ukuran": "Agen menjawab di Telegram dan kelima butir daftar periksa keamanan terpenuhi",
                "format": "Praktik terbimbing",
            },
        ],
    },
    {
        "kode": "M7",
        "judul": "AI Agent Implementation",
        "judul_id": "Penerapan AI Agent untuk CRM, iklan, marketing, dan analisis",
        "fokus": "Peserta menjalankan agen untuk tiga alur kerja MFA dengan data rekaan dan menyusun rencana penerapan 30 hari.",
        "prasyarat": "Agen pertama berjalan (Modul 6) atau akses ke server latihan",
        "topik": [
            {
                "kode": "7.1",
                "judul": "Agen CRM: segmentasi donatur dan tindak lanjut",
                "menit": 25,
                "tujuan": "C3 Menjalankan agen untuk mengelompokkan donatur rekaan. C5 Memeriksa draf pesan tindak lanjut sebelum dikirim",
                "outline": [
                    "Segmen sederhana: donatur baru, donatur rutin, donatur yang lama tidak berdonasi",
                    "Draf pesan per segmen dan per bahasa, hanya untuk donatur yang setuju dihubungi",
                    "Pemeriksaan manusia sebelum pesan keluar",
                ],
                "aktivitas": [
                    (5, "Trainer memberi berkas donatur-rekaan.csv dan prompt templat CRM dari pustaka"),
                    (15, "Peserta meminta agen menghitung jumlah donatur per segmen dan menyusun draf pesan untuk dua segmen"),
                    (5, "Peserta memeriksa draf dengan daftar periksa dan mencatat satu perbaikan"),
                ],
                "alat": "Hermes (laptop atau server latihan), data-latihan/donatur-rekaan.csv, pustaka prompt templat CRM",
                "output": "Tabel segmen donatur dan dua draf pesan tindak lanjut yang sudah diperiksa",
                "ukuran": "Jumlah per segmen cocok dengan kunci jawaban trainer. Draf tidak menyapa donatur yang menolak dihubungi",
                "format": "Praktik",
            },
            {
                "kode": "7.2",
                "judul": "Agen iklan dan marketing: brief dan variasi iklan",
                "menit": 25,
                "tujuan": "C6 Menyusun brief dan variasi teks iklan program masjid untuk audiens Australia dan Indonesia dengan bantuan agen",
                "outline": [
                    "Brief iklan: tujuan, audiens, pesan utama, ajakan, larangan klaim",
                    "Lokalisasi nada untuk Australia, Malaysia, dan Indonesia",
                    "Aturan etika penggalangan dana: tidak mengarang angka dampak, tidak melebih-lebihkan",
                ],
                "aktivitas": [
                    (5, "Trainer menjelaskan brief contoh untuk program air bersih"),
                    (15, "Peserta meminta Agen Iklan menyusun brief dan 3 variasi teks iklan program masjid untuk Australia dan 3 untuk Indonesia"),
                    (5, "Pasangan saling memeriksa variasi dengan aturan etika dan memilih satu terbaik per negara"),
                ],
                "alat": "Hermes, templat SOUL Agen Iklan, pustaka prompt templat iklan, glosarium",
                "output": "Brief iklan dan 6 variasi teks iklan, 2 terpilih",
                "ukuran": "Tidak ada variasi terpilih yang memuat angka dampak tanpa sumber",
                "format": "Praktik berpasangan",
            },
            {
                "kode": "7.3",
                "judul": "Agen analis: laporan kampanye terjadwal dan kerja tiga agen",
                "menit": 25,
                "tujuan": "C4 Menganalisis kinerja kampanye per negara dan program dengan agen. C3 Menjadwalkan laporan mingguan yang dikirim ke Telegram",
                "outline": [
                    "Ukuran kampanye: biaya, klik, CTR, jumlah donasi, biaya per donasi",
                    "Meminta agen menghitung dan menjelaskan, lalu mengecek satu angka secara manual",
                    "Membuat jadwal laporan setiap Senin pukul 09.00",
                    "Alur tiga agen: Analis memberi angka, Iklan memberi usulan, CRM memberi draf pesan, manusia memutuskan",
                ],
                "aktivitas": [
                    (10, "Peserta meminta agen menganalisis kampanye-iklan-rekaan.csv dan menjawab: program dan negara mana yang biaya per donasinya paling rendah"),
                    (5, "Peserta mengecek satu angka di spreadsheet dan membandingkan dengan jawaban agen"),
                    (10, "Peserta membuat jadwal laporan mingguan, lalu trainer menjalankan alur tiga agen di grup latihan dengan laporan itu"),
                ],
                "alat": "Hermes, data-latihan/kampanye-iklan-rekaan.csv, Google Sheets, grup Telegram latihan",
                "output": "Ringkasan analisis kampanye dan satu jadwal laporan mingguan aktif",
                "ukuran": "Angka biaya per donasi yang dicek manual sama dengan angka agen. Jadwal tercatat di daftar jadwal Hermes",
                "format": "Praktik, Demo",
            },
            {
                "kode": "7.4",
                "judul": "Rencana penerapan 30 hari",
                "menit": 15,
                "tujuan": "C6 Merancang satu agen yang akan dijalankan di pekerjaan dalam 30 hari, lengkap dengan pemilik, data, dan titik pemeriksaan",
                "outline": [
                    "Kanvas agen: tugas, pemicu, data yang boleh dipakai, alat, hasil, pemeriksa, ukuran berhasil",
                    "Urutan: uji dengan data rekaan, uji terbatas, baru dipakai rutin",
                    "Apa yang dibawa ke klinik pendampingan",
                ],
                "aktivitas": [
                    (10, "Peserta mengisi kanvas agen di lembar kerja halaman 10"),
                    (5, "Tiga peserta membacakan kanvasnya, trainer memberi satu masukan per kanvas"),
                ],
                "alat": "Kanvas agen di lembar kerja halaman 10",
                "output": "Kanvas agen 30 hari per peserta",
                "ukuran": "Kanvas terisi lengkap, ada nama pemeriksa dan ukuran berhasil",
                "format": "Praktik individu",
            },
        ],
    },
]


def total_menit_inti():
    return sum(t["menit"] for m in MODUL for t in m["topik"])


def menit_modul(m):
    return sum(t["menit"] for t in m["topik"])


# Rundown. Tiap baris: (mulai, selesai, kegiatan, keterangan)
SKEMA_A = {
    "nama": "Skema A: intensif 1 hari",
    "ringkas": "1 hari, 08.30 - 17.00 WIB, luring di Jakarta. Peserta Malaysia dapat ikut penuh secara daring (sampai 18.00 waktu Kuala Lumpur). Peserta Sydney dan Melbourne hanya terjangkau sampai sekitar 13.00 WIB (17.00 waktu setempat), sehingga melewatkan modul Hermes",
    "rundown": [
        ("08.00", "08.30", "Registrasi dan cek laptop", "Asisten memeriksa Wi-Fi, akun Claude, Telegram, dan hasil cek perangkat H-2"),
        ("08.30", "08.45", "Pembukaan, perkenalan, tujuan pelatihan", "Sambutan MFA, alur hari ini"),
        ("08.45", "08.55", "Pre-test", "10 soal pilihan ganda dan 1 tugas prompt"),
        ("08.55", "09.30", "M1 Introduction to AI", "Topik 1.1 dan 1.2"),
        ("09.30", "10.30", "M2 Claude AI Utilization", "Topik 2.1 dan 2.2"),
        ("10.30", "10.45", "Rehat", ""),
        ("10.45", "12.15", "M3 Prompt Engineering", "Topik 3.1, 3.2, 3.3"),
        ("12.15", "13.00", "Ishoma", ""),
        ("13.00", "13.25", "M4 Introduction to AI Agent", "Topik 4.1"),
        ("13.25", "13.50", "M5 Introduction to Hermes", "Topik 5.1, demo tiga agen"),
        ("13.50", "14.55", "M6 Hermes Setup and Configuration", "Topik 6.1 dan 6.2"),
        ("14.55", "15.10", "Rehat", ""),
        ("15.10", "16.40", "M7 AI Agent Implementation", "Topik 7.1 sampai 7.4"),
        ("16.40", "17.00", "Post-test, survei kepuasan, penutup", "Jadwal klinik pendampingan diumumkan"),
    ],
}

SKEMA_B = {
    "nama": "Skema B: bertahap 4 sesi x 2 jam",
    "ringkas": "4 sesi, 09.00 - 11.00 WIB (10.00 - 12.00 Kuala Lumpur, 13.00 - 15.00 Sydney), jeda 2 sampai 3 hari antarsesi. Sesi 1 dan 3 luring di Jakarta, sesi 2 dan 4 hibrida, klinik daring. Peserta Malaysia dan Australia selalu daring",
    "sesi": [
        {
            "nama": "Sesi 1: Dasar AI dan Claude",
            "bentuk": "Luring",
            "ket_bentuk": "Tim Jakarta hadir di ruang kelas kantor MFA bersama trainer dan asisten. Tim Malaysia dan Australia bergabung lewat Google Meet. Luring karena sesi pembuka, perkenalan, dan aktivitas kartu tempel",
            "rundown": [
                ("09.00", "09.10", "Pembukaan dan perkenalan", "Sambutan MFA, alur 4 sesi"),
                ("09.10", "09.20", "Pre-test", "10 soal pilihan ganda dan 1 tugas prompt"),
                ("09.20", "09.55", "M1 Introduction to AI", "Topik 1.1 dan 1.2"),
                ("09.55", "10.55", "M2 Claude AI Utilization", "Topik 2.1 dan 2.2"),
                ("10.55", "11.00", "Tugas mandiri", "Pakai Claude untuk 2 tugas kerja nyata dan catat hasilnya"),
            ],
        },
        {
            "nama": "Sesi 2: Prompt Engineering dan Standar Prompt MFA",
            "bentuk": "Hibrida",
            "ket_bentuk": "Trainer di ruang kelas. Tim Jakarta boleh hadir di ruang kelas atau ikut dari laptop masing-masing. Tim Malaysia dan Australia lewat Google Meet. Kelompok penyusun templat dicampur antarnegara di breakout room",
            "rundown": [
                ("09.00", "09.10", "Bahas tugas mandiri", "2 peserta berbagi hasil"),
                ("09.10", "10.40", "M3 Prompt Engineering", "Topik 3.1, 3.2, 3.3"),
                ("10.40", "10.55", "Cek perangkat untuk sesi 3", "Asisten memeriksa laptop: Git, WSL2 untuk Windows, Telegram"),
                ("10.55", "11.00", "Tugas mandiri", "Pakai satu templat Standar Prompt MFA di pekerjaan dan catat skornya"),
            ],
        },
        {
            "nama": "Sesi 3: AI Agent, Hermes, dan setup",
            "bentuk": "Luring",
            "ket_bentuk": "Tim Jakarta wajib hadir di ruang kelas karena instalasi Hermes di laptop masing-masing. Trainer dan asisten hadir. Peserta daring dipandu asisten lewat berbagi layar. Bila peserta daring lebih dari 3 orang, perlu satu asisten daring tambahan",
            "rundown": [
                ("09.00", "09.05", "Bahas tugas mandiri", ""),
                ("09.05", "09.30", "M4 Introduction to AI Agent", "Topik 4.1"),
                ("09.30", "09.55", "M5 Introduction to Hermes", "Topik 5.1, demo tiga agen"),
                ("09.55", "11.00", "M6 Hermes Setup and Configuration", "Topik 6.1 dan 6.2. Peserta yang belum selesai lanjut di klinik"),
            ],
        },
        {
            "nama": "Sesi 4: Penerapan dan rencana 30 hari",
            "bentuk": "Hibrida",
            "ket_bentuk": "Sama dengan sesi 2. Agen sudah terpasang, jadi praktik bisa dari meja masing-masing. Presentasi kanvas agen lewat layar bersama agar ketiga negara mengikuti",
            "rundown": [
                ("09.00", "09.10", "Cek agen peserta", "Semua agen pertama menjawab di Telegram"),
                ("09.10", "10.40", "M7 AI Agent Implementation", "Topik 7.1 sampai 7.4"),
                ("10.40", "10.50", "Post-test", "10 soal pilihan ganda dan 1 tugas prompt"),
                ("10.50", "11.00", "Survei kepuasan dan penutup", "Jadwal klinik pendampingan diumumkan"),
            ],
        },
    ],
    "antara": "Klinik setup daring 30 menit di antara sesi 3 dan 4 untuk peserta yang instalasinya belum selesai",
    "klinik": [
        ("Klinik setup", "Daring", "Di antara sesi 3 dan 4, 30 menit, lewat Google Meet dengan berbagi layar. Hanya untuk peserta yang instalasinya belum selesai"),
        ("Klinik pendampingan", "Daring", "1 sampai 2 minggu setelah sesi 4, 60 menit, lewat Google Meet. Membahas agen pertama di pekerjaan nyata"),
    ],
    "platform": "Google Meet, mengikuti platform rapat MFA. [ISI TIM: konfirmasi platform dengan MFA]",
}

HASIL = [
    ("Peta tugas tim: hijau, kuning, merah", "1.2"),
    ("Project 'Latihan MFA' di Claude", "2.1"),
    ("Ringkasan program, draf pesan dua bahasa, tabel ringkas per negara", "2.2"),
    ("Prompt 6 unsur milik peserta", "3.1"),
    ("Tiga prompt perbaikan dengan skor sebelum dan sesudah", "3.2"),
    ("Draf Standar Prompt MFA: minimal 3 templat dua bahasa", "3.3"),
    ("Calon agen dengan jawaban empat pertanyaan", "4.1"),
    ("Diagram alur tiga agen dengan titik pemeriksaan manusia", "5.1"),
    ("Hermes terpasang di laptop atau akun di server latihan", "6.1"),
    ("Agen pertama yang menjawab lewat Telegram", "6.2"),
    ("Tabel segmen donatur dan dua draf pesan tindak lanjut", "7.1"),
    ("Brief iklan dan variasi teks iklan program masjid", "7.2"),
    ("Analisis kampanye dan jadwal laporan mingguan", "7.3"),
    ("Kanvas agen 30 hari", "7.4"),
]

EVALUASI = [
    ("Level 1 Reaksi", "Survei kepuasan 8 butir di akhir pelatihan", "Rata-rata minimal 4 dari 5"),
    ("Level 2 Pembelajaran", "Pre-test dan post-test: 10 soal pilihan ganda dan 1 tugas prompt yang dinilai dengan rubrik 6 unsur", "Skor rata-rata naik. Skor prompt rata-rata minimal 9 dari 12 di post-test, dan selisih rata-rata antarnegara tidak lebih dari 2 poin bila tim Malaysia dan Australia ikut"),
    ("Level 3 Perilaku", "Klinik pendampingan dan formulir singkat 30 hari setelah pelatihan", "Minimal separuh peserta menjalankan satu agen atau satu templat Standar Prompt MFA secara rutin"),
]

PERSIAPAN = [
    ("H-5", "Formulir asesmen dan cek perangkat dikirim ke peserta", "Sanggabiz", "Formulir daring"),
    ("H-3", "Peserta membuat akun Claude dan Telegram", "Peserta, dibantu HR MFA", "Panduan singkat"),
    ("H-3", "Keputusan akun Claude: Free, Pro, atau Team", "MFA", "Lihat rekomendasi"),
    ("H-3", "Kunci API latihan per peserta dengan batas belanja", "Sanggabiz", "OpenRouter atau Anthropic Console"),
    ("H-2", "Uji instalasi Git dan WSL2 di laptop Windows, perlu hak admin", "Tim IT MFA dan asisten Sanggabiz", "Panduan Setup Hermes bagian A"),
    ("H-2", "Server latihan Hermes dengan 3 profil agen dan grup Telegram latihan", "Trainer Sanggabiz", "Templat SOUL"),
    ("H-1", "Cocokkan perintah instalasi dengan dokumentasi resmi Hermes terbaru", "Trainer Sanggabiz", "hermes-agent.nousresearch.com"),
    ("H-1", "Ruang, proyektor, Wi-Fi, dan tautan rapat daring", "MFA dan Sanggabiz", ""),
]
