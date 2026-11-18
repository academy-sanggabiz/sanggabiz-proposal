// Membuat silabus pelatihan Communication & Leadership untuk Tim Kitchen Cafe Melt Me.
// Jalankan: NODE_PATH=$(npm root -g) node build_silabus.js
// Gaya: keluarga compro Sanggabiz (navy 0B396D, kuning FFC00C), Arial, A4.
const path = require("path");
const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Footer, Header,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber, HighlightColor,
} = require("docx");

const NAVY = "0B396D", FIRST = "EEF3F9", LINE = "BFC8D4", GOLD = "FFC00C";
const FONT = "Arial";
const W = 9638; // lebar isi A4, margin 1134
const OUT = path.join(__dirname, "..", "silabus", "v1 Silabus Communication dan Leadership Tim Kitchen - Cafe Melt Me.docx");

// Teks berformat [ISI TIM: ...] diberi stabilo kuning.
function runs(text, o = {}) {
  return text.split(/(\[ISI TIM:[^\]]*\])/).filter(Boolean).map((t) => new TextRun({
    text: t, font: FONT, color: o.color || "000000", size: o.size || 20, bold: o.bold, italics: o.italics,
    highlight: t.startsWith("[ISI TIM:") ? HighlightColor.YELLOW : undefined,
  }));
}
const para = (text, o = {}) => new Paragraph({
  alignment: o.align || AlignmentType.LEFT,
  spacing: { after: o.after ?? 140, before: o.before ?? 0, line: 276 },
  keepNext: o.keepNext,
  children: runs(text, o),
});
const title = (text) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { before: 0, after: 80, line: 300 },
  children: runs(text, { bold: true, color: NAVY, size: 34 }),
});
const subtitle = (text) => new Paragraph({
  alignment: AlignmentType.CENTER, spacing: { after: 240 },
  children: runs(text, { size: 20, color: "444444" }),
});
const h2 = (text) => new Paragraph({
  keepNext: true, spacing: { before: 280, after: 140, line: 269 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 2 } },
  children: runs(text, { bold: true, color: NAVY, size: 26 }),
});
const h3 = (text) => new Paragraph({
  keepNext: true, spacing: { before: 260, after: 100, line: 269 },
  children: runs(text, { bold: true, color: NAVY, size: 22 }),
});
const focus = (text) => new Paragraph({
  keepNext: true, spacing: { after: 120, line: 276 },
  children: [...runs("Fokus: ", { bold: true, color: NAVY }), ...runs(text)],
});

const border = { style: BorderStyle.SINGLE, size: 6, color: LINE };
const borders = { top: border, bottom: border, left: border, right: border };

function cell(content, width, o = {}) {
  const lines = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, verticalAlign: o.valign || VerticalAlign.TOP,
    shading: o.fill ? { type: ShadingType.CLEAR, fill: o.fill, color: "auto" } : undefined,
    margins: { top: 80, bottom: 80, left: 110, right: 110 },
    children: lines.map((l, k) => new Paragraph({
      alignment: o.align || AlignmentType.LEFT,
      spacing: { after: k < lines.length - 1 ? 50 : 0, line: 252 },
      children: runs(l, { size: o.size || 18, color: o.color, bold: o.bold }),
    })),
  });
}
function table(widths, head, rows, o = {}) {
  const size = o.size || 18;
  const trs = [];
  if (head) trs.push(new TableRow({ cantSplit: true, tableHeader: true,
    children: head.map((h, i) => cell(h, widths[i], { fill: NAVY, bold: true, color: "FFFFFF", align: AlignmentType.CENTER, size, valign: VerticalAlign.CENTER })) }));
  rows.forEach((r) => trs.push(new TableRow({ cantSplit: o.split ? false : true,
    children: r.map((c, i) => cell(c, widths[i], { size, fill: i === 0 ? FIRST : undefined, bold: i === 0 })) })));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, alignment: AlignmentType.CENTER, rows: trs });
}
const gap = () => new Paragraph({ spacing: { after: 100 }, children: [] });

// Tabel rinci satu topik: label di kiri, isi di kanan.
function topik(judul, rows) {
  return [h3(judul), table([2100, 7538], null, rows, { split: true }), gap()];
}

const body = [];

body.push(title("SILABUS PELATIHAN COMMUNICATION & LEADERSHIP"));
body.push(subtitle("Untuk Tim Kitchen Cafe Melt Me, Batam. Disusun Sanggabiz, 18 November 2026. Versi 1."));

