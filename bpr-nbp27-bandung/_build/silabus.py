"""Isi silabus IHT Layanan Inklusif BPR NBP 27. Satu sumber untuk halaman proposal dan panduan fasilitator.

Urutan dan jam mengikuti rundown TOR bagian V. Kode aset merujuk ke isi kit (lihat KIT).
"""

# Isi kit: (no, nama berkas, untuk siapa, dipakai di)
KIT = [
    ("00", "Panduan Fasilitator", "Tim Sanggabiz", "Sebelum, selama, dan sesudah kelas"),
    ("01", "Ringkasan Regulasi dan SOP Layanan Disabilitas", "Peserta", "Modul 1, lalu dipakai di loket"),
    ("02", "Kartu Saku Isyarat Perbankan", "Peserta", "Modul 3 dan 6"),
    ("03", "Lembar Praktik Pemanduan dan Kursi Roda", "Peserta (berpasangan)", "Modul 2 dan 4"),
    ("04", "Kartu Skenario Role-Play", "Peserta dan peraga", "Modul 6"),
    ("05", "Rubrik Observasi Layanan", "Kasie Operasional dan trainer", "Modul 6, lalu di kantor"),
    ("06", "Pre-Test dan Post-Test", "Peserta", "Awal dan akhir hari"),
    ("07", "Contoh Formulir Pembacaan Slip dan Kesaksian Cap Jempol", "Teller, CS, Kasie", "Modul 5"),
    ("08", "Lembar Audit Aksesibilitas Kantor", "Kelompok peserta", "Modul 4, bahan laporan"),
    ("09", "Contoh Sertifikat Pelatihan", "Peserta", "Sesudah kelas"),
    ("10", "Draf Contoh Laporan Evaluasi Program", "Manajemen BPR", "Sesudah kelas"),
    ("11", "Rekap Nilai dan Rubrik (Excel)", "Tim Sanggabiz", "Sesudah kelas, bahan laporan"),
]

# Ringkasan rundown: (jam, sesi, menit, metode, hasil)
RINGKAS = [
    ("08.30 - 08.45", "Pembukaan dan pembagian peran", 15, "Pengarahan", "Peserta tahu perannya di tiap simulasi"),
    ("08.45 - 09.00", "Pre-test", 15, "Tes tertulis 15 soal", "Nilai awal per peserta"),
    ("09.00 - 09.30", "Modul 1. Regulasi POJK 22/2023 dan Pedoman SETARA", 30, "Pemaparan dan kuis kartu", "Daftar bukti audit yang disimpan BPR"),
    ("09.30 - 10.15", "Modul 2. Etiket dan pemanduan nasabah netra", 45, "Praktik berpasangan", "Lembar praktik pemanduan terisi"),
    ("10.30 - 12.00", "Modul 3. Komunikasi inklusif dan isyarat dasar perbankan", 90, "Drill dan loket tanpa suara", "Kartu saku isyarat dengan catatan peragaan"),
    ("13.00 - 14.00", "Modul 4. Kursi roda, ramp, dan tata letak loket", 60, "Praktik dan audit ruang layanan", "Lembar audit aksesibilitas terisi"),
    ("14.00 - 15.00", "Modul 5. Legalitas transaksi, warkat, dan administrasi", 60, "Simulasi bertiga", "Tiga set berkas simulasi lengkap"),
    ("15.15 - 16.30", "Modul 6. Simulasi terpadu, post-test, dan penutupan", 75, "Role-play lima skenario", "Rubrik observasi dan nilai post-test"),
]

