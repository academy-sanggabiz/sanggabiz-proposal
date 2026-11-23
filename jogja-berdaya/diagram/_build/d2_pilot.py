import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "02-alur-pilot-8-minggu.svg")
s = SVG(1200)
header(s, "Pilot 8 minggu: kegiatan, bukti, dan titik keputusan",
       "Pilot dibuat untuk menjawab satu pertanyaan: apakah keterampilan warga dibutuhkan usaha setempat dan menghasilkan penghasilan nyata? Jawabannya dicek di lima titik (G1 sampai G5).")

X0, LW, CW = 30, 110, 114          # kiri, lebar label, lebar kolom
cols = ["Minggu 1", "Minggu 2", "Minggu 3", "Minggu 4", "Minggu 5", "Minggu 6", "Minggu 7", "Minggu 8", "Hari ke 90"]
def cx(i): return X0 + LW + i * CW
y = 140
s.rect(X0 + LW, y, CW * 9, 32, TEAL, rx=6)
for i, c in enumerate(cols):
    s.text(cx(i) + CW / 2, y + 8, c, 13, "#fff", True, "middle")
    if i:
        s.line(cx(i), y + 32, cx(i), 0, LINE, 1)  # placeholder, diganti di bawah
s.p = [p for p in s.p if 'y2="0.0"' not in p]
y += 44

def row(label, items, y, fill, fs=12.3, minh=60):
    hs = [s.height_of(t, fs, CW * span - 20) + 18 for (_, span, t) in items]
    h = max(hs + [minh])
    s.text(X0 + 4, y + 8, label, 13.5, NAVY, True, maxw=LW - 10)
    for (col, span, t) in items:
        s.rect(cx(col) + 3, y, CW * span - 6, h, fill, LINE, rx=6)
        s.text(cx(col) + 10, y + 8, t, fs, INK, maxw=CW * span - 20)
    return h

h1 = row("Kegiatan", [
    (0, 1, "Pilih kampung. Rekrut 20 warga dan 4 UMKM. Catat kondisi awal."),
    (1, 1, "UMKM tanda tangan brief. Tes awal. Modul 1."),
    (2, 2, "Latihan modul 2 sampai 4: layanan pelanggan, WhatsApp Business, CRM, spreadsheet, konten."),
    (4, 1, "Uji praktik. Presentasi 20 portofolio."),
    (5, 2, "Proyek nyata di 4 UMKM, dibimbing mentor, KPI dicatat."),
    (7, 1, "Evaluasi dan showcase."),
    (8, 1, "Cek kerja atau tugas berbayar."),
], y, TEALBG)
y += h1 + 10
h2 = row("Bukti yang disimpan", [
    (0, 1, "20 formulir, 4 brief kebutuhan, data awal."),
    (1, 1, "Project brief yang disetujui."),
    (2, 2, "Catatan kemajuan dan tugas praktik."),
    (4, 1, "Hasil uji dan rubrik tiap orang."),
    (5, 2, "Hasil kerja yang dipakai UMKM, log KPI."),
    (7, 1, "Scorecard dan laporan 8 minggu."),
    (8, 1, "Slip, kontrak, atau konfirmasi."),
], y, GRAYBG)
y += h2 + 14

# Jalur gerbang
s.text(X0 + 4, y + 8, "Titik cek", 13.5, NAVY, True, maxw=LW - 10)
s.line(cx(0) + 10, y + 22, cx(9) - 10, y + 22, MUTED, 2)
gates = [(1, ["G1"]), (4, ["G3"]), (7, ["G2", "G4"]), (8, ["G5"])]
for col, ids in gates:
    for k, g in enumerate(ids):
        off = (k - (len(ids) - 1) / 2) * 38
        px = cx(col) + CW / 2 + off
        s.diamond(px, y + 22, 17, NAVY if g != "G5" else RED)
        s.text(px, y + 15, g, 11.5, "#fff", True, "middle")
y += 58

