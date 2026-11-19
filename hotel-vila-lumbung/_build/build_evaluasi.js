// Instrumen evaluasi (peserta) dan kunci (pengajar). NODE_PATH=$(npm root -g) node build_evaluasi.js
const path = require("path");
const L = require("./lib.js");
const { p, h1, h2, h3, bullet, num, spacer, table, cover, footer, makeDoc, save, D } = L;
const { AlignmentType } = D;
const W = 9638, C = AlignmentType.CENTER, LEFT = AlignmentType.LEFT;
const page = { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } };
const LET = ["A", "B", "C", "D"];

// [pertanyaan, benar, [salah1, salah2, salah3], pembahasan]
const PRE = [
  ["Total saldo folio tamu yang masih menginap di hotel disebut:", "Guest ledger", ["City ledger", "Advance deposit", "Piutang OTA"], "Guest ledger adalah saldo tamu menginap. City ledger adalah piutang setelah check-out."],
  ["Uang muka yang diterima dari tamu sebelum menginap dicatat sebagai:", "Kewajiban (advance deposit)", ["Pendapatan kamar", "Piutang usaha", "Beban dibayar di muka"], "Pendapatan diakui saat kamar dipakai, jadi uang muka adalah kewajiban sampai saat itu."],
  ["Hotel punya 80 kamar. Pada satu hari 60 kamar terjual berbayar dan pendapatan kamar Rp 36.000.000. ARR hari itu:", "Rp 600.000", ["Rp 450.000", "Rp 480.000", "Rp 750.000"], "ARR = pendapatan kamar dibagi kamar terjual = 36.000.000 dibagi 60."],
  ["Berdasarkan data soal 3, okupansi hari itu:", "75 persen", ["60 persen", "67 persen", "80 persen"], "Okupansi = 60 dibagi 80."],
  ["Berdasarkan data soal 3, RevPAR hari itu:", "Rp 450.000", ["Rp 360.000", "Rp 500.000", "Rp 600.000"], "RevPAR = pendapatan kamar dibagi kamar tersedia = 36.000.000 dibagi 80."],
  ["Night audit adalah:", "Penutupan hari transaksi hotel: memastikan transaksi hari itu lengkap, memposting tarif kamar, dan menyiapkan laporan harian", ["Pemeriksaan laporan keuangan tahunan oleh auditor eksternal", "Penagihan piutang pada malam hari", "Penghitungan stok gudang tiap malam"], "Night audit menutup hari operasional. Income audit memeriksa hasilnya keesokan harinya."],
  ["Tujuan utama income audit harian:", "Memastikan pendapatan yang tercatat benar, lengkap, dan sesuai bukti", ["Menentukan tarif kamar bulan depan", "Mempercepat proses check-in", "Menyusun gaji karyawan"], "Income audit memeriksa pendapatan dengan bukti."],
  ["Tamu perusahaan check-out dan perusahaannya akan membayar. Tindakan kasir yang benar:", "Memindahkan folio ke city ledger dengan otorisasi dan dokumen jaminan", ["Membatalkan folio", "Meminta tamu membayar tunai tanpa konfirmasi", "Membiarkan folio terbuka tanpa dokumen"], "Transfer ke city ledger butuh otorisasi dan dokumen agar piutang bisa ditagih."],
  ["Faktur terbit 1 Desember 2026 dengan termin 30 hari. Jatuh tempo:", "31 Desember 2026", ["15 Desember 2026", "30 Desember 2026", "1 Januari 2027"], "1 Desember ditambah 30 hari adalah 31 Desember."],
  ["Per 10 Desember 2026, sebuah faktur jatuh tempo 5 November 2026. Kelompok umurnya:", "31 sampai 60 hari", ["1 sampai 30 hari", "61 sampai 90 hari", "Belum jatuh tempo"], "Terlambat 35 hari."],
  ["Pelanggan membayar Rp 4.605.000 untuk faktur Rp 4.620.000 tanpa penjelasan. Tindakan awal terbaik:", "Mencatat pembayaran dan mengonfirmasi selisih Rp 15.000 ke pelanggan karena kemungkinan biaya transfer", ["Menganggap lunas tanpa catatan", "Mengembalikan seluruh uang", "Menghapus faktur"], "Selisih beberapa ribu rupiah sering berasal dari biaya transfer. Tetap dikonfirmasi dan dicatat."],
  ["OTA membayar Rp 18.513.000 untuk tagihan Rp 21.780.000. Penyebab paling mungkin:", "Komisi OTA yang dipotong", ["Pembayaran ganda", "Pelanggan membatalkan reservasi", "Salah nomor rekening"], "18.513.000 adalah 85 persen dari 21.780.000, artinya komisi 15 persen."],
  ["DSO menunjukkan:", "Rata-rata hari yang dibutuhkan untuk menagih piutang", ["Jumlah faktur per hari", "Persentase okupansi", "Jumlah pelanggan baru"], "DSO adalah days sales outstanding."],
  ["Saldo buku pembantu city ledger Rp 150.000.000 dan saldo akun di buku besar Rp 149.500.000. Langkah pertama:", "Menelusuri transaksi periode untuk menemukan penyebab selisih Rp 500.000", ["Membuat jurnal penyesuaian agar sama", "Mengabaikan karena nilainya sedikit", "Mengganti saldo buku besar"], "Penyebab ditemukan dulu, baru dikoreksi."],
  ["Faktur sudah lebih dari 90 hari dan pelanggan tidak merespons. Langkah yang tepat:", "Eskalasi sesuai kebijakan: surat peringatan, tahan kredit baru, dan ajukan penyisihan atau penghapusan ke pihak berwenang", ["Menunggu pelanggan menghubungi", "Menghapus faktur dari laporan", "Menagih tamu secara pribadi tanpa dasar"], "Eskalasi, penahanan kredit, dan otorisasi atas penyisihan atau penghapusan."],
];
const POST = [
  ["Piutang atas tagihan yang dibayar setelah tamu check-out disebut:", "City ledger", ["Guest ledger", "Advance deposit", "House use"], "City ledger."],
  ["Hotel menerima deposit dari tamu sebelum tamu tiba. Jurnalnya:", "Debit bank, kredit advance deposit", ["Debit bank, kredit pendapatan kamar", "Debit piutang, kredit bank", "Debit guest ledger, kredit bank"], "Uang muka adalah kewajiban."],
  ["Hotel 100 kamar, 70 terjual berbayar, pendapatan kamar Rp 42.000.000. ARR:", "Rp 600.000", ["Rp 420.000", "Rp 540.000", "Rp 700.000"], "42.000.000 dibagi 70."],
  ["Berdasarkan data soal 3, okupansi:", "70 persen", ["60 persen", "65 persen", "75 persen"], "70 dibagi 100."],
  ["Berdasarkan data soal 3, RevPAR:", "Rp 420.000", ["Rp 350.000", "Rp 500.000", "Rp 600.000"], "42.000.000 dibagi 100."],
  ["Posting tarif kamar, service, dan pajak untuk tamu menginap dilakukan:", "Untuk tamu yang menginap malam itu, sebelum tanggal sistem diganti", ["Hanya saat check-out", "Oleh bagian AR di akhir bulan", "Setelah income audit selesai"], "Posting kamar adalah bagian night audit."],
  ["Setoran kasir kurang Rp 35.000 dari laporan PMS. Langkah income audit:", "Meminta penjelasan kasir, memeriksa void dan paid out, dan mencatat selisih sesuai kebijakan", ["Menambah uang dari dompet pribadi kasir tanpa catatan", "Menghapus transaksi yang selisih", "Menunggu akhir bulan"], "Selisih kas ditelusuri dan dicatat."],
  ["Tarif terposting Rp 450.000, tarif kode CORP seharusnya Rp 380.000. Dampaknya:", "Tamu ditagih lebih Rp 70.000 sebelum service dan pajak", ["Hotel kurang menagih Rp 70.000", "Tamu ditagih lebih Rp 40.000", "Tidak ada dampak"], "450.000 dikurangi 380.000."],
  ["Faktur terbit 20 November 2026 dengan termin 14 hari. Jatuh tempo:", "4 Desember 2026", ["3 Desember 2026", "14 Desember 2026", "20 Desember 2026"], "20 November ditambah 14 hari."],
  ["Per 10 Desember 2026 sebuah faktur jatuh tempo 12 Oktober 2026. Kelompok umurnya:", "31 sampai 60 hari", ["1 sampai 30 hari", "61 sampai 90 hari", "Belum jatuh tempo"], "Terlambat 59 hari."],
  ["Pelanggan membayar Rp 12.000.000 tanpa nomor faktur dan punya dua faktur terbuka. Langkah yang tepat:", "Konfirmasi alokasi ke pelanggan dan, selama menunggu, aplikasikan ke faktur terlama bila kebijakan mengizinkan", ["Mencatat sebagai pendapatan kamar", "Mengaplikasikan ke faktur terbaru", "Mengabaikan sampai pelanggan menagih"], "Konfirmasi lebih dulu, faktur terlama sebagai dasar sementara."],
  ["Transfer Rp 1.000.000 masuk tanpa keterangan pengirim. Perlakuan:", "Dicatat di dana belum teridentifikasi dan pengirimnya ditelusuri", ["Dicatat sebagai pendapatan kamar", "Dikreditkan ke pelanggan terbesar", "Tidak dicatat"], "Dana belum teridentifikasi sampai pengirim jelas."],
  ["Pelanggan menolak invoice karena tidak ada nomor PO. Langkah terbaik:", "Menerbitkan koreksi melalui credit note dan invoice baru yang memuat nomor PO", ["Mengabaikan penolakan", "Menghapus faktur dari buku", "Mengubah angka di invoice lama tanpa dokumen"], "Koreksi meninggalkan jejak dokumen."],
  ["DSO 45 hari sedangkan termin rata-rata pelanggan 30 hari. Artinya:", "Penagihan tertinggal dari termin dan penyebabnya perlu dicari", ["Penagihan sangat lancar", "Okupansi turun", "Piutang harus dihapus"], "DSO melebihi termin."],
  ["Limit kredit pelanggan Rp 20.000.000 dan sisa tagihannya Rp 31.695.000. Tindakan:", "Menahan kredit baru dan meminta pelunasan atau deposit sesuai kebijakan", ["Menaikkan limit otomatis", "Menghapus limit", "Mengabaikan"], "Pemakaian limit melebihi 100 persen."],
];
const URAIAN = [
  "Income audit menemukan dua selisih pada satu hari: batch EDC lebih rendah Rp 150.000 dari laporan PMS dan setoran tunai kurang Rp 35.000. Tulis untuk tiap selisih satu dugaan penyebab, bukti yang diminta, dan tindak lanjut.",
  "Pelanggan korporasi sudah melewati limit kredit dan punya satu faktur yang terlambat 75 hari. Susun lima langkah penanganan dengan penanggung jawab tiap langkah.",
];

