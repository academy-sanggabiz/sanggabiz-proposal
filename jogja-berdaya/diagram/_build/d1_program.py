import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "01-apa-itu-jogja-berdaya.svg")
s = SVG(1200)
header(s, "Jogja Berdaya: programnya apa?",
       "Warga kampung di Kota Yogyakarta dilatih keterampilan kerja yang dibutuhkan usaha setempat, lalu dibantu mendapat kerja atau penghasilan. Hasilnya dihitung dengan bukti, bukan dengan janji.")

# 1. Siapa terlibat
y = section(s, 140, 1, "Siapa yang terlibat dan apa tugasnya")
who = [
    ("Warga peserta", "20 orang (pilot) atau 90 orang (program penuh). Belajar, lalu mengerjakan proyek nyata.", TEALBG, TEAL),
    ("UMKM mitra", "4 usaha setempat di pilot. Memberi tugas nyata, menilai hasil, dan bisa memakai tenaga peserta.", TEALBG, TEAL),
    ("Sanggabiz Academy", "Pelaksana: seleksi, pelatihan, pendampingan, pengukuran hasil, laporan.", GRAYBG, NAVY),
    ("Pemkot dan kelurahan", "Pengampu wilayah: memvalidasi kampung, menyediakan aula, menghubungkan ke UMKM.", GRAYBG, NAVY),
    ("Polda DIY (Ditbinmas)", "Fasilitator: mengajak warga ikut secara sukarela. Bukan penjamin kerja, bukan pemakai data peserta.", GRAYBG, NAVY),
]
cw, gap, x0 = 208, 15, 50
hh = max(need(s, cw, t, b) for t, b, _, _ in who)
for i, (t, b, f, bar) in enumerate(who):
    card(s, x0 + i * (cw + gap), y, cw, t, b, h=hh, fill=f, bar=bar)
y += hh + 38

# 2. Perjalanan satu peserta
y = section(s, y, 2, "Perjalanan satu peserta di pilot (8 minggu, lalu dicek sampai hari ke 90)")
steps = [
    ("Daftar dan seleksi", "Minggu 1", "Isi formulir. Dicek domisili dan niat ikut.", "Hasil: formulir seleksi"),
    ("Tes awal", "Minggu 2", "Pre-test dan kenalan dengan alur layanan pelanggan.", "Hasil: nilai awal"),
    ("Latihan", "Minggu 3 dan 4", "Layanan pelanggan, WhatsApp Business, spreadsheet, CRM sederhana, konten dan AI.", "Hasil: tugas praktik"),
    ("Uji praktik", "Minggu 5", "Mengerjakan simulasi, dinilai rubrik 100 poin.", "Hasil: portofolio"),
    ("Proyek nyata", "Minggu 6 dan 7", "Mengerjakan tugas untuk salah satu dari 4 UMKM, dibimbing mentor.", "Hasil: kerja dipakai UMKM"),
    ("Cek hasil", "Minggu 8 sampai hari ke 90", "Ada kerja atau penugasan berbayar? Dibuktikan dengan konfirmasi pemberi kerja.", "Hasil: bukti penghasilan"),
]
cw, gap = 160, 28
hh = max(need(s, cw, t, "\n".join([w, d, o])) for t, w, d, o in steps) + 22
for i, (t, w, d, o) in enumerate(steps):
    x = x0 + i * (cw + gap)
    s.rect(x, y, cw, hh, "#fff", TEAL, sw=1.6)
    s.circle(x + 22, y + 22, 13, TEAL)
    s.text(x + 22, y + 15, i + 1, 14, "#fff", True, "middle")
    ty = y + 14
    th = s.text(x + 42, ty, t, 14.5, NAVY, True, maxw=cw - 52)
    yy = y + 14 + max(th, 26) + 4
    yy += s.text(x + 14, yy, w, 12.5, TEAL, True, maxw=cw - 24) + 4
    yy += s.text(x + 14, yy, d, 12.5, INK, maxw=cw - 24) + 6
    s.text(x + 14, y + hh - 34, o, 12.5, NAVY, True, maxw=cw - 24)
    if i < len(steps) - 1:
        s.line(x + cw + 2, y + hh / 2, x + cw + gap - 2, y + hh / 2, MUTED, 2, arrow=True)
