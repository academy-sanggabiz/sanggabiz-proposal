import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "07-program-serupa-dan-posisi-pilot.svg")
PURPLE = "#7A5BA6"
s = SVG(1200)
header(s, "Program serupa: cara mereka menjalankan dan posisi pilot kita",
       "Dibandingkan dengan tiga program Plan Indonesia yang kami kerjakan, program Poliran milik Polri, target Kemnaker, dan bukti riset. Label sumber: I = internal Sanggabiz, B = berita, R = riset terbitan.")

SRC = {"I": (TEAL, "#fff"), "B": (MUTED, "#fff"), "R": (PURPLE, "#fff")}
def chip(x, y, k):
    bg, fg = SRC[k]
    s.rect(x, y, 22, 18, bg, None, rx=9)
    s.text(x + 11, y + 3.5, k, 11, fg, True, "middle")

# 1. Enam program
y = section(s, 140, 1, "Enam program pembanding")
progs = [
    ("P1  TechPath 1.0, Bojonegoro", "I", "Plan Indonesia, pelaksana Sanggabiz, Juli 2025 sampai April 2026. 300 daftar, 84 diterima, 56 lulus, 47 bekerja atau mendapat kesempatan kerja. Kelas akhir pekan, sekitar 2 sampai 3 bulan."),
    ("P2  TechPath 2.0, Bojonegoro", "I", "Kontrak Oktober 2026 sampai Juli 2027. 150 peserta, target 100 bekerja. 10 sesi bootcamp 3 jam, proyek di 25 mitra, mentoring 3 bulan setelah kerja. Anggaran Rp433 juta."),
    ("P3  You RISE Retail dan Hospitality", "I", "Plan dan DBS Foundation, Jawa Timur. ToR: 250 peserta, penempatan 50 persen. Draf kami: batch 20 orang, 80 JP dalam 2 minggu penuh, HR mitra ikut menyeleksi."),
    ("P4  Futuremakers YEP", "I", "Plan dan Standard Chartered, termasuk DIY. Kuota 200, target 150 diterima kerja, sekitar Rp1,3 miliar, mentoring 3 bulan. Masih rancangan, hasil nyata belum ada di Drive."),
    ("P5  Poliran (Polri)", "B", "Latih, sertifikasi, salurkan ke perusahaan, pantau setelah kerja, bersama Kemnaker, Disnaker, atau BLK. Diluncurkan nasional 11 November 2026. Banten: 502 dilatih. Angka yang bekerja belum terbit."),
    ("P6  Kemnaker dan BLK", "B", "Target kebekerjaan lulusan 70 persen, pelacakan lulusan paling lambat dua bulan setelah pelatihan. BLKPP DIY membuka pelatihan gratis tujuh bidang pada 2026."),
]
cw, gap = 355, 17.5
for r in range(2):
    row = progs[r * 3:(r + 1) * 3]
    hh = max(need(s, cw - 30, t, b, tfs=14, bfs=12.5) for t, _, b in row) + 4
    for c, (t, k, b) in enumerate(row):
        x = 50 + c * (cw + gap)
        s.rect(x, y, cw, hh, GRAYBG, LINE, rx=8)
        s.rect(x, y, 6, hh, TEAL if k == "I" else MUTED, None, rx=3)
        th = s.text(x + 18, y + 12, t, 14, NAVY, True, maxw=cw - 60)
        chip(x + cw - 34, y + 10, k)
        s.text(x + 18, y + 12 + th + 6, b, 12.5, INK, maxw=cw - 34)
    y += hh + 14
y += 22

# 2. Persen bekerja
y = section(s, y, 2, "Berapa persen peserta yang ditargetkan atau tercatat bekerja")
bars = [
    ("Futuremakers YEP", 75, "target", "75 persen"),
    ("Kemnaker, nasional", 70, "target", "70 persen"),
    ("TechPath 2.0", 67, "target", "67 persen (100 dari 150)"),
    ("TechPath 1.0", 56, "hasil", "56 persen (47 dari 84 diterima)"),
    ("You RISE Retail, ToR", 50, "target", "50 persen"),
    ("Jogja Berdaya penuh", 50, "target", "50 persen (30 dari 60 jalur kerja)"),
    ("Prakerja, survei pelaksana", 26, "hasil", "26 persen (dilaporkan peserta, termasuk usaha)"),
    ("Pilot Jogja Berdaya", 20, "pilot", "20 persen (4 dari 20)"),
]
bx, bw = 290, 520
for name, v, kind, lab in bars:
    s.text(50, y + 6, name, 13.5, INK, kind == "pilot", maxw=230)
    w = bw * v / 100
    if kind == "hasil":
        s.rect(bx, y, w, 26, TEAL, None, rx=4)
    elif kind == "target":
        s.rect(bx, y, w, 26, "#D6EEF0", TEAL, rx=4, sw=1.2)
    else:
        s.rect(bx, y, w, 26, YEL, "#B8860B", rx=4, sw=1.5)
    s.text(bx + w + 10, y + 6, lab, 13, INK, kind == "pilot")
    y += 34
