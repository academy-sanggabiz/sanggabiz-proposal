import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "06-ide-umum-alur-sekarang-dan-disarankan.svg")
PURPLE = "#7A5BA6"
s = SVG(1200)
header(s, "Ide umum proposal: alur sekarang dan alur disarankan",
       "Bukan soal detail bagian, tetapi soal ide besarnya: apakah pembaca yang berbeda akan menangkap hal yang sama? Nomor kuning menandai titik yang bisa disalahpahami. Penjelasannya ada di bawah.")

TAGC = {"BARU": (PURPLE, "#fff"), "UBAH": (YEL, INK), "TAMBAH": (BLUE, "#fff"), "TETAP": (GRN, "#fff")}

def tag(x, y, name):
    bg, fg = TAGC[name]
    w = 16 + len(name) * 7.4
    s.rect(x, y, w, 20, bg, None, rx=10)
    s.text(x + w / 2, y + 4.5, name, 11, fg, True, "middle")

def mark(cx_, cy_, n):
    s.circle(cx_, cy_, 13, YEL, "#B8860B")
    s.text(cx_, cy_ - 7.5, n, 13, INK, True, "middle")

# 1. Identitas
y = section(s, 140, 1, "Ide dalam satu kalimat: sekarang tiga identitas, sebaiknya satu")
hats = [("Pelatihan kerja", "Dibaca Disnaker dan Pemkot: program pelatihan seperti yang sudah ada."),
        ("Pemberdayaan ekonomi warga", "Dibaca Bappeda dan calon pendana CSR: program usaha dan UMKM."),
        ("Kemitraan polisi dan masyarakat", "Dibaca Polda: program Polmas dengan Bhabinkamtibmas.")]
cw = 214
hh = max(need(s, cw, t, b, tfs=13.5, bfs=12) for t, b in hats)
s.text(50, y - 2, "Sekarang: pembaca berbeda menangkap hal berbeda", 13.5, MUTED, True)
yy = y + 22
for i, (t, b) in enumerate(hats):
    card(s, 50, yy + i * (hh + 10), cw, t, b, h=hh, fill=GRAYBG, tfs=13.5, bfs=12, bar=MUTED)
left_h = 3 * hh + 20
box_x = 50 + cw + 50
s.line(50 + cw + 6, yy + left_h / 2, box_x - 6, yy + left_h / 2, MUTED, 3, arrow=True)
bw = 1150 - box_x
s.rect(box_x, yy, bw, left_h, TEALBG, TEAL, rx=8, sw=1.6)
s.rect(box_x, yy, 6, left_h, TEAL, None, rx=3)
s.text(box_x + 18, yy + 12, "Disarankan: satu kalimat definisi di halaman pertama", 14.5, NAVY, True, maxw=bw - 36)
ty = yy + 40
ty += s.text(box_x + 18, ty, "Jogja Berdaya adalah pelatihan kerja berbasis potensi kampung di Kota Yogyakarta. Warga dilatih keterampilan yang dibutuhkan usaha setempat, lalu diukur apakah muncul kerja atau penghasilan nyata. Dimulai dari pilot, diperluas hanya bila terbukti.", 13.5, INK, maxw=bw - 36) + 12
s.text(box_x + 18, ty, "Program ini bukan:", 13, NAVY, True)
ty += 22
for t in ["program keamanan atau penegakan hukum", "pengganti pelatihan Disnaker dan BLK", "sertifikasi nasional atau jaminan kerja"]:
    s.circle(box_x + 26, ty + 8, 4, TEAL)
    ty += s.text(box_x + 38, ty, t, 13, INK, maxw=bw - 60) + 4
mark(box_x + bw - 22, yy + 22, "1")
y = yy + left_h + 38

