import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "05-peta-proposal-sekarang-dan-ke-depan.svg")
PURPLE = "#7A5BA6"
s = SVG(1200)
header(s, "Peta proposal: isi sekarang dan yang bisa ditambah",
       "Satu halaman untuk melihat proposal strategis Jogja Berdaya bagian demi bagian: apa isinya sekarang, mana yang dipertahankan, dan mana yang perlu diubah atau ditambah ke depan.")

ST = {
    "PERTAHANKAN": (GRN, "#fff"),
    "UBAH": (YEL, INK),
    "TAMBAH": (BLUE, "#fff"),
    "BARU": (PURPLE, "#fff"),
}

def badge(x, y, name):
    bg, fg = ST[name]
    w = 16 + len(name) * 7
    s.rect(x, y, w, 20, bg, None, rx=10)
    s.text(x + w / 2, y + 4.5, name, 11, fg, True, "middle")
    return 24

# 1. Posisi
y = 140
cw = 520
h1 = max(need(s, cw, "Sekarang (draf 22 November 2026)",
              "Ada tiga dokumen: proposal strategis (3 kampung, 90 peserta, 6 bulan, Rp495 juta) serta deck dan executive proposal pilot (1 kampung, 20 peserta, 8 minggu, Rp48,9 juta). Rancangan dan ukuran hasilnya kuat. Anggaran, metode, dan gaya tulis belum mengikuti aturan Sanggabiz. Profil tim, tempat, dan metode belum ada.", bfs=13.5),
         need(s, cw, "Ke depan (usulan, menunggu keputusan tim)",
              "Satu proposal terpadu versi 1 yang memakai isi berita Kedaulatan Rakyat dengan tepat, mengukur mutu pekerjaan dan pendapatan, memuat anggaran dengan Fee 10 persen yang tersusun menurut tahap kerja, memuat silabus rinci, profil tim, tempat, dan metode. Satu paket untuk klien.", bfs=13.5))
card(s, 50, y, cw, "Sekarang (draf 22 November 2026)",
     "Ada tiga dokumen: proposal strategis (3 kampung, 90 peserta, 6 bulan, Rp495 juta) serta deck dan executive proposal pilot (1 kampung, 20 peserta, 8 minggu, Rp48,9 juta). Rancangan dan ukuran hasilnya kuat. Anggaran, metode, dan gaya tulis belum mengikuti aturan Sanggabiz. Profil tim, tempat, dan metode belum ada.",
     h=h1, fill=GRAYBG, bar=NAVY, bfs=13.5)
s.line(50 + cw + 6, y + h1 / 2, 50 + cw + 54, y + h1 / 2, MUTED, 3, arrow=True)
card(s, 50 + cw + 60, y, 520, "Ke depan (usulan, menunggu keputusan tim)",
     "Satu proposal terpadu versi 1 yang memakai isi berita Kedaulatan Rakyat dengan tepat, mengukur mutu pekerjaan dan pendapatan, memuat anggaran dengan Fee 10 persen yang tersusun menurut tahap kerja, memuat silabus rinci, profil tim, tempat, dan metode. Satu paket untuk klien.",
     h=h1, fill=TEALBG, stroke=TEAL, bar=TEAL, bfs=13.5)
y += h1 + 34

# 2. Alur cerita
y = section(s, y, 1, "Alur cerita proposal: pembaca dibawa menjawab enam pertanyaan")
flow = [("Mengapa perlu?", "Bagian 02"), ("Apa dan dengan siapa?", "Bagian 01, 03, 05"),
        ("Bagaimana warga belajar?", "Bagian 04, 06, 07, 08"), ("Apa buktinya?", "Bagian 09"),
        ("Berapa biayanya?", "Bagian 10"), ("Apa yang diminta?", "Bagian 11, 12, 13")]
cw, gap = 165, 22
for i, (q, b) in enumerate(flow):
    x = 50 + i * (cw + gap)
    s.rect(x, y, cw, 78, TEALBG, TEAL, rx=8, sw=1.5)
    s.text(x + cw / 2, y + 11, q, 14, NAVY, True, "middle", maxw=cw - 16)
    s.text(x + cw / 2, y + 52, b, 12, TEAL, True, "middle", maxw=cw - 12)
    if i < 5:
        s.line(x + cw + 2, y + 39, x + cw + gap - 2, y + 39, MUTED, 2, arrow=True)
y += 78 + 36

