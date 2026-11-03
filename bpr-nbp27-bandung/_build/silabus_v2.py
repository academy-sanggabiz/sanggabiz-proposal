"""Isi silabus v2: bahasa sehari-hari untuk pembaca awam (ATURAN-PROPOSAL.md bagian 9).

Tanpa kode atau istilah akademik. Alat dan media ditulis umum. Rincian menit ada di panduan fasilitator (silabus.py).
"""

PEMBUKA = ("Staf garda depan belajar dengan mempraktikkan langsung, didampingi penyandang disabilitas. "
           "Teori hanya 30 menit. Sisa hari dipakai untuk mencoba sendiri setiap situasi yang akan mereka temui di loket.")

SOROTAN = [
    ("30 menit", "teori", "Sisanya, lebih dari 5 jam, dipakai untuk praktik dan simulasi."),
    ("2 peraga", "disabilitas", "Co-trainer Tuli dan peraga netra memandu praktik dan memberi masukan langsung."),
    ("10 peserta", "praktik semua", "Setiap peserta mencoba sendiri setiap praktik, dengan pasangan yang tetap sepanjang hari."),
]

RUNDOWN = [
    ("08.30 - 08.45", "Pembukaan", "Peserta berkenalan dengan tim dan dibagi menjadi pasangan praktik."),
    ("08.45 - 09.00", "Pre-test", "15 soal singkat untuk melihat pemahaman awal peserta."),
    ("09.00 - 09.30", "Modul 1. Aturan OJK untuk layanan disabilitas", "Satu-satunya sesi paparan: apa yang wajib dilakukan bank dan bukti apa yang disimpan."),
    ("09.30 - 10.15", "Modul 2. Menyambut dan memandu nasabah netra", "Peserta bergantian memakai penutup mata dan memandu rekannya dari pintu sampai kursi."),
    ("10.15 - 10.30", "Rehat kopi", ""),
    ("10.30 - 12.00", "Modul 3. Bahasa isyarat di loket", "Belajar langsung dari co-trainer Tuli: abjad jari, angka, dan 20 kata yang paling sering dipakai di loket."),
    ("12.00 - 13.00", "Istirahat, salat, dan makan siang", ""),
    ("13.00 - 14.00", "Modul 4. Kursi roda dan ruang layanan", "Mendorong kursi roda di ramp dan memeriksa bersama ruang layanan BPR."),
    ("14.00 - 15.00", "Modul 5. Slip, cap jempol, dan saksi", "Simulasi transaksi nasabah netra, dari pembacaan slip sampai pengesahan."),
    ("15.00 - 15.15", "Rehat kopi", ""),
    ("15.15 - 16.30", "Modul 6. Simulasi layanan lengkap dan penutupan", "Lima situasi nyata dari pintu masuk sampai keluhan, lalu post-test dan penutupan."),
]