y += 6
s.rect(50, y, 18, 14, TEAL, None, rx=3); s.text(74, y, "hasil nyata atau dilaporkan", 12, MUTED)
s.rect(290, y, 18, 14, "#D6EEF0", TEAL, rx=3); s.text(314, y, "target", 12, MUTED)
s.rect(380, y, 18, 14, YEL, "#B8860B", rx=3); s.text(404, y, "pilot kita", 12, MUTED)
y += 26
y += s.text(50, y, "Definisi \"bekerja\" tidak sama di semua program. P1 menulis \"bekerja atau mendapat kesempatan kerja\" dan belum dipisah berbayar atau tidak. Pilot kita mensyaratkan bukti berbayar dari pihak luar.", 12.5, MUTED, maxw=1100)
y += 34

# 3. Biaya
y = section(s, y, 3, "Biaya per penempatan dan per peserta (Rp juta)")
cost = [
    ("TechPath 1.0", 3.72, 2.08, "hasil", "47 bekerja"),
    ("TechPath 2.0", 4.33, 2.89, "target", "100 target"),
    ("Futuremakers YEP", 8.67, 6.5, "target", "150 target"),
    ("Jogja Berdaya penuh", 11.0, 5.5, "target", "45 target (kerja dan usaha)"),
    ("Pilot, bila 4 bekerja", 12.23, 2.445, "pilot", "target saat ini"),
    ("Pilot, bila 8 bekerja", 6.11, 2.445, "pilot2", "usulan"),
    ("Pilot, bila 10 bekerja", 4.89, 2.445, "pilot2", ""),
]
s.text(50, y, "Program", 12.5, MUTED, True); s.text(260, y, "Biaya per penempatan", 12.5, MUTED, True)
s.text(800, y, "Per peserta", 12.5, MUTED, True); s.text(910, y, "Dasar penempatan", 12.5, MUTED, True)
y += 24
sc = 450 / 13
for name, v, pp, kind, base in cost:
    s.text(50, y + 6, name, 13.5, INK, kind != "hasil" and kind.startswith("pilot"), maxw=200)
    w = v * sc
    fill = {"hasil": TEAL, "target": "#D6EEF0", "pilot": YEL, "pilot2": "#FFE9A8"}[kind]
    stroke = {"hasil": None, "target": TEAL, "pilot": "#B8860B", "pilot2": "#B8860B"}[kind]
    s.rect(260, y, w, 26, fill, stroke, rx=4, sw=1.2)
    s.text(260 + w + 8, y + 6, f"{v:.1f}".replace(".", ","), 13, INK, True)
    s.text(800, y + 6, "2,445" if abs(pp - 2.445) < 1e-9 else (f"{pp:.2f}".replace(".", ",") if pp < 3 else f"{pp:.1f}".replace(".", ",")), 13, INK)
    s.text(910, y + 6, base, 12.5, MUTED, maxw=240)
    y += 34
y += 6
y += s.text(50, y, "Biaya per peserta pilot sebanding dengan TechPath. Biaya per penempatan baru sebanding bila capaiannya 8 sampai 10, bukan 4. Angka P1 memakai nilai proyek di daftar klien perusahaan (Rp175 juta), cakupannya belum dipastikan.", 12.5, MUTED, maxw=1100)
y += 34

# 4. Matriks
y = section(s, y, 4, "Cara kerja: apa yang dilakukan program lain dan pilot kita")
L, C, SYM = 50, [400, 590, 780, 970], 0
cols = ["TechPath 2.0", "You RISE Retail", "Poliran", "Pilot kita"]
s.rect(50, y, 1100, 32, NAVY, rx=6)
s.text(62, y + 8, "Praktik", 13.5, "#fff", True)
for c, t in zip(C, cols):
    s.text(c, y + 8, t, 13.5, "#fff", True)
y += 32
Y_, S_, T_, Q_ = "ya", "sebagian", "tidak", "tanya"
rows = [
    ("Pemberi kerja terlibat sebelum pelatihan", [(S_, "25 mitra, belum posisi"), (Y_, "HR ikut seleksi"), (S_, "MoU perusahaan"), (S_, "4 UMKM tanda brief")]),
    ("Penempatan harus berbayar dan berbukti", [(Y_, "berbayar, surat bukti"), (S_, "OJT, magang, kerja"), (Q_, "belum diketahui"), (S_, "berbayar, tanpa nilai")]),
    ("Rekrut lebih banyak dari target", [(Y_, "175 untuk 150"), (Y_, "30 untuk 20"), (Q_, "belum diketahui"), (T_, "20 untuk 20")]),
    ("Pelacakan bertahan kerja", [(Y_, "bulan 1 dan 3"), (S_, "1 bulan"), (Y_, "pemantauan diminta"), (T_, "sampai hari 90")]),
    ("Pendampingan setelah kerja", [(Y_, "3 bulan"), (S_, "1 bulan"), (S_, "usaha (Banten)"), (T_, "tidak ada")]),
    ("Biaya peserta ditanggung", [(Y_, "tempat, konsumsi, transport"), (S_, "BPJS 1 bulan"), (Q_, "belum diketahui"), (S_, "aula, konsumsi gabungan")]),
    ("Sertifikasi kompetensi", [(S_, "sertifikat lulus"), (Y_, "ToR: sertifikasi"), (Y_, "lulusan bersertifikat"), (T_, "sertifikat internal")]),
    ("Mitra pelatihan pemerintah", [(Y_, "Disnaker dan BLK"), (Y_, "TVET, PPKD, BLK"), (Y_, "Kemnaker, Disnaker"), (S_, "hanya di strategis")]),
    ("Ukur pendapatan atau mutu kerja", [(S_, "patokan UMK"), (T_, "tidak"), (Q_, "belum diketahui"), (T_, "tidak")]),
]
def dot(cx_, cy_, kind):
    if kind == "ya":
        s.circle(cx_, cy_, 8, GRN)
    elif kind == "sebagian":
        s.circle(cx_, cy_, 8, YEL, "#B8860B")
    elif kind == "tidak":
        s.circle(cx_, cy_, 8, "#fff", MUTED)
    else:
        s.circle(cx_, cy_, 8, "#fff", MUTED)
        s.text(cx_, cy_ - 7, "?", 12, MUTED, True, "middle")
