import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "08-pilot-versi-realistis.svg")
PURPLE = "#7A5BA6"
s = SVG(1200)
header(s, "Pilot Jogja Berdaya versi lebih realistis",
       "Apa yang diubah dari rancangan sekarang, dibandingkan dengan program serupa, dan alasannya. Semua angka usulan perlu diputuskan tim. Dasar angka ada di 05-RISET-PROGRAM-SERUPA.md.")

TAGC = {"BARU": (PURPLE, "#fff"), "UBAH": (YEL, INK), "TAMBAH": (BLUE, "#fff"), "TETAP": (GRN, "#fff")}
def tag(x, y, name):
    bg, fg = TAGC[name]
    w = 16 + len(name) * 7.4
    s.rect(x, y, w, 20, bg, None, rx=10)
    s.text(x + w / 2, y + 4.5, name, 11, fg, True, "middle")
    return w

# 1. Alur
y = section(s, 140, 1, "Alur pilot yang disarankan")
steps = [
    ("0. Kunci pemberi kerja", "8 sampai 10 pemberi kerja. Minimal 4 mengunci posisi atau tugas berbayar tertulis sebelum rekrutmen.", "BARU"),
    ("1. Asesmen 14 hari", "Pilih kampung dari potensinya, cocokkan dengan permintaan kerja, baru tetapkan jalur.", "UBAH"),
    ("2. Rekrut dan seleksi", "Daftarkan 28 sampai 30 orang. Seleksi dua tahap, UMKM ikut wawancara singkat.", "UBAH"),
    ("3. Latih dan uji", "36 JP seperti sekarang, dengan tujuan terukur dan uji praktik.", "TETAP"),
    ("4. Praktik terbimbing", "Tugas nyata di pemberi kerja, jam dibatasi, dinilai pemberi kerja.", "UBAH"),
    ("5. Lacak 30, 60, 90 hari", "Verifikasi tiga pihak, retensi, pendapatan sebelum dan sesudah.", "TAMBAH"),
]
cw, gap = 160, 28
hh = max(need(s, cw, t, d, tfs=13.5, bfs=12) for t, d, _ in steps) + 30
for i, (t, d, tg) in enumerate(steps):
    x = 50 + i * (cw + gap)
    stroke = {"BARU": PURPLE, "UBAH": YEL, "TAMBAH": BLUE, "TETAP": GRN}[tg]
    fill = {"BARU": "#F1ECF7", "UBAH": YELBG, "TAMBAH": "#E8F1FB", "TETAP": GRNBG}[tg]
    s.rect(x, y, cw, hh, fill, stroke, rx=8, sw=1.6)
    th = s.text(x + 12, y + 12, t, 13.5, NAVY, True, maxw=cw - 24)
    s.text(x + 12, y + 12 + th + 6, d, 12, INK, maxw=cw - 24)
    tag(x + 12, y + hh - 28, tg)
    if i < len(steps) - 1:
        s.line(x + cw + 2, y + hh / 2, x + cw + gap - 2, y + hh / 2, MUTED, 2, arrow=True)
y += hh + 14
y += card(s, 50, y, 1100, "Keputusan di hari ke 90 tetap tiga kemungkinan: GO, IMPROVE, NO-GO",
          "Ambang GO diubah mengikuti target baru di tabel di bawah. GO tetap berarti layak diuji lebih besar, bukan izin perluasan.",
          fill=GRAYBG, bar=MUTED, tfs=13.5, bfs=12.5) + 36

# 2. Corong
y = section(s, y, 2, "Hitungan corong peserta (perkiraan, bukan janji)")
fun = [
    ("Pendaftar yang perlu dijangkau", "sekitar 100", 100, "#C9D3DA", "Bila rasio diterima seperti TechPath 1.0 (84 dari 300 daftar)"),
    ("Diterima dan mulai", "28 sampai 30", 30, NAVY, "Cadangan agar cukup bila sebagian berhenti"),
    ("Menyelesaikan program", "sekitar 20", 20, BLUE, "Rencana 70 persen selesai, TechPath 1.0 mencatat 67 persen"),
    ("Kerja atau tugas berbayar, terverifikasi", "8 (target), minimal 5", 8, YEL, "40 persen dari yang selesai. Ambang GO 25 persen (5 dari 20)"),
]
mx = 220
for name, val, n, colr, note in fun:
    th_ = s.text(50, y + 7, name, 13.5, INK, True, maxw=300)
    w = mx * n / 100
    s.rect(380, y, w, 28, colr, "#B8860B" if colr == YEL else None, rx=4)
    s.text(380 + w + 10, y + 7, val, 13.5, INK, True)
    s.text(790, y + 7, note, 12, MUTED, maxw=360)
    y += max(44, th_ + 20)
