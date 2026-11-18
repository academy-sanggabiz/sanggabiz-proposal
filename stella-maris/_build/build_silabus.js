// v1: Silabus pelatihan AI Video Generation untuk Stella Maris School (docx, A4 portrait).
// Sumber: sumber/Minutes of Meetings - Stella Maris 17 Nov 2026.pdf
// Jalankan: NODE_PATH=/opt/node-tools/node_modules node build_silabus.js
const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, Footer, Header,
  AlignmentType, BorderStyle, WidthType, ShadingType, PageNumber, LevelFormat, VerticalAlign,
} = require("docx");

const NAVY = "0B396D", INK = "1D1D1F", MUTED = "5C5F66", GOLD = "FFC00C", LINE = "C9D2DE", TEAL = "DCE6F2";
const FONT = "Montserrat";
const W = 9638;

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
  spacing: { after: o.after ?? 110, before: o.before ?? 0, line: o.line ?? 290 }, keepNext: o.keepNext, indent: o.indent,
});
const h1 = (text) => new Paragraph({ heading: "Heading1", children: [new TextRun({ text })], keepNext: true });
const h2 = (text) => new Paragraph({ heading: "Heading2", children: [new TextRun({ text })], keepNext: true });
const h3 = (text) => new Paragraph({ children: [new TextRun({ text, bold: true, size: 20, color: NAVY })], spacing: { before: 220, after: 90 }, keepNext: true });
const note = (text) => new Paragraph({ children: runs(text, { size: 16, color: MUTED }), spacing: { before: 60, after: 160, line: 260 } });
const gap = () => p("", { after: 60 });

// ---------- penolong tabel ----------
const thin = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: thin, bottom: thin, left: thin, right: thin };
function cell(content, width, o = {}) {
  const lines = Array.isArray(content) ? content : [content];
  return new TableCell({
    width: { size: width, type: WidthType.DXA }, borders, columnSpan: o.span,
    shading: o.fill ? { fill: o.fill, type: ShadingType.CLEAR, color: "auto" } : undefined,
    verticalAlign: VerticalAlign.TOP, margins: { top: 70, bottom: 70, left: 100, right: 100 },
    children: lines.map((t) => new Paragraph({
      alignment: o.align || AlignmentType.LEFT, spacing: { after: 40, line: 260 },
      indent: o.hang ? { left: 300, hanging: 300 } : undefined,
      children: runs(t, { size: o.size || 17, bold: o.bold, color: o.color || INK }),
    })),
  });
}
function table(widths, header, rows, o = {}) {
  const head = new TableRow({ tableHeader: true, cantSplit: true, children: header.map((t, i) => cell(t, widths[i], { fill: NAVY, color: "FFFFFF", bold: true, size: 16 })) });
  const body = rows.map((r, ri) => new TableRow({
    cantSplit: true,
    children: r.map((c, i) => cell(c, widths[i], { fill: ri % 2 ? "F7F9FC" : undefined, bold: o.boldFirst && i === 0 })),
  }));
  return new Table({ width: { size: W, type: WidthType.DXA }, columnWidths: widths, rows: [head, ...body] });
}
// tabel dua kolom: label di kiri, isi di kanan (untuk satu topik)
function kv(rows) {
  const wl = 1900, wr = W - wl;
  return new Table({
    width: { size: W, type: WidthType.DXA }, columnWidths: [wl, wr],
    rows: rows.map(([k, v]) => new TableRow({
      children: [
        cell(k, wl, { fill: TEAL, bold: true, size: 16, color: NAVY }),
        cell(v, wr, { hang: Array.isArray(v) && v.length > 1 }),
      ],
    })),
  });
}
const num = (arr) => arr.map((t, i) => `${i + 1}. ${t}`);

