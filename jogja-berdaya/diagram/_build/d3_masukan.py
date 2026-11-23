import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "03-masukan-perbaikan.svg")
s = SVG(1200)
header(s, "Masukan perbaikan proposal: sekarang, masalahnya, usulannya",
       "Hasil membandingkan proposal dengan berita Kedaulatan Rakyat 29 Oktober 2026 dan aturan Sanggabiz. Tujuh masukan prioritas tinggi ada di tabel. Tujuh lainnya ada di bawahnya.")

y = 140
y += card(s, 50, y, 1100, "Tiga inti masukan",
          "1. Pakai isi berita dengan tepat, dan jangan menulis lebih dari yang dikatakan berita.   2. Ukur mutu pekerjaan dan pendapatan, tidak hanya jumlah orang yang dapat kerja.   3. Rapikan susunan anggaran, urutan mitra, dan batas waktu pelacakan.",
          fill=TEALBG, stroke=TEAL, bar=TEAL, tfs=16, bfs=14) + 22

TAG = {"Koran": (BLUE, "#fff"), "Aturan": (NAVY, "#fff"), "Analisis": (TEAL, "#fff")}
rows = [
    (1, ["Koran"], "Bagian urgensi",
     "Berita Kedaulatan Rakyat hanya muncul satu baris di tabel urgensi (proposal strategis, bagian 02).",
     "Berita memuat angka yang bisa menentukan pilihan jalur: empat sektor menyerap 66,51 persen pekerja DIY, tetapi produktivitasnya di bawah rata-rata daerah. Angka itu belum dipakai. Berita juga tidak menyebut Polda atau Kota Yogyakarta, jadi kalimat \"didukung Gubernur\" tidak bisa dipertahankan.",
     "Kutip angka dan pernyataan apa adanya, lengkap dengan tanggal dan halaman. Tulis \"per pekerja\" tanpa menambah \"per tahun\". Hubungkan tiga jalur ke empat sektor (sebagai penilaian kami). Tulis \"sejalan dengan arahan Gubernur\"."),
    (2, ["Koran"], "Ukuran berhasil",
     "Ukuran akhir hanya \"dapat kerja atau tugas berbayar\" (G5: minimal 4 dari 20).",
     "Sultan dan Menaker membahas mutu: produktivitas, pendapatan, kerja formal, jaminan sosial. Pengangguran DIY sudah rendah (3,11 persen), jadi jumlah orang bekerja saja tidak menjawab persoalannya. Pekerjaan berpenghasilan sangat rendah tetap dihitung berhasil.",
     "Tambah data yang dilaporkan: pendapatan sebelum dan di hari ke 90, bentuk hubungan kerja (kontrak, lepas, usaha sendiri), kepesertaan jaminan sosial. Jangan jadikan syarat GO sebelum ada data awal."),
    (3, ["Koran"], "Jalur dan kampung",
     "Pilot menetapkan jalur digital dulu, lalu mencari kampung yang cocok.",
     "Arahan Sultan: pelatihan menyesuaikan potensi kalurahan. Dengan urutan terbalik, proposal terbaca sebagai paket jadi yang dipasang ke kampung.",
     "Pilih kampung dulu lewat asesmen 14 hari, baru tetapkan jalur. Atau tulis alasan jalur digital cocok di kampung mana pun: dipakai untuk menjual dan melayani produk lokal."),
    (4, ["Koran", "Analisis"], "Sasaran peserta",
     "Sasaran \"warga dewasa\". Usia 18 sampai 35 tahun di proposal strategis, 18 tahun ke atas di pilot.",
     "Sultan menyebut lulusan SMK yang tidak kuliah dan anggota Karang Taruna. Dua rentang usia membuat jumlah calon peserta dan target tidak bisa dibandingkan.",
     "Satukan rentang usia. Jadikan Karang Taruna kampung dan SMK sekitar sebagai saluran pendaftaran. Pendaftaran tetap terbuka untuk warga lain."),
    (5, ["Koran", "Analisis"], "Mitra",
     "Deck dan executive proposal menaruh Polda DIY di urutan pertama peran.",
     "Semua arahan kebijakan di berita berasal dari Pemda DIY dan Kementerian Ketenagakerjaan. Kepala BBPVP Semarang menyatakan siap berkolaborasi, tetapi belum disebut di proposal.",
     "Urutan peran: Pemkot dan kelurahan pengampu, Sanggabiz pelaksana, Polda fasilitator ajakan warga. Tambahkan BBPVP Semarang sebagai pihak yang dijajaki untuk standar kompetensi dan asesmen."),
    (6, ["Aturan"], "Anggaran",
     "Ada baris Contingency Rp1.000.000 dan tidak ada baris Fee. Beberapa baris menggabungkan banyak biaya, misalnya \"materi, transport, konsumsi, kit\" Rp5.500.000.",
     "Aturan Sanggabiz: satu baris Fee 10 persen, tanpa baris cadangan, dan tiap baris punya volume dan harga satuan supaya klien bisa menguji angkanya.",
     "Ganti Contingency dengan Fee 10 persen. Pecah baris gabungan. Susun anggaran mengikuti tujuh tahap proses (lihat gambar 04)."),
    (7, ["Analisis"], "Garis waktu",
     "Pilot menulis \"D+30\" di satu tempat dan \"hari ke 90\" di tempat lain untuk keputusan yang sama.",
     "Pembaca tidak tahu kapan pilot selesai dan kapan G5 dihitung. Biaya pelacakan juga sulit diperkirakan.",
     "Tetapkan satu definisi, misalnya hari ke 90 dihitung dari hari terakhir pelatihan, lalu pakai di semua dokumen."),
]
cx = [50, 128, 440, 800]
cwid = [70, 300, 340, 350]
s.rect(50, y, 1100, 34, NAVY, rx=6)
for t, x in [("No", 62), ("Sekarang di proposal", 140), ("Kenapa jadi masalah", 452), ("Usulan perbaikan", 812)]:
    s.text(x, y + 9, t, 14, "#fff", True)