# 3. Peta
y = section(s, y, 2, "Peta bagian demi bagian (proposal strategis, 11 halaman)")
lx = 50
for name, desc in [("PERTAHANKAN", "sudah baik"), ("UBAH", "isi sekarang perlu diganti"), ("TAMBAH", "isi sekarang kurang"), ("BARU", "belum ada sama sekali")]:
    w = badge(lx, y, name)
    s.text(lx + 16 + len(name) * 7 + 8, y + 3, desc, 12.5, MUTED)
    lx += 16 + len(name) * 7 + 8 + len(desc) * 6.6 + 26
y += 34

BX, NX, SX, TX = 50, 62, 624, 740   # kolom
s.rect(50, y, 1100, 32, NAVY, rx=6)
for t, x in [("Bagian", 62), ("Isi sekarang", 292), ("Status", 624), ("Yang bisa ditambah atau diubah", 740)]:
    s.text(x, y + 8, t, 13.5, "#fff", True)
y += 32

groups = [
    ("A. Pembuka: mengapa program ini perlu", [
        ("Sampul", "Judul, slogan berbahasa Inggris, angka 3 kampung, 90 peserta, 6 bulan, Rp495 juta, dan catatan bahwa ini bukan anggaran yang sudah disetujui.", ["UBAH"],
         "Slogan Indonesia dari kosakata berita (masukan 11). Satu paket saja untuk klien (14). Nama pelaksana seragam."),
        ("01 Ringkasan eksekutif", "Tabel rancangan: sasaran, lokasi, tiga jalur, 100 JP, output, target hasil, investasi.", ["TAMBAH"],
         "Sebut lulusan SMK dan Karang Taruna (4). Tambah ukuran mutu pekerjaan di target hasil (2). Satu kalimat tentang metode."),
        ("02 Mengapa sekarang", "Tiga agenda kebijakan, tabel bukti (berita KR hanya satu baris), dan penjelasan melengkapi program yang sudah ada.", ["UBAH"],
         "Pakai angka dan kutipan berita dengan tepat (1). Hubungkan tiga jalur ke empat sektor produktivitas rendah. Tulis posisi terhadap \"training di Bantul\" (13)."),
    ]),
    ("B. Rancangan: apa yang dilakukan dan dengan siapa", [
        ("03 Kemitraan dan mandat", "Peran Polda DIY, Pemkot, Disnaker dan BLK, Sanggabiz, perusahaan, dan warga, masing-masing dengan batas \"yang tidak diklaim\".", ["PERTAHANKAN", "TAMBAH"],
         "Pertahankan kolom \"tidak diklaim\". Tambah BBPVP Semarang sebagai pihak yang dijajaki, dan urutkan Pemkot sebelum Polda (5)."),
        ("04 Model operasional", "HASTA (alur kemitraan Pemkot) digabung 4D dari playbook Pemkot: Define, Design, Deploy, Develop.", ["UBAH"],
         "Tulis HASTA dan 4D sebagai istilah klien. Tambah ADDIE untuk alur pelaksanaan dan backward design untuk menyusun materi (9)."),
        ("05 Lokasi dan rekrutmen", "Lima kriteria seleksi kampung berbobot, shortlist berupa tipe kampung, rekrutmen terbuka dan inklusif.", ["TAMBAH"],
         "Karang Taruna dan SMK sebagai saluran daftar, satu rentang usia (4). Di pilot, pilih kampung dulu baru jalur (3)."),
    ]),
    ("C. Isi pelatihan: bagaimana warga belajar", [
        ("06 Kurikulum 100 JP", "8 + 8 + 8 JP kompetensi inti, 56 JP spesialisasi jalur, 20 JP proyek dan uji akhir.", ["PERTAHANKAN", "TAMBAH"],
         "Pertahankan struktur JP. Tambah 2 JP hak pekerja dan jaminan sosial dari 8 JP inti (10). Rumuskan tujuan tiap unit dengan kata kerja Bloom."),
        ("07 Silabus tiga jalur", "Tabel per jalur: unit, JP, simulasi, standar lulus.", ["TAMBAH"],
         "Perinci per topik: tujuan, outline, aktivitas per menit, alat, output, ukuran berhasil. Tambah daftar \"hasil yang dibawa pulang\"."),
        ("08 Jadwal 6 bulan", "Bulan 1 sampai 6 (Januari sampai Juni 2027) dengan keluaran tiap bulan. Rencana 30 hari ada di bagian 13.", ["UBAH"],
         "Tulis dengan hari H atau geser mulai bila dana belum ada (12). Satukan batas pelacakan hasil, 30 atau 90 hari (7)."),
    ]),
    ("D. Bukti dan biaya", [
        ("09 KPI dan Kirkpatrick", "Target per level: reaksi, pembelajaran, perilaku, hasil kerja dan usaha, kemitraan, rasa aman komunitas.", ["PERTAHANKAN", "TAMBAH"],
         "Pertahankan Kirkpatrick. Tambah pendapatan sebelum dan sesudah, bentuk hubungan kerja, jaminan sosial (2). Tambah indikator usaha di pilot (8)."),
        ("10 RAB dan nilai penawaran", "Sepuluh baris biaya, total Rp495 juta, tiga paket (Rp185, 495, 915 juta), skema pembayaran 30, 40, 20, 10 persen.", ["UBAH"],
         "Fee 10 persen sebagai baris sendiri, rincian volume kali harga satuan, tersusun menurut tujuh tahap, satu paket, pajak seragam (6, 14). Lihat gambar 04."),
    ]),
    ("E. Tata kelola dan permintaan keputusan", [
        ("11 Tata kelola, RACI, risiko", "Tabel RACI lima pekerjaan dan delapan risiko dengan penangkal dan kriteria berhenti.", ["PERTAHANKAN", "TAMBAH"],
         "Tambah BBPVP di RACI bila disetujui. Tambah risiko keterlambatan dana dan PKS."),
        ("12 Manfaat tiap pihak", "Satu baris manfaat untuk Polda, Pemkot, perusahaan, kampus, warga, Sanggabiz.", ["PERTAHANKAN"],
         "Tidak ada perubahan wajib."),
        ("13 Keputusan dan rencana 30 hari", "Tiga permintaan (liaison Polda, focal point Pemkot, izin asesmen cepat) dan rencana empat minggu.", ["UBAH"],
         "Pastikan 30 hari itu selesai sebelum kelas mulai. Sesuaikan permintaan dengan pembaca dan pendana yang dipilih tim."),
        ("Lampiran A: rubrik", "Rubrik lima kompetensi, skala 1, 3, 5, dan aturan lulus.", ["PERTAHANKAN"],
         "Tidak ada perubahan wajib."),
        ("Lampiran B: sumber", "Tiga dokumen pengguna, berita KR, sembilan tautan situs resmi, dan catatan asumsi biaya.", ["TAMBAH"],
         "Buka dan cek tiap tautan, cek angka berita ke BPS, unggah tiga dokumen pengguna ke folder sumber."),
    ]),
]
NW, CWD, TWD = 215, 320, 380
for gname, items in groups:
    s.rect(50, y + 4, 1100, 28, TEALBG, None, rx=0)
    s.text(62, y + 10, gname, 14, TEAL, True)
    y += 36
    for i, (name, now, sts, todo) in enumerate(items):
        h = max(s.height_of(name, 14, NW, True), s.height_of(now, 13, CWD), s.height_of(todo, 13, TWD), len(sts) * 24) + 20
        s.rect(50, y, 1100, h, "#fff", None, rx=0)
        s.line(50, y + h, 1150, y + h, "#E3E8EC", 1)
        s.text(62, y + 10, name, 14, NAVY, True, maxw=NW)
        s.text(292, y + 10, now, 13, INK, maxw=CWD)
        by = y + 9
        for st in sts:
            by += badge(624, by, st)
        s.text(740, y + 10, todo, 13, INK, maxw=TWD)
        y += h
    y += 8