# 2. Alur
y = section(s, y, 2, "Alur program: sekarang (kiri) dan yang disarankan (kanan)")
LX, LW, RX, RW = 50, 390, 492, 468
s.text(LX, y, "Alur sekarang, seperti terbaca di dokumen", 14, MUTED, True)
s.text(RX, y, "Alur yang disarankan", 14, TEAL, True)
s.text(970, y, "Perubahan", 14, MUTED, True)
s.text(1070, y, "Titik rawan", 14, MUTED, True)
y += 28
rows = [
    (None, "Tidak ada langkah ini. Dokumen belum menetapkan siapa klien, siapa pendana, dan apa hasil utama yang dijanjikan.",
     "0. Tetapkan dulu: klien dan pendana, satu hasil utama, dan pembaca keputusan. Tulis di halaman pertama.", "BARU", [1, 2, 4]),
    ("1. Ide diajukan ke Polda, Pemkot, dan calon pendana untuk didiskusikan.",
     None, "1. Ide diajukan dengan satu kalimat definisi, peran tiap pihak, dan tahapan: pilot dulu, program penuh bila terbukti.", "UBAH", [3]),
    ("2. Kampung dan UMKM dicari setelah ide disetujui. Di pilot, jalur keterampilan sudah ditetapkan lebih dulu.",
     None, "2. Asesmen cepat 14 hari: pilih kampung dari potensinya, cari UMKM dan permintaan kerja, baru tetapkan jalur.", "UBAH", [5]),
    ("3. Kelas dibuka bila ada minimal 2 mitra pengguna dan persetujuan kampung.",
     None, "3. Syarat mulai ditambah dana dan PKS yang sudah terkonfirmasi. Jadwal dihitung dari hari H, bukan dari bulan tetap.", "UBAH", [8]),
    ("4. Pendaftaran terbuka untuk warga dewasa. Rentang usia berbeda di tiap dokumen.",
     None, "4. Pendaftaran terbuka dengan satu rentang usia dan saluran Karang Taruna serta SMK. Hak peserta ditulis: biaya, uang saku, jenis sertifikat.", "UBAH", [6]),
    ("5. Pelatihan 36 JP (pilot) atau 100 JP (penuh), lalu uji praktik.",
     None, "5. Tetap. Ditambah tujuan terukur tiap unit dan daftar hasil yang dibawa pulang peserta.", "TAMBAH", []),
    ("6. Peserta mengerjakan proyek nyata di UMKM, dibimbing mentor.",
     None, "6. Praktik terbimbing: jam dan tugas dibatasi, UMKM menilai, dan status peserta (bukan pekerja tanpa upah) ditulis jelas.", "UBAH", [6]),
    ("7. Dicek apakah ada kerja atau tugas berbayar, di hari ke 30 atau hari ke 90.",
     None, "7. Dilacak sampai hari ke 90 dengan definisi baku: jenis kerja, batas minimal, bukti, pendapatan sebelum dan sesudah.", "UBAH", [7, 8]),
    ("8. Keputusan GO, IMPROVE, atau NO-GO di hari ke 90, disertai laporan.",
     None, "8. Sama. Arti GO ditulis di awal dokumen: layak diuji lebih besar, bukan izin perluasan dan bukan jaminan.", "TETAP", [9]),
]
for i, (lt, _, rt, tg, mk) in enumerate(rows):
    lt_ = lt or "(belum ada)"
    lh = s.height_of(lt_ if lt else rows[0][1], 13, LW - 28)
    rh = s.height_of(rt, 13, RW - 28)
    h = max(lh, rh, 36) + 24
    if lt:
        s.rect(LX, y, LW, h, GRAYBG, LINE, rx=8)
        s.text(LX + 14, y + 12, lt, 13, INK, maxw=LW - 28)
    else:
        s.rect(LX, y, LW, h, "#fff", MUTED, rx=8)
        s.add(f'<rect x="{LX}" y="{y}" width="{LW}" height="{h:.1f}" rx="8" fill="none" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 4"/>')
        s.text(LX + 14, y + 12, rows[0][1], 13, MUTED, maxw=LW - 28)
    s.line(LX + LW + 6, y + h / 2, RX - 6, y + h / 2, MUTED, 2.5, arrow=True)
    fillr = {"BARU": "#F1ECF7", "UBAH": YELBG, "TAMBAH": "#E8F1FB", "TETAP": GRNBG}[tg]
    strokr = {"BARU": PURPLE, "UBAH": YEL, "TAMBAH": BLUE, "TETAP": GRN}[tg]
    s.rect(RX, y, RW, h, fillr, strokr, rx=8, sw=1.5)
    s.text(RX + 14, y + 12, rt, 13, INK, maxw=RW - 28)
    tag(970, y + h / 2 - 10, tg)
    for k, m in enumerate(mk):
        mark(1082 + k * 30, y + h / 2, m)
    y += h + 12