// ---------------- 1 ----------------
body.push(h2("1. Ringkasan Program"));
body.push(table([2300, 7338], ["Elemen", "Isi"], [
  ["Klien", "Cafe Melt Me, diwakili Lidya (Owner). Dasar silabus: rapat 17 November 2026 melalui Gmeet."],
  ["Fokus", "Komunikasi, teamwork, koordinasi antarbagian, dan leadership Head Kitchen."],
  ["Peserta", "Tim Kitchen, 4 sampai 5 orang termasuk Head Kitchen. Jumlah pasti menunggu konfirmasi klien."],
  ["Durasi", "1 hari, 6 jam efektif (360 menit). Rundown 09.00 - 16.00 WIB sudah termasuk istirahat. Jam mulai bisa digeser mengikuti jam operasional cafe."],
  ["Tempat", "Tatap muka di Batam. Usul kami di cafe sendiri pada waktu tutup, supaya simulasi memakai ruang dan alur kerja yang sama dengan sehari-hari dan tidak ada biaya sewa tempat. [ISI TIM: konfirmasi ke Lidya, alamat cafe]"],
  ["Jadwal", "Target akhir November 2026. [ISI TIM: usulan hari dan tanggal alternatif setelah cek ketersediaan trainer]"],
  ["Trainer", "Satu trainer dari Batam sesuai preferensi klien. [ISI TIM: nama dan profil trainer]"],
  ["Pendekatan", "Aplikatif. Setiap topik menyisakan lebih dari separuh waktu untuk praktik dan simulasi memakai situasi dapur yang dikenal peserta."],
]));

// ---------------- 2 ----------------
body.push(h2("2. Dasar Penyusunan"));
body.push(para("Kolom kiri memuat isi MoM 17 November 2026. Kolom kanan adalah tafsiran kami tentang bagian silabus yang menjawabnya. Koreksi bila ada yang keliru.", { keepNext: true }));
body.push(table([5200, 4438], ["Temuan dalam MoM (nomor bagian)", "Dijawab di (tafsiran kami)"], [
  ["Kerja sama antarbagian di Kitchen belum optimal setelah operasional sekitar satu tahun (1.1, 1.2)", "Sesi 1 dan Sesi 2"],
  ["Menu bergeser dari pasta ke konsep brunch, sehingga koordinasi dan komunikasi perlu lebih baik (1.3, 1.4)", "Topik 2.2 dan 4.1 memakai tiket pesanan brunch"],
  ["Head Kitchen perlu mengarahkan, mengkoordinasikan, dan membangun kerja sama anggota (1.5)", "Sesi 3"],
  ["Cafe belum pernah mengadakan pelatihan serupa (1.6)", "Pembukaan dan pre-test. Materi mulai dari dasar dan kedalamannya disesuaikan hasil asesmen awal (bagian 2 MoM)"],
  ["Metode aplikatif dengan materi, diskusi, simulasi, praktik, dan melibatkan semua peserta (4.2 sampai 4.4)", "Semua topik. Tidak ada sesi ceramah lebih dari 10 menit"],
  ["Penawaran efisien, trainer dari Batam, pelatihan di jam kerja (5.1, 7.3, 7.4, 9)", "Satu hari, satu trainer, simulasi memakai kartu tanpa memasak sungguhan, bahan cetak sederhana"],
]));

// ---------------- 3 ----------------
body.push(h2("3. Metode yang Dipakai"));
body.push(table([2200, 3300, 4138], ["Metode", "Dipakai di", "Alasan"], [
  ["ADDIE", "Alur program: analisis (formulir dan wawancara), desain (silabus ini), pengembangan bahan, pelaksanaan satu hari, evaluasi", "Alur baku untuk pelatihan yang punya bahan dan evaluasi"],
  ["Backward design (Wiggins dan McTighe)", "Asesmen awal sebelum hari pelatihan. Trainer menyesuaikan contoh dan kedalaman materi dengan temuannya", "MoM bagian 2 meminta kedalaman materi mengikuti kondisi aktual tim"],
  ["Andragogi (Knowles)", "Semua aktivitas dimulai dari kejadian nyata di dapur peserta. Trainer berperan sebagai fasilitator", "Peserta orang dewasa yang belajar dari pengalamannya"],
  ["Taksonomi Bloom revisi", "Tujuan pembelajaran tiap topik memakai kata kerja Bloom (C2 memahami, C3 menerapkan, C4 menganalisis, C5 mengevaluasi, C6 mencipta)", "Tujuan terukur dan bisa diamati"],
  ["Kirkpatrick", "Evaluasi pada level 1 sampai 3 (bagian 9)", "Klien meminta bukti peningkatan kemampuan yang dapat dipakai di pekerjaan"],
]));

// ---------------- 4 ----------------
body.push(h2("4. Ringkasan Silabus"));
body.push(table([1500, 3600, 1300, 3238], ["Sesi", "Topik", "Durasi", "Hasil"], [
  ["Persiapan (sebelum hari H)", "Asesmen awal: formulir 10 menit per peserta dan wawancara daring 15 menit dengan Lidya dan Head Kitchen", "25 menit di luar hari pelatihan", "Peta kondisi awal tim dan daftar menu brunch untuk bahan simulasi"],
  ["Pembukaan", "Kontrak belajar dan pre-test", "30 menit", "Skor pre-test dan Papan Tantangan Dapur Kami"],
  ["Sesi 1 Komunikasi", "1.1 Pesan singkat dan jelas saat jam sibuk", "45 menit", "Kartu Bahasa Dapur Kami"],
  ["", "1.2 Mendengar, umpan balik, dan menyelesaikan salah paham", "45 menit", "Satu kejadian teranalisis dan tiga kalimat umpan balik"],
  ["Sesi 2 Teamwork dan koordinasi", "2.1 Peran, tanggung jawab, dan serah terima antarbagian", "45 menit", "Peta Peran Tim Kitchen"],
  ["", "2.2 Koordinasi alur pesanan brunch", "45 menit", "Alur Pesanan Brunch dan tiga aturan koordinasi"],
  ["Sesi 3 Leadership Head Kitchen", "3.1 Peran pemimpin dan gaya mengarahkan", "45 menit", "Matriks gaya mengarahkan dan dua komitmen Head Kitchen"],
  ["", "3.2 Briefing, delegasi, dan umpan balik kepada anggota", "45 menit", "Templat Briefing 5 Menit dan Kartu Delegasi"],
  ["Sesi 4 Praktik terpadu", "4.1 Simulasi layanan brunch terpadu", "35 menit", "Lembar penilaian simulasi"],
  ["", "4.2 Rencana penerapan 30 hari, post-test, dan penutup", "25 menit", "Kartu Komitmen, Rencana 30 Hari, skor post-test"],
]));