y += 22

# 4. Belum ada
y = section(s, y, 3, "Bagian yang belum ada sama sekali dan layak ditambahkan")
new = [
    ("Profil dan rekam jejak Sanggabiz", "Pengalaman program serupa dan klien sebelumnya. Bahannya ada di company profile.", "[ISI TIM: pengalaman yang boleh ditampilkan]", "Analisis"),
    ("Tim pelaksana dan pelatih", "Nama, peran, dan pengalaman. Jumlah orang sesuai kebutuhan nyata.", "[ISI TIM: nama dan profil tim]", "Aturan"),
    ("Tempat pelaksanaan", "Nama aula, alamat, ukuran, kapasitas, harga acuan, dan akses penyandang disabilitas.", "[ISI TIM: aula setelah kampung ditetapkan]", "Aturan"),
    ("Metode dan alasan pemilihan", "ADDIE, backward design, andragogi, Bloom, Kirkpatrick, dan di bagian mana tiap metode dipakai.", "", "Aturan"),
    ("Hasil yang dibawa pulang", "Daftar semua output peserta dan UMKM, dengan keterangan dihasilkan di topik mana.", "", "Aturan"),
    ("Proses bisnis program", "Tujuh tahap kerja sebagai tulang punggung rundown, silabus, tim, dan anggaran.", "", "Arahan Pak Priyo"),
]
cw, gap = 262, 17
for r in range(2):
    items = new[r * 3: r * 3 + 3] if False else None