// ---------- data topik ----------
// Aktivitas: [menit, teks]. Jumlah menit dicek terhadap durasi topik.
const topik = [
  {
    id: "1.1", hari: 1, judul: "Alur kerja video AI dan brief video", menit: 55,
    tujuan: [
      "Menjelaskan (C2) enam tahap alur kerja video AI dari ide sampai video akhir.",
      "Menyusun (C6) brief satu halaman untuk satu video promosi sekolah.",
    ],
    outline: [
      "Enam tahap alur kerja: ide, brief, skrip dan storyboard, generasi klip, perakitan, tinjauan dan publikasi.",
      "Unsur brief: tujuan, audiens, pesan utama, durasi dan rasio layar (9:16 atau 16:9), gaya visual, saluran tayang.",
      "Dua kebutuhan di Stella Maris: promosi pendaftaran dan kegiatan sekolah (tim Marketing), pemanfaatan fasilitas sekolah untuk promosi (tim Business Development).",
      "Batas teknis video AI: durasi klip per generasi, konsistensi tampilan antar klip, teks dan wajah di dalam video.",
      "Daftar cek mutu brief, lima butir: tujuan terukur, audiens spesifik, satu pesan utama, durasi dan rasio sesuai saluran, gaya visual yang bisa dideskripsikan.",
    ],
    aktivitas: [
      [10, "Trainer membagikan layar dan memperlihatkan satu alur utuh, dari brief satu halaman sampai video 15 detik, sambil menyebut keputusan di tiap tahap."],
      [5, "Tiap peserta menulis di kolom obrolan satu kebutuhan video di divisinya."],
      [25, "Tiap peserta mengisi Lembar Brief Video untuk satu video promosi sekolah. Peserta Marketing memilih tema pendaftaran atau kegiatan sekolah, peserta Business Development memilih satu fasilitas sekolah."],
      [10, "Peserta berpasangan di breakout room, saling memeriksa brief dengan daftar cek lima butir, lalu memperbaikinya."],
      [5, "Trainer merangkum dan menjawab pertanyaan."],
    ],
    alat: "Platform rapat daring [ISI TIM: Google Meet atau Zoom, ikuti pilihan Stella Maris], slide, templat Lembar Brief Video (Google Docs), daftar cek mutu brief.",
    output: "Lembar Brief Video, satu per peserta.",
    ukuran: "Brief memuat keenam unsur dan memenuhi minimal 4 dari 5 butir daftar cek yang diperiksa pasangan.",
  },
  {
    id: "2.1", hari: 1, judul: "Struktur prompt video", menit: 35,
    tujuan: [
      "Menerapkan (C3) rumus prompt tujuh unsur untuk mengubah brief menjadi prompt.",
      "Menganalisis (C4) perbedaan hasil dari dua prompt yang berbeda tingkat kejelasannya.",
    ],
    outline: [
      "Tujuh unsur prompt: subjek, aksi, latar, gaya visual, gerak kamera, pencahayaan, durasi dan rasio.",
      "Dari kalimat brief menjadi prompt, dengan contoh untuk acara sekolah dan fasilitas sekolah.",
      "Bahasa prompt: Indonesia atau Inggris. Trainer menunjukkan perbandingan hasil pada tool yang dipakai.",
      "Kesalahan umum: prompt terlalu umum, terlalu banyak perintah dalam satu klip, istilah visual yang saling bertentangan.",
      "Menyimpan prompt yang berhasil beserta alasannya.",
    ],
    aktivitas: [
      [10, "Trainer membedah satu prompt umum dan versi tujuh unsurnya, lalu menayangkan dua hasil berdampingan yang sudah disiapkan sebelum sesi."],
      [15, "Tiap peserta menulis tiga prompt dari briefnya, satu untuk tiap adegan, di Templat Prompt."],
      [10, "Berpasangan di breakout room, peserta bertukar templat, menandai unsur yang belum ada, lalu merevisi."],
    ],
    alat: "Slide, Templat Prompt (Google Docs), dua pasang video pembanding dari trainer.",
    output: "Templat Prompt terisi, tiga prompt per peserta.",
    ukuran: "Tiap prompt memuat tujuh unsur, atau menyebut alasan satu unsur dilewati, dan sudah diperiksa pasangan.",
  },
  {
    id: "2.2", hari: 1, judul: "Prompt gambar ke video, gerak kamera, dan konsistensi", menit: 35,
    tujuan: [
      "Menerapkan (C3) teknik gambar ke video dan instruksi gerak kamera pada prompt.",
      "Mengevaluasi (C5) risiko hak pakai dan persetujuan orang tua pada bahan visual sekolah.",
    ],
    outline: [
      "Teks ke video dan gambar ke video: kapan memilih yang mana.",
      "Foto asli fasilitas sekolah sebagai gambar acuan.",
      "Menyebut gerak kamera (geser, miring, zoom, mengikuti objek) beserta kecepatannya.",
      "Menjaga konsistensi tokoh dan gaya antar klip: deskripsi yang dipakai berulang, gambar acuan, dan pengaturan penguncian hasil bila tool menyediakannya.",
      "Aturan aman: foto dan wajah siswa memerlukan persetujuan orang tua, data pribadi tidak diunggah ke tool tanpa cek kebijakan sekolah, ketentuan platform tayang soal pelabelan konten buatan AI dicek sebelum unggah.",
    ],
    aktivitas: [
      [10, "Trainer mengubah satu foto fasilitas menjadi klip dengan dua versi instruksi kamera dan menunjukkan selisih hasilnya."],
      [15, "Tiap peserta merevisi satu dari tiga promptnya menjadi versi gambar ke video dengan instruksi kamera. Peserta memakai foto fasilitas dari folder bersama [ISI TIM: foto fasilitas dan foto acuan dari Maria sebelum Hari 1]."],
      [10, "Diskusi kelas: peserta menyusun lima butir Daftar Cek Aman Publikasi di dokumen bersama, trainer mencatat."],
    ],
    alat: "Folder bersama Google Drive berisi foto fasilitas, slide, dokumen Daftar Cek Aman Publikasi.",
    output: "Satu prompt gambar ke video per peserta, dan draf Daftar Cek Aman Publikasi milik kelas (lima butir).",
    ukuran: "Prompt memuat instruksi kamera dan rujukan gambar. Daftar cek berisi lima butir yang disepakati kelas.",
  },
  {
    id: "3.1", hari: 1, judul: "Praktik membuat klip dan memperbaiki hasil", menit: 80,
    tujuan: [
      "Mencipta (C6) tiga klip video dari prompt buatan sendiri.",
      "Mengevaluasi (C5) hasil generasi terhadap brief dan memperbaikinya lewat percobaan berulang.",
    ],
    outline: [
      "Aturan satu perubahan per percobaan supaya penyebab perbaikan terlihat.",
      "Membaca hasil: bagian yang sesuai brief, bagian yang melenceng (bentuk tubuh, teks, gerak).",
      "Cara memperbaiki: menambah atau mengurangi detail, mengganti gerak kamera, mengganti gambar acuan.",
      "Log iterasi: prompt, hasil, perubahan, penilaian.",
      "Memilih klip terbaik untuk dibawa ke Hari 2.",
    ],
    aktivitas: [
      [10, "Trainer mendemokan Log Iterasi dengan tiga percobaan atas satu prompt."],
      [40, "Tiap peserta membuat tiga klip dari tiga promptnya dan mengisi Log Iterasi. Saat menunggu hasil, peserta menulis perbaikan prompt berikutnya. Trainer masuk ke breakout room secara bergilir, sekitar lima menit per peserta."],
      [20, "Tiap peserta menayangkan satu klip terbaik selama 2 menit dan menyebut satu perubahan prompt yang paling berpengaruh."],
      [10, "Peserta melengkapi Log Iterasi dan memilih klip yang dibawa ke Hari 2."],
    ],
    alat: "Tool generasi video AI [ISI TIM: tool dan paket akun ditentukan trainer bersama Maria, cek kuota generasi per peserta], templat Log Iterasi (Google Sheets).",
    output: "Tiga klip video per peserta dan satu Log Iterasi.",
    ukuran: "Minimal satu klip sesuai brief menurut daftar cek brief. Log Iterasi memuat minimal tiga percobaan dengan perubahan yang dicatat.",
  },
  {
    id: "4.1", hari: 2, judul: "Storyboard dan perakitan klip", menit: 40,
    tujuan: [
      "Menyusun (C6) storyboard empat sampai lima adegan dari klip yang sudah ada.",
      "Menerapkan (C3) perakitan klip menjadi satu video berurutan.",
    ],
    outline: [
      "Storyboard tiga bagian: pembuka, isi, penutup dengan ajakan bertindak.",
      "Urutan adegan dan durasi tiap adegan, dijumlahkan ke durasi di brief.",
      "Menutup celah cerita dengan klip pelengkap.",
      "Perakitan di aplikasi penyunting video: memotong, mengurutkan, transisi sederhana.",
    ],
    aktivitas: [
      [5, "Trainer memperlihatkan satu storyboard video 25 detik dengan lima adegan."],
      [10, "Tiap peserta mengisi tabel storyboard: adegan, isi, durasi, klip yang sudah ada, klip yang masih harus dibuat."],
      [25, "Peserta membuat klip pelengkap, lalu mulai merakit semua klip di aplikasi penyunting video."],
    ],
    alat: "Templat storyboard (Google Sheets), tool generasi video, aplikasi penyunting video [ISI TIM: tanya Maria aplikasi penyunting yang sudah dipakai tim, agar tidak ada instalasi baru].",
    output: "Storyboard dan draf rakitan video, satu per peserta.",
    ukuran: "Storyboard memuat empat sampai lima adegan dengan total durasi sesuai brief (20 sampai 30 detik).",
  },
  {
    id: "4.2", hari: 2, judul: "Suara, teks, dan finalisasi video", menit: 40,
    tujuan: [
      "Menerapkan (C3) narasi, musik latar, teks layar, dan logo pada video.",
      "Mengevaluasi (C5) hak pakai musik dan suara sebelum video dipublikasikan.",
    ],
    outline: [
      "Narasi: skrip pendek, suara rekaman sendiri atau suara buatan AI bila tool menyediakannya.",
      "Musik latar yang boleh dipakai untuk promosi: pustaka berlisensi atau bebas hak cipta.",
      "Teks, logo, dan ajakan bertindak ditambahkan di penyunting video, tidak lewat prompt, karena teks di dalam video hasil AI sering salah eja.",
      "Ekspor: resolusi, rasio layar, dan ukuran berkas untuk Instagram, TikTok, YouTube, dan situs sekolah.",
      "Penamaan dan penyimpanan berkas di folder bersama.",
    ],
    aktivitas: [
      [5, "Trainer memperlihatkan cara menambah narasi, teks, dan logo pada rakitan."],
      [30, "Tiap peserta menyelesaikan videonya dan mengekspor. Logo dan panduan merek Stella Maris dipakai dari folder bersama [ISI TIM: logo dan panduan merek dari Maria]."],
      [5, "Peserta mengunggah video ke folder bersama Google Drive."],
    ],
    alat: "Aplikasi penyunting video, folder bersama Google Drive, daftar sumber musik berlisensi dari trainer.",
    output: "Satu video AI berdurasi 20 sampai 30 detik, siap ditinjau.",
    ukuran: "Video terekspor sesuai rasio di brief, memuat teks dan logo sekolah, dan sudah diunggah ke folder bersama.",
  },
  {
    id: "5.1", hari: 2, judul: "Peta peluang AI di tiap divisi", menit: 55,
    tujuan: [
      "Menganalisis (C4) tugas kerja di divisi sendiri yang cocok dibantu AI.",
      "Mengevaluasi (C5) nilai, usaha, dan risiko tiap peluang.",
    ],
    outline: [
      "Ciri tugas yang cocok dibantu AI: berulang, bahan jelas, draf cepat membantu, hasil tetap dicek orang.",
      "Empat kelompok pemakaian di sekolah sebagai bahan diskusi: konten (teks, gambar, video), komunikasi (draf surat dan balasan), administrasi (merapikan data, notulen), analisis (merangkum masukan dan survei).",
      "Menilai peluang dengan skor nilai dan usaha, masing-masing 1 sampai 5.",
      "Risiko yang dicek: data pribadi siswa dan orang tua, akurasi hasil, hak cipta, kebijakan internal sekolah.",
    ],
    aktivitas: [
      [10, "Trainer menjelaskan ciri tugas yang cocok dan empat kelompok pemakaian, dengan dua contoh di luar video."],
      [25, "Peserta berkumpul per divisi di breakout room (satu divisi satu ruang, peserta tunggal bergabung dengan divisi terdekat). Tiap divisi mengisi Peta Peluang AI minimal tiga tugas dengan kolom: tugas, cara mengerjakan sekarang, bantuan AI, risiko, skor nilai dan usaha."],
      [15, "Tiap divisi mempresentasikan petanya selama 3 menit, peserta lain bertanya."],
      [5, "Tiap divisi memilih satu peluang prioritas untuk Rencana 30 Hari."],
    ],
    alat: "Templat Peta Peluang AI (Google Sheets), slide.",
    output: "Peta Peluang AI per divisi dan satu peluang prioritas.",
    ukuran: "Tiap divisi memuat minimal tiga peluang dengan skor dan risiko terisi, serta satu peluang prioritas.",
  },
  {
    id: "6.1", hari: 2, judul: "Tayang dan tinjauan video akhir", menit: 35,
    tujuan: [
      "Mengevaluasi (C5) video sendiri dan video rekan memakai rubrik empat kriteria.",
      "Memperbaiki (C3) video berdasarkan umpan balik.",
    ],
    outline: [
      "Rubrik: kesesuaian dengan brief, mutu prompt dan iterasi, kejelasan pesan, kesiapan pakai. Skala 1 sampai 4.",
      "Cara memberi umpan balik: satu hal yang sudah berhasil dan satu hal yang diperbaiki.",
    ],
    aktivitas: [
      [3, "Trainer menjelaskan rubrik."],
      [28, "Tiap peserta menayangkan videonya selama 1,5 menit, lalu menerima umpan balik 2 menit dari trainer dan satu rekan."],
      [4, "Tiap peserta mencatat satu perbaikan untuk videonya."],
    ],
    alat: "Lembar rubrik (Google Sheets), video di folder bersama.",
    output: "Video akhir dan lembar rubrik yang diisi trainer dan rekan.",
    ukuran: "Tiap peserta menayangkan satu video akhir dan menerima skor rubrik. Usulan target: skor minimal 3 dari 4 pada kriteria kesesuaian dengan brief.",
  },
  {
    id: "7.1", hari: 2, judul: "Rencana penerapan 30 hari dan penugasan pasca-pelatihan", menit: 35,
    tujuan: [
      "Menyusun (C6) Rencana 30 Hari untuk menjaga pemakaian AI tetap berjalan di pekerjaan.",
      "Menjelaskan (C2) ketentuan dan penilaian penugasan pasca-pelatihan.",
    ],
    outline: [
      "Kebiasaan yang menjaga pemakaian AI: jadwal latihan mingguan, perpustakaan prompt bersama, templat brief yang dipakai ulang, tinjauan hasil tiap bulan.",
      "Pembagian peran di tim: pemilik perpustakaan prompt dan penjaga Daftar Cek Aman Publikasi.",
      "Ketentuan penugasan: satu video baru 30 sampai 45 detik untuk kebutuhan nyata divisi, dengan brief, prompt akhir, dan Log Iterasi.",
      "Cara bertanya setelah pelatihan [ISI TIM: kanal dukungan dan lamanya, misalnya grup WhatsApp selama 30 hari].",
    ],
    aktivitas: [
      [10, "Trainer menjelaskan penugasan, membagikan rubrik dan Lembar Penugasan."],
      [15, "Tiap peserta mengisi Rencana 30 Hari dari peluang prioritas di Peta Peluang AI: tiga langkah, tanggal, dan tanda selesai."],
      [10, "Tim memasukkan prompt terbaik tiap peserta ke Perpustakaan Prompt bersama dan menyepakati pemiliknya."],
    ],
    alat: "Templat Rencana 30 Hari, Lembar Penugasan, dokumen Perpustakaan Prompt (Google Docs).",
    output: "Rencana 30 Hari per peserta, isi awal Perpustakaan Prompt bersama, dan Lembar Penugasan.",
    ukuran: "Rencana memuat tiga langkah bertanggal dengan tanda selesai. Tiap peserta memasukkan minimal dua prompt ke perpustakaan.",
  },
];