// ---------------- 5 ----------------
body.push(h2("5. Rundown Hari Pelatihan"));
body.push(table([1900, 5538, 2200], ["Waktu", "Kegiatan", "Menit efektif"], [
  ["09.00 - 09.30", "Pembukaan, kontrak belajar, pre-test", "30"],
  ["09.30 - 11.00", "Sesi 1: topik 1.1 dan 1.2", "90"],
  ["11.00 - 11.15", "Istirahat", "-"],
  ["11.15 - 12.45", "Sesi 2: topik 2.1 dan 2.2", "90"],
  ["12.45 - 13.30", "Ishoma", "-"],
  ["13.30 - 15.00", "Sesi 3: topik 3.1 dan 3.2", "90"],
  ["15.00 - 16.00", "Sesi 4: topik 4.1 dan 4.2", "60"],
  ["Total", "", "360 (6 jam)"],
]));
body.push(gap());
body.push(para("Bila dapur tidak bisa ditinggal sehari penuh, hari yang sama dapat dipecah menjadi dua pertemuan: pertemuan pertama memuat Pembukaan, Sesi 1, dan Sesi 2 (3,5 jam), pertemuan kedua memuat Sesi 3 dan Sesi 4 (2,5 jam). Isi dan urutan tidak berubah."));

// ---------------- 6 ----------------
body.push(h2("6. Silabus Rinci"));
body.push(para("Istilah yang dipakai di silabus. Mise en place adalah persiapan bahan dan alat sebelum jam sibuk. Tiket pesanan adalah kertas atau layar yang memuat pesanan satu meja. Ulang pesan (closed-loop communication) adalah cara penerima mengulang isi pesan dan pengirim membenarkannya. Titik serah piring adalah tempat semua komponen satu pesanan dikumpulkan dan diperiksa sebelum diantar. Alat bantu cetak seperti kartu tiket dan lembar daftar periksa disiapkan trainer."));

body.push(h3("Pembukaan: Kontrak Belajar dan Pre-Test (30 menit)"));
body.push(table([2100, 7538], null, [
  ["Tujuan pembelajaran", ["Peserta menjelaskan (C2) tujuan hari ini dan menyepakati aturan main kelas.", "Peserta menyebutkan (C1) satu tantangan nyata di dapur yang ingin diselesaikan."]],
  ["Outline materi", ["1. Tujuan dan alur satu hari.", "2. Aturan main: semua bicara, tidak ada jawaban yang dinilai benar atau salah, cerita dapur tidak keluar dari ruangan.", "3. Pre-test."]],
  ["Aktivitas", [
    "1. (5 menit) Trainer membuka dan menempel rundown di dinding. Peserta membaca urutan hari.",
    "2. (10 menit) Peserta mengerjakan pre-test sendiri-sendiri: 8 soal pilihan ganda dan 2 situasi dapur yang dijawab satu kalimat. Trainer membacakan soal bila diminta.",
    "3. (10 menit) Tiap peserta menulis di kertas tempel satu hal yang paling sering membuat dapur kacau saat ramai, lalu menempelnya di papan. Trainer mengelompokkan kertas yang mirip dan memberi judul papan: Tantangan Dapur Kami. Papan dipakai sampai penutup.",
    "4. (5 menit) Peserta dan trainer menyepakati tiga aturan main dan menulisnya di kertas besar."]],
  ["Alat dan media", "Lembar pre-test, kertas tempel, spidol, kertas besar, dinding atau papan tulis."],
  ["Output", "Skor pre-test tiap peserta dan Papan Tantangan Dapur Kami."],
  ["Ukuran keberhasilan", "Semua peserta mengisi pre-test dan menempel sedikitnya satu tantangan."],
]));
body.push(gap());

