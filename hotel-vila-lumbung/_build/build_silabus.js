// Silabus pelatihan AR dan Income Audit Hotel. NODE_PATH=$(npm root -g) node build_silabus.js
const path = require("path");
const L = require("./lib.js");
const { p, h1, h2, h3, bullet, num, caption, spacer, table, cover, footer, makeDoc, save, D } = L;
const { AlignmentType, PageOrientation } = D;

const WP = 9638, WL = 14570;
const LABEL = "Silabus Pelatihan Online AR dan Income Audit Hotel";

// ---------- sampul ----------
const sampul = cover(WP, "SILABUS PELATIHAN ONLINE",
  "Account Receivable dan Income Audit Hotel",
  "Untuk Departemen Accounting, Hotel Vila Lumbung",
  [["3 sesi, 9 jam", "Daring, masing-masing 3 jam tatap muka"], ["1 peserta", "Pendampingan satu lawan satu"], ["Desember 2026", "Tanggal pasti disepakati bersama"]],
  ["Disusun oleh Sanggabiz", "November 2026"]);

// ---------- bagian 1 ----------
const bag1 = [
  h1("1. Ringkasan program"),
  table([2600, 7038], ["Hal", "Keterangan"], [
    ["Peserta", "1 orang dari departemen accounting Hotel Vila Lumbung, dengan fokus kerja di bagian AR dan Income Audit."],
    ["Bentuk", "Pelatihan daring melalui Zoom atau Google Meet. Pengajar membagikan layar, peserta mengerjakan kasus di Excel atau Google Sheets miliknya."],
    ["Durasi", "3 sesi, masing-masing 3 jam, total 9 jam tatap muka. Tiap sesi bisa berdiri sendiri, sehingga jadwalnya dapat dibuat berurutan atau diberi jeda."],
    ["Waktu", "Desember 2026. [ISI TIM: tanggal dan jam tiap sesi, zona waktu]"],
    ["Pengajar", "[ISI TIM: nama, jabatan, dan pengalaman pengajar pelatihan AR dan income audit hotel]"],
    ["Bahan peserta", "Modul peserta, workbook latihan, templat invoice dan checklist, bank soal pre-test dan post-test."],
    ["Sertifikat", "E-sertifikat atas nama peserta, dengan keterangan 9 jam tatap muka daring. Syarat penerbitan ada di bagian 7."],
  ], { firstBold: true, firstFill: true }),
  spacer(),
  h2("1.1 Permintaan Hotel Vila Lumbung"),
  p("Silabus ini disusun dari lembar permintaan yang kami terima dari Hotel Vila Lumbung. Ringkasan jawabannya:"),
  table([3000, 6638], ["Pertanyaan kami", "Jawaban Hotel Vila Lumbung"], [
    ["Peserta", "1 orang, departemen accounting"],
    ["Area yang perlu ditingkatkan", "Pengetahuan dan penerapan pada section AR dan Income Audit"],
    ["Tujuan pelatihan", "Target perusahaan untuk menuju level berikutnya. Peserta diwajibkan mengikuti pelatihan untuk mendapatkan sertifikat."],
    ["Harapan", "Lebih paham alur dan pengetahuan tentang AR dan income di perhotelan, dan bisa menerapkannya di lapangan"],
    ["Metode dan waktu", "Online, Desember 2026, 1 sampai 3 hari"],
    ["Format", "Penjelasan dan studi kasus"],
    ["Masalah yang ingin diselesaikan", "Lebih bisa menyelesaikan kasus yang ada di lapangan"],
    ["Target kompetensi", "Memahami dan menerapkan proses Account Receivable (AR) Income Hotel secara mandiri, mulai dari pencatatan pendapatan, pengelolaan piutang tamu dan perusahaan (city ledger), pembuatan invoice, monitoring outstanding balance, rekonsiliasi pembayaran, hingga penyusunan laporan AR."],
  ], { firstBold: true, firstFill: true }),
  spacer(),
  h2("1.2 Bagian target kompetensi dan tempatnya di silabus"),
  table([4400, 2400, 2838], ["Target kompetensi dari Hotel Vila Lumbung", "Sesi dan topik", "Bukti yang dihasilkan"], [
    ["Pencatatan pendapatan", "Sesi 1, topik 1.1 sampai 1.3", "Lembar tarif dan rekap income audit terisi, laporan temuan"],
    ["Pengelolaan piutang tamu dan perusahaan (city ledger)", "Sesi 2, topik 2.1 dan 2.2", "Keputusan kredit tiga pemohon, tabel jurnal lima transaksi"],
    ["Pembuatan invoice", "Sesi 2, topik 2.3 dan 2.4", "Satu invoice lengkap, tiga invoice yang diperiksa dan diperbaiki"],
    ["Monitoring outstanding balance", "Sesi 3, topik 3.1", "Lembar city ledger dengan umur piutang dan lima prioritas penagihan"],
    ["Rekonsiliasi pembayaran", "Sesi 3, topik 3.2", "Lembar rekon bank dan tiga jurnal penyelesaian"],
    ["Penyusunan laporan AR", "Sesi 3, topik 3.3 dan 3.4", "Laporan AR satu halaman, daftar tindakan kasus terpadu"],
  ], { firstBold: true, firstFill: true }),

  h1("2. Metode dan alur program", true),
  p("Kami memakai lima kerangka yang umum di dunia pelatihan, masing-masing untuk satu keperluan yang jelas."),
  table([2400, 3000, 4238], ["Kerangka", "Dipakai untuk", "Muncul di bagian"], [
    ["Backward design", "Menyusun materi mulai dari hasil akhir yang diminta, bukan dari daftar teori", "Bagian 2.1. Target kompetensi hotel menjadi hasil akhir, lalu bukti, lalu materi"],
    ["ADDIE", "Alur penyelenggaraan dari analisis sampai evaluasi", "Bagian 2.2, tahap proses program"],
    ["Andragogi (Knowles)", "Cara belajar peserta dewasa: dari pengalaman kerja sendiri, berorientasi masalah", "Aktivitas tiap topik. Peserta memulai dari alur dan dokumen hotelnya sendiri"],
    ["Taksonomi Bloom revisi", "Merumuskan tujuan dengan kata kerja yang terukur", "Kolom tujuan pembelajaran tiap topik"],
    ["Kirkpatrick, level 1 dan 2", "Evaluasi reaksi dan pembelajaran", "Bagian 7. Survei kepuasan, pre-test, post-test, dan penilaian hasil kerja"],
  ], { firstBold: true, firstFill: true }),
  h2("2.1 Backward design untuk program ini"),
  p("Pemetaan awal sudah ada dari lembar permintaan Hotel Vila Lumbung dan dilengkapi pre-test 15 butir sebelum sesi 1."),
  num("Kondisi awal: peserta bekerja di accounting dan perlu memperkuat pengetahuan serta penerapan di AR dan income audit. Pre-test menunjukkan bagian yang paling perlu waktu.", "num"),
  num("Hasil akhir: peserta menjalankan proses AR dan income hotel secara mandiri, dari pencatatan pendapatan sampai laporan AR.", "num"),
  num("Bukti keberhasilan: post-test, hasil kerja tiap topik (lihat bagian 5), dan rencana penerapan 30 hari di hotelnya.", "num"),
  num("Materi dan aktivitas: sebelas topik dalam tiga sesi. Bila pre-test menunjukkan bagian yang sudah dikuasai, pengajar memadatkan bagian itu dan menambah waktu pada kasus.", "num"),
  num("Pelaksanaan, evaluasi, lalu perbaikan: dijelaskan di bagian 2.2.", "num"),
  h2("2.2 Tahap proses program"),
  p("Proses bisnis program kami pecah menjadi lima tahap. Isi silabus, hasil kerja, dan evaluasi mengikuti tahap ini."),
  table([500, 2500, 4300, 2338], ["No", "Tahap (ADDIE)", "Pekerjaan", "Waktu"], [
    ["1", "Pemetaan awal (Analysis)", "Membaca lembar permintaan, mencocokkan dengan target kompetensi, mengirim pre-test dan daftar persiapan peserta", "Sebelum sesi 1"],
    ["2", "Penyusunan materi (Design dan Development)", "Menyusun silabus, modul, workbook, bank soal, dan sertifikat. Materi sudah siap pada dokumen ini", "Sudah tersedia, disesuaikan setelah pre-test"],
    ["3", "Pelaksanaan (Implementation)", "Tiga sesi daring, masing-masing 3 jam", "Desember 2026"],
    ["4", "Monitoring dan evaluasi (Evaluation)", "Post-test, survei kepuasan, penilaian hasil kerja, rencana penerapan 30 hari", "Akhir sesi 3"],
    ["5", "Laporan dan sertifikat", "Ringkasan hasil pre-test dan post-test serta e-sertifikat ke peserta dan atasan", "Maksimal 5 hari kerja setelah sesi 3"],
  ], { firstBold: true, firstFill: true }),

  h1("3. Rangkuman silabus", true),
  table([700, 4100, 1100, 3738], ["Topik", "Judul", "Menit", "Hasil"], [
    { group: "Sesi 1. Pendapatan hotel dan income audit (180 menit)" },
    ["", "Pembukaan, kesepakatan belajar, tinjauan pre-test", "15", "Tujuan pribadi peserta tertulis"],
    ["1.1", "Peta pendapatan dan alur dokumen hotel", "40", "Lembar alur dokumen, hasil hitung okupansi, ARR, RevPAR"],
    ["1.2", "Night audit dan laporan harian", "55", "Checklist night audit, klasifikasi enam catatan serah terima"],
    ["", "Jeda", "10", ""],
    ["1.3", "Income audit harian, kontrol dan temuan", "60", "Lembar tarif dan rekap terisi, laporan temuan satu halaman"],
    { group: "Sesi 2. Piutang, city ledger, dan invoice (180 menit)" },
    ["2.1", "Jenis piutang dan kebijakan kredit", "35", "Keputusan kredit tiga pemohon"],
    ["2.2", "Alur folio ke city ledger dan jurnalnya", "50", "Tabel jurnal lima transaksi"],
    ["", "Jeda", "10", ""],
    ["2.3", "Invoice dan dokumen penagihan", "45", "Satu invoice lengkap"],
    ["2.4", "Praktik memeriksa dan memperbaiki invoice", "40", "Tiga invoice terperiksa, satu draf credit note"],
    { group: "Sesi 3. Monitoring, rekonsiliasi, dan laporan AR (180 menit)" },
    ["3.1", "Aging dan monitoring outstanding", "40", "Lembar city ledger berumus, lima prioritas penagihan"],
    ["3.2", "Rekonsiliasi pembayaran", "45", "Lembar rekon bank, tiga jurnal"],
    ["", "Jeda", "10", ""],
    ["3.3", "Laporan AR", "35", "Laporan AR satu halaman, tiga rekomendasi"],
    ["3.4", "Kasus terpadu", "25", "Daftar tindakan terurut lima kejadian"],
    ["", "Penutup: post-test, survei, rencana penerapan 30 hari", "25", "Skor post-test, survei, rencana 30 hari"],
  ], { align: [AlignmentType.CENTER, AlignmentType.LEFT, AlignmentType.CENTER, AlignmentType.LEFT] }),
  p("Semua angka, nama pelanggan, dan tanggal di kasus latihan adalah rekaan. Data hotel peserta tidak diminta. Bila peserta ingin memakai contoh dari hotelnya, nama dan nilainya disamarkan lebih dulu.", { before: 140 }),
];

