// Membuat proposal docx Aqiqah Al Kautsar. Jalankan: NODE_PATH=$(npm root -g) node build_proposal.js
// Kartu saku dibuat lebih dulu dengan: NODE_PATH=$(npm root -g) node render_kartu.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun, Footer,
  AlignmentType, BorderStyle, WidthType, ShadingType, HeightRule, PageNumber, LevelFormat,
  VerticalAlign, TabStopType,
} = require("docx");

const NAVY = "0B396D", GOLD = "FFC00C", INK = "1D1D1F", MUTED = "5C5F66", LINE = "C9D2DE", SOFT = "EEF3F9";
const FONT = "Montserrat";
const W = 9638; // lebar isi A4 dengan margin 2 cm
const A = (f) => path.join(__dirname, "assets", f);
const JUDUL = "Training CS for Improving Sales Closing Rate";

// ---------- penolong teks ----------
function runs(text, base = {}) {
  const out = [];
  const re = /(\[ISI TIM:[^\]]*\])|(\*\*[^*]+\*\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    if (m[1]) out.push(new TextRun({ text: m[1], ...base, bold: true, shading: { type: ShadingType.CLEAR, fill: "FFF200", color: "auto" }, color: INK }));
    else out.push(new TextRun({ text: m[2].slice(2, -2), ...base, bold: true }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}
const p = (text, o = {}) => new Paragraph({
  children: runs(text, o.run || {}), alignment: o.align || AlignmentType.LEFT,
  spacing: { after: o.after ?? 120, before: o.before ?? 0, line: o.line ?? 300 },
  keepNext: o.keepNext,
});
const h1 = (text, pb = true) => new Paragraph({ heading: "Heading1", children: [new TextRun({ text })], pageBreakBefore: pb, keepNext: true, spacing: pb ? undefined : { before: 360, after: 200 } });
const h2 = (text) => new Paragraph({ heading: "Heading2", children: [new TextRun({ text })], keepNext: true });
const h3 = (text, sub) => [
  new Paragraph({ children: [new TextRun({ text, bold: true, size: 21, color: NAVY })], spacing: { before: 240, after: 30 }, keepNext: true }),
  ...(sub ? [new Paragraph({ children: [new TextRun({ text: sub, size: 17, color: MUTED })], spacing: { after: 90 }, keepNext: true })] : []),
];
const bullet = (text) => new Paragraph({ numbering: { reference: "bul", level: 0 }, children: runs(text), spacing: { after: 70, line: 290 } });
const caption = (text) => new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text, size: 17, color: INK })], spacing: { after: 200 } });
const spacer = (n = 120) => new Paragraph({ spacing: { after: n }, children: [] });
const img = (file, w, h, type = "png") => new ImageRun({ type, data: fs.readFileSync(A(file)), transformation: { width: w, height: h } });

// ---------- penolong tabel ----------
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(content, width, o = {}) {
  const lines = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders: o.borders || borders, columnSpan: o.span,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    verticalAlign: o.valign || VerticalAlign.TOP,
    margins: { top: o.pad ?? 80, bottom: o.pad ?? 80, left: 120, right: 120 },
    children: lines.map((t) => new Paragraph({
      alignment: o.align || AlignmentType.LEFT, spacing: { after: 40, line: 270 },
      children: runs(t, { size: o.size || 18, bold: o.bold, color: o.color || INK }),
    })),
  });
}
function table(widths, header, rows, o = {}) {
  const head = header ? [new TableRow({
    tableHeader: true, cantSplit: true,
    children: header.map((t, i) => cell(t, widths[i], { fill: NAVY, color: "FFFFFF", bold: true, size: 17 })),
  })] : [];
  const body = rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((c, i) => cell(c, widths[i], {
      fill: o.firstFill && i === 0 ? o.firstFill : (o.zebra === false ? undefined : (ri % 2 ? "F7F9FC" : undefined)),
      bold: o.boldFirst !== false && i === 0, size: o.size, color: o.boldFirst !== false && i === 0 ? NAVY : INK,
    })),
  }));
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths, rows: [...head, ...body] });
}
// kotak sorotan dengan garis kuning di kiri
function callout(title, lines) {
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({ cantSplit: true, children: [new TableCell({
      width: { size: W, type: WidthType.DXA },
      borders: { top: none, bottom: none, right: none, left: { style: BorderStyle.SINGLE, size: 36, color: GOLD } },
      shading: { fill: SOFT, type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 140, bottom: 140, left: 220, right: 220 },
      children: [
        new Paragraph({ spacing: { after: 70 }, children: [new TextRun({ text: title, bold: true, size: 19, color: NAVY })] }),
        ...lines.map((t) => new Paragraph({ spacing: { after: 50, line: 285 }, children: runs(t, { size: 18 }) })),
      ],
    })] })],
  });
}