// Sesi 1
body.push(h2("Sesi 1. Komunikasi di Dapur"));
body.push(focus("pesan yang sampai utuh pada saat dapur ramai dan salah paham yang selesai tanpa mencari siapa yang salah."));
body.push(...topik("Topik 1.1 Pesan Singkat dan Jelas saat Jam Sibuk (45 menit)", [
  ["Tujuan pembelajaran", ["Peserta menjelaskan (C2) unsur pesan yang lengkap di dapur.", "Peserta menerapkan (C3) ulang pesan pada tiket pesanan di tengah suara bising."]],
  ["Outline materi", [
    "1. Mengapa pesan salah tangkap di dapur ramai: bising, tergesa, dan singkatan yang berbeda antarorang.",
    "2. Pesan lengkap: ditujukan ke siapa, apa, berapa, kapan.",
    "3. Ulang pesan: penerima mengulang isi pesan, pengirim membenarkan.",
    "4. Kata dan isyarat bersama untuk minta bantuan, menahan pesanan, dan pesanan siap."]],
  ["Aktivitas", [
    "1. (10 menit) Trainer mengucapkan dua pesan. Pesan pertama: \"Yang tadi tolong dicepetin.\" Pesan kedua: \"Yang pegang telur, dua porsi pancake meja 5, keluar dua menit lagi.\" Peserta menulis apa saja yang tidak jelas di pesan pertama. Contoh menu diganti dengan menu brunch Cafe Melt Me.",
    "2. (15 menit) Peserta berpasangan. Trainer menyalakan musik keras dari speaker. A membacakan lima tiket pesanan dari kartu, B mencatat dan mengulangnya. Peran ditukar. Bila peserta berjumlah ganjil, satu orang berpasangan dengan trainer.",
    "3. (10 menit) Tiap pasangan menyepakati satu kata atau isyarat untuk tiga keadaan: minta bantuan, tahan pesanan, pesanan siap. Semua pasangan menyatukan hasilnya menjadi satu daftar.",
    "4. (10 menit) Tiap pasangan mempraktikkan daftar itu di depan kelas dengan dua tiket. Trainer mencentang lembar daftar periksa pola pesan."]],
  ["Alat dan media", "Kartu tiket pesanan dari menu brunch (5 lembar per pasangan), speaker, lembar daftar periksa pola pesan, kertas besar."],
  ["Output", "Kartu Bahasa Dapur Kami: daftar kata dan isyarat bersama, ditempel di dapur."],
  ["Ukuran keberhasilan", "Dalam latihan pasangan, sedikitnya 4 dari 5 tiket dicatat dan diulang dengan benar tanpa koreksi trainer."],
]));
body.push(...topik("Topik 1.2 Mendengar, Umpan Balik, dan Menyelesaikan Salah Paham (45 menit)", [
  ["Tujuan pembelajaran", ["Peserta menganalisis (C4) satu kejadian salah paham antarbagian.", "Peserta menerapkan (C3) umpan balik model Situasi, Perilaku, Dampak (SBI)."]],
  ["Outline materi", [
    "1. Mendengar aktif: menatap lawan bicara, tidak memotong, merangkum sebelum menjawab.",
    "2. Umpan balik SBI: sebutkan situasinya, perilaku yang terlihat, dan dampaknya.",
    "3. Menyampaikan keberatan: saat ramai cukup satu kalimat, pembahasan penuh setelah jam sibuk.",
    "4. Menyelesaikan salah paham dengan menanyakan apa yang terjadi, bukan siapa yang salah."]],
  ["Aktivitas", [
    "1. (10 menit) Kelompok memilih satu kejadian dari Papan Tantangan Dapur Kami, misalnya pesanan terlambat karena bagian lain belum siap. Tiap peserta menulis versi ceritanya dalam tiga kalimat.",
    "2. (10 menit) Cerita dibacakan bergiliran. Peserta menandai bagian yang berbeda antarversi. Trainer menjelaskan SBI dengan satu contoh dari cerita itu.",
    "3. (15 menit) Peserta berpasangan. A menyampaikan umpan balik atas kejadian itu memakai SBI, B merangkum ucapan A sebelum menjawab. Peran ditukar.",
    "4. (10 menit) Kelompok menilai kalimat mana yang terasa menyalahkan dan mana yang terasa membantu, lalu menulis tiga kalimat umpan balik siap pakai di kartu."]],
  ["Alat dan media", "Kertas cerita, lembar SBI satu halaman, kartu kalimat."],
  ["Output", "Satu kejadian yang sudah dianalisis (tiga versi cerita dan titik salah pahamnya) dan tiga kalimat umpan balik siap pakai."],
  ["Ukuran keberhasilan", "Setiap peserta menyampaikan satu umpan balik yang memuat ketiga unsur SBI, dicek trainer dengan daftar periksa."],
]));