// ---------- jadwal: urutan blok per hari, menit dicek ----------
const jadwal = [
  { hari: 1, mulai: "09.00", blok: [
    { nama: "Pembukaan: tujuan dua hari, ringkasan hasil pemetaan awal peserta", menit: 15 },
    { topik: "1.1" }, { topik: "2.1" }, { topik: "2.2" },
    { nama: "Istirahat", menit: 10 },
    { topik: "3.1" },
    { nama: "Penutup Hari 1: rangkuman dan tugas antar hari", menit: 10 },
  ] },
  { hari: 2, mulai: "09.00", blok: [
    { nama: "Pembukaan Hari 2: tinjau tugas antar hari dan kendala", menit: 10 },
    { topik: "4.1" }, { topik: "4.2" },
    { nama: "Istirahat", menit: 10 },
    { topik: "5.1" }, { topik: "6.1" }, { topik: "7.1" },
    { nama: "Post-test dan survei kepuasan", menit: 15 },
  ] },
];
const hasilRingkas = {
  "1.1": "Lembar Brief Video", "2.1": "Templat Prompt, tiga prompt", "2.2": "Prompt gambar ke video, Daftar Cek Aman Publikasi",
  "3.1": "Tiga klip dan Log Iterasi", "4.1": "Storyboard dan draf rakitan", "4.2": "Video AI 20 sampai 30 detik",
  "5.1": "Peta Peluang AI per divisi", "6.1": "Video akhir dan rubrik terisi", "7.1": "Rencana 30 Hari dan Perpustakaan Prompt",
};
const hasNama = {
  "Pembukaan: tujuan dua hari, ringkasan hasil pemetaan awal peserta": "Peserta mengetahui target dua hari",
  "Istirahat": "",
  "Penutup Hari 1: rangkuman dan tugas antar hari": "Tugas antar hari dipahami",
  "Pembukaan Hari 2: tinjau tugas antar hari dan kendala": "Kendala Hari 1 terjawab",
  "Post-test dan survei kepuasan": "Skor post-test dan survei",
};