function mc(items, offset) {
  const out = []; const keys = [];
  items.forEach(([q, ok, bad], i) => {
    const pos = (i * 3 + offset + Math.floor(i / 4)) % 4; const opts = [...bad]; opts.splice(pos, 0, ok); keys.push(LET[pos]);
    out.push(new D.Paragraph({ spacing: { before: 110, after: 40, line: 280 }, keepNext: true, children: L.runs(`${i + 1}. ${q}`, { bold: true, size: 19 }) }));
    opts.forEach((o, j) => out.push(new D.Paragraph({ indent: { left: 400 }, spacing: { after: 20, line: 270 }, keepNext: j < 3, children: L.runs(`${LET[j]}. ${o}`, { size: 18 }) })));
  });
  return { out, keys };
}
const pre = mc(PRE, 2), post = mc(POST, 1);

const idForm = table([3000, 6638], ["Data peserta", "Isian"], [["Nama", ""], ["Jabatan dan departemen", ""], ["Tanggal", ""], ["Lama bekerja di AR atau income audit", ""]], { firstBold: true, firstFill: true });

// ---------- Instrumen (peserta) ----------
const rubrikHasil = table([2000, 1900, 1900, 1900, 1938], ["Aspek", "1 Perlu penguatan", "2 Cukup", "3 Baik", "4 Sangat baik"], [
  ["Ketepatan angka", "Banyak angka salah, rumus tidak jalan", "Sebagian angka benar, ada salah hitung yang berulang", "Hampir semua angka benar, satu atau dua salah", "Semua angka benar dan konsisten antar lembar"],
  ["Alasan dan penjelasan", "Tidak ada alasan", "Alasan ada tetapi umum", "Alasan sesuai kasus", "Alasan sesuai kasus dan menyebut dampak serta bukti"],
  ["Kelengkapan", "Kurang dari separuh bagian terisi", "Separuh sampai tiga perempat terisi", "Hampir semua terisi", "Semua terisi, termasuk catatan tambahan"],
  ["Kesiapan dipakai", "Perlu dikerjakan ulang", "Bisa dipakai setelah perbaikan besar", "Bisa dipakai setelah perbaikan ringan", "Siap dipakai di hotel"],
], { firstBold: true, firstFill: true });
// "kecil" dilarang di dokumen klien
const survei = table([600, 6038, 3000], ["No", "Pernyataan", "Skala 1 (sangat tidak setuju) sampai 5 (sangat setuju)"], [
  ["1", "Tujuan pelatihan sesuai dengan kebutuhan pekerjaan saya", "1  2  3  4  5"],
  ["2", "Materi mudah diikuti dan runtut", "1  2  3  4  5"],
  ["3", "Studi kasus mirip dengan kejadian di tempat kerja saya", "1  2  3  4  5"],
  ["4", "Pengajar menjawab pertanyaan dengan jelas", "1  2  3  4  5"],
  ["5", "Format daring dan alat bantu (workbook, modul) membantu belajar", "1  2  3  4  5"],
  ["6", "Saya siap menerapkan hasil pelatihan di hotel", "1  2  3  4  5"],
], { align: [C, LEFT, C] });