# Detail per modul untuk tabel kurikulum
MODUL = [
    {
        "no": "Modul 1",
        "judul": "Regulasi POJK 22/2023 dan Pedoman SETARA OJK",
        "jam": "09.00 - 09.30 (30 menit, satu-satunya sesi teori)",
        "tujuan": "Peserta mampu menjelaskan (C2) kewajiban layanan inklusif BPR menurut POJK 22/2023 dan Pedoman SETARA, dan menyebutkan (C1) bukti yang disimpan untuk pemeriksaan OJK.",
        "materi": [
            "Kewajiban PUJK kepada konsumen penyandang disabilitas dalam POJK 22/2023",
            "Isi Pedoman SETARA: aksesibilitas fisik dan digital, sensitivitas layanan",
            "Ragam disabilitas menurut UU 8/2016: fisik, intelektual, mental, sensorik",
            "Risiko bila layanan ditolak atau transaksi tidak sah: keluhan, sengketa, temuan pemeriksaan",
            "Bukti yang disimpan: sertifikat, daftar hadir, formulir pembacaan slip, log keluhan",
        ],
        "aktivitas": [
            "Menit 0-5: trainer membuka dengan satu kasus rekaan, nasabah netra diminta datang lagi dengan keluarga untuk membuka rekening.",
            "Menit 5-20: pemaparan enam slide. Peserta menandai daftar bukti di aset 01.",
            "Menit 20-30: kuis kartu. Trainer membacakan enam situasi, peserta mengangkat kartu Boleh atau Tidak, lalu satu peserta menjelaskan alasannya.",
        ],
        "alat": "Slide, aset 01 Ringkasan Regulasi, kartu Boleh dan Tidak",
        "indikator": "Peserta menjawab benar minimal 5 dari 6 situasi kuis kartu",
        "output": "Daftar bukti audit yang ditandai di aset 01",
    },
    {
        "no": "Modul 2",
        "judul": "Etiket dan pemanduan nasabah netra (sighted guide)",
        "jam": "09.30 - 10.15 (45 menit)",
        "tujuan": "Peserta mampu memperagakan (C3) cara menyambut nasabah disabilitas dan memandu nasabah netra dari pintu masuk sampai duduk di depan meja layanan.",
        "materi": [
            "Menyapa, menyebut nama dan jabatan, bertanya sebelum membantu",
            "Bicara langsung kepada nasabah, bukan kepada pendamping",
            "Bahasa deskriptif: arah jarum jam, jumlah langkah, nama benda",
            "Teknik pemanduan: posisi lengan, setengah langkah di depan, lorong selebar satu orang, pintu, tangga, kursi",
            "Tongkat dan anjing pemandu tidak disentuh tanpa izin pemiliknya",
        ],
        "aktivitas": [
            "Menit 0-10: peraga netra dan trainer memperagakan rute dari pintu ke kursi CS.",
            "Menit 10-35: berpasangan. Satu peserta memakai penutup mata, satu memandu lewat rute empat titik bertanda lakban (pintu, undakan, lorong antrean, kursi), lalu tukar peran. Pasangan lain mencentang aset 03 bagian A.",
            "Menit 35-45: peraga netra memberi umpan balik kepada tiap pasangan dan memaraf lembar praktik.",
        ],
        "alat": "Penutup mata 10 buah, tongkat putih, lakban warna, aset 03",
        "indikator": "Setiap peserta menyelesaikan rute empat titik dan semua butir wajib di aset 03 bagian A tercentang",
        "output": "Lembar praktik pemanduan terisi dan diparaf peraga netra",
    },
    {
        "no": "Modul 3",
        "judul": "Komunikasi inklusif dan isyarat dasar perbankan",
        "jam": "10.30 - 12.00 (90 menit)",
        "tujuan": "Peserta mampu memperagakan (C3) abjad jari, angka, dan 20 kosakata isyarat loket, lalu melayani (C3) satu transaksi dengan nasabah Tuli memakai isyarat, tulisan, dan gerak bibir.",
        "materi": [
            "Budaya Tuli, beda BISINDO dan SIBI, alasan memakai BISINDO",
            "Menarik perhatian, posisi berhadapan, cahaya, mulut tidak ditutup masker atau tangan",
            "Abjad jari dan angka 0 sampai 9, ribu, juta",
            "Kosakata loket: salam, rekening, setor, tarik, formulir, tanda tangan, ATM, buku tabungan",
            "Komunikasi tulisan dengan papan tulis genggam dan kalimat pendek",
            "Melayani nasabah yang datang dengan juru bahasa isyarat atau pendamping",
        ],
        "aktivitas": [
            "Menit 0-15: co-trainer Tuli memperkenalkan diri dengan isyarat, trainer menerjemahkan. Peserta menebak isinya.",
            "Menit 15-40: drill abjad jari dan angka. Tiap peserta mengeja namanya dan satu nomor rekening 10 digit.",
            "Menit 40-65: drill kosakata loket per lima kata. Co-trainer mengoreksi bentuk tangan, peserta mencatat di aset 02.",
            "Menit 65-85: loket tanpa suara. Berpasangan, satu menjadi nasabah Tuli dengan kartu transaksi, satu menjadi teller yang tidak boleh bersuara.",
            "Menit 85-90: tiga hal yang paling sulit dicatat untuk diulang di Modul 6.",
        ],
        "alat": "Aset 02 Kartu Saku Isyarat, papan tulis genggam dan spidol 5 set, kartu transaksi",
        "indikator": "Setiap peserta mengeja nomor rekening 10 digit tanpa salah dan menyelesaikan satu transaksi loket tanpa suara",
        "output": "Kartu saku isyarat dengan catatan peragaan dari co-trainer",
    },
    {
        "no": "Modul 4",
        "judul": "Kursi roda, ramp, dan tata letak loket",
        "jam": "13.00 - 14.00 (60 menit)",
        "tujuan": "Peserta mampu mengoperasikan (C3) kursi roda di ramp dengan aman, dan menilai (C5) aksesibilitas ruang layanan BPR dengan lembar audit.",
        "materi": [
            "Bertanya sebelum mendorong, bicara sejajar mata pengguna kursi roda",
            "Rem, naik ramp, turun ramp, melewati undakan",
            "Membantu pindah duduk hanya bila nasabah meminta dan dengan cara yang ia tunjukkan",
            "Tata letak loket: tinggi meja, ruang putar, alat tulis yang terjangkau",
            "Antrean prioritas dan kursi tunggu",
        ],
        "aktivitas": [
            "Menit 0-10: trainer memperagakan urutan rem, naik ramp, dan turun ramp.",
            "Menit 10-35: peserta bergantian duduk dan mendorong kursi roda di ramp kantor. Pasangan mencentang aset 03 bagian B.",
            "Menit 35-55: dua kelompok mengaudit ruang layanan BPR dengan aset 08, mengukur, dan memotret temuan.",
            "Menit 55-60: tiap kelompok menyampaikan tiga temuan utama.",
        ],
        "alat": "Kursi roda 1 unit, meteran, ponsel untuk foto, aset 03 dan aset 08",
        "indikator": "Setiap peserta menjalankan urutan rem dan ramp tanpa koreksi. Tiap kelompok mengisi minimal 10 butir audit dengan foto",
        "output": "Lembar audit aksesibilitas terisi, menjadi bahan rekomendasi fasilitas di laporan",
    },
    {
        "no": "Modul 5",
        "judul": "Legalitas transaksi, warkat, dan administrasi",
        "jam": "14.00 - 15.00 (60 menit)",
        "tujuan": "Peserta mampu menerapkan (C3) verifikasi e-KTP, pembacaan slip, dan cap jempol di hadapan saksi internal. Kasie mampu memeriksa (C4) kelengkapan berkas transaksi.",
        "materi": [
            "Verifikasi e-KTP dan pencocokan wajah",
            "Batas kewenangan pendamping: membantu, tidak memutuskan. Surat kuasa bila mewakili",
            "Pembacaan slip: nama, nomor rekening, nominal angka dan terbilang",
            "Tanda tangan atau cap jempol: tanya dulu, hadirkan saksi internal, catat di formulir",
            "Kerahasiaan: suara pelan, data tidak dibacakan di depan antrean",
        ],
        "aktivitas": [
            "Menit 0-10: trainer menjelaskan alur dengan SOP internal BPR yang diterima sebelum kelas.",
            "Menit 10-45: simulasi bertiga (teller, nasabah netra dengan pendamping, saksi). Tiga putaran, peran berganti, memakai slip kosong dari BPR dan aset 07.",
            "Menit 45-60: Kasie Operasional memeriksa berkas tiap kelompok dengan daftar periksa di aset 07, lalu membahas temuan.",
        ],
        "alat": "Slip setoran dan penarikan kosong dari BPR, bantalan tinta, e-KTP rekaan, aset 07",
        "indikator": "Berkas tiap kelompok lengkap saat diperiksa Kasie: identitas, slip dibacakan, saksi, cap jempol atau tanda tangan",
        "output": "Tiga set berkas simulasi lengkap",
    },
    {
        "no": "Modul 6",
        "judul": "Simulasi terpadu, post-test, dan penutupan",
        "jam": "15.15 - 16.30 (75 menit)",
        "tujuan": "Peserta mampu melaksanakan (C3) alur layanan dari pintu masuk sampai otorisasi. Kasie mampu mengevaluasi (C5) layanan dengan rubrik dan menangani keluhan.",
        "materi": [
            "Alur Security, CS, Teller, dan Kasie untuk nasabah netra, Tuli, dan pengguna kursi roda",
            "Penanganan keluhan dan eskalasi di ruang layanan",
            "Pencatatan bukti untuk pemeriksaan",
        ],
        "aktivitas": [
            "Menit 0-45: lima skenario dari aset 04, masing-masing 8 menit main dan 1 menit umpan balik. Peraga netra dan co-trainer Tuli berperan sebagai nasabah. Kasie mengisi aset 05.",
            "Menit 45-55: trainer membahas pola temuan rubrik.",
            "Menit 55-70: post-test dan survei kepuasan.",
            "Menit 70-75: penutupan dan foto bersama.",
        ],
        "alat": "Aset 04 Kartu Skenario, aset 05 Rubrik, aset 06 Post-Test, kamera",
        "indikator": "Rata-rata skor rubrik tiap skenario minimal 2,5 dari 3. Nilai post-test minimal 80",
        "output": "Rubrik observasi terisi dan nilai post-test",
    },
]

# Hasil yang dibawa pulang: (hasil, dari, dipakai untuk)
HASIL = [
    ("Ringkasan Regulasi dan SOP dengan daftar bukti audit yang ditandai", "Modul 1", "Pegangan di loket dan bahan pemeriksaan"),
    ("Lembar praktik pemanduan dan kursi roda yang diparaf peraga", "Modul 2 dan 4", "Bukti praktik per peserta"),
    ("Kartu saku isyarat dengan catatan peragaan", "Modul 3", "Disimpan di meja teller dan CS"),
    ("Lembar audit aksesibilitas ruang layanan dengan foto", "Modul 4", "Rekomendasi perbaikan fasilitas di laporan"),
    ("Tiga set berkas simulasi slip dan cap jempol", "Modul 5", "Contoh berkas lengkap untuk Kasie"),
    ("Rubrik observasi layanan yang sudah dipakai sekali", "Modul 6", "Alat Kasie untuk memantau layanan di kantor"),
    ("Nilai pre-test dan post-test", "Awal dan akhir hari", "Laporan evaluasi dan bukti audit"),
    ("Sertifikat perorangan yang merujuk POJK 22/2023", "Sesudah kelas", "Bukti pemenuhan pelatihan"),
]