const T = Object.fromEntries(topik.map((t) => [t.id, t]));
// cek jumlah menit per topik dan per hari
for (const t of topik) {
  const s = t.aktivitas.reduce((a, x) => a + x[0], 0);
  if (s !== t.menit) throw new Error(`Topik ${t.id}: aktivitas ${s} menit, seharusnya ${t.menit}`);
}
const fmt = (m) => `${String(Math.floor(m / 60)).padStart(2, "0")}.${String(m % 60).padStart(2, "0")}`;
const ringkasRows = [];
for (const d of jadwal) {
  let cur = 9 * 60, total = 0;
  for (const b of d.blok) {
    const menit = b.topik ? T[b.topik].menit : b.menit;
    const nama = b.topik ? `Topik ${b.topik}. ${T[b.topik].judul}` : b.nama;
    const hasil = b.topik ? hasilRingkas[b.topik] : hasNama[b.nama] || "";
    ringkasRows.push([`Hari ${d.hari}`, `${fmt(cur)} - ${fmt(cur + menit)}`, nama, `${menit} menit`, hasil]);
    cur += menit; total += menit;
  }
  if (total !== 240) throw new Error(`Hari ${d.hari}: total ${total} menit, seharusnya 240`);
}

// ---------- isi dokumen ----------
const isi = [];