y += 26

# 3. Titik rawan
y = section(s, y, 3, "Sembilan titik yang bisa disalahpahami, dan cara menuliskannya agar jelas")
risks = [
    ("Program ini sebenarnya apa?", "Satu dokumen memuat tiga identitas (pelatihan kerja, pemberdayaan ekonomi, kemitraan polisi). Tiap pembaca memilih satu.", "Satu kalimat definisi di halaman pertama, plus tiga hal yang bukan program ini."),
    ("Siapa klien, pendana, dan penanggung jawab?", "Dokumen ditujukan ke Polda, Pemkot, dan mitra pendanaan sekaligus. Polda dinyatakan tidak wajib mendanai, tetapi pendananya belum disebut.", "Tabel empat peran: pengampu, pendana, pelaksana, fasilitator. [ISI TIM: pendana]"),
    ("Pilot dan program penuh itu apa hubungannya?", "Ada pilot Rp48,9 juta, paket STARTER Rp185 juta, dan program penuh Rp495 juta. Pembaca bisa mengira harus memilih satu atau tidak tahu mana yang ditawarkan.", "Satu bagan tahapan: pilot adalah tahap 1. Program penuh hanya bila pilot terbukti. Satu paket per dokumen."),
    ("Apa yang dijanjikan hasilnya?", "Disebut pelatihan, kerja, penghasilan, usaha, bahkan rasa aman komunitas. Pembaca menagih semuanya.", "Satu hasil utama, hasil pendukung, dan daftar yang tidak dijanjikan (kerja dan penurunan kriminalitas)."),
    ("Berbasis potensi kampung atau paket jadi?", "Pilot menetapkan jalur lebih dulu, lalu mencari kampung. Terbaca sebagai paket yang dipasang ke kampung.", "Tulis urutan: potensi kampung, permintaan kerja, baru jalur. Atau alasan jalur digital cocok di mana saja."),
    ("Status dan hak peserta saat praktik di UMKM?", "Peserta mengerjakan tugas nyata untuk usaha. Bisa dibaca sebagai tenaga kerja tanpa upah. Biaya peserta dan uang saku tidak disebut.", "Tulis: praktik terbimbing, batas jam, penilaian oleh UMKM, ada atau tidaknya uang saku. [ISI TIM]"),
    ("Apa arti \"kerja berbayar\"?", "Satu tugas sekali bayar dengan nilai berapa pun bisa dihitung berhasil. Standar \"4 dari 20\" jadi longgar atau berbeda tafsirnya.", "Definisi baku: jenis (kontrak, lepas, usaha), nilai minimal, bukti, siapa yang memeriksa. [ISI TIM: batas minimal]"),
    ("Kapan programnya selesai dan kapan dinilai?", "Ada 8 minggu, D+30, hari ke 90, dan 6 bulan. Pembaca tidak tahu kapan biaya berhenti dan kapan hasil dihitung.", "Satu baris garis waktu: kegiatan sampai hari X, pelacakan sampai hari Y, keputusan hari Z."),
    ("Apa arti GO?", "GO bisa dibaca sebagai persetujuan perluasan atau jaminan keberhasilan jangka panjang.", "Tulis di awal: GO berarti layak diuji lebih besar. Bukan izin otomatis, bukan jaminan."),
]
cw, gap = 355, 17.5
for r in range(3):
    row = risks[r * 3:(r + 1) * 3]
    hs = []
    for (t, a, b) in row:
        hs.append(max(s.height_of(t, 14, cw - 60, True), 22) + 8 + s.height_of(a, 12.5, cw - 28) + 8 + 16 + s.height_of(b, 12.5, cw - 28) + 36)
    hh = max(hs)
    for c, (t, a, b) in enumerate(row):
        n = r * 3 + c + 1
        x = 50 + c * (cw + gap)
        s.rect(x, y, cw, hh, "#fff", LINE, rx=8, sw=1.3)
        mark(x + 24, y + 26, str(n))
        th = s.text(x + 46, y + 14, t, 14, NAVY, True, maxw=cw - 60)
        yy = y + 14 + max(th, 22) + 8
        s.text(x + 14, yy, "Bisa dibaca:", 11.5, RED, True)
        yy += 16
        yy += s.text(x + 14, yy, a, 12.5, INK, maxw=cw - 28) + 8
        s.text(x + 14, yy, "Tulis jelas:", 11.5, GRN, True)
        yy += 16
        s.text(x + 14, yy, b, 12.5, INK, maxw=cw - 28)
    y += hh + 14