// ---------- isi sesi workshop ----------
const SESI = [
  { judul: "Sesi 1. Target Bulanan Menjadi Pegangan Harian", waktu: "08.45 - 09.15 WIB, 30 menit",
    belajar: "Cara menghitung berapa chat yang perlu ditangani dan berapa pesanan yang perlu didapat setiap hari supaya target bulanan tercapai.",
    kegiatan: [
      "Trainer menampilkan perjalanan seorang calon pelanggan, dari chat pertama sampai membayar lunas, lengkap dengan angka tim Al Kautsar sendiri dari tahap mengenal tim.",
      "Sebelum angkanya dibuka, setiap CS menebak berapa dari 10 chat yang biasanya menjadi pesanan. Tebakan dibandingkan dengan angka sebenarnya.",
      "Setiap CS menghitung target hariannya di lembar hitung sederhana, lalu saling memeriksa dengan teman sebelah.",
    ],
    alat: "Lembar hitung, kalkulator di ponsel, kertas plano, spidol.",
    hasil: "Setiap CS tahu jumlah chat dan pesanan yang perlu dicapai per hari." },
  { judul: "Sesi 2. Bertanya Dulu, Baru Memberi Harga", waktu: "09.15 - 09.50 WIB, 35 menit",
    belajar: "Cara menggali kebutuhan keluarga lewat chat sebelum mengirim harga, supaya penawaran yang diberikan tepat sasaran.",
    kegiatan: [
      "Dibuka dengan permainan Pelanggan yang Tidak Terlihat. Satu peserta memakai penutup mata dan harus menebak paket yang diinginkan temannya hanya dengan bertanya. Permainan ini menggambarkan keadaan CS sehari-hari: CS tidak melihat pelanggannya, sehingga pertanyaan yang baik adalah cara utama memahami kebutuhan.",
      "Dua kelompok membedah tiga contoh chat nyata yang sudah disamarkan, lalu menempelkan stiker di titik tempat calon pelanggan berhenti membalas.",
      "Peserta berlatih berpasangan. Satu orang berperan sebagai keluarga dengan kartu profil, satu orang sebagai CS yang memakai enam pertanyaan kunci. Peran ditukar setelah 5 menit.",
    ],
    alat: "Penutup mata, kartu gambar paket, contoh chat tercetak, stiker penanda warna, kartu profil keluarga.",
    hasil: "Daftar pertanyaan yang disepakati tim untuk setiap chat baru." },
  { judul: "Sesi 3. Menyusun Chat Penawaran Lima Langkah", waktu: "09.50 - 10.30 WIB, 40 menit",
    belajar: "Alur chat lima langkah: sapa, gali kebutuhan, rekomendasikan satu paket, jawab keraguan, lalu ajak memesan.",
    kegiatan: [
      "Trainer menampilkan satu chat yang berhasil menjadi pesanan dan membahasnya langkah demi langkah.",
      "Peserta memilihkan satu paket untuk tiga contoh keluarga yang berbeda, lengkap dengan satu kalimat alasannya.",
      "Setiap CS menulis ulang satu chat nyata yang gagal, lalu bertukar dengan teman untuk dicek memakai daftar lima langkah. Dua hasil terbaik dibacakan di depan.",
    ],
    alat: "Contoh chat tercetak, kartu profil keluarga, daftar paket dan harga Al Kautsar, ponsel peserta.",
    hasil: "Contoh chat lima langkah versi tim Al Kautsar." },
  { judul: "Sesi 4. Menjawab Keraguan Pelanggan", waktu: "10.45 - 11.30 WIB, 45 menit",
    belajar: "Pola akui, tanya, jawab, ajak untuk empat keraguan yang paling sering muncul: harga, ingin membandingkan, menunda, dan menunggu keputusan keluarga.",
    kegiatan: [
      "Trainer mengenalkan pola menjawab dengan satu contoh untuk setiap keraguan. Diskon diletakkan sebagai pilihan terakhir.",
      "Peserta bermain peran bertiga. Satu orang menjadi CS, satu menjadi pelanggan yang memegang kartu keraguan, dan satu mengamati. Ada tiga putaran sehingga setiap orang mencoba semua peran. Supervisor ikut mengamati.",
      "Jawaban terbaik dari setiap kelompok dikumpulkan menjadi pegangan bersama tim.",
    ],
    alat: "Kartu keraguan pelanggan, pengatur waktu dan bel, lembar pengamatan, kertas plano.",
    hasil: "Kumpulan jawaban terbaik untuk empat keraguan pelanggan." },
  { judul: "Sesi 5. Follow-up Sampai Memesan", waktu: "11.30 - 12.05 WIB, 35 menit",
    belajar: "Kapan dan bagaimana menghubungi kembali calon pelanggan yang belum memutuskan, lewat chat maupun telepon.",
    kegiatan: [
      "Peserta menyusun jadwal follow-up untuk tiga calon pelanggan contoh, dihitung dari chat pertama dan tanggal aqiqah keluarga tersebut.",
      "Setiap CS menulis tiga pesan follow-up: pengingat ringan, info penguat, dan ajakan memesan.",
      "Peserta berlatih berpasangan menelepon calon pelanggan yang tidak membalas chat, masing-masing dua menit.",
    ],
    alat: "Kalender kertas, catatan tempel, ponsel peserta, pengatur waktu.",
    hasil: "Jadwal follow-up serta contoh pesan dan percakapan telepon." },
  { judul: "Penutup. Siap Menjalani Pendampingan", waktu: "12.05 - 12.30 WIB, 25 menit",
    belajar: "Cara mencatat calon pelanggan setiap hari dan aturan main pendampingan selama satu bulan.",
    kegiatan: [
      "Setiap CS mencoba mengisi catatan calon pelanggan di Google Sheets lewat ponselnya.",
      "Setiap CS menuliskan tiga kebiasaan yang akan diterapkan selama sebulan. Supervisor menyimpan catatan ini untuk dicek setiap minggu.",
      "Sesi ditutup dengan kuis singkat, survei kepuasan, dan pembagian kartu saku CS.",
    ],
    alat: "Ponsel peserta, kartu komitmen, kartu saku CS.",
    hasil: "Catatan calon pelanggan siap dipakai dan tiga komitmen dari setiap CS." },
];
function blokSesi(s) {
  const L = 2200, R = W - L;
  const row = (label, content) => new TableRow({ cantSplit: true, children: [
    cell(label, L, { fill: SOFT, bold: true, color: NAVY, size: 17 }),
    cell(content, R, { size: 18 }),
  ] });
  return [
    ...h3(s.judul, s.waktu),
    new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: [L, R], rows: [
      row("Yang dipelajari", s.belajar),
      row("Kegiatannya", s.kegiatan.map((k, i) => `${i + 1}. ${k}`)),
      row("Alat dan media", s.alat),
      row("Hasil", s.hasil),
    ] }),
  ];
}