// Sesi 2
body.push(h2("Sesi 2. Teamwork dan Koordinasi Antarbagian"));
body.push(focus("tiap tugas punya pemilik, serah terima jelas, dan pesanan brunch mengalir tanpa macet."));
body.push(...topik("Topik 2.1 Peran, Tanggung Jawab, dan Serah Terima Antarbagian (45 menit)", [
  ["Tujuan pembelajaran", ["Peserta menganalisis (C4) tugas yang bertumpuk dan tugas yang belum punya pemilik.", "Peserta menyusun (C6) peta peran tim."]],
  ["Outline materi", [
    "1. Pembagian kerja dari sebelum buka, jam ramai, sampai setelah tutup.",
    "2. Tiga pertanyaan untuk tiap tugas: siapa yang mengerjakan, siapa yang membantu, siapa yang diberi tahu.",
    "3. Titik serah terima: bahan datang, mise en place ke tiap bagian, piring ke pelayan, pergantian shift.",
    "4. Tugas bertumpuk dan tugas tanpa pemilik."]],
  ["Aktivitas", [
    "1. (10 menit) Tiap peserta menulis di kartu semua tugasnya dari buka sampai tutup, satu tugas satu kartu.",
    "2. (15 menit) Semua kartu ditempel pada alur hari di dinding: sebelum buka, jam ramai, setelah tutup. Kelompok menandai kartu yang bertumpuk dengan stiker merah (dua orang mengerjakan hal sama) dan tugas yang belum punya pemilik dengan stiker kuning.",
    "3. (15 menit) Kelompok menyepakati satu pemilik dan satu pembantu untuk tiap tugas bertanda, lalu menulis namanya di kartu.",
    "4. (5 menit) Kelompok memilih tiga titik serah terima yang paling sering macet dan menulis satu kalimat serah terima untuk masing-masing."]],
  ["Alat dan media", "Kartu tugas dua warna, stiker merah dan kuning, dinding atau papan lebar, spidol."],
  ["Output", "Peta Peran Tim Kitchen: satu lembar berisi tugas, pemilik, pembantu, dan tiga kalimat serah terima. Difoto trainer dan dicetak untuk ditempel."],
  ["Ukuran keberhasilan", "Di peta akhir tidak ada kartu tanpa pemilik. Tiap peserta dapat menyebut tiga tugas yang menjadi tanggung jawabnya dan siapa pembantunya."],
]));
body.push(...topik("Topik 2.2 Koordinasi Alur Pesanan Brunch (45 menit)", [
  ["Tujuan pembelajaran", ["Peserta menerapkan (C3) peta peran dan ulang pesan pada alur pesanan brunch.", "Peserta mengevaluasi (C5) titik macet pada alur itu."]],
  ["Outline materi", [
    "1. Alur satu pesanan: tiket masuk, dibagi ke bagian, dimasak, dirakit, diperiksa, diantar.",
    "2. Menu yang komponennya dari beberapa bagian harus selesai bersamaan.",
    "3. Siapa memberi aba di titik serah piring.",
    "4. Menyampaikan keterlambatan sedini mungkin."]],
  ["Aktivitas", [
    "1. (10 menit) Trainer membagikan enam tiket brunch dari menu aktual. Kelompok menggambar di papan alur satu tiket: siapa menerima, diteruskan ke siapa, siapa memeriksa, siapa mengantar.",
    "2. (20 menit) Simulasi 1. Peserta mengambil posisi sesuai Peta Peran. Selama 12 menit, enam tiket dijalankan berurutan tanpa memasak sungguhan: peserta memindahkan kartu komponen antarbagian di meja. Delapan menit sisanya untuk membagi posisi dan menjelaskan aturan. Satu anggota mengamati dengan lembar pengamatan, trainer ikut mencatat.",
    "3. (10 menit) Pengamat melaporkan apa yang terlihat dan terdengar. Kelompok menandai tiga titik macet pada gambar alur.",
    "4. (5 menit) Kelompok menulis satu aturan baru untuk tiap titik macet."]],
  ["Alat dan media", "Enam kartu tiket brunch, kartu komponen menu, meja panjang, lembar pengamatan, penghitung waktu."],
  ["Output", "Alur Pesanan Brunch (gambar difoto) dan tiga aturan koordinasi."],
  ["Ukuran keberhasilan", "Tiga titik macet tercatat dengan bukti dari lembar pengamatan. Titik yang sama diamati lagi pada Simulasi 2 di Topik 4.1."],
]));