MODUL = [
    {
        "no": "Modul 1", "judul": "Aturan OJK untuk layanan nasabah disabilitas", "jam": "09.00 - 09.30",
        "dipelajari": ["Kewajiban bank menurut POJK 22/2023 dan Pedoman SETARA OJK",
                       "Ragam disabilitas yang mungkin datang ke kantor",
                       "Risiko bila nasabah ditolak atau transaksinya tidak sah",
                       "Bukti layanan yang perlu disimpan untuk pemeriksaan OJK"],
        "kegiatan": ["Trainer membuka dengan satu cerita: nasabah netra diminta pulang dan datang lagi bersama keluarga. Peserta membahas apa yang keliru.",
                     "Paparan singkat tentang aturan dan bukti yang disimpan.",
                     "Kuis cepat: peserta mengangkat kartu Boleh atau Tidak untuk enam situasi di loket."],
        "alat": "Kartu Boleh dan Tidak", "media": "Presentasi, modul ringkas aturan dan SOP",
        "hasil": "Peserta tahu apa yang wajib dilakukan bank dan bukti apa yang disimpan.",
    },
    {
        "no": "Modul 2", "judul": "Menyambut dan memandu nasabah netra", "jam": "09.30 - 10.15",
        "dipelajari": ["Menyapa dan menawarkan bantuan tanpa langsung menyentuh",
                       "Bicara langsung kepada nasabah, bukan kepada pendamping",
                       "Memandu nasabah: posisi lengan, pintu, undakan, sampai duduk",
                       "Menjelaskan arah dengan jelas, misalnya \"kursi ada di kanan Ibu\""],
        "kegiatan": ["Peraga netra dan trainer memperagakan rute dari pintu masuk sampai meja CS.",
                     "Peserta berpasangan. Satu memakai penutup mata, satu memandu lewat rute yang ditandai di lantai, lalu bertukar.",
                     "Peraga netra memberi masukan langsung kepada setiap pasangan."],
        "alat": "Penutup mata, tongkat putih, lakban penanda rute", "media": "Peragaan langsung, lembar praktik",
        "hasil": "Setiap peserta pernah memandu dan pernah dipandu, jadi paham rasanya dari dua sisi.",
    },
    {
        "no": "Modul 3", "judul": "Bahasa isyarat di loket", "jam": "10.30 - 12.00",
        "dipelajari": ["Menarik perhatian dan berhadapan dengan nasabah Tuli",
                       "Abjad jari dan angka untuk nama, nomor rekening, dan nominal",
                       "20 isyarat loket: salam, setor, tarik, rekening, tanda tangan, dan lainnya",
                       "Menulis kalimat pendek bila isyarat belum cukup"],
        "kegiatan": ["Co-trainer Tuli membuka sesi dengan isyarat, peserta menebak artinya.",
                     "Latihan abjad jari: setiap peserta mengeja namanya dan satu nomor rekening.",
                     "Latihan 20 isyarat loket, dikoreksi langsung oleh co-trainer.",
                     "Loket tanpa suara: berpasangan, satu peserta menjadi teller yang tidak boleh bersuara."],
        "alat": "Papan tulis genggam dan spidol, kartu transaksi latihan", "media": "Kartu Saku Isyarat Perbankan, peragaan co-trainer Tuli",
        "hasil": "Peserta bisa melayani satu transaksi sederhana dengan nasabah Tuli dan membawa pulang kartu saku isyarat.",
    },
    {
        "no": "Modul 4", "judul": "Kursi roda dan ruang layanan", "jam": "13.00 - 14.00",
        "dipelajari": ["Bertanya dulu sebelum mendorong, bicara sejajar mata",
                       "Mengunci rem, naik dan turun ramp dengan aman",
                       "Menata meja loket agar terjangkau dari kursi roda",
                       "Mengatur antrean prioritas"],
        "kegiatan": ["Trainer memperagakan cara memakai rem dan melewati ramp.",
                     "Peserta bergantian duduk di kursi roda dan mendorong rekannya di ramp.",
                     "Dua kelompok berkeliling ruang layanan BPR dengan daftar periksa, lalu memotret yang sudah baik dan yang perlu diperbaiki."],
        "alat": "Kursi roda, meteran, kamera ponsel", "media": "Peragaan langsung, daftar periksa ruang layanan",
        "hasil": "Daftar temuan ruang layanan yang menjadi rekomendasi perbaikan fasilitas di laporan.",
    },
    {
        "no": "Modul 5", "judul": "Slip, cap jempol, dan saksi", "jam": "14.00 - 15.00",
        "dipelajari": ["Memeriksa e-KTP dan mencocokkan wajah",
                       "Membacakan slip: nama, nomor rekening, dan nominal dalam angka dan kata",
                       "Memberi pilihan tanda tangan atau cap jempol, dengan saksi dari bank",
                       "Batas peran pendamping dan menjaga kerahasiaan data"],
        "kegiatan": ["Trainer menjelaskan alur sesuai SOP BPR.",
                     "Simulasi bertiga: teller, nasabah netra dengan pendamping, dan saksi. Tiga putaran dengan peran bergantian.",
                     "Kasie Operasional memeriksa kelengkapan berkas setiap kelompok."],
        "alat": "Slip setoran dan penarikan kosong, bantalan tinta, KTP contoh", "media": "Contoh formulir pembacaan slip",
        "hasil": "Peserta tahu langkah transaksi yang sah, dan Kasie memegang contoh berkas yang lengkap.",
    },
    {
        "no": "Modul 6", "judul": "Simulasi layanan lengkap", "jam": "15.15 - 16.30",
        "dipelajari": ["Alur layanan dari security, CS, teller, sampai Kasie",
                       "Menanggapi keluhan nasabah disabilitas dengan tenang",
                       "Mencatat layanan sebagai bukti"],
        "kegiatan": ["Lima situasi dimainkan: nasabah netra di pintu masuk, nasabah Tuli membuka rekening, setoran nasabah netra, penarikan dengan cap jempol, dan keluhan pengguna kursi roda.",
                     "Peraga netra dan co-trainer Tuli berperan sebagai nasabah. Kasie mengamati dengan lembar pengamatan.",
                     "Trainer membahas hasilnya, lalu post-test, survei kepuasan, dan penutupan."],
        "alat": "Kartu situasi role-play", "media": "Simulasi, lembar pengamatan, post-test",
        "hasil": "Setiap peserta sudah mempraktikkan layanan utuh sebelum kembali ke loket.",
    },
]

DIDAPAT = [
    ("Untuk staf garda depan", ["Percaya diri melayani nasabah netra, Tuli, dan pengguna kursi roda",
                               "Kartu saku isyarat untuk meja teller dan CS",
                               "Modul ringkas aturan dan SOP layanan disabilitas",
                               "Sertifikat perorangan yang merujuk POJK 22/2023"]),
    ("Untuk Kasie dan manajemen", ["Lembar pengamatan untuk memantau layanan di kantor",
                                  "Contoh berkas transaksi cap jempol yang lengkap",
                                  "Laporan evaluasi: nilai pre-test dan post-test, foto dan video",
                                  "Rekomendasi perbaikan fasilitas dari pemeriksaan ruang layanan"]),
    ("Cara kami memastikan hasilnya", ["Pre-test dan post-test dengan soal yang sama",
                                      "Setiap praktik diamati dan diberi masukan oleh peraga disabilitas",
                                      "Kasie ikut menilai simulasi akhir",
                                      "Laporan dikirim paling lambat 7 hari kerja setelah pelatihan"]),
]

KARTU = {
    "apa": "Kartu dua sisi seukuran A5, dilaminasi. Sisi depan memuat 20 isyarat loket dengan foto peragaan. Sisi belakang adalah kartu tunjuk: nasabah menunjuk layanan dan jumlah uang, petugas mengonfirmasi.",
    "foto": "Foto isyarat diperagakan oleh co-trainer Tuli dari Bandung, karena bahasa isyarat punya variasi daerah. Isyarat di kartu sama dengan yang dipakai nasabah setempat.",
    "dipakai": "Dipakai di Modul 3 dan simulasi Modul 6, lalu disimpan di meja teller dan CS.",
}