// ================= ISI =================
const bab1 = [
  h1("1. Pendahuluan", false),
  h2("1.1 Latar Belakang"),
  p("Aqiqah Al Kautsar mulai memberi target penjualan kepada tim Customer Service. Peran CS ikut berubah. CS tidak lagi hanya menjawab pertanyaan, tetapi diharapkan mengubah calon pelanggan yang bertanya lewat WhatsApp dan telepon menjadi pelanggan yang memesan."),
  p("Hampir setiap pesanan aqiqah berawal dari satu chat. Keluarga yang menghubungi biasanya sedang membandingkan beberapa pilihan dan perlu memutuskan sebelum tanggal aqiqah. Pada rentang waktu yang singkat itu, cara CS membalas chat ikut menentukan apakah keluarga tersebut memesan di Al Kautsar."),
  p("Tantangannya ada di dua sisi. Di sisi CS, belum ada alur percakapan yang sama untuk seluruh tim, sehingga setiap orang membalas dengan caranya sendiri. Di sisi Supervisor, target bulanan sudah ada tetapi belum dipecah menjadi pegangan harian untuk setiap CS."),
  p("Kami belum memegang data berapa chat yang biasanya berakhir menjadi pesanan [ISI TIM: konfirmasi ke Al Kautsar]. Karena itu program dimulai dengan mengenal kondisi tim lebih dulu. Angka awal ini juga menjadi pembanding di akhir program."),

  h2("1.2 Yang Ingin Dicapai"),
  p("Tabel berikut membandingkan kebiasaan yang sering kami temui di tim CS dengan kebiasaan yang dituju program ini. Kondisi Al Kautsar yang sebenarnya akan kami pastikan pada tahap mengenal tim."),
  table([4819, 4819], ["Yang sering terjadi", "Yang dituju setelah program"], [
    ["Chat dibalas dengan daftar harga, lalu calon pelanggan berhenti membalas", "Chat dibuka dengan pertanyaan tentang kebutuhan keluarga, lalu ditawarkan satu paket yang sesuai"],
    ["Setiap CS membalas dengan caranya sendiri", "Seluruh tim memakai lima langkah chat yang sama"],
    ["Calon pelanggan yang bilang nanti dulu jarang dihubungi lagi", "Setiap calon pelanggan punya jadwal follow-up yang tercatat"],
    ["Target bulanan terasa jauh dari pekerjaan harian", "Setiap CS tahu berapa chat dan pesanan yang perlu dicapai per hari"],
    ["Supervisor melihat hasil di akhir bulan", "Supervisor memantau setiap hari lewat rapat singkat 10 menit dan catatan tim"],
  ], { boldFirst: false }),
  spacer(),

  h2("1.3 Tujuan"),
  p("Program ini membantu tim CS Aqiqah Al Kautsar mengubah lebih banyak chat menjadi pesanan, dengan cara kerja yang sama di seluruh tim dan hasil yang bisa dipantau setiap minggu. Setelah program:"),
  bullet("setiap CS tahu target hariannya sendiri,"),
  bullet("CS menanyakan kebutuhan keluarga sebelum memberi harga,"),
  bullet("CS menawarkan satu paket yang sesuai dan menjawab keraguan pelanggan dengan tenang,"),
  bullet("CS menindaklanjuti calon pelanggan sesuai jadwal sampai memesan atau jelas menolak,"),
  bullet("Supervisor membagi target ke setiap CS, memimpin rapat harian singkat, dan membimbing CS dari chat nyata."),

  h2("1.4 Cara Kami Mengukur Hasil"),
  table([2000, 3900, 3738], ["Kapan", "Yang kami lihat", "Tanda berhasil"], [
    ["Hari workshop", "Kuis singkat di awal dan akhir sesi, serta hasil latihan menulis chat", "Nilai kuis naik, dan sebagian besar CS bisa menulis chat lima langkah dengan lengkap"],
    ["Setiap minggu", "Contoh chat nyata yang kami pilih acak dan catatan follow-up tim", "Makin banyak chat mengikuti lima langkah. Pada minggu ke-4, minimal 7 dari 10 chat"],
    ["Akhir bulan", "Persentase chat yang menjadi DP atau lunas, dibandingkan dengan sebelum program", "Angka target disepakati bersama setelah kondisi awal diketahui [ISI TIM: target]"],
  ]),
  spacer(80),
  p("Penjualan juga dipengaruhi jumlah calon pelanggan dari iklan, harga, dan musim. Karena itu yang kami bandingkan adalah persentase chat yang menjadi pesanan, bukan hanya total omzet. Kami tidak menjanjikan kenaikan penjualan dalam angka tertentu.", { run: { color: MUTED, size: 18 } }),

  h2("1.5 Tentang Sanggabiz"),
  p("Sanggabiz adalah mitra bisnis yang menyediakan layanan department-as-a-service: keuangan, sumber daya manusia, layanan pelanggan, pemasaran, manajemen proyek, administrasi, dan operasional. Layanan pelanggan termasuk pekerjaan yang kami jalankan sehari-hari untuk klien. Di bidang pelatihan, kami mengelola program dari persiapan sampai laporan."),
  table([2600, 7038], null, [
    ["Skala", "400+ proyek dan layanan, 500+ pakar dan trainer, 6.000+ mitra engagement"],
    ["Pengalaman relevan", "Layanan pelanggan sebagai department-as-a-service [ISI TIM: proyek CS atau penjualan yang pernah dijalankan]"],
    ["Klien", "[ISI TIM: tiga sampai lima klien yang relevan]"],
  ]),
  spacer(160),
  new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [4819, 4819],
    rows: [new TableRow({ children: [["foto-pelatihan-1.jpg", 227, 170], ["foto-pelatihan-2.jpg", 302, 170]].map(([f, w, h]) => new TableCell({
      width: { size: 4819, type: WidthType.DXA }, borders: { top: none, bottom: none, left: none, right: none },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [img(f, w, h, "jpg")] })],
    })) })],
  }),
  caption("Gambar 1. Dokumentasi pelatihan yang diselenggarakan Sanggabiz"),
];