// Sesi 3
body.push(h2("Sesi 3. Leadership Head Kitchen"));
body.push(focus("Head Kitchen memilih cara mengarahkan yang cocok untuk tiap anggota, dan anggota ikut menyampaikan apa yang mereka butuhkan. Seluruh tim hadir di sesi ini."));
body.push(...topik("Topik 3.1 Peran Pemimpin dan Gaya Mengarahkan (45 menit)", [
  ["Tujuan pembelajaran", ["Peserta menjelaskan (C2) empat gaya mengarahkan.", "Head Kitchen menganalisis (C4) gaya yang cocok untuk tiap anggota dan tiap tugas."]],
  ["Outline materi", [
    "1. Tugas pemimpin di dapur: menetapkan arah, membagi kerja, menjaga mutu, menjaga suasana.",
    "2. Empat gaya mengarahkan menurut kesiapan anggota: mengarahkan, melatih, mendukung, mendelegasikan (Hersey dan Blanchard).",
    "3. Memilih gaya per orang dan per tugas. Contoh: anggota yang baru memegang menu brunch berbeda kebutuhannya dengan anggota yang sudah lama memegang menu pasta.",
    "4. Apa yang bisa dilakukan anggota agar arahan pemimpin lebih mudah dijalankan."]],
  ["Aktivitas", [
    "1. (10 menit) Trainer menjelaskan empat gaya dengan dua contoh dapur: koki baru pada menu baru dan koki lama pada menu lama.",
    "2. (15 menit) Head Kitchen mengisi matriks untuk tiap anggota: tugas utama, tingkat kesiapan pada menu brunch (rendah, sedang, tinggi), dan gaya yang dipilih. Matriks hanya dipegang Head Kitchen dan tidak dibagikan. Pada waktu yang sama, tiap anggota menulis di kartu satu kalimat: yang saya butuhkan dari Head Kitchen untuk tugas saya.",
    "3. (15 menit) Anggota membacakan kartunya kepada Head Kitchen satu per satu, 3 menit per orang. Head Kitchen menjawab dengan satu kalimat: yang akan saya ubah, atau yang perlu kita bicarakan lagi.",
    "4. (5 menit) Head Kitchen menulis dua komitmen cara mengarahkan yang akan dicoba bulan ini."]],
  ["Alat dan media", "Lembar matriks gaya mengarahkan, kartu kebutuhan anggota, lembar komitmen."],
  ["Output", "Matriks gaya mengarahkan (milik Head Kitchen), kartu kebutuhan tiap anggota, dan dua komitmen Head Kitchen."],
  ["Ukuran keberhasilan", "Head Kitchen menyebut gaya yang dipilih beserta alasannya untuk setiap anggota. Setiap anggota menulis satu kebutuhan dan mendapat jawaban."],
]));
body.push(...topik("Topik 3.2 Briefing, Delegasi, dan Umpan Balik kepada Anggota (45 menit)", [
  ["Tujuan pembelajaran", ["Head Kitchen menerapkan (C3) briefing sebelum buka dan delegasi yang jelas.", "Anggota mengevaluasi (C5) kejelasan briefing dan delegasi lewat umpan balik SBI."]],
  ["Outline materi", [
    "1. Briefing sebelum buka selama 5 menit: menu andalan dan stok, target hari itu, pembagian tugas, satu hal yang diingatkan.",
    "2. Delegasi yang jelas: hasil yang diminta, batas waktu, tanda sudah selesai, kepada siapa bertanya.",
    "3. Memeriksa hasil tanpa mengawasi terus-menerus.",
    "4. Memberi pujian dan koreksi pada hari yang sama."]],
  ["Aktivitas", [
    "1. (10 menit) Trainer memperagakan dua briefing. Briefing pertama panjang dan tanpa pembagian tugas. Briefing kedua lima menit dengan empat bagian. Peserta mencentang lembar daftar periksa briefing untuk masing-masing.",
    "2. (15 menit) Head Kitchen menyusun briefing untuk satu hari brunch akhir pekan memakai kartu briefing, dibantu trainer. Anggota menulis pertanyaan yang biasanya tidak terjawab saat briefing.",
    "3. (15 menit) Head Kitchen menyampaikan briefing selama 5 menit. Lalu Head Kitchen mendelegasikan satu tugas kepada satu anggota memakai kartu delegasi. Anggota mengulang tugasnya. Trainer membandingkan dengan daftar periksa.",
    "4. (5 menit) Dua anggota memberi satu umpan balik SBI kepada Head Kitchen tentang kejelasan briefing. Head Kitchen mencatatnya."]],
  ["Alat dan media", "Kartu briefing, kartu delegasi, lembar daftar periksa briefing, penghitung waktu."],
  ["Output", "Templat Briefing 5 Menit dan Kartu Delegasi, masing-masing satu lembar, siap dipakai pada hari kerja."],
  ["Ukuran keberhasilan", "Briefing memuat keempat bagian dalam waktu 5 menit. Anggota yang menerima tugas mengulangnya tanpa salah."],
]));