y += 22

# 4. Keputusan tim
y = section(s, y, 4, "Lima keputusan tim yang menutup titik rawan di atas")
dec = [
    ("Klien, pendana, hasil utama", "Siapa pembaca dan pendana, dan satu hasil utama apa.", "Menutup 1, 2, 4"),
    ("Hubungan pilot dan program", "Apakah pilot jadi tahap 1 program penuh, dan kampung dipilih sebelum jalur.", "Menutup 3, 5"),
    ("Hak peserta", "Biaya peserta, uang saku, dan status saat praktik di UMKM.", "Menutup 6"),
    ("Batas \"kerja berbayar\"", "Jenis dan nilai minimal yang dihitung berhasil.", "Menutup 7, 9"),
    ("Garis waktu dan tanggal mulai", "Kapan mulai, kapan kegiatan selesai, sampai hari ke berapa dilacak.", "Menutup 8"),
]
cw, gap = 207, 16
hh = max(need(s, cw, t, d + "\n" + c, tfs=13.5, bfs=12.5) for t, d, c in dec) + 14
for i, (t, d, c) in enumerate(dec):
    x = 50 + i * (cw + gap)
    s.rect(x, y, cw, hh, YELBG, YEL, rx=8, sw=1.5)
    th = s.text(x + 14, y + 14, t, 13.5, NAVY, True, maxw=cw - 28)
    th += s.text(x + 14, y + 14 + th + 8, d, 12.5, INK, maxw=cw - 28)
    s.text(x + 14, y + hh - 28, c, 12, "#8A6500", True)
y += hh + 32

# 5. Sudah aman
y = section(s, y, 5, "Yang sudah jelas di dokumen dan aman dipertahankan")
safe = ["Target ditulis sebagai target, bukan hasil dan bukan jaminan.", "Sertifikat Sanggabiz adalah sertifikat internal, bukan BNSP.",
        "Polda difasilitasi sukarela, tanpa memakai data kepolisian untuk seleksi.", "Cohort tidak dibuka tanpa 2 mitra pengguna dan persetujuan kampung.",
        "Keputusan akhir punya tiga kemungkinan dengan ambang yang jelas."]
for t in safe:
    s.circle(66, y + 9, 5, GRN)
    y += s.text(82, y, t, 13.5, INK, maxw=1060) + 7
y += 18
s.text(50, y, "Penilaian \"bisa dibaca\" adalah analisis kami atas tiga dokumen Jogja Berdaya (22 November 2026), bukan keluhan dari pembaca nyata. Mohon dikoreksi bila keliru. Detail per bagian ada di gambar 05.", 12.5, MUTED, maxw=1100)
y += 50
s.save(OUT, y, "Ide umum proposal Jogja Berdaya: alur sekarang dan alur yang disarankan",
       "Satu identitas program, alur sekarang dibandingkan alur yang disarankan, sembilan titik rawan salah paham, dan lima keputusan tim.")
print("ok", y)