// ---------- silabus rinci (lanskap) ----------
const W5 = [2300, 2900, 4300, 2000, 3070];
const head5 = ["Topik dan tujuan pembelajaran", "Outline materi", "Aktivitas (menit, siapa melakukan apa)", "Alat dan media", "Output dan ukuran keberhasilan"];
const row = (judul, tujuan, outline, aktivitas, alat, output, ukuran) => [
  [`**${judul}**`, tujuan], outline, aktivitas, alat, [`Output: ${output}`, `Ukuran: ${ukuran}`]];
const ALAT_DASAR = "Zoom atau Google Meet dengan berbagi layar";

const sesi1 = [
  row("Pembukaan (15 menit)", "Peserta menyebut tujuan pribadinya dan menyepakati cara belajar.",
    ["1. Perkenalan dan peta tiga sesi", "2. Hasil pre-test: tiga bagian yang paling perlu dikuatkan", "3. Aturan kerja: kamera, berbagi layar, tanya kapan saja"],
    ["Menit 0 sampai 5: pengajar membuka dan menunjukkan peta tiga sesi.", "Menit 5 sampai 12: pengajar menayangkan hasil pre-test per bagian. Peserta menjelaskan bagian mana yang paling sering ia temui di hotelnya.", "Menit 12 sampai 15: peserta menulis satu tujuan pribadi di kolom chat."],
    [ALAT_DASAR, "Slide pembuka", "Hasil pre-test"], "satu kalimat tujuan pribadi.", "tujuan tertulis dan terkait dengan target kompetensi."),
  row("Topik 1.1. Peta pendapatan dan alur dokumen hotel (40 menit)", "Peserta mampu menjelaskan alur dari reservasi sampai laporan pendapatan, membedakan guest ledger, city ledger, dan advance deposit, serta menghitung okupansi, ARR, dan RevPAR.",
    ["1. Sumber pendapatan: kamar, makanan dan minuman, lain-lain", "2. Peran kasir front office, night auditor, income auditor, AR, dan buku besar, serta dokumen yang berpindah antar bagian", "3. Guest ledger, city ledger, advance deposit, folio, master folio", "4. Rumus okupansi, ARR, RevPAR"],
    ["Menit 0 sampai 15: pengajar menayangkan bagan alur satu tamu korporasi dari reservasi sampai pelunasan. Peserta menyela dengan istilah yang berbeda di hotelnya.", "Menit 15 sampai 30: peserta menggambar alur dokumen di hotelnya pada lembar alur (kolom langkah, dokumen, bagian, sistem) dan membagikan layar.", "Menit 30 sampai 40: peserta menghitung okupansi, ARR, dan RevPAR dari data hari kasus (50 kamar tersedia, 28 terjual berbayar, pendapatan kamar Rp 15.240.000) di lembar IA-Rekap. Pengajar mengoreksi."],
    ["Slide sesi 1", "Modul Bab 1", "Workbook lembar IA-Rekap", "Lembar alur dokumen (Modul Lampiran D)"], "lembar alur dokumen pendapatan hotel milik peserta, hasil tiga rasio.", "peserta menyebut tiga jenis saldo dengan benar dan hasil hitung sesuai kunci (okupansi 56 persen, ARR Rp 544.286, RevPAR Rp 304.800)."),
  row("Topik 1.2. Night audit dan laporan harian (55 menit)", "Peserta mampu menguraikan langkah night audit dan memeriksa catatan serah terima untuk menemukan transaksi yang belum lengkap.",
    ["1. Urutan night audit: tutup shift, cocokkan POS dan PMS, posting kamar, service dan pajak, no-show, ganti tanggal, cetak laporan", "2. Laporan harian: daily revenue report, laporan transaksi kasir, laporan transfer city ledger, laporan deposit", "3. Kesalahan umum: charge terlambat, transaksi manual, void tanpa otorisasi", "4. Serah terima ke income audit"],
    ["Menit 0 sampai 15: pengajar menjelaskan urutan night audit dengan contoh tampilan laporan rekaan.", "Menit 15 sampai 35: peserta membaca enam catatan serah terima night auditor (Modul Bab 2) dan menandai mana yang wajar dan mana yang harus ditindaklanjuti, dengan alasan.", "Menit 35 sampai 50: pengajar dan peserta membahas jawaban. Pengajar menambah contoh dari praktik lapangan.", "Menit 50 sampai 55: peserta menyesuaikan checklist night audit dengan sistem hotelnya."],
    ["Slide sesi 1", "Modul Bab 2 dan Lampiran A (checklist night audit)"], "checklist night audit yang sudah disesuaikan, klasifikasi enam catatan.", "minimal 5 dari 6 catatan diklasifikasi benar, tiap jawaban disertai alasan."),
  row("Topik 1.3. Income audit harian, kontrol dan temuan (60 menit)", "Peserta mampu memeriksa tarif kamar, pemindahan F&B ke kamar, dan penyelesaian per metode bayar, lalu menulis temuan dan usulan koreksi.",
    ["1. Sepuluh kontrol income audit harian", "2. Cek tarif: kode tarif, kontrak, persetujuan komplimen dan house use", "3. Cocokkan POS dengan PMS untuk F&B yang dipindah ke kamar", "4. Cocokkan penyelesaian: tunai, EDC, QRIS, transfer, city ledger", "5. Menulis temuan: fakta, dampak dalam rupiah, tindakan"],
    ["Menit 0 sampai 10: pengajar menjelaskan sepuluh kontrol dan alur kerja di workbook.", "Menit 10 sampai 20: peserta mengisi lembar IA-Tarif kamar (30 kamar) dan menandai selisih.", "Menit 20 sampai 40: peserta mengisi IA-Rekap bagian A dan B sambil berbagi layar. Pengajar bertanya 'kenapa' pada tiap selisih.", "Menit 40 sampai 55: peserta menulis tiga temuan terpenting memakai format fakta, dampak, tindakan. Pengajar memberi umpan balik.", "Menit 55 sampai 60: rangkuman."],
    ["Workbook lembar IA-Tarif kamar dan IA-Rekap", "Modul Bab 2 dan Lampiran B (format laporan temuan)"], "dua lembar terisi dan laporan temuan satu halaman.", "minimal 7 dari 9 temuan ditanam (3 selisih tarif, 1 komplimen tanpa persetujuan, 2 selisih F&B, 3 selisih penyelesaian) ditemukan dengan nilai rupiah yang benar."),
];
const sesi2 = [
  row("Topik 2.1. Jenis piutang dan kebijakan kredit (35 menit)", "Peserta mampu membedakan piutang tamu dari city ledger dan menetapkan limit serta termin untuk pemohon kredit baru.",
    ["1. Guest ledger, city ledger, piutang agen dan OTA", "2. Dokumen pembukaan kredit: formulir permohonan, perjanjian kerja sama, NPWP, referensi", "3. Limit kredit, termin, jaminan deposit", "4. Siapa yang menyetujui: sales, GM, keuangan", "5. Direct billing dan bayar di muka"],
    ["Menit 0 sampai 12: pengajar memaparkan dan menunjukkan contoh formulir permohonan kredit.", "Menit 12 sampai 27: peserta menilai tiga permohonan rekaan (korporasi baru, agen dengan riwayat terlambat, instansi dengan pembayaran 45 hari) dan memutuskan limit, termin, dan syarat.", "Menit 27 sampai 35: pengajar membahas keputusan peserta dan membandingkan dengan praktik yang lazim."],
    ["Modul Bab 3 dan Lampiran C (formulir permohonan kredit)", "Slide sesi 2"], "keputusan kredit untuk tiga pemohon.", "tiap keputusan punya alasan tertulis dan minimal dua syarat dokumen."),
  row("Topik 2.2. Alur folio ke city ledger dan jurnalnya (50 menit)", "Peserta mampu menelusuri satu tagihan dari posting kamar sampai pelunasan dan menyusun jurnal tiap langkah.",
    ["1. Posting tarif kamar, service, dan pajak", "2. Advance deposit dan pemakaiannya", "3. Pindah folio ke city ledger saat check-out: otorisasi dan dokumen", "4. Pelunasan, termasuk pembayaran OTA yang sudah dipotong komisi", "5. Koreksi: rebill, credit note, pembatalan"],
    ["Menit 0 sampai 15: pengajar membahas jurnal berantai untuk satu kamar dengan tarif nett Rp 500.000.", "Menit 15 sampai 40: peserta menyusun jurnal lima transaksi (Modul Bab 3, latihan 2) sambil berbagi layar.", "Menit 40 sampai 50: pengajar membahas kesalahan umum, misalnya deposit yang salah dicatat sebagai pendapatan."],
    ["Modul Bab 3", "Slide sesi 2"], "tabel jurnal lima transaksi.", "minimal 4 dari 5 jurnal seimbang dan memakai akun yang benar."),
  row("Topik 2.3. Invoice dan dokumen penagihan (45 menit)", "Peserta mampu menyusun invoice lengkap dan paket penagihan yang bisa diproses bagian keuangan pelanggan.",
    ["1. Unsur invoice: nomor, tanggal, pelanggan dan NPWP, uraian, tarif, service, pajak, termin, rekening", "2. Lampiran: folio, PO atau voucher, daftar tamu, BEO untuk acara", "3. Penomoran dan arsip", "4. Faktur pajak dan bea meterai: ketentuan dikonfirmasi dengan bagian pajak hotel", "5. Pengiriman dan tanda terima"],
    ["Menit 0 sampai 15: pengajar menunjukkan contoh invoice yang ditolak pelanggan dan alasannya (tanpa PO, nama PT salah, pajak salah).", "Menit 15 sampai 30: peserta mengisi templat invoice di workbook dengan data kasus PT Maju Bersama.", "Menit 30 sampai 45: pengajar berperan sebagai staf keuangan PT Maju Bersama, memeriksa invoice, dan menolak bila ada kekurangan. Peserta memperbaiki."],
    ["Workbook lembar Invoice", "Modul Bab 4 dan Lampiran E (daftar periksa invoice)"], "satu invoice lengkap.", "total tagihan Rp 3.630.000 dan jatuh tempo benar, serta 10 butir daftar periksa terpenuhi."),
  row("Topik 2.4. Praktik memeriksa dan memperbaiki invoice (40 menit)", "Peserta mampu menemukan kesalahan pada invoice dan memperbaikinya lewat credit note atau rebill.",
    ["1. Kesalahan yang sering terjadi: hitung pajak, termin tidak sesuai kontrak, tarif berbeda dari folio", "2. Credit note dan rebill: kapan dipakai dan dokumennya", "3. Mencatat koreksi di city ledger"],
    ["Menit 0 sampai 5: pengajar membagikan tiga invoice berisi kesalahan (Modul Bab 4, latihan 3).", "Menit 5 sampai 25: peserta menandai kesalahan dan menulis versi perbaikan.", "Menit 25 sampai 35: peserta menyusun draf credit note untuk satu invoice.", "Menit 35 sampai 40: umpan balik pengajar."],
    ["Modul Bab 4, latihan 3"], "tiga invoice terperiksa dan satu draf credit note.", "minimal 5 dari 6 kesalahan yang ditanam ditemukan (dua per invoice)."),
];
const sesi3 = [
  row("Topik 3.1. Aging dan monitoring outstanding (40 menit)", "Peserta mampu menyusun umur piutang, menentukan prioritas penagihan, dan menyusun jadwal pengingat.",
    ["1. Jatuh tempo, hari lewat jatuh tempo, kelompok umur", "2. Rumus spreadsheet: jatuh tempo, hari lewat, kelompok", "3. Prioritas penagihan: nilai, umur, riwayat pelanggan", "4. Siklus pengingat: tiga hari sebelum jatuh tempo, satu hari sesudah, tujuh, empat belas, tiga puluh hari dengan eskalasi", "5. Catatan penagihan"],
    ["Menit 0 sampai 10: pengajar memaparkan.", "Menit 10 sampai 30: peserta menulis rumus pada lembar City Ledger (19 faktur) untuk sisa tagihan, jatuh tempo, hari lewat, dan kelompok umur.", "Menit 30 sampai 40: peserta memilih lima faktur yang ditagih lebih dulu dan menjelaskan alasannya."],
    ["Workbook lembar City Ledger", "Modul Bab 5"], "lembar City Ledger berumus dan daftar lima prioritas.", "total sisa tagihan Rp 147.030.000 dan angka tiap kelompok umur sesuai kunci, alasan prioritas masuk akal."),
  row("Topik 3.2. Rekonsiliasi pembayaran (45 menit)", "Peserta mampu mencocokkan pembayaran masuk dengan faktur dan memperlakukan selisihnya.",
    ["1. Sumber pembayaran: transfer bank, giro, settlement OTA, virtual account", "2. Mencocokkan per faktur dan urutan faktur terlama bila pelanggan tidak menyebut nomor", "3. Jenis selisih: biaya transfer, bayar kurang atau lebih, komisi OTA, dana belum teridentifikasi", "4. Jurnal penyelesaian", "5. Konfirmasi ke pelanggan"],
    ["Menit 0 sampai 10: pengajar menjelaskan jenis selisih dengan contoh.", "Menit 10 sampai 35: peserta mengerjakan tujuh mutasi bank pada lembar Rekon Bank.", "Menit 35 sampai 45: pembahasan dan jurnal komisi OTA."],
    ["Workbook lembar Rekon Bank", "Modul Bab 6"], "lembar Rekon Bank terisi dan tiga jurnal.", "tujuh mutasi tercocokkan, total Rp 63.343.000, dan empat selisih diperlakukan dengan benar."),
  row("Topik 3.3. Laporan AR (35 menit)", "Peserta mampu menyusun laporan AR bulanan dan menjelaskan DSO, pemakaian limit, serta tindakan yang diusulkan.",
    ["1. Isi laporan: umur piutang, piutang per pelanggan, limit, DSO, piutang lewat jatuh tempo", "2. Mencocokkan buku pembantu city ledger dengan akun di buku besar", "3. Penyisihan dan penghapusan piutang secara garis besar", "4. Menyampaikan laporan kepada atasan: tiga temuan dan tiga tindakan"],
    ["Menit 0 sampai 10: pengajar memaparkan isi laporan.", "Menit 10 sampai 25: peserta melengkapi lembar Laporan AR dan menulis tiga rekomendasi.", "Menit 25 sampai 35: peserta menyampaikan tiga poin secara lisan. Pengajar berperan sebagai Financial Controller dan bertanya."],
    ["Workbook lembar Laporan AR", "Modul Bab 7"], "laporan AR satu halaman dan tiga rekomendasi.", "DSO 71,1 hari, dua pelanggan melebihi limit teridentifikasi, tiap rekomendasi menyebut tindakan dan penanggung jawab."),
  row("Topik 3.4. Kasus terpadu (25 menit)", "Peserta mampu menerapkan alur income audit dan AR pada satu kasus baru yang berisi lima kejadian sekaligus.",
    ["1. Menentukan urutan tindakan", "2. Dokumen dan pihak yang terlibat", "3. Menjelaskan alasan"],
    ["Menit 0 sampai 3: pengajar membacakan lima kejadian Senin pagi (Modul Bab 8).", "Menit 3 sampai 18: peserta menentukan urutan, tindakan, dokumen, dan penanggung jawab tiap kejadian.", "Menit 18 sampai 25: peserta menjelaskan pilihannya dan pengajar menanggapi."],
    ["Modul Bab 8"], "daftar tindakan terurut untuk lima kejadian.", "tiap kejadian memiliki tindakan, dokumen, dan penanggung jawab, urutan bisa dijelaskan."),
  row("Penutup (25 menit)", "Peserta mengukur hasil belajarnya dan merencanakan penerapan di hotelnya.",
    ["1. Post-test", "2. Survei kepuasan", "3. Rencana penerapan 30 hari"],
    ["Menit 0 sampai 15: peserta mengerjakan post-test 15 butir lewat formulir.", "Menit 15 sampai 18: peserta mengisi survei kepuasan.", "Menit 18 sampai 25: peserta menulis tiga hal yang akan ia terapkan dalam 30 hari, lengkap dengan tanggal. Pengajar memberi masukan."],
    ["Formulir post-test", "Formulir survei", "Modul Lampiran F (rencana penerapan)"], "skor post-test, survei, dan rencana 30 hari.", "skor post-test minimal 11 dari 15 dan lebih tinggi dari pre-test (usulan Sanggabiz)."),
];
const lanskap = [
  h1("4. Silabus rinci per sesi"),
  p("Waktu dalam menit dihitung dari awal topik. Peserta bekerja dengan Excel atau Google Sheets di laptopnya dan membagikan layar bila diminta."),
  h2("Sesi 1. Pendapatan hotel dan income audit"),
  table(W5, head5, sesi1, { split: true }),
  h2("Sesi 2. Piutang, city ledger, dan invoice"),
  table(W5, head5, sesi2, { split: true }),
  h2("Sesi 3. Monitoring, rekonsiliasi, dan laporan AR"),
  table(W5, head5, sesi3, { split: true }),
];