// Sesi 4
body.push(h2("Sesi 4. Praktik Terpadu dan Rencana Penerapan"));
body.push(focus("semua kebiasaan hari ini dipakai bersamaan, lalu tim memilih yang dibawa ke pekerjaan."));
body.push(...topik("Topik 4.1 Simulasi Layanan Brunch Terpadu (35 menit)", [
  ["Tujuan pembelajaran", ["Peserta menerapkan (C3) ulang pesan, peta peran, aturan koordinasi, dan briefing dalam satu simulasi.", "Peserta mengevaluasi (C5) hasil simulasi dibandingkan Simulasi 1."]],
  ["Outline materi", [
    "1. Briefing oleh Head Kitchen memakai Templat Briefing 5 Menit.",
    "2. Simulasi 2 dengan enam tiket baru.",
    "3. Penilaian bersama pada empat aspek: pesan diulang, peran jelas, alur lancar, arahan Head Kitchen."]],
  ["Aktivitas", [
    "1. (5 menit) Head Kitchen membriefing. Anggota mengambil posisi sesuai Peta Peran. Kartu Bahasa Dapur Kami dipasang di meja.",
    "2. (15 menit) Simulasi 2: enam tiket brunch baru, 12 menit berjalan dan 3 menit pembagian posisi. Aturan koordinasi dari Topik 2.2 berlaku. Satu anggota dan trainer mengamati dengan lembar pengamatan yang sama dengan Simulasi 1.",
    "3. (15 menit) Pengamat melaporkan pengamatannya. Peserta memberi nilai 1 sampai 4 untuk tiap aspek, lalu membandingkannya dengan catatan Simulasi 1 dan menentukan satu hal yang paling perlu dipertahankan."]],
  ["Alat dan media", "Enam kartu tiket baru, kartu komponen menu, lembar pengamatan, lembar penilaian, penghitung waktu."],
  ["Output", "Lembar penilaian simulasi yang membandingkan Simulasi 1 dan Simulasi 2."],
  ["Ukuran keberhasilan", "Titik macet dari Simulasi 1 yang masih terjadi di Simulasi 2 dicatat pengamat. Kami tidak menjanjikan angka tertentu, yang dilihat adalah arah perubahan."],
]));
body.push(...topik("Topik 4.2 Rencana Penerapan 30 Hari, Post-Test, dan Penutup (25 menit)", [
  ["Tujuan pembelajaran", ["Peserta menyusun (C6) rencana penerapan 30 hari yang spesifik.", "Peserta menerapkan (C3) pengetahuannya pada post-test."]],
  ["Outline materi", [
    "1. Memilih kebiasaan dari hari ini yang paling mudah dan paling berguna dimulai.",
    "2. Rencana: apa, kapan mulai, siapa, tanda berhasil.",
    "3. Tinjauan penerapan 30 hari."]],
  ["Aktivitas", [
    "1. (10 menit) Tiap peserta memilih satu kebiasaan, misalnya ulang pesan, briefing 5 menit, atau serah terima, lalu menulis di Kartu Komitmen: apa, kapan mulai, tanda berhasil. Head Kitchen menulis dua kartu, satu untuk dirinya dan satu untuk tim. Kelompok menyepakati satu kebiasaan bersama.",
    "2. (10 menit) Peserta mengerjakan post-test dengan soal yang sama dengan pre-test dalam urutan acak.",
    "3. (5 menit) Peserta mengisi formulir reaksi empat pertanyaan. Trainer menutup dengan membacakan isi Papan Tantangan Dapur Kami dan satu kebiasaan bersama."]],
  ["Alat dan media", "Kartu Komitmen, lembar post-test, formulir reaksi."],
  ["Output", "Kartu Komitmen tiap peserta, Rencana 30 Hari tim (satu lembar), skor post-test, dan formulir reaksi."],
  ["Ukuran keberhasilan", "Tiap peserta punya satu kartu yang memuat kapan mulai dan tanda berhasil. Trainer melaporkan berapa peserta yang skornya naik. Kami tidak menetapkan target skor."],
]));

// ---------------- 7 ----------------
body.push(h2("7. Hasil yang Dibawa Pulang"));
body.push(table([3200, 1600, 4838], ["Output", "Dihasilkan di", "Bentuk dan kegunaan"], [
  ["Papan Tantangan Dapur Kami", "Pembukaan", "Foto dan kertas tempel. Daftar tantangan nyata tim, rujukan untuk tinjauan 30 hari"],
  ["Kartu Bahasa Dapur Kami", "Topik 1.1", "Cetak A4. Ditempel di dapur"],
  ["Satu kejadian teranalisis dan tiga kalimat umpan balik", "Topik 1.2", "Cetak A4. Dipakai saat membahas salah paham"],
  ["Peta Peran Tim Kitchen", "Topik 2.1", "Cetak A4. Ditempel di dapur dan dipakai saat ada anggota baru"],
  ["Alur Pesanan Brunch dan tiga aturan koordinasi", "Topik 2.2", "Foto gambar alur dan cetak A4"],
  ["Matriks gaya mengarahkan, kartu kebutuhan anggota, dua komitmen Head Kitchen", "Topik 3.1", "Matriks dibawa Head Kitchen. Kartu dan komitmen difoto"],
  ["Templat Briefing 5 Menit dan Kartu Delegasi", "Topik 3.2", "Cetak A4, digandakan untuk dipakai tiap hari"],
  ["Lembar penilaian simulasi", "Topik 4.1", "Foto. Pembanding bila pelatihan diulang atau ditinjau"],
  ["Kartu Komitmen dan Rencana 30 Hari", "Topik 4.2", "Kartu dipegang peserta, rencana tim ditempel"],
  ["Skor pre-test dan post-test, formulir reaksi, laporan singkat trainer", "Pembukaan dan Topik 4.2", "Dikirim ke Lidya dalam bentuk PDF. [ISI TIM: batas waktu pengiriman laporan dan panjangnya]"],
]));