isi.push(new Paragraph({ children: [new TextRun({ text: "SILABUS PELATIHAN", bold: true, size: 40, color: NAVY })], spacing: { after: 40 } }));
isi.push(new Paragraph({ children: [new TextRun({ text: "AI Video Generation untuk Promosi dan Pemasaran Stella Maris School", bold: true, size: 26, color: INK })], spacing: { after: 100 } }));
isi.push(new Paragraph({
  children: [new TextRun({ text: "Disusun oleh Sanggabiz. Versi 1, 18 November 2026. Dasar: rapat dengan Stella Maris International Education (Maria, HR) pada 17 November 2026.", size: 17, color: MUTED })],
  spacing: { after: 200 }, border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: GOLD, space: 6 } },
}));

isi.push(h2("1. Ringkasan program"));
isi.push(table([2300, 7338], ["Hal", "Isi"], [
  ["Tujuan program", "Peserta menghasilkan video promosi dengan AI secara mandiri, mulai dari brief dan prompt sampai video akhir, dan mampu menemukan pemakaian AI di divisinya masing-masing."],
  ["Peserta", "7 sampai 8 orang, level staff sampai manajerial, dari tim Marketing, Business Development, dan divisi lain. Sudah pernah memakai AI, belum mahir."],
  ["Level materi", "Intermediate sampai advanced awal. Tidak dimulai dari pengenalan dasar. Penyesuaian dilakukan setelah pemetaan awal."],
  ["Format", "Online, dengan praktik langsung oleh peserta di setiap sesi. Gabungan penyampaian materi, demonstrasi tool, dan praktik mandiri."],
  ["Durasi", "Dua hari, masing-masing setengah hari (4 jam, 09.00 - 13.00 WIB, usulan jam mulai). Total 8 jam, termasuk pembukaan, istirahat, dan penutup."],
  ["Jadwal", "Januari 2027, minggu kedua atau ketiga. Tanggal final menunggu persetujuan internal Stella Maris."],
  ["Studi kasus", "Kebutuhan promosi Stella Maris: pendaftaran, kegiatan sekolah, dan fasilitas sekolah yang dikelola tim Business Development."],
  ["Pengajar", "[ISI TIM: nama dan profil trainer]"],
  ["Evaluasi", "Pre-test dan post-test, rubrik video akhir, survei kepuasan, dan penugasan pasca-pelatihan berupa satu video AI."],
], { boldFirst: true }));
isi.push(gap());