for i, (lab, cells) in enumerate(rows):
    h = 40
    s.rect(50, y, 1100, h, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.rect(970 - 8, y, 190, h, "#FFF6D6", None, rx=0)
    s.text(62, y + 12, lab, 13, INK, True, maxw=320)
    for c, (k, note) in zip(C, cells):
        dot(c + 8, y + h / 2, k)
        s.text(c + 24, y + 12, note, 11.5, INK, maxw=160)
    y += h
y += 12
lx = 50
for k, t in [("ya", "ya"), ("sebagian", "sebagian"), ("tidak", "tidak"), ("tanya", "belum diketahui (sumber tidak memuat)")]:
    dot(lx + 8, y + 8, k)
    s.text(lx + 22, y + 2, t, 12, MUTED)
    lx += 40 + len(t) * 7
y += 34
y += s.text(50, y, "Kolom TechPath 2.0 dan You RISE dari dokumen internal. Kolom Poliran dari ringkasan hasil pencarian berita dan perlu dicek ke sumber aslinya. Penilaian sebagian, ya, dan tidak adalah bacaan kami.", 12.5, MUTED, maxw=1100)
y += 34

# 5. Riset
y = section(s, y, 5, "Bukti riset yang perlu diingat saat menetapkan target")
res = [
    ("Pelatihan singkat sering tidak mengubah peluang kerja", "Tinjauan McKenzie (2017) atas banyak evaluasi: banyak yang tidak menemukan dampak signifikan pada kerja atau penghasilan."),
    ("Program per sektor dekat pemberi kerja menaikkan penghasilan", "Empat studi acak: naik 11 sampai 40 persen. Ciri bersama: seleksi awal, teknis dan soft skill, hubungan pemberi kerja, layanan pendukung."),
    ("Hasilnya berbeda antar penyelenggara", "WorkAdvance 10 tahun: satu penyelenggara naik 32 persen, tiga lainnya tidak berdampak. Rancangan dan pelaksanaan menentukan."),
    ("Pendapatan lebih peka daripada status kerja", "Studi UGM atas Prakerja: lebih efektif menaikkan pendapatan daripada peluang kerja. Program per sektor: pekerjaan lebih baik, bukan lebih banyak orang bekerja."),
]
cw, gap = 262, 17
hh = max(need(s, cw, t, b, tfs=13.5, bfs=12) for t, b in res)
for i, (t, b) in enumerate(res):
    card(s, 50 + i * (cw + gap), y, cw, t, b, h=hh, fill="#F1ECF7", stroke=PURPLE, tfs=13.5, bfs=12, bar=PURPLE)
y += hh + 24

# Kesimpulan
y += card(s, 50, y, 1100, "Bacaan teknis kami",
          "1. Arah pilot sudah benar, tetapi lebih ringan dari pembanding di empat hal: keterlibatan pemberi kerja sebelum pelatihan, cadangan rekrutmen, pelacakan bertahan kerja, dan pendampingan setelah kerja.   2. Target 20 persen belum punya dasar. Ia tidak diturunkan dari angka pembanding dan tidak dari jumlah posisi yang sudah terkunci.   3. Bila Poliran masuk DIY, penempatan terverifikasi akan menjadi bahasa bersama Polda. Pilot perlu siap berbicara dengan ukuran itu.",
          fill=TEALBG, stroke=TEAL, bar=TEAL, tfs=15, bfs=13) + 20
s.text(50, y, "Sumber lengkap dan batas riset ada di 05-RISET-PROGRAM-SERUPA.md. Angka target adalah target, bukan hasil.", 12.5, MUTED, maxw=1100)
y += 46
s.save(OUT, y, "Program serupa dan posisi pilot Jogja Berdaya",
       "Perbandingan enam program, persen bekerja, biaya per penempatan, matriks praktik, dan bukti riset.")
print("ok", y)