# Tabel gerbang
y = section(s, y, 1, "Arti tiap titik cek (semua angka adalah target, bukan jaminan)")
rows = [
    ("G1", "Demand", "Apakah usaha benar-benar membutuhkan?", "Minimal 4 UMKM menandatangani brief dan menyerahkan data awal.", "Minggu 2"),
    ("G3", "Competence", "Apakah peserta bisa mengerjakan?", "Minimal 14 dari 20 lulus uji praktik (skor 75 dari 100 atau lebih).", "Minggu 5"),
    ("G2", "Completion", "Apakah peserta menyelesaikan program?", "Minimal 16 dari 20 hadir 80 persen atau lebih dan menyelesaikan proyek.", "Minggu 8"),
    ("G4", "Value", "Apakah UMKM terbantu?", "Minimal 3 dari 4 UMKM memakai hasilnya. KPI yang dipilih membaik 20 persen atau lebih.", "Minggu 8"),
    ("G5", "Paid outcome", "Apakah ada penghasilan nyata?", "Minimal 4 dari 20 mendapat kerja atau tugas berbayar dari pihak luar, terverifikasi, tanpa subsidi pilot.", "Hari ke 90"),
]
s.rect(50, y, 1100, 32, NAVY, rx=6)
for n, hx in [("Titik", 62), ("Nama", 100), ("Pertanyaan yang dijawab", 225), ("Ukuran lulus", 450), ("Kapan", 1000)]:
    s.text(hx, y + 8, n, 13.5, "#fff", True)
y += 32
for i, r in enumerate(rows):
    lines = max(len(wrap(r[3], 13.5, 535)), len(wrap(r[2], 13.5, 205)))
    h = max(38, lines * 18 + 18)
    s.rect(50, y, 1100, h, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.diamond(70, y + h / 2, 14, RED if r[0] == "G5" else NAVY)
    s.text(70, y + h / 2 - 7, r[0], 10.5, "#fff", True, "middle")
    s.text(100, y + 10, r[1], 13.5, NAVY, True, maxw=115)
    s.text(225, y + 10, r[2], 13.5, INK, maxw=205)
    s.text(440, y + 10, r[3], 13.5, INK, maxw=535)
    s.text(1000, y + 10, r[4], 13.5, INK, True, maxw=140)
    y += h
y += 34

# Corong
y = section(s, y, 2, "Dari 20 peserta, berapa yang ditargetkan sampai di tiap tahap")
fun = [("Mendaftar dan diterima", 20, "20", NAVY), ("Menyelesaikan program (G2)", 16, "minimal 16", BLUE),
       ("Lulus uji praktik (G3)", 14, "minimal 14", TEAL), ("Kerja atau tugas berbayar (G5)", 4, "minimal 4", RED)]
maxw = 560
for name, n, lab, colr in fun:
    w = maxw * n / 20
    s.text(50, y + 7, name, 14, INK, True, maxw=300)
    s.rect(360, y, w, 30, colr, None, rx=5)
    s.text(360 + w + 10, y + 7, f"{lab} orang ({n * 5} persen)", 13.5, INK, True)
    y += 40
y += 4
y += s.text(50, y, "Lulus uji praktik (minggu 5) terjadi sebelum penyelesaian program (minggu 8). Urutan di atas disusun menurut besar targetnya, bukan menurut waktu.", 12.5, MUTED, maxw=1100)
y += 30

# Keputusan
y = section(s, y, 3, "Keputusan akhir di hari ke 90")
dec = [
    ("GO: layak diuji lebih besar", "Kelima titik cek tercapai dan tidak ada masalah integritas serius. Perluasan baru boleh diajukan setelah pihak pembiaya mengonfirmasi.", GRNBG, GRN),
    ("IMPROVE: perbaiki dan uji ulang", "Tepat satu titik meleset tipis (minimal 80 persen dari target). Minimal 2 hasil berbayar ada. Perbaikan paling lama 30 hari.", YELBG, YEL),
    ("NO-GO: rancang ulang", "Dua titik atau lebih gagal, tidak ada hasil berbayar, atau ada pelanggaran integritas atau perlindungan peserta yang berat.", REDBG, RED),
]
cw, gap = 355, 17.5
hh = max(need(s, cw, t, b) for t, b, _, _ in dec)
for i, (t, b, f, c) in enumerate(dec):
    card(s, 50 + i * (cw + gap), y, cw, t, b, h=hh, fill=f, stroke=c, bar=c)
y += hh + 14
y += card(s, 50, y, 1100, "Catatan: dokumen sumber belum seragam soal batas waktu pelacakan",
          "Deck pilot menulis \"8 minggu delivery + 30 hari outcome tracking\" dan \"D+30\", tetapi titik cek G5 dan keputusan memakai hari ke 90. Gambar ini memakai hari ke 90. Tim perlu memutuskan satu definisi (lihat masukan nomor 7).",
          fill=YELBG, stroke=YEL, bar=YEL) + 24
s.text(50, y, "Sumber: Sanggabiz PoldaDIY Pilot 49Juta (deck dan executive proposal), 22 November 2026.", 12.5, MUTED, maxw=1100)
y += 40
s.save(OUT, y, "Alur pilot 8 minggu Jogja Berdaya", "Garis waktu minggu ke minggu, bukti yang disimpan, lima titik cek G1 sampai G5, corong peserta, dan aturan keputusan hari ke 90.")
print("ok", y)