const bab2 = [
  h1("2. Alur Program, Tempat, dan Waktu"),
  h2("2.1 Alur Program"),
  p("Program berjalan sekitar enam minggu dalam empat tahap. Setiap tahap punya hasil yang jelas dan menjadi bahan tahap berikutnya."),
  table([600, 2500, 4038, 2500], ["", "Tahap", "Yang dilakukan", "Hasil"], [
    ["1", ["Mengenal tim", "9 - 13 November 2026, online"], "Kuesioner singkat untuk CS dan Supervisor, contoh chat yang berhasil dan yang gagal, data penjualan sebulan terakhir, dan obrolan 30 menit dengan pemilik", "Gambaran kondisi awal dan materi workshop yang memakai kasus Al Kautsar sendiri"],
    ["2", ["Workshop", "Pekan 16 - 21 November 2026, 4 jam di kantor Al Kautsar"], "Latihan menulis chat, bermain peran, dan menyusun jadwal follow-up dengan contoh nyata", "Kartu saku, contoh chat versi tim, jawaban keraguan, jadwal follow-up"],
    ["3", ["Pendampingan", "4 minggu setelah workshop, lewat WhatsApp"], "Materi singkat tiga kali seminggu, pemeriksaan contoh chat setiap Jumat, dan bimbingan pribadi untuk Supervisor", "Empat rekap mingguan dan kebiasaan baru yang berjalan"],
    ["4", ["Laporan", "Paling lambat 5 hari kerja setelah minggu ke-4"], "Perbandingan kondisi awal dan akhir, catatan untuk setiap CS, dan saran untuk bulan berikutnya", "Laporan akhir untuk pemilik"],
  ], { boldFirst: true }),
  spacer(),
  callout("Mengapa satu kali kelas ditambah pendampingan satu bulan", [
    "Kemampuan closing terbentuk saat membalas chat sungguhan, bukan di kelas. Workshop 4 jam dipakai untuk menyamakan cara kerja seluruh tim. Setelah itu, selama sebulan kami memeriksa chat asli setiap minggu dan memberi masukan, sehingga perbaikan terjadi pada pekerjaan sehari-hari. Cara ini lebih hemat waktu tim dibanding menambah kelas kedua.",
  ]),
  h2("2.2 Tempat dan Waktu"),
  table([3000, 6638], null, [
    ["Tempat", "Kantor Aqiqah Al Kautsar, [ISI TIM: alamat]. Ruang untuk 10 orang dengan dua meja kelompok, layar atau TV, dan colokan listrik"],
    ["Tanggal workshop", "[ISI TIM: tanggal] pada pekan 16 - 21 November 2026"],
    ["Jam workshop", "08.30 - 12.30 WIB, registrasi mulai 08.15. Jam dapat digeser mengikuti jam sepi chat"],
    ["Pendampingan", "Senin sampai Jumat, 09.00 - 17.00 WIB, pesan dibalas paling lambat 1 x 24 jam kerja"],
  ]),
  h2("2.3 Peserta"),
  table([2600, 1600, 5438], ["Peserta", "Jumlah", "Keterlibatan"], [
    ["Customer Service", "[ISI TIM: 6 - 8] orang", "Mengisi kuesioner, mengikuti workshop penuh, aktif di grup pendampingan, mencatat calon pelanggan setiap hari"],
    ["Supervisor", "1 orang", "Mengikuti workshop penuh, mendapat bimbingan pribadi setiap minggu, memimpin rapat harian 10 menit"],
    ["Pemilik atau manajemen", "1 orang", "Obrolan 30 menit di tahap awal, membuka workshop, memutuskan target dan pembagian penjualan per CS"],
  ]),
  spacer(80),
  p("Selama workshop, chat pelanggan dialihkan sementara ke pesan otomatis atau petugas cadangan supaya seluruh CS bisa fokus.", { run: { color: MUTED, size: 18 } }),
];