const instrumen = [
  h1("Instrumen Evaluasi"),
  p("Dipakai untuk pelatihan AR dan Income Audit Hotel. Pre-test dikerjakan paling lambat sehari sebelum sesi 1. Post-test dan survei dikerjakan pada penutup sesi 3. Kunci ada di berkas pengajar."),
  idForm,
  h1("Bagian 1. Pre-test (15 butir, 15 menit)", true),
  p("Pilih satu jawaban yang paling tepat."),
  ...pre.out,
  h1("Bagian 2. Post-test (15 butir pilihan ganda dan 2 uraian, 20 menit)", true),
  p("Pilih satu jawaban yang paling tepat untuk butir 1 sampai 15. Jawab butir uraian dengan singkat dan jelas."),
  ...post.out,
  h3("Uraian"),
  ...URAIAN.map((u, i) => p(`${i + 1}. ${u}`)),
  h1("Bagian 3. Rubrik penilaian hasil kerja", true),
  p("Pengajar menilai tujuh hasil kerja utama: lembar tarif dan rekap income audit, laporan temuan, tabel jurnal, invoice, lembar city ledger, lembar rekon bank, dan laporan AR. Tiap hasil kerja dinilai dengan empat aspek berikut."),
  rubrikHasil,
  h1("Bagian 4. Survei kepuasan"),
  survei,
  p("Pertanyaan terbuka 1: bagian mana yang paling bermanfaat bagi pekerjaan Anda?", { before: 140 }),
  p("Pertanyaan terbuka 2: bagian mana yang perlu diperbaiki atau ditambah?"),
];
save(makeDoc("Instrumen Evaluasi AR dan Income Audit Hotel", [{ properties: { page }, footers: { default: footer(W, "Instrumen Evaluasi AR dan Income Audit Hotel") }, children: instrumen }]),
  path.join(__dirname, "..", "assets", "4 Instrumen Evaluasi Pre-test Post-test dan Survei.docx"));