y += hh + 12
s.text(50, y, "JP = jam pelajaran. 1 JP = 45 menit. Pilot memakai 36 JP (sama dengan 27 jam belajar). UMKM = usaha mikro, kecil, dan menengah.", 12.5, MUTED, maxw=1100)
y += 40

# 3. Contoh isi latihan
y = section(s, y, 3, "Contoh tugas yang benar-benar dikerjakan peserta (dari silabus jalur digital)")
ex = [
    ("Layanan pelanggan", "Membalas 50 tiket atau chat pelanggan memakai SOP eskalasi."),
    ("Spreadsheet", "Menyusun spreadsheet 50 transaksi dan ringkasan KPI."),
    ("CRM", "Mengelola daftar 20 calon pembeli dan 3 latihan menelepon ulang."),
    ("Konten dan katalog", "Membuat 6 konten dan 3 listing produk jualan."),
]
cw, gap = 262, 17
hh = max(need(s, cw, t, b) for t, b in ex)
for i, (t, b) in enumerate(ex):
    card(s, x0 + i * (cw + gap), y, cw, t, b, h=hh, fill=GRAYBG, bar=BLUE)
y += hh + 14
kh = card(s, x0, y, 1100,
          "Cara UMKM menilai hasilnya",
          "Tiap UMKM memilih satu ukuran sejak awal: waktu respons ke pelanggan, penyelesaian tindak lanjut, atau ketepatan administrasi. Angkanya dicatat sebelum latihan dan dibandingkan lagi di minggu ke 8. Target pilot: ukuran itu membaik minimal 20 persen di sedikitnya 3 dari 4 UMKM.",
          fill=YELBG, stroke=YEL, bar=YEL)
y += kh + 38

# 4. Dua ukuran
y = section(s, y, 4, "Dua ukuran program yang ada di dokumen")
cols = [("", 230), ("Pilot", 430), ("Program penuh", 440)]
rows = [
    ("Jumlah kampung", "1", "3"),
    ("Jumlah peserta", "20 orang", "90 orang (3 kelompok belajar, masing-masing 30)"),
    ("Jalur keterampilan", "1: digital commerce dan customer operations", "3: digital commerce, hospitality, kuliner dan usaha kreatif"),
    ("Jam belajar per peserta", "36 JP", "100 JP"),
    ("Lama", "8 minggu, lalu pelacakan sampai hari ke 90", "6 bulan (Januari sampai Juni 2027, usulan)"),
    ("Biaya (target rancangan)", "Rp48.900.000", "Rp495.000.000"),
    ("Biaya per peserta", "Rp2.445.000", "Rp5.500.000"),
]
xx = x0
rh = 34
s.rect(x0, y, 1100, rh, NAVY, rx=6)
cx = x0
for name, w in cols:
    s.text(cx + 12, y + 9, name, 14, "#fff", True)
    cx += w
y += rh
for i, r in enumerate(rows):
    lines = max(len(wrap(r[1], 13.5, 405)), len(wrap(r[2], 13.5, 415)), 1)
    h = max(34, lines * 18 + 16)
    s.rect(x0, y, 1100, h, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.text(x0 + 12, y + 9, r[0], 13.5, NAVY, True, maxw=210)
    s.text(x0 + 242, y + 9, r[1], 13.5, INK, maxw=405)
    s.text(x0 + 672, y + 9, r[2], 13.5, INK, maxw=415)
    y += h
s.line(x0, y, x0 + 1100, y, LINE, 1)
y += 12
y += s.text(50, y, "Biaya per peserta tidak bisa dibandingkan langsung karena isinya berbeda: program penuh punya 3 jalur, jam belajar lebih banyak, dan pelacakan hasil lebih panjang.", 12.5, MUTED, maxw=1100)
y += 28
s.text(50, y, "Semua angka adalah target rancangan, bukan hasil dan bukan jaminan kerja. Sumber: tiga PDF Jogja Berdaya (22 November 2026), folder sumber/.", 12.5, MUTED, maxw=1100)
y += 40
s.save(OUT, y, "Jogja Berdaya: programnya apa?", "Penjelasan bergambar: pihak yang terlibat, perjalanan satu peserta, contoh tugas, dan perbandingan pilot dengan program penuh.")
print("ok", y)