const bab3 = [
  h1("3. Materi dan Kegiatan"),
  h2("3.1 Gambaran Workshop"),
  p("Workshop berlangsung 4 jam dan sebagian besar waktunya dipakai untuk praktik. Bahan latihan diambil dari chat Al Kautsar sendiri yang sudah disamarkan, sehingga peserta berlatih dengan kasus yang mereka temui setiap hari."),
  table([2100, 4400, 3138], ["Waktu", "Sesi", "Yang dibawa pulang"], [
    ["08.45 - 09.15", "Target bulanan menjadi pegangan harian", "Target harian setiap CS"],
    ["09.15 - 09.50", "Bertanya dulu, baru memberi harga", "Daftar pertanyaan tim"],
    ["09.50 - 10.30", "Menyusun chat penawaran lima langkah", "Contoh chat versi tim"],
    ["10.45 - 11.30", "Menjawab keraguan pelanggan", "Kumpulan jawaban terbaik"],
    ["11.30 - 12.05", "Follow-up sampai memesan", "Jadwal dan contoh pesan follow-up"],
    ["12.05 - 12.30", "Siap menjalani pendampingan", "Catatan calon pelanggan, komitmen, kartu saku"],
  ]),
  h2("3.2 Rincian Sesi"),
  ...SESI.flatMap(blokSesi),

  h2("3.3 Contoh Alat yang Dibawa Pulang: Kartu Saku CS"),
  p("Setiap CS menerima satu kartu saku berukuran A6 yang bisa diletakkan di samping ponsel kerja. Sisi depan memuat lima langkah chat beserta contoh kalimatnya. Sisi belakang memuat enam pertanyaan sebelum memberi harga, cara menjawab keraguan, dan jadwal follow-up. Isi final disusun dari chat dan daftar paket Al Kautsar setelah tahap mengenal tim.", { keepNext: true }),
  new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [4819, 4819],
    rows: [new TableRow({ cantSplit: true, children: ["kartu-saku-depan.png", "kartu-saku-belakang.png"].map((f) => new TableCell({
      width: { size: 4819, type: WidthType.DXA }, borders: { top: none, bottom: none, left: none, right: none },
      shading: { fill: "E9EDF2", type: ShadingType.CLEAR, color: "auto" },
      margins: { top: 160, bottom: 160, left: 100, right: 100 },
      children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [img(f, 286, 403)] })],
    })) })],
  }),
  caption("Gambar 2. Contoh kartu saku CS, sisi depan dan sisi belakang"),

  h2("3.4 Pendampingan Satu Bulan"),
  p("Setelah workshop, tim didampingi lewat WhatsApp selama empat minggu. Setiap minggu punya ritme yang sama:"),
  bullet("**Senin, Rabu, dan Jumat**: materi singkat dan tantangan praktik di grup CS. Temanya diambil dari langkah yang paling sering terlewat pada minggu sebelumnya."),
  bullet("**Setiap hari**: CS mencatat calon pelanggan di Google Sheets, dan Supervisor memimpin rapat 10 menit untuk melihat angka kemarin dan prioritas hari ini."),
  bullet("**Jumat**: pendamping memilih tiga chat acak dari setiap CS, memeriksanya dengan lima langkah, lalu mengirim rekap mingguan."),
  bullet("**Senin**: pendamping dan Supervisor membahas rekap bersama dan menentukan satu fokus perbaikan."),
  spacer(60),
  table([1500, 4069, 4069], ["Minggu", "Fokus tim CS", "Fokus Supervisor"], [
    ["Minggu 1", "Menyapa, menggali kebutuhan, dan rajin mencatat calon pelanggan", "Membagi target tim ke setiap CS dan memulai rapat harian 10 menit"],
    ["Minggu 2", "Memperbaiki langkah yang paling sering terlewat pada pemeriksaan minggu pertama", "Bimbingan pribadi dengan setiap CS memakai contoh chatnya sendiri"],
    ["Minggu 3", "Menjawab keraguan dan follow-up tepat waktu", "Membaca penyebab target meleset: jumlah chat, cara membalas, atau follow-up"],
    ["Minggu 4", "Mengajak memesan dan merapikan seluruh lima langkah", "Menyusun target dan kebiasaan tim untuk bulan berikutnya tanpa pendampingan"],
  ]),

  h2("3.5 Yang Dibawa Pulang"),
  table([4000, 5638], ["Hasil", "Kegunaan"], [
    ["Target harian setiap CS", "Pegangan jumlah chat dan pesanan per hari, dicek di rapat harian"],
    ["Daftar pertanyaan dan contoh chat versi tim", "Cara membalas yang sama untuk seluruh CS"],
    ["Kumpulan jawaban keraguan pelanggan", "Jawaban siap pakai, terus ditambah selama pendampingan"],
    ["Jadwal dan contoh pesan follow-up", "Calon pelanggan tidak terlewat"],
    ["Kartu saku CS", "Pengingat lima langkah di samping ponsel kerja"],
    ["Catatan calon pelanggan di Google Sheets", "Dasar rekap mingguan dan keputusan Supervisor"],
    ["Empat rekap mingguan dan laporan akhir", "Gambaran perkembangan tim dan saran untuk bulan berikutnya"],
  ]),
];