// ---------------- 8 ----------------
body.push(h2("8. Kaitan dengan Output yang Diharapkan Klien"));
body.push(para("Kolom kiri adalah enam output pada bagian 6 MoM. Kolom tengah dan kanan adalah tafsiran kami tentang topik yang menjawabnya dan bukti yang bisa dilihat pada hari pelatihan.", { keepNext: true }));
body.push(table([3500, 1700, 4438], ["Output menurut MoM", "Topik", "Bukti pada hari pelatihan"], [
  ["1. Kemampuan komunikasi antaranggota meningkat", "1.1, 1.2", "Kartu Bahasa Dapur Kami. Tiket yang diulang dengan benar. Umpan balik SBI lengkap"],
  ["2. Koordinasi dan kerja sama tim lebih efektif dalam operasional", "2.2, 4.1", "Alur dan aturan koordinasi. Perbandingan Simulasi 1 dan 2"],
  ["3. Head Kitchen lebih mampu mengarahkan, mengelola, dan memimpin", "3.1, 3.2", "Briefing dan delegasi sesuai daftar periksa. Komitmen Head Kitchen"],
  ["4. Setiap anggota memahami peran dan tanggung jawabnya", "2.1", "Peta Peran. Tiap peserta menyebut tiga tugasnya"],
  ["5. Lingkungan kerja lebih kolaboratif dan suportif", "1.2, 3.1, 4.1", "Umpan balik SBI, kartu kebutuhan anggota yang dijawab Head Kitchen, penilaian bersama"],
  ["6. Peserta menerapkan keterampilan untuk tantangan sehari-hari", "4.2", "Kartu Komitmen dan tinjauan 30 hari"],
]));

// ---------------- 9 ----------------
body.push(h2("9. Evaluasi"));
body.push(table([1700, 4200, 3738], ["Level Kirkpatrick", "Alat", "Waktu"], [
  ["1. Reaksi", "Formulir reaksi empat pertanyaan", "Topik 4.2"],
  ["2. Pembelajaran", "Pre-test dan post-test dengan soal sama. Lembar pengamatan dan penilaian simulasi", "Pembukaan, Topik 4.1, Topik 4.2"],
  ["3. Perilaku", "Kartu Komitmen. Tinjauan penerapan lewat Gmeet 30 menit dengan Lidya dan Head Kitchen. [ISI TIM: tinjauan masuk paket atau ditawarkan sebagai opsi]", "30 hari setelah pelatihan"],
  ["4. Dampak", "Belum diukur dalam paket satu hari. Bila Cafe Melt Me mencatat keterlambatan pesanan atau keluhan tamu, catatan itu bisa menjadi pembanding. Saat ini kami belum punya data awal", "-"],
]));

// ---------------- 10 ----------------
body.push(h2("10. Yang Perlu Disiapkan Klien dan Hal yang Masih Terbuka"));
body.push(para("Yang perlu disiapkan Cafe Melt Me: daftar menu brunch beserta komponen tiap menu (paling lambat tiga hari sebelum hari pelatihan), nama dan jabatan peserta, ruang dengan meja panjang dan dinding kosong untuk menempel kertas, serta kesediaan menjawab formulir asesmen awal."));
body.push(para("Yang masih terbuka: jumlah peserta pasti, hari pelaksanaan, pilihan satu hari penuh atau dua pertemuan, tempat pelaksanaan, dan nama trainer dari Batam. Semuanya dikonfirmasi setelah klien menerima penawaran."));

// ---------------- 11 ----------------
body.push(h2("11. Rujukan"));
[
  "Anderson, L.W. dan Krathwohl, D.R. (2001). A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives. Longman.",
  "Branch, R.M. (2009). Instructional Design: The ADDIE Approach. Springer.",
  "Center for Creative Leadership. Situation-Behavior-Impact (SBI) feedback model.",
  "Hersey, P. dan Blanchard, K.H. (1969). Life Cycle Theory of Leadership. Training and Development Journal, 23(5), 26-34.",
  "Kirkpatrick, D.L. (1994). Evaluating Training Programs: The Four Levels. Berrett-Koehler.",
  "Knowles, M.S. (1984). Andragogy in Action. Jossey-Bass.",
  "Wiggins, G. dan McTighe, J. (2005). Understanding by Design, edisi kedua. ASCD.",
].forEach((t) => body.push(para(t, { after: 80, size: 18 })));

// ---------------- dokumen ----------------
const footerLine = { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 4 };
const doc = new Document({
  creator: "Sanggabiz",
  title: "Silabus Communication dan Leadership Tim Kitchen - Cafe Melt Me",
  styles: { default: { document: { run: { font: FONT, size: 20 } } } },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1300, bottom: 1300, left: 1134, right: 1134 } } },
    headers: { default: new Header({ children: [new Paragraph({
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "000000", space: 4 } },
      tabStops: [{ type: "right", position: W }],
      children: [
        new TextRun({ text: "SANGGABIZ", font: FONT, bold: true, size: 20, color: NAVY }),
        new TextRun({ text: "\tSilabus Cafe Melt Me, 2026", font: FONT, size: 16, color: "444444" }),
      ] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({
      border: { top: footerLine }, tabStops: [{ type: "right", position: W }],
      children: [
        new TextRun({ text: "WhatsApp 0877-7413-4288  |  www.sanggabiz.com  |  partnership@sanggabiz.com", font: FONT, size: 14, color: "444444" }),
        new TextRun({ children: ["\tHalaman ", PageNumber.CURRENT], font: FONT, size: 14, color: "444444" }),
      ] })] }) },
    children: body,
  }],
});

Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(OUT, buf); console.log("OK", OUT); });