rows_new = [new[0:3], new[3:6]]
cw, gap = 355, 17.5
for row in rows_new:
    hh = max(need(s, cw, t, d + ("\n" + p if p else "") + "\nDasar: " + b, tfs=14.5, bfs=13) for t, d, p, b in row)
    for i, (t, d, p, b) in enumerate(row):
        x = 50 + i * (cw + gap)
        s.rect(x, y, cw, hh, "#fff", PURPLE, rx=8, sw=1.6)
        s.rect(x, y, 6, hh, PURPLE, None, rx=3)
        th = s.text(x + 16, y + 14, t, 14.5, NAVY, True, maxw=cw - 30)
        yy = y + 14 + th + 8
        yy += s.text(x + 16, yy, d, 13, INK, maxw=cw - 30)
        if p:
            tw = len(p) * 6.9 + 12
            s.rect(x + 14, yy + 6, tw, 20, YEL, None, rx=3)
            s.text(x + 20, yy + 10, p, 12, INK)
            yy += 28
        s.text(x + 16, yy + 4, "Dasar: " + b, 12, MUTED, maxw=cw - 30)
    y += hh + 14
y += 22

# 5. Langkah
y = section(s, y, 4, "Langkah ke depan (usulan urutan kerja)")
steps = [
    ("1. Putuskan", "Pembaca dan keputusan yang diminta. Siapa pendana. Dokumen mana yang jadi dasar."),
    ("2. Lengkapi data", "Unggah tiga dokumen pengguna. Buka tautan sumber. Cek angka berita ke BPS."),
    ("3. Tulis ulang inti", "Bagian urgensi, indikator mutu, mitra, dan garis waktu pelacakan."),
    ("4. Susun isi pelatihan", "Silabus per topik dengan Bloom dan backward design. Tempat dan tim."),
    ("5. Susun anggaran", "Tujuh tahap, volume kali harga satuan, Fee 10 persen, satu paket, pajak seragam."),
    ("6. Cek dan simpan", "Cek gaya, cek klaim, simpan sebagai v1 di folder proposal."),
]
cw, gap = 165, 22
hh = max(need(s, cw, t, d, tfs=14, bfs=12.5) for t, d in steps)
for i, (t, d) in enumerate(steps):
    x = 50 + i * (cw + gap)
    card(s, x, y, cw, t, d, h=hh, fill=GRAYBG, tfs=14, bfs=12.5, bar=TEAL)
    if i < 5:
        s.line(x + cw + 2, y + hh / 2, x + cw + gap - 2, y + hh / 2, MUTED, 2, arrow=True)
y += hh + 38

# 6. Padanan pilot
y = section(s, y, 5, "Bila membaca dokumen pilot: padanannya di proposal strategis")
pad = [
    ("E01 Keputusan yang ingin dibuktikan", "Bagian 01 dan 02"), ("E02 Ruang lingkup", "Bagian 05 dan 03"), ("E03 Deliverables bernilai", "Bagian 01 (output utama)"),
    ("E04 Kurikulum 36 JP", "Bagian 06 dan 07"), ("E05 Timeline 8 minggu", "Bagian 08"), ("E06 Pihak dan akuntabilitas", "Bagian 03 dan 11"),
    ("E07 Scorecard G1 sampai G5", "Bagian 09"), ("E08 Penawaran Rp48,9 juta", "Bagian 10"), ("E09 14 hari awal", "Bagian 13"),
]
cw, gap = 355, 17.5
for r in range(3):
    for c in range(3):
        a, b = pad[r * 3 + c]
        x = 50 + c * (cw + gap)
        yy = y + r * 58
        s.rect(x, yy, cw, 50, GRAYBG, LINE, rx=6)
        s.text(x + 12, yy + 9, a, 12.5, NAVY, True, maxw=175)
        s.text(x + cw - 12, yy + 9, b, 12.5, TEAL, True, "end", maxw=150)
y += 3 * 58 + 8
s.text(50, y, "E = executive proposal pilot (3 halaman, Rp48,9 juta). Deck pilot (D) berisi bahan yang sama dalam bentuk slide. Sumber: tiga PDF Jogja Berdaya, 22 November 2026. Angka dalam masukan merujuk gambar 03.", 12.5, MUTED, maxw=1100)
y += 52
s.save(OUT, y, "Peta proposal Jogja Berdaya: sekarang dan ke depan",
       "Peta bagian demi bagian proposal strategis dengan isi sekarang, status pertahankan, ubah, tambah, bagian yang belum ada, dan langkah ke depan.")
print("ok", y)