const bab4 = [
  h1("4. Susunan Acara Workshop", false),
  p("Jam di bawah adalah usulan awal. Bila tanggal atau jam berubah, urutan dan durasi setiap sesi tetap sama."),
  table([1900, 1300, 4038, 2400], ["Waktu (WIB)", "Durasi", "Kegiatan", "Pemandu"], [
    ["08.15 - 08.30", "15 menit", "Registrasi dan pengalihan chat", "Tim Sanggabiz"],
    ["08.30 - 08.45", "15 menit", "Pembukaan oleh pemilik dan kuis awal", "Pemilik, trainer"],
    ["08.45 - 09.15", "30 menit", "**Sesi 1.** Target bulanan menjadi pegangan harian", "Trainer"],
    ["09.15 - 09.50", "35 menit", "**Sesi 2.** Bertanya dulu, baru memberi harga", "Trainer"],
    ["09.50 - 10.30", "40 menit", "**Sesi 3.** Menyusun chat penawaran lima langkah", "Trainer"],
    ["10.30 - 10.45", "15 menit", "Istirahat", ""],
    ["10.45 - 11.30", "45 menit", "**Sesi 4.** Menjawab keraguan pelanggan", "Trainer, Supervisor sebagai pengamat"],
    ["11.30 - 12.05", "35 menit", "**Sesi 5.** Follow-up sampai memesan", "Trainer"],
    ["12.05 - 12.30", "25 menit", "**Penutup.** Siap menjalani pendampingan", "Trainer, pendamping"],
  ], { boldFirst: true }),
];