isi.push(h2("2. Dasar penyusunan dan metode"));
isi.push(p("Silabus ini mengikuti lima hal yang disampaikan Maria pada rapat 17 November 2026: fokus pada pembuatan video dengan AI, materi tidak dimulai dari dasar, praktik langsung secara online, evaluasi lewat penugasan berupa video, dan arahan agar pemakaian AI berlanjut setelah pelatihan."));
isi.push(table([2400, 4400, 2838], ["Metode", "Alasan dipilih", "Muncul di"], [
  ["Andragogi (Knowles)", "Peserta dewasa dan sudah berpengalaman. Mereka belajar paling cepat dari tugas kerja sendiri, jadi tiap latihan memakai kebutuhan promosi sekolah.", "Aktivitas semua topik"],
  ["Taksonomi Bloom revisi", "Klien meminta kemampuan yang terukur. Kata kerja Bloom (C2 sampai C6) membuat tujuan tiap topik bisa dinilai.", "Tujuan pembelajaran tiap topik"],
  ["Backward design", "Hasil akhir dan buktinya, yaitu video dan rubrik, ditetapkan lebih dulu. Materi disusun dari sana, dan diperiksa dengan pemetaan awal peserta.", "Bagian 3 dan 4"],
  ["ADDIE", "Alur program dari analisis sampai evaluasi: Analysis lewat rapat dan pemetaan awal, Design lewat silabus ini, Development lewat templat dan soal, Implementation dua hari, Evaluation lewat post-test dan penugasan.", "Bagian 3, 7, dan 8"],
  ["Kirkpatrick", "Klien ingin mengukur kemampuan dan pemakaian lanjutan. Empat level memisahkan reaksi, pembelajaran, perilaku, dan dampak.", "Bagian 8"],
], { boldFirst: true }));
isi.push(gap());

isi.push(h2("3. Tujuan pelatihan"));
isi.push(p("Setelah dua hari, peserta mampu:"));
[
  "Menjelaskan alur kerja video AI dari ide sampai video akhir (C2).",
  "Menyusun brief dan prompt yang efektif untuk satu video promosi (C6).",
  "Mengevaluasi hasil generasi dan memperbaikinya lewat percobaan berulang (C5).",
  "Mencipta satu video AI berdurasi 20 sampai 30 detik yang siap ditinjau (C6).",
  "Menganalisis peluang pemakaian AI di divisinya dan menyusun rencana penerapan 30 hari (C4, C6).",
].forEach((t, i) => isi.push(p(`${i + 1}. ${t}`, { indent: { left: 360, hanging: 360 }, after: 60 })));
isi.push(gap());

isi.push(h2("4. Persiapan sebelum Hari 1"));
isi.push(table([2600, 7038], ["Persiapan", "Isi"], [
  ["Pemetaan awal (pre-test)", "Formulir online dikirim tiga hari sebelum Hari 1, berisi 10 soal pengetahuan prompt dan alur kerja, serta penilaian diri atas pengalaman memakai AI. Hasilnya dirangkum di pembukaan Hari 1 dan dipakai untuk menyesuaikan kedalaman materi."],
  ["Akun dan kuota tool", "Tiap peserta memiliki akun aktif di tool generasi video yang disepakati, dengan kuota generasi yang cukup untuk dua hari dan tugas antar hari. [ISI TIM: jumlah klip per peserta, paket akun, dan pihak yang membayar kuota]."],
  ["Perangkat dan koneksi", "Satu laptop per peserta, kamera dan mikrofon aktif, koneksi internet stabil. Ponsel hanya sebagai cadangan."],
  ["Bahan dari Stella Maris", "Foto fasilitas sekolah, logo, panduan merek, dan satu contoh video promosi yang sudah ada. Dikumpulkan di folder bersama sebelum Hari 1."],
  ["Bahan dari Sanggabiz", "Templat Lembar Brief Video, Templat Prompt, Log Iterasi, storyboard, Peta Peluang AI, Rencana 30 Hari, rubrik, dan slide, semua di folder bersama."],
], { boldFirst: true }));
isi.push(gap());

isi.push(h2("5. Jadwal dua hari"));
isi.push(table([800, 1300, 3900, 1000, 2638], ["Hari", "Waktu (WIB)", "Sesi dan topik", "Durasi", "Hasil"], ringkasRows));
isi.push(note("Jam mulai 09.00 WIB adalah usulan. Maria belum menyebut jam. Tugas antar hari berlangsung di luar jam ini, sekitar 30 sampai 45 menit."));

isi.push(h2("6. Rincian per topik"));
for (const hari of [1, 2]) {
  isi.push(h3(hari === 1 ? "Hari 1. Dari brief ke prompt ke klip" : "Hari 2. Dari klip ke video akhir dan penerapan di pekerjaan"));
  for (const t of topik.filter((x) => x.hari === hari)) {
    isi.push(new Paragraph({
      children: [new TextRun({ text: `Topik ${t.id}. ${t.judul} (${t.menit} menit)`, bold: true, size: 19, color: INK })],
      spacing: { before: 160, after: 70 }, keepNext: true,
    }));
    isi.push(kv([
      ["Tujuan pembelajaran", num(t.tujuan)],
      ["Outline materi", num(t.outline)],
      ["Aktivitas", t.aktivitas.map(([m, tx], i) => `${i + 1}. (${m} menit) ${tx}`)],
      ["Alat dan media", t.alat],
      ["Output", t.output],
      ["Ukuran keberhasilan", t.ukuran],
    ]));
  }
  if (hari === 1) {
    isi.push(new Paragraph({
      children: runs("**Tugas antar hari (usulan, 30 sampai 45 menit).** Peserta melengkapi sampai empat atau lima klip yang bisa dirangkai menjadi video 20 sampai 30 detik, lalu membawanya ke Hari 2. Tugas ini memberi ruang mengembangkan hasil praktik sebelum materi berikutnya, sesuai harapan klien.", { size: 17 }),
      spacing: { before: 140, after: 100, line: 270 },
    }));
  }
}