y += 4
y += s.text(50, y, "Angka 40 persen adalah usulan kami. Pembanding: TechPath 1.0 mencatat 56 persen dari yang diterima, target TechPath 2.0 67 persen, ToR You RISE 50 persen. Definisi dan hasil program lain tidak sama dengan definisi ketat pilot ini.", 12.5, MUTED, maxw=1100)
y += 36

# 3. Tabel parameter
y = section(s, y, 3, "Parameter: sekarang, pembanding, usulan")
rows = [
    ("Pemberi kerja", "4 UMKM menandatangani brief", "TechPath 2.0: 25 mitra untuk 100 penempatan. You RISE: HR menyeleksi dan memberi surat penawaran", "8 sampai 10 pemberi kerja, minimal 4 mengunci posisi atau tugas berbayar sebelum rekrutmen", "BARU"),
    ("Rekrutmen", "20 peserta, tanpa cadangan", "TechPath 1.0: 300 daftar, 84 diterima, 56 lulus. TechPath 2.0: 175 untuk 150", "28 sampai 30 peserta, seleksi dua tahap", "UBAH"),
    ("Penyelesaian", "16 dari 20 (80 persen)", "TechPath 1.0: 67 persen dari yang diterima", "Rencanakan 70 persen, jumlah rekrutan menyesuaikan", "UBAH"),
    ("Arti kerja berbayar", "\"Kerja atau tugas berbayar\", tanpa nilai", "Plan: berbayar, patokan upah minimum, bukti tertulis, magang tanpa bayar tidak dihitung. UMK Kota Yogyakarta 2026 Rp2.827.593", "Penuh waktu minimal UMK. Paruh waktu dan lepas bila penghasilan tercatat dan berbukti. [ISI TIM: batas minimal]", "UBAH"),
    ("Target penempatan", "4 dari 20 (20 persen)", "Pembanding 50 sampai 75 persen. Hasil nyata TechPath 1.0: 56 persen", "8 dari 20 (40 persen), ambang GO 5 dari 20", "UBAH"),
    ("Pelacakan", "Hari ke 30 atau hari ke 90", "Rancangan TechPath 2.0: retensi bulan 1 dan 3, tiga pihak. Kemnaker: pelacakan maksimal dua bulan", "Hari ke 30, 60, 90 dengan verifikasi peserta, pemberi kerja, dan supervisor", "TAMBAH"),
    ("Pendapatan", "Tidak diukur", "Studi Prakerja dan program per sektor: pendapatan lebih peka daripada status kerja", "Pendapatan sebelum dan hari ke 90, dilaporkan sebagai data", "TAMBAH"),
    ("Dukungan peserta", "Tidak disebut. Konsumsi dan transport di baris gabungan", "Plan menanggung tempat, konsumsi, transport. Subsidi transport saja efeknya cepat hilang (studi Addis Ababa)", "Bantuan seperlunya dan jadwal sore atau akhir pekan. [ISI TIM: bantuan transport dan konsumsi]", "UBAH"),
    ("Manajemen program", "Rp6,0 juta untuk sekitar lima bulan", "TechPath 2.0: koordinator Rp6,5 juta per bulan, petugas lapangan Rp3,5 juta per bulan", "Hitung ulang menurut bulan kerja nyata", "UBAH"),
    ("Peran Polda", "Fasilitator ajakan warga", "Poliran: pelatihan, sertifikasi, penyaluran, pemantauan, bersama Kemnaker, Disnaker, BLK", "Konfirmasi ke Ditbinmas apakah Polda DIY menjalankan Poliran. Bila ya, posisikan sebagai pelaksana teknis", "UBAH"),
    ("Sertifikasi", "Sertifikat internal", "Poliran: lulusan bersertifikat. ToR You RISE: sertifikasi kompetensi", "Tetap internal. Jajaki uji kompetensi lewat BBPVP atau BLKPP bila ada dana. Jangan dijanjikan", "TETAP"),
]
cx = [50, 190, 410, 780]
cwid = [135, 215, 365, 330]
s.rect(50, y, 1100, 32, NAVY, rx=6)
for t, x in [("Parameter", 62), ("Sekarang", 202), ("Pembanding", 422), ("Usulan", 792), ("Ubah", 1076)]:
    s.text(x, y + 8, t, 13.5, "#fff", True)