const bab5 = [
  h1("5. Investasi"),
  p("Program ini kami tawarkan dengan skema kemitraan yang terkait dengan acara Sanggabiz pada 7 November 2026."),
  table([3600, 2200, 3838], ["Komponen", "Nilai", "Keterangan"], [
    ["Nilai program", "Rp 7.500.000", "Mengenal tim, workshop 4 jam, pendampingan 4 minggu, kartu saku, dan laporan akhir"],
    ["Nilai kemitraan", "Rp 5.500.000", "Dibayar dengan konsumsi dan biaya tunai di bawah ini"],
    ["Konsumsi acara Sanggabiz", "Rp 3.500.000", "Makan dan snack untuk 50 orang pada 7 November 2026. Menu dan jumlah disepakati bersama"],
    ["Biaya pelatihan tunai", "Rp 2.000.000", "Rp 1.000.000 saat kerja sama dikonfirmasi, paling lambat 5 November 2026. Rp 1.000.000 setelah workshop"],
    ["Dukungan publikasi", "Tanpa biaya", "Izin dokumentasi dan testimoni untuk publikasi Sanggabiz [ISI TIM: pertahankan atau hapus]"],
  ]),
  spacer(80),
  p("Nilai konsumsi mengikuti harga jual menu dan jumlah yang disepakati. Belum termasuk pajak bila berlaku dan biaya perjalanan ke luar DIY. Seluruh data Al Kautsar kami jaga kerahasiaannya dan hanya dipakai untuk program ini.", { run: { color: MUTED, size: 18 } }),
  h2("5.1 Yang Perlu Disiapkan Al Kautsar"),
  bullet("Contoh chat dan data penjualan diterima paling lambat tiga hari sebelum workshop."),
  bullet("Seluruh CS dan Supervisor mengikuti workshop penuh selama 4 jam."),
  bullet("Ruang, layar atau TV, dan colokan listrik."),
  bullet("Setiap CS mencatat calon pelanggan setiap hari selama empat minggu. Catatan ini menjadi dasar rekap mingguan dan laporan akhir."),
  bullet("Satu orang dari manajemen untuk memutuskan target dan pembagian penjualan per CS."),
  h2("5.2 Di Luar Program Ini"),
  bullet("Pengelolaan iklan dan jumlah calon pelanggan yang masuk."),
  bullet("Pembelian atau pemasangan aplikasi CRM berbayar."),
  bullet("Penetapan skema komisi. Kami memberi masukan, keputusan ada di manajemen."),
  bullet("Pendampingan lebih dari empat minggu."),
];

const bab6 = [
  h1("6. Trainer dan Pendamping", false),
  p("Trainer dan pendamping kami pilih dengan tiga syarat:"),
  bullet("pernah menjual atau memimpin tim penjualan lewat chat dan telepon,"),
  bullet("pernah melatih atau membimbing tim CS atau penjualan,"),
  bullet("terbiasa membaca angka penjualan sederhana untuk mengambil keputusan."),
  spacer(80),
  table([3000, 6638], ["Trainer dan pendamping", ""], [
    ["Nama", "[ISI TIM: nama dan gelar]"],
    ["Jabatan", "[ISI TIM: jabatan dan instansi]"],
    ["Pengalaman penjualan atau CS", "[ISI TIM: lama pengalaman, jenis usaha, ukuran tim]"],
    ["Pengalaman melatih", "[ISI TIM: program dan klien yang relevan]"],
    ["Peran di program ini", "Memandu workshop dan mendampingi tim selama empat minggu [ISI TIM: sesuaikan bila dua orang]"],
    ["Foto", "[ISI TIM: foto]"],
  ]),
];

const bab7 = [
  h1("7. Penutup", false),
  p("Program ini kami rancang terfokus: satu cara membalas chat yang dipakai seluruh tim, satu catatan calon pelanggan, dan pendampingan sampai kebiasaan baru berjalan. Kami berharap proposal ini menjadi bahan diskusi lebih lanjut. Jadwal, jumlah peserta, dan penekanan materi dapat kami sesuaikan dengan arahan Bapak dan Ibu."),
  h2("Langkah Berikutnya"),
  table([3200, 6438], ["Waktu", "Kegiatan"], [
    ["Paling lambat 5 November 2026", "Konfirmasi kerja sama, pembayaran pertama, kesepakatan menu dan jumlah konsumsi"],
    ["7 November 2026", "Pengiriman makan dan snack untuk 50 orang di acara Sanggabiz"],
    ["9 - 13 November 2026", "Mengenal tim"],
    ["Pekan 16 - 21 November 2026", "Workshop 4 jam dan pembayaran kedua"],
    ["Sekitar 23 November - 18 Desember 2026", "Pendampingan empat minggu"],
    ["Paling lambat 5 hari kerja setelahnya", "Laporan akhir"],
  ]),
  spacer(200),
  p("**Kontak program**: [ISI TIM: nama, jabatan, nomor WhatsApp]"),
  p("partnership@sanggabiz.com  |  WhatsApp 0877-7413-4288  |  www.sanggabiz.com", { run: { color: MUTED } }),
];