isi.push(h2("7. Penugasan pasca-pelatihan"));
isi.push(p("Penugasan menguji apakah peserta bisa mengulang proses tanpa pendampingan trainer. Hasilnya menjadi bahan evaluasi tingkat pemahaman, kemampuan menyusun prompt, dan keterampilan membuat video."));
isi.push(table([2300, 7338], ["Unsur", "Ketentuan"], [
  ["Tugas", "Satu video AI baru berdurasi 30 sampai 45 detik untuk kebutuhan nyata di divisi peserta."],
  ["Berkas yang dikumpulkan", "Video, Lembar Brief Video, prompt akhir, Log Iterasi (minimal tiga percobaan), dan refleksi satu paragraf tentang apa yang berhasil dan apa yang akan diubah."],
  ["Tenggat", "[ISI TIM: tenggat pengumpulan, usulan 14 hari setelah Hari 2]"],
  ["Penilaian", "Rubrik empat kriteria di bawah, skala 1 sampai 4, sama dengan rubrik Topik 6.1 supaya hasilnya bisa dibandingkan."],
  ["Umpan balik", "Usulan: umpan balik tertulis singkat dari trainer untuk tiap peserta dan rekap skor untuk Maria. [ISI TIM: batas waktu umpan balik dan keputusan apakah masuk biaya]"],
], { boldFirst: true }));
isi.push(gap());
isi.push(table([1900, 1900, 1900, 1900, 2038], ["Kriteria", "Skor 1", "Skor 2", "Skor 3", "Skor 4"], [
  ["Kesesuaian dengan brief", "Video tidak sesuai brief.", "Sebagian unsur brief terpenuhi.", "Semua unsur utama brief terpenuhi.", "Semua unsur terpenuhi dan disesuaikan dengan saluran tayang."],
  ["Mutu prompt dan iterasi", "Prompt umum, tanpa Log Iterasi.", "Prompt memuat sebagian unsur. Log kurang dari tiga percobaan.", "Prompt memuat tujuh unsur. Log tiga percobaan beserta alasan perubahan.", "Prompt lengkap dan Log menunjukkan perbaikan nyata dari percobaan pertama ke terakhir."],
  ["Kejelasan pesan", "Pesan tidak terbaca.", "Pesan ada tetapi tertutup visual.", "Satu pesan utama jelas dan ada ajakan bertindak.", "Pesan jelas, ritme sesuai audiens, ajakan bertindak mudah ditindaklanjuti."],
  ["Kesiapan pakai", "Melanggar Daftar Cek Aman Publikasi.", "Perlu perbaikan besar sebelum tayang.", "Siap tayang dengan perbaikan ringan.", "Siap tayang."],
]));
isi.push(gap());

isi.push(h2("8. Evaluasi (model Kirkpatrick)"));
isi.push(table([1900, 3200, 4538], ["Level", "Alat ukur", "Waktu dan keterangan"], [
  ["1. Reaksi", "Survei kepuasan, 8 pertanyaan skala 1 sampai 5.", "Akhir Hari 2, 5 menit."],
  ["2. Pembelajaran", "Pre-test dan post-test dengan soal yang setara, ditambah rubrik video akhir.", "Pre-test tiga hari sebelum Hari 1. Post-test dan rubrik di Hari 2."],
  ["3. Perilaku", "Penugasan pasca-pelatihan dan Rencana 30 Hari.", "Penugasan dikumpulkan sesuai tenggat. Tinjauan Rencana 30 Hari pada hari ke-30 adalah usulan. [ISI TIM: apakah klien menghendaki tinjauan ini]"],
  ["4. Dampak", "Tidak diukur dalam paket ini.", "Indikator seperti jumlah video per bulan atau waktu produksi memerlukan data awal dari Stella Maris. Usulan: Stella Maris mencatat dua angka itu sebelum dan sesudah pelatihan."],
], { boldFirst: true }));
isi.push(gap());