// ---------- bagian akhir ----------
const bagAkhir = [
  h1("5. Hasil yang dibawa pulang"),
  p("Semua hasil kerja disimpan di workbook dan modul peserta. Peserta membawa pulang berkas berikut."),
  table([3700, 2000, 3938], ["Hasil", "Dihasilkan di topik", "Dipakai peserta untuk"], [
    ["Lembar alur dokumen pendapatan hotel", "1.1", "Memetakan alur kerja di hotelnya dan menemukan titik rawan"],
    ["Checklist night audit yang sudah disesuaikan", "1.2", "Memeriksa serah terima night audit tiap pagi"],
    ["Lembar tarif dan rekap income audit, format laporan temuan", "1.3", "Kerangka income audit harian"],
    ["Keputusan kredit tiga pemohon dan formulir permohonan kredit", "2.1", "Menilai pelanggan korporasi baru"],
    ["Tabel jurnal city ledger", "2.2", "Rujukan jurnal tiap tahap tagihan"],
    ["Templat invoice dan daftar periksa invoice", "2.3 dan 2.4", "Menerbitkan dan memeriksa invoice"],
    ["Lembar city ledger berumus", "3.1", "Memantau umur piutang tiap minggu"],
    ["Lembar rekon bank", "3.2", "Mencocokkan pembayaran masuk"],
    ["Laporan AR satu halaman", "3.3", "Bahan laporan bulanan ke atasan"],
    ["Rencana penerapan 30 hari", "Penutup", "Menjalankan hasil belajar dan melapor ke atasan"],
  ], { firstFill: false }),

  h1("6. Alat dan persiapan peserta", true),
  num("Laptop dengan Excel atau Google Sheets, kamera, mikrofon, dan koneksi internet yang stabil.", "num2"),
  num("Ruang tenang selama tiga jam tiap sesi. Peserta diberi tahu jadwal sedikitnya tujuh hari sebelumnya.", "num2"),
  num("Pre-test 15 butir, dikerjakan paling lambat sehari sebelum sesi 1 dan memakan waktu sekitar 15 menit.", "num2"),
  num("Contoh dokumen dari hotel (folio, laporan kasir, daftar piutang) boleh dibawa bila nama dan angkanya sudah disamarkan. Dokumen itu tidak wajib.", "num2"),
  num("Rekaman sesi dibuat hanya dengan persetujuan peserta dan hotel, dan dipakai peserta untuk mengulang materi.", "num2"),

  h1("7. Evaluasi dan syarat sertifikat"),
  p("Evaluasi memakai dua level Kirkpatrick: reaksi dan pembelajaran. Penerapan di tempat kerja (level 3) dimulai lewat rencana 30 hari milik peserta. Pemantauannya tidak termasuk dalam paket ini."),
  table([2400, 3500, 3738], ["Alat evaluasi", "Isi", "Waktu"], [
    ["Pre-test", "15 butir pilihan ganda, tiga butir per bagian utama", "Sebelum sesi 1"],
    ["Penilaian hasil kerja", "Rubrik empat tingkat pada tujuh hasil kerja utama", "Tiap topik, diringkas pada akhir sesi 3"],
    ["Post-test", "15 butir paralel dengan pre-test dan 2 kasus uraian singkat", "Penutup sesi 3"],
    ["Survei kepuasan", "Enam butir skala 1 sampai 5 dan dua pertanyaan terbuka", "Penutup sesi 3"],
  ], { firstBold: true, firstFill: true }),
  p("Syarat sertifikat yang kami usulkan: hadir di ketiga sesi (sesi yang terlewat dapat diganti pada jadwal lain), mengerjakan pre-test dan post-test, dan menyerahkan hasil kerja tiap topik. Bila Hotel Vila Lumbung punya syarat lain untuk sertifikat, kami mengikutinya.", { before: 120 }),
  p("Contoh sertifikat dan instrumen evaluasi lengkap ada pada berkas pendamping.", { after: 60 }),

  h1("8. Berkas pendamping sebagai bukti kesiapan", true),
  p("Berikut berkas yang sudah kami siapkan untuk program ini. Semuanya bisa dibuka dan dinilai sebelum pelaksanaan."),
  table([3700, 3600, 2338], ["Berkas", "Isi", "Dipakai di"], [
    ["1 Modul Peserta", "Delapan bab dan enam lampiran: konsep, rumus, contoh jurnal, latihan, checklist, templat", "Semua sesi"],
    ["2 Workbook Latihan (peserta)", "Enam lembar kerja dengan data kasus rekaan, sel isian diberi warna", "Topik 1.1 sampai 3.3"],
    ["3 Workbook Latihan (kunci pengajar)", "Isi yang sama dengan jawaban dan rumus", "Pengajar"],
    ["4 Instrumen Evaluasi", "Pre-test, post-test, rubrik penilaian, survei kepuasan", "Sebelum sesi 1 dan penutup sesi 3"],
    ["5 Kunci dan Pembahasan (pengajar)", "Kunci pre-test dan post-test, kunci latihan modul, rubrik uraian", "Pengajar"],
    ["6 Contoh Sertifikat", "Rancangan e-sertifikat dengan kolom isian", "Setelah sesi 3"],
    ["7 Slide Sesi 1", "Sepuluh slide sesi 1", "Sesi 1"],
  ], { firstBold: true, firstFill: true }),

  h1("9. Pengajar dan rujukan"),
  h2("9.1 Pengajar"),
  p("[ISI TIM: nama pengajar, jabatan, pengalaman mengelola AR dan income audit hotel, pendidikan, sertifikasi, foto]"),
  h2("9.2 Rujukan materi"),
  p("Rumus dan istilah yang dipakai dalam materi mengikuti praktik umum industri perhotelan. Rujukan berikut dibuka tim sebelum dokumen dikirim, lihat catatan tim untuk statusnya."),
  num("Kasavana, M. L. dan Brooks, R. M. Managing Front Office Operations. American Hotel and Lodging Educational Institute. Bahan untuk night audit, folio, dan city ledger.", "num3"),
  num("Hotel Association of New York City dan American Hotel and Lodging Association. Uniform System of Accounts for the Lodging Industry (USALI). Bahan untuk rasio kamar dan klasifikasi pendapatan.", "num3"),
  num("Ikatan Akuntan Indonesia. PSAK 71 tentang Instrumen Keuangan dan PSAK 72 tentang Pendapatan dari Kontrak dengan Pelanggan. Bahan untuk penyisihan piutang dan pengakuan pendapatan.", "num3"),
  num("Undang-Undang Nomor 1 Tahun 2022 tentang Hubungan Keuangan antara Pemerintah Pusat dan Pemerintahan Daerah. Bahan untuk pajak barang dan jasa tertentu atas jasa perhotelan. Tarif di daerah Hotel Vila Lumbung mengikuti peraturan daerah setempat.", "num3"),
  num("Knowles, M. S. The Adult Learner. Bahan untuk pendekatan andragogi.", "num3"),
  num("Anderson, L. W. dan Krathwohl, D. R. A Taxonomy for Learning, Teaching, and Assessing. Bahan untuk rumusan tujuan pembelajaran.", "num3"),
  num("Kirkpatrick, D. L. dan Kirkpatrick, J. D. Evaluating Training Programs. Bahan untuk evaluasi.", "num3"),
];

const page = { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } };
const pageL = { size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE }, margin: { top: 1000, bottom: 1000, left: 1134, right: 1134 } };
const doc = makeDoc("Silabus Pelatihan Online AR dan Income Audit Hotel", [
  { properties: { page: { ...page, margin: { top: 700, bottom: 700, left: 1134, right: 1134 } } }, children: sampul },
  { properties: { page }, footers: { default: footer(WP, LABEL) }, children: bag1 },
  { properties: { page: pageL }, footers: { default: footer(WL, LABEL) }, children: lanskap },
  { properties: { page }, footers: { default: footer(WP, LABEL) }, children: bagAkhir },
]);
save(doc, path.join(__dirname, "..", "silabus", "Silabus Pelatihan Online AR dan Income Audit Hotel - Hotel Vila Lumbung.docx"));