// ---------- sampul ----------
const cover = [
  new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [W],
    rows: [new TableRow({
      height: { value: 12300, rule: HeightRule.EXACT },
      children: [new TableCell({
        width: { size: W, type: WidthType.DXA },
        shading: { fill: NAVY, type: ShadingType.CLEAR, color: "auto" },
        borders: { top: none, bottom: none, left: none, right: none },
        margins: { top: 500, bottom: 400, left: 560, right: 560 },
        children: [
          new Paragraph({ spacing: { after: 2600 }, children: [img("logo_white.png", 150, 30)] }),
          new Paragraph({ spacing: { after: 160 }, children: [new TextRun({ text: "PROPOSAL PELATIHAN", font: FONT, bold: true, size: 20, color: GOLD, characterSpacing: 60 })] }),
          new Paragraph({ spacing: { after: 240, line: 400, lineRule: "atLeast" }, children: [new TextRun({ text: JUDUL, font: FONT, bold: true, size: 52, color: "FFFFFF" })] }),
          new Paragraph({ spacing: { after: 2400 }, border: { bottom: { style: BorderStyle.SINGLE, size: 24, color: GOLD, space: 14 } }, children: [new TextRun({ text: "Pelatihan closing lewat WhatsApp untuk tim CS Aqiqah Al Kautsar", font: FONT, size: 24, color: "DCE6F2" })] }),
          new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: "Diajukan oleh Sanggabiz", font: FONT, bold: true, size: 22, color: "FFFFFF" })] }),
          new Paragraph({ children: [new TextRun({ text: "November 2026", font: FONT, size: 22, color: "DCE6F2" })] }),
        ],
      })],
    })],
  }),
  spacer(300),
  new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [3212, 3213, 3213],
    rows: [new TableRow({ children: [
      ["Seluruh tim CS", "6 sampai 8 CS dan 1 Supervisor"],
      ["Workshop 4 jam", "Sebagian besar waktu untuk praktik dengan chat nyata"],
      ["Didampingi 1 bulan", "Lewat WhatsApp, dengan laporan hasil di akhir"],
    ].map(([a, b], i) => new TableCell({
      width: { size: 3212 + (i ? 1 : 0), type: WidthType.DXA },
      borders: { top: { style: BorderStyle.SINGLE, size: 18, color: GOLD }, bottom: none, left: none, right: none },
      margins: { top: 120, bottom: 60, left: 120, right: 160 },
      children: [
        new Paragraph({ spacing: { after: 40 }, children: [new TextRun({ text: a, bold: true, size: 26, color: NAVY })] }),
        new Paragraph({ children: [new TextRun({ text: b, size: 17, color: MUTED })] }),
      ],
    })) })],
  }),
];

const footer = new Footer({
  children: [new Paragraph({
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: LINE, space: 6 } },
    tabStops: [{ type: TabStopType.RIGHT, position: W }],
    children: [
      new TextRun({ text: "Sanggabiz  |  " + JUDUL + "  |  Aqiqah Al Kautsar", size: 14, color: MUTED }),
      new TextRun({ text: "\t", size: 14 }),
      new TextRun({ children: ["Halaman ", PageNumber.CURRENT], size: 14, color: MUTED }),
    ],
  })],
});

const page = { size: { width: 11906, height: 16838 }, margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } };
const doc = new Document({
  creator: "Sanggabiz", title: JUDUL + " - Aqiqah Al Kautsar",
  styles: {
    default: { document: { run: { font: FONT, size: 19, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 30, bold: true, color: NAVY },
        paragraph: { spacing: { before: 0, after: 200 }, outlineLevel: 0, border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: GOLD, space: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 22, bold: true, color: NAVY },
        paragraph: { spacing: { before: 260, after: 110 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 260 } } } }] }] },
  sections: [
    { properties: { page: { ...page, margin: { top: 700, bottom: 700, left: 1134, right: 1134 } } }, children: cover },
    { properties: { page }, footers: { default: footer }, children: [...bab1, ...bab2, ...bab3, ...bab4, ...bab5, ...bab6, ...bab7] },
  ],
});

const outDir = path.join(__dirname, "..", "proposal");
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, "v1 Proposal Training CS Closing - Aqiqah Al Kautsar.docx");
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log("ditulis:", out); });