// ---------- Kunci (pengajar) ----------
const keyRows = (items, keys) => items.map(([q, ok, , why], i) => [String(i + 1), keys[i], ok, why]);
const kunci = [
  h1("Kunci dan Pembahasan (khusus pengajar)"),
  p("Berkas ini tidak dibagikan kepada peserta sebelum evaluasi selesai. Isinya kunci pre-test dan post-test, rubrik uraian, dan kunci latihan modul. Angka latihan bersumber dari workbook kunci pengajar."),
  h2("1. Kunci pre-test"),
  table([600, 800, 4300, 3938], ["No", "Kunci", "Jawaban", "Pembahasan"], keyRows(PRE, pre.keys), { align: [C, C, LEFT, LEFT], size: 16 }),
  h2("2. Kunci post-test"),
  table([600, 800, 4300, 3938], ["No", "Kunci", "Jawaban", "Pembahasan"], keyRows(POST, post.keys), { align: [C, C, LEFT, LEFT], size: 16 }),
  h2("3. Rubrik uraian post-test"),
  table([1000, 8638], ["Skor", "Kriteria"], [
    ["3", "Penyebab masuk akal, bukti atau tindakan jelas, memuat batas waktu atau penanggung jawab"],
    ["2", "Penyebab dan tindakan ada tetapi umum, atau salah satu tidak ada"],
    ["1", "Hanya menyebut masalah, tidak ada tindakan yang konkret"],
    ["0", "Tidak dijawab atau tidak sesuai"],
  ], { firstBold: true, align: [C, LEFT] }),
  p("Contoh jawaban uraian 1: EDC lebih rendah Rp 150.000, dugaan satu transaksi belum masuk batch atau batch ditutup sebelum transaksi terakhir, bukti slip EDC dan settlement hari berikutnya, tindak lanjut cocokkan settlement besok dan posting koreksi bila ada transaksi ganda. Kas kurang Rp 35.000, dugaan kesalahan kembalian atau paid out tanpa bukti, bukti laporan kasir dan struk, tindak lanjut minta penjelasan kasir dan catat selisih sesuai kebijakan.", { before: 100 }),
  p("Contoh jawaban uraian 2: (1) Hubungi kontak keuangan pelanggan hari itu juga, penanggung jawab AR. (2) Kirim surat peringatan dengan tembusan sales, AR. (3) Tahan booking baru atau minta bayar di muka, kepala sales dan keuangan. (4) Eskalasi ke manajer keuangan dan GM bila tidak ada janji bayar dalam 7 hari. (5) Ajukan penyisihan bila melewati 90 hari tanpa janji bayar, manajer keuangan."),
  h1("4. Kunci latihan modul", true),
  table([1500, 8138], ["Latihan", "Kunci"], [
    ["1. Rasio", "Okupansi 60 dibagi 80 = 75 persen. ARR 36.000.000 dibagi 60 = Rp 600.000. RevPAR 36.000.000 dibagi 80 = Rp 450.000."],
    ["2. Catatan serah terima", "Perlu ditindaklanjuti: no. 1 (batch EDC belum ditutup), no. 2 (void tanpa pemberi izin), no. 5 (charge manual tanpa struk), no. 6 (komplimen tanpa persetujuan). Wajar: no. 3 (ada surat jaminan), no. 4 (no-show sesuai kebijakan)."],
    ["3. Income audit", "Sembilan temuan. Tarif: kamar 105 lebih Rp 70.000, kamar 109 kurang Rp 40.000, kamar 203 kurang Rp 40.000 (selisih bersih Rp 10.000 kurang). Komplimen kamar 207 tanpa persetujuan. F&B: bar lebih Rp 50.000, room service kurang Rp 100.000. Penyelesaian: kas kurang Rp 35.000, EDC kurang Rp 150.000, transfer city ledger tanpa otorisasi Rp 505.000. Rasio: 28 kamar berbayar, okupansi 56 persen, ARR Rp 544.286, RevPAR Rp 304.800."],
    ["4. Kredit", "Hasil berupa pertimbangan, bukan jawaban tunggal. PT Nusa Teknik: setujui limit sekitar Rp 20.000.000 (40 x 380.000 x 1,21 = Rp 18.392.000), termin 30 hari, dokumen NPWP dan akta, deposit untuk transaksi awal. CV Cahaya Wisata: tolak kenaikan limit, tahan kredit baru dan minta pelunasan lebih dulu. Dinas Pendidikan: setujui termin 45 hari dengan syarat dokumen surat tugas atau SPK, tercantum di perjanjian."],
    ["5. Jurnal", "(1) Debit bank 500.000, kredit advance deposit 500.000. (2) Debit guest ledger 605.000, kredit pendapatan kamar 500.000, kredit utang service charge 50.000, kredit utang pajak hotel 55.000. (3) Debit advance deposit 500.000, kredit guest ledger 500.000. (4) Debit kas 105.000, kredit guest ledger 105.000. (5) Debit city ledger PT Maju Bersama 1.210.000, kredit guest ledger 1.210.000."],
    ["6. Invoice", "Nett 3.000.000, service 300.000, pajak 330.000, total Rp 3.630.000. Jatuh tempo 9 Januari 2027 (10 Desember 2026 ditambah 30 hari)."],
    ["7. Tiga invoice", "A: pajak seharusnya 10 persen dari 1.672.000 = Rp 167.200, total Rp 1.839.200, dan nomor PO wajib diisi. B: nama pelanggan Kab. Contoh (bukan Kota), termin 45 hari sehingga jatuh tempo 15 Januari 2027. C: tarif Rp 560.000 dan 2 malam, nett Rp 1.120.000, service Rp 112.000, pajak Rp 123.200, total Rp 1.355.200."],
    ["8. Aging", "Total sisa Rp 147.030.000. Belum jatuh tempo Rp 71.995.000, 1-30 hari Rp 47.190.000, 31-60 hari Rp 20.200.000, 61-90 hari Rp 4.620.000, lebih dari 90 hari Rp 3.025.000. Catatan: INV-2610-1001, 2609-0902, 2610-1002, 2610-1004, 2610-1006, dan 2611-1103 sudah ada pembayarannya di bank (latihan 9), jadi rekonsiliasi dilakukan sebelum menagih. Prioritas yang masuk akal dari sisa faktur: INV-2608-0701 (108 hari), INV-2610-1005 (37 hari, Rp 5.445.000), INV-2611-1101 (Rp 7.260.000), INV-2611-1105 (Rp 6.655.000), INV-2611-1102 sisa setelah alokasi pembayaran."],
    ["9. Rekon bank", "Total mutasi Rp 63.343.000. Selisih: 4 Desember kurang Rp 15.000 (biaya transfer), 5 Desember tanpa nomor faktur (alokasi INV-2610-1002 sisa 5.680.000 dan INV-2611-1102 sebesar 6.320.000 setelah konfirmasi), 9 Desember kurang Rp 3.267.000 (komisi OTA 15 persen), 10 Desember Rp 1.000.000 tidak dikenali (dana belum teridentifikasi). Mutasi lain cocok penuh."],
    ["10. Laporan AR", "DSO 71,1 hari. Persentase piutang lewat jatuh tempo lebih dari 30 hari 18,9 persen. CV Cahaya Wisata (131,6 persen limit) dan PT Samudra Logistik (158,5 persen) melebihi limit. OTA Sampel mendekati limit (96,8 persen)."],
    ["Bab 8. Kasus terpadu", "Urutan yang masuk akal: (5) aging untuk rapat 14.00 karena ada batas waktu, dengan catatan pembayaran bank belum diaplikasi. (2) Protes tarif PT Maju Bersama, bandingkan invoice dengan kontrak dan folio, bila salah terbitkan credit note, penanggung jawab AR. (1) Transfer city ledger tanpa otorisasi, tahan penagihan sampai ada persetujuan, penanggung jawab income audit dan supervisor front office. (3) Dana Rp 1.000.000 tanpa keterangan, catat di dana belum teridentifikasi dan telusuri lewat bank. (4) Booking CV Cahaya Wisata, jangan setujui kredit karena melewati limit dan ada faktur lebih dari 90 hari, tawarkan bayar di muka."],
  ], { firstBold: true, firstFill: true }),
];
save(makeDoc("Kunci dan Pembahasan AR dan Income Audit Hotel", [{ properties: { page }, footers: { default: footer(W, "Kunci Pengajar") }, children: kunci }]),
  path.join(__dirname, "..", "assets", "5 Kunci dan Pembahasan (pengajar).docx"));
console.log("kunci pre", pre.keys.join(""), "post", post.keys.join(""));