y += 32
for i, (p, now, comp, prop, tg) in enumerate(rows):
    h = max(s.height_of(p, 13, 120, True), s.height_of(now, 12.5, 200), s.height_of(comp, 12.5, 350), s.height_of(prop, 12.5, 270)) + 20
    s.rect(50, y, 1100, h, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.rect(775, y, 375, h, "#FFFBEA", None, rx=0)
    s.text(62, y + 10, p, 13, NAVY, True, maxw=120)
    s.text(202, y + 10, now, 12.5, INK, maxw=200)
    s.text(422, y + 10, comp, 12.5, INK, maxw=350)
    s.text(792, y + 10, prop, 12.5, INK, maxw=270)
    tag(1076, y + 8, tg)
    y += h
y += 10
y += s.text(50, y, "Kolom Ubah: BARU, UBAH, TAMBAH, TETAP mengikuti arti di gambar alur di atas. Alur dan tabel memuat perubahan yang sama.", 12.5, MUTED, maxw=1100)
y += 30

# 4. Biaya
y = section(s, y, 4, "Satu hal biaya yang ikut berubah")
y += card(s, 50, y, 1100, "Biaya per penempatan turun bila capaian naik, bukan bila baris dipotong",
          "Anggaran pilot Rp48.900.000 dibagi 4 penempatan menjadi Rp12,2 juta per penempatan. Dibagi 8 menjadi Rp6,1 juta, dibagi 10 menjadi Rp4,9 juta. Pembanding: TechPath 1.0 Rp3,7 juta, TechPath 2.0 Rp4,3 juta (target), Futuremakers YEP Rp8,7 juta (target). Baris manajemen program dan pendampingan perlu dihitung ulang, dan baris Fee 10 persen menggantikan baris Contingency (lihat gambar 04).",
          fill=YELBG, stroke=YEL, bar=YEL, tfs=14, bfs=13) + 36

# 5. Keputusan tim
y = section(s, y, 5, "Yang perlu diputuskan tim sebelum angka usulan dipakai")
dec = [
    ("Target penempatan", "Jadi 8 dari 20 atau tetap 4? Putuskan setelah melihat berapa posisi yang bisa dikunci pemberi kerja."),
    ("Batas minimal kerja lepas", "Berapa penghasilan bulanan yang dihitung berhasil untuk kerja paruh waktu atau lepas?"),
    ("Bantuan peserta", "Ada atau tidak bantuan transport dan konsumsi, dan dari mana dananya."),
    ("Peran Polda dan Poliran", "Tanyakan ke Ditbinmas Polda DIY apakah Poliran akan dijalankan di DIY."),
    ("Jumlah pemberi kerja", "Siapa saja 8 sampai 10 pemberi kerja yang bisa dihubungi sebelum rekrutmen."),
]
cw, gap = 207, 16
hh = max(need(s, cw, t, d, tfs=13.5, bfs=12.5) for t, d in dec) + 4
for i, (t, d) in enumerate(dec):
    x = 50 + i * (cw + gap)
    s.rect(x, y, cw, hh, YELBG, YEL, rx=8, sw=1.5)
    th = s.text(x + 14, y + 14, t, 13.5, NAVY, True, maxw=cw - 28)
    s.text(x + 14, y + 14 + th + 8, d, 12.5, INK, maxw=cw - 28)
y += hh + 26
s.text(50, y, "Angka usulan adalah usulan kami dari perbandingan, bukan temuan. Pembanding Poliran dan Kemnaker berasal dari ringkasan hasil pencarian berita dan perlu dicek ke sumber aslinya.", 12.5, MUTED, maxw=1100)
y += 46
s.save(OUT, y, "Pilot Jogja Berdaya versi lebih realistis",
       "Alur pilot yang disarankan, hitungan corong peserta, tabel parameter dengan pembanding dan usulan, dan keputusan tim.")
print("ok", y)