isi.push(h2("9. Hasil yang dibawa pulang"));
isi.push(table([3600, 1400, 4638], ["Hasil", "Topik", "Bentuk"], [
  ["Lembar Brief Video", "1.1", "Dokumen satu halaman, satu per peserta."],
  ["Templat Prompt, tiga prompt", "2.1", "Dokumen, satu per peserta."],
  ["Prompt gambar ke video", "2.2", "Satu prompt per peserta."],
  ["Daftar Cek Aman Publikasi", "2.2", "Lima butir milik kelas, dipakai ulang sesudah pelatihan."],
  ["Tiga klip dan Log Iterasi", "3.1", "Berkas video dan lembar kerja, per peserta."],
  ["Storyboard", "4.1", "Tabel empat sampai lima adegan, per peserta."],
  ["Video AI akhir 20 sampai 30 detik", "4.2", "Berkas video terekspor, per peserta."],
  ["Peta Peluang AI per divisi", "5.1", "Tabel minimal tiga tugas per divisi."],
  ["Rubrik video akhir", "6.1", "Skor dan umpan balik trainer dan rekan."],
  ["Rencana 30 Hari", "7.1", "Tiga langkah bertanggal, per peserta."],
  ["Perpustakaan Prompt bersama", "7.1", "Dokumen bersama berisi prompt terbaik tiap peserta."],
  ["Video penugasan pasca-pelatihan", "Setelah Hari 2", "Satu video 30 sampai 45 detik beserta berkas pendukung."],
  ["Slide dan semua templat", "Seluruh topik", "Disimpan di folder bersama Google Drive."],
]));
isi.push(gap());

isi.push(h2("10. Kesesuaian dengan output yang diminta klien"));
isi.push(p("Daftar di bawah mengikuti sembilan output yang tercatat di bagian 7 notulen rapat 17 November 2026."));
isi.push(table([700, 4800, 4138], ["No", "Output yang diminta (ringkas)", "Dipenuhi di"], [
  ["1", "Memahami penggunaan tool AI untuk menghasilkan video secara mandiri", "Topik 3.1, 4.1, 4.2"],
  ["2", "Mampu menyusun prompt yang efektif", "Topik 2.1, 2.2"],
  ["3", "Memahami alur kerja dari pengembangan ide sampai video akhir", "Topik 1.1, 4.1, 4.2"],
  ["4", "Menghasilkan minimal satu video AI dari praktik", "Topik 4.2"],
  ["5", "Mengidentifikasi peluang pemakaian AI di divisi masing-masing", "Topik 5.1"],
  ["6", "Memahami cara menjaga dan memperluas pemakaian AI setelah pelatihan", "Topik 7.1"],
  ["7", "Memperoleh penugasan pasca-pelatihan", "Topik 7.1 dan bagian 7"],
  ["8", "Hasil penugasan berupa video AI", "Bagian 7"],
  ["9", "Hasil penugasan menjadi bahan evaluasi pemahaman, prompt, dan keterampilan", "Bagian 7 dan 8"],
], { boldFirst: true }));
isi.push(gap());

isi.push(h2("11. Hal yang masih perlu dikonfirmasi"));
isi.push(table([5400, 4238], ["Hal", "Dari siapa"], [
  ["Tool generasi video dan aplikasi penyunting yang dipakai, serta kuota per peserta", "Trainer Sanggabiz dan Maria"],
  ["Platform rapat daring dan jam mulai", "Maria"],
  ["Nama divisi dan daftar 7 sampai 8 peserta", "Maria"],
  ["Foto fasilitas, logo, panduan merek, contoh video promosi", "Maria dan tim Business Development"],
  ["Tanggal final di minggu kedua atau ketiga Januari 2027", "Stella Maris, setelah persetujuan internal"],
  ["Tenggat dan umpan balik penugasan, kanal dukungan, tinjauan hari ke-30", "Sanggabiz dan Maria"],
], { boldFirst: false }));
isi.push(note("Silabus ini belum memuat anggaran, timeline persiapan, dan mekanisme invoice. Ketiganya dibahas terpisah dalam proposal penawaran."));

// ---------- dokumen ----------
const contact = "WhatsApp 0877-7413-4288   |   www.sanggabiz.com   |   partnership@sanggabiz.com";
const footer = new Footer({ children: [new Paragraph({
  alignment: AlignmentType.CENTER, border: { top: { style: BorderStyle.SINGLE, size: 4, color: INK, space: 6 } },
  children: [new TextRun({ text: contact + "   |   Halaman ", size: 14, color: MUTED }), new TextRun({ children: [PageNumber.CURRENT], size: 14, color: MUTED })],
})] });
const header = new Header({ children: [new Paragraph({
  border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: INK, space: 4 } },
  tabStops: [{ type: "right", position: W }],
  children: [new TextRun({ text: "SANGGABIZ", bold: true, size: 18, color: NAVY }), new TextRun({ text: "\t2027", size: 16, color: MUTED })],
})] });

const doc = new Document({
  creator: "Sanggabiz", title: "Silabus Pelatihan AI Video Generation - Stella Maris School",
  styles: {
    default: { document: { run: { font: FONT, size: 19, color: INK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 30, bold: true, color: NAVY },
        paragraph: { spacing: { before: 0, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 23, bold: true, color: NAVY },
        paragraph: { spacing: { before: 280, after: 120 }, outlineLevel: 1 } },
    ],
  },
  numbering: { config: [{ reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 260 } } } }] }] },
  sections: [{
    properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1250, bottom: 1134, left: 1134, right: 1134 } } },
    headers: { default: header }, footers: { default: footer }, children: isi,
  }],
});

const outDir = path.join(__dirname, "..", "silabus");
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, "v1 Silabus Pelatihan AI Video Generation - Stella Maris.docx");
Packer.toBuffer(doc).then((buf) => { fs.writeFileSync(out, buf); console.log("ditulis:", out); });