y += 34
for i, (n, tags, name, a, b, c) in enumerate(rows):
    h = max(s.height_of(a, 13, 285) + 22, s.height_of(b, 13, 325), s.height_of(c, 13, 335)) + 22
    h = max(h, 100)
    s.rect(50, y, 1100, h, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.rect(50, y, 5, h, RED, None, rx=0)
    s.circle(82, y + 24, 15, NAVY)
    s.text(82, y + 17, n, 15, "#fff", True, "middle")
    ty = y + 46
    for tg in tags:
        bg, fg = TAG[tg]
        w = 14 + len(tg) * 7
        s.rect(62, ty, w, 18, bg, None, rx=9)
        s.text(62 + w / 2, ty + 3.5, tg, 11, fg, True, "middle")
        ty += 22
    s.text(140, y + 10, name, 14, NAVY, True, maxw=285)
    off = 22
    s.text(140, y + 10 + off, a, 13, INK, maxw=285)
    s.text(452, y + 10, b, 13, INK, maxw=325)
    s.rect(795, y + 8, 1, h - 16, LINE, None, rx=0)
    s.text(812, y + 10, c, 13, INK, maxw=325)
    y += h
s.line(50, y, 1150, y, LINE, 1)
y += 36

y = section(s, y, 2, "Tujuh masukan lain (prioritas sedang dan rendah)")
more = [
    ("8. Dua tujuan lulusan", "Sultan menyebut \"pegawai atau pionir bisnis\". Pilot hanya mengukur kerja. Tambah satu indikator usaha (transaksi pertama sebagai penyedia jasa atau pedagang)."),
    ("9. Metode", "Pakai backward design (ada satu bulan pemetaan awal), andragogi (peserta dewasa), dan taksonomi Bloom untuk tujuan tiap unit. Kirkpatrick sudah ada."),
    ("10. Topik baru", "Dua JP tentang hak pekerja, kontrak sederhana, dan jaminan sosial, diambil dari 8 JP kompetensi inti. Total JP tidak berubah."),
    ("11. Slogan dan judul", "Ganti slogan berbahasa Inggris dengan kosakata dari berita: \"potensi lokal\", \"pionir bisnis\", \"pelatihan kerja berbasis potensi\"."),
    ("12. Jadwal mulai", "Mulai Januari 2027 ketat bila dana dan PKS belum ada. Tulis jadwal dengan hari H, atau geser mulai ke Februari atau Maret."),
    ("13. Training di Bantul", "Sultan menyebutnya. Cari tahu programnya, lalu tulis posisi kita sebagai pelengkap atau pembanding tanpa menilai pihak lain."),
    ("14. Satu paket", "Dokumen klien memuat satu paket saja. Sekarang ada tiga (Rp185 juta, Rp495 juta, Rp915 juta) ditambah pilot Rp48,9 juta."),
]
cw, gap = 262, 17
for r in range(2):
    items = more[r * 4:(r + 1) * 4]
    hh = max(need(s, cw, t, b, tfs=14, bfs=12.5) for t, b in items)
    for i, (t, b) in enumerate(items):
        card(s, 50 + i * (cw + gap), y, cw, t, b, h=hh, fill=GRAYBG, tfs=14, bfs=12.5, bar=TEAL)
    y += hh + 14
y += 20

y = section(s, y, 3, "Yang sudah baik dan sebaiknya dipertahankan")
keep = ["Aturan: cohort tidak dibuka tanpa minimal 2 mitra pengguna dan persetujuan kampung.",
        "Batas klaim: target bukan hasil, sertifikat internal, penempatan tidak dijamin.",
        "Perlindungan data, dan tidak ada seleksi berdasarkan riwayat kontak dengan penegak hukum.",
        "Ambang keputusan GO, IMPROVE, NO-GO yang jelas, dan tabel risiko dengan kriteria berhenti.",
        "Hitungan JP konsisten: 8 + 8 + 8 + 56 + 20 sama dengan 100 per peserta."]
for k in keep:
    s.circle(66, y + 9, 5, GRN)
    y += s.text(82, y, k, 14, INK, maxw=1060) + 7
y += 20
s.text(50, y, "Label dasar: Koran = isi berita KR 29 Okt 2026. Aturan = aturan repo Sanggabiz. Analisis = pembacaan kami atas dokumen. Semua masukan berstatus usulan untuk diputuskan tim.", 12.5, MUTED, maxw=1100)
y += 50
s.save(OUT, y, "Masukan perbaikan proposal Jogja Berdaya", "Tabel tujuh masukan prioritas tinggi dengan kondisi sekarang, alasan teknis, dan usulan, ditambah tujuh masukan lain dan hal yang sudah baik.")
print("ok", y)
