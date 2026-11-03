"""Membuat proposal Aqiqah Al Kautsar dalam bentuk PPTX 16:9 agar bisa diunggah ke Canva.

Jalankan: python3 build_pptx.py
Isi sama dengan proposal docx v1. Semua teks berupa kotak teks biasa sehingga bisa diedit di Canva.
Huruf memakai keluarga Montserrat (tersedia di Canva). Tebal diatur lewat atribut bold.
"""
import os
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
A = lambda f: os.path.join(HERE, "assets", f)
OUT = os.path.join(HERE, "..", "proposal", "v1 Proposal Training CS Closing - Aqiqah Al Kautsar.pptx")

NAVY, NAVY_D, PANEL, TEAL = "0B396D", "092647", "0D2A4E", "2F7E9D"
GOLD, WHITE, SOFT, MUTED, INK = "FFC00C", "FFFFFF", "CFDCEC", "9FB4CC", "1D1D1F"
FONT = "Montserrat"
SW, SH, ML = 13.333, 7.5, 0.65
CW = SW - 2 * ML
JUDUL = "Training CS for Improving Sales Closing Rate"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(SW), Inches(SH)
NOMOR = [0]


def rgb(h):
    return RGBColor.from_string(h)


# ---------------- penolong dasar ----------------
def shape(s, x, y, w, h, fill=None, line=None, lw=1.25, r=None):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if r else MSO_SHAPE.RECTANGLE
    sh = s.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if r:
        sh.adjustments[0] = min(0.5, r / min(w, h))
    if fill:
        sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    else:
        sh.fill.background()
    if line:
        sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
    else:
        sh.line.fill.background()
    sh.shadow.inherit = False
    return sh


def _runs(p, txt, size, bold, color):
    """**tebal** dan [ISI TIM: ...] dengan stabilo kuning."""
    for part in re.split(r"(\*\*[^*]+\*\*|\[ISI TIM:[^\]]*\])", txt):
        if not part:
            continue
        b, c = bold, color
        isi = part.startswith("[ISI TIM")
        if part.startswith("**"):
            part, b = part[2:-2], True
        r = p.add_run()
        r.text = part
        f = r.font
        f.size, f.bold, f.name = Pt(size), b or isi, FONT
        f.color.rgb = rgb(INK if isi else c)
        rPr = r._r.get_or_add_rPr()
        if isi:
            hl = etree.SubElement(rPr, qn("a:highlight"))
            clr = etree.SubElement(hl, qn("a:srgbClr")); clr.set("val", "FFF200")
        for tag in ("a:latin", "a:ea", "a:cs"):
            el = rPr.find(qn(tag))
            if el is None:
                el = etree.SubElement(rPr, qn(tag))
            el.set("typeface", FONT)


def text(s, x, y, w, h, paras, size=13, bold=False, color=WHITE, align="l", anchor="t", after=5, spacing=1.12, box=None):
    tb = box or s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    if box is None:
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        p.line_spacing, p.space_after = spacing, Pt(after)
        if isinstance(para, tuple):  # (teks, ukuran, tebal, warna)
            t, sz, b, c = (list(para) + [None] * 4)[:4]
            _runs(p, t, sz or size, bold if b is None else b, c or color)
        else:
            _runs(p, para, size, bold, color)
    return tb


def card(s, x, y, w, h, fill=TEAL, line=WHITE, lw=1.5, r=0.14, pad=0.2):
    sh = shape(s, x, y, w, h, fill=fill, line=line, lw=lw, r=r)
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(pad)
    tf.margin_top = tf.margin_bottom = Inches(pad * 0.8)
    return sh


def pill(s, x, y, w, h, label, fill=GOLD, color=NAVY, size=11):
    sh = shape(s, x, y, w, h, fill=fill, r=h / 2)
    tf = sh.text_frame
    tf.margin_left = tf.margin_right = Inches(0.08); tf.margin_top = tf.margin_bottom = 0
    text(s, 0, 0, 0, 0, [label], size=size, bold=True, color=color, align="c", anchor="m", box=sh)
    return sh


def circle(s, x, y, d, label, fill=GOLD, color=NAVY, size=14):
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill); sh.line.fill.background(); sh.shadow.inherit = False
    tf = sh.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    text(s, 0, 0, 0, 0, [label], size=size, bold=True, color=color, align="c", anchor="m", box=sh)


def picture(s, f, x, y, w=None, h=None):
    return s.shapes.add_picture(A(f), Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)


def slide(eyebrow=None, title=None, footer=True):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    f = s.background.fill
    f.gradient(); f.gradient_angle = 300
    st = f.gradient_stops
    st[0].position, st[1].position = 0.0, 1.0
    st[0].color.rgb, st[1].color.rgb = rgb(NAVY), rgb(NAVY_D)
    NOMOR[0] += 1
    if eyebrow:
        text(s, ML, 0.42, CW, 0.3, [eyebrow.upper()], size=11, bold=True, color=GOLD)
    if title:
        text(s, ML, 0.72, CW, 1.0, [title], size=27, bold=True, color=WHITE, spacing=1.05)
    if footer:
        picture(s, "logo_white.png", ML, 6.98, w=1.05)
        text(s, ML + 1.3, 7.0, 8, 0.25, [f"Proposal {JUDUL}  |  Aqiqah Al Kautsar  |  November 2026"], size=8.5, color=MUTED)
        text(s, SW - ML - 0.6, 6.98, 0.6, 0.3, [str(NOMOR[0])], size=11, bold=True, color=GOLD, align="r")
    return s


def grid(s, x, y, widths, rows, header=None, row_h=0.42, size=11.5, head_size=11, first_bold=True):
    """Tabel dari kotak, mudah diedit di Canva. rows: list of list teks. row_h boleh list."""
    cy = y
    if header:
        cx = x
        for i, w in enumerate(widths):
            sh = shape(s, cx, cy, w, 0.42, fill=GOLD, line=NAVY_D, lw=0.75)
            tf = sh.text_frame; tf.margin_left = tf.margin_right = Inches(0.12); tf.margin_top = tf.margin_bottom = Inches(0.03)
            text(s, 0, 0, 0, 0, [header[i]], size=head_size, bold=True, color=NAVY, anchor="m", box=sh)
            cx += w
        cy += 0.42
    for ri, row in enumerate(rows):
        h = row_h[ri] if isinstance(row_h, list) else row_h
        cx = x
        for i, w in enumerate(widths):
            fill = PANEL if ri % 2 == 0 else "123A66"
            sh = shape(s, cx, cy, w, h, fill=fill, line=TEAL, lw=0.75)
            tf = sh.text_frame; tf.margin_left = tf.margin_right = Inches(0.12); tf.margin_top = tf.margin_bottom = Inches(0.05)
            val = row[i]
            lines = val if isinstance(val, list) else [val]
            text(s, 0, 0, 0, 0, lines, size=size, bold=(first_bold and i == 0), color=WHITE, anchor="m", after=2, box=sh)
            cx += w
        cy += h
    return cy


# ================= SLIDE =================
# 1. Sampul
s = slide(footer=False)
picture(s, "logo_white.png", ML, 0.55, w=1.75)
text(s, ML, 2.0, 7.3, 0.3, ["PROPOSAL PELATIHAN"], size=13, bold=True, color=GOLD)
text(s, ML, 2.4, 7.3, 1.6, [JUDUL], size=34, bold=True, spacing=1.0)
text(s, ML, 4.2, 7.2, 0.7, ["Pelatihan closing lewat WhatsApp untuk tim Customer Service Aqiqah Al Kautsar"], size=16, color=SOFT)
pl = shape(s, ML, 5.1, 7.3, 0.55, fill=PANEL, line=TEAL, lw=1.5, r=0.27)
text(s, 0, 0, 0, 0, ["6 sampai 8 CS dan 1 Supervisor  •  Workshop 4 jam  •  Didampingi 1 bulan"], size=12, bold=True, align="c", anchor="m", box=pl)
text(s, ML, 6.0, 7.2, 0.3, [("Disiapkan untuk: **Aqiqah Al Kautsar**", 13, False, SOFT)])
text(s, ML, 6.35, 7.2, 0.3, ["Diajukan oleh Sanggabiz, November 2026"], size=11, color=MUTED)
for f, x, y, w, h in [("foto-pelatihan-2.jpg", 8.25, 0.55, 4.45, 2.5)]:
    fr = shape(s, x - 0.05, y - 0.05, w + 0.1, h + 0.1, fill=WHITE)
    picture(s, f, x, y, w=w, h=h)
picture(s, "kartu-saku-depan.png", 8.25, 3.3, h=3.7)
c = card(s, 11.05, 3.3, 1.65, 3.7, fill=GOLD, line=None)
text(s, 0, 0, 0, 0, [("5", 44, True, NAVY), ("langkah chat closing yang dipakai seluruh tim", 12, True, NAVY)], align="c", anchor="m", box=c)

# 2. Ringkasan
s = slide("Ringkasan proposal", "Satu workshop dan satu bulan pendampingan agar lebih banyak chat menjadi pesanan")
blok = [
    ("Kebutuhan.", "Tim CS mulai memegang target penjualan. Belum ada cara membalas chat yang sama untuk seluruh tim, dan target bulanan belum dipecah menjadi pegangan harian."),
    ("Usulan kami.", "Mengenal tim lewat contoh chat dan data penjualan, lalu workshop 4 jam yang sebagian besar berisi praktik. Setelah itu tim didampingi lewat WhatsApp selama empat minggu."),
    ("Hasil.", "Setiap CS memakai lima langkah chat yang sama, tahu target hariannya, dan mencatat setiap calon pelanggan. Supervisor memantau tim setiap hari."),
    ("Investasi.", "Nilai program Rp 7.500.000. Dengan skema kemitraan menjadi Rp 5.500.000, dibayar dengan konsumsi acara Sanggabiz dan Rp 2.000.000 tunai."),
]
text(s, ML, 2.05, 6.7, 4.6, [(f"**{a}** {b}", 13.5, False, WHITE) for a, b in blok], after=12, spacing=1.15)
for i, (big, small) in enumerate([("6 - 8", "CS dan 1 Supervisor"), ("4 jam", "workshop di kantor Al Kautsar"), ("4 minggu", "pendampingan lewat WhatsApp"), ("5", "langkah chat closing")]):
    x, y = 7.75 + (i % 2) * 2.5, 2.05 + (i // 2) * 2.3
    c = card(s, x, y, 2.3, 2.1)
    text(s, 0, 0, 0, 0, [(big, 27, True, WHITE), (small, 12, True, WHITE)], align="c", anchor="m", box=c, after=8)

# 3. Latar belakang
s = slide("Latar belakang", "Hampir setiap pesanan aqiqah berawal dari satu chat")
text(s, ML, 1.75, CW, 0.9, ["Keluarga yang menghubungi biasanya sedang membandingkan beberapa pilihan dan perlu memutuskan sebelum tanggal aqiqah. Pada rentang waktu yang singkat itu, cara CS membalas chat ikut menentukan apakah keluarga tersebut memesan di Al Kautsar."], size=14, color=SOFT)
for i, (lbl, body) in enumerate([
    ("Di sisi CS", ["Belum ada alur percakapan yang sama untuk seluruh tim.", "Setiap orang membalas dengan caranya sendiri.", "Harga sering dikirim sebelum kebutuhan keluarga diketahui."]),
    ("Di sisi Supervisor", ["Target bulanan sudah ada.", "Target belum dipecah menjadi pegangan harian untuk setiap CS.", "Hasil baru terlihat di akhir bulan."]),
]):
    x = ML + i * 6.1
    c = card(s, x, 3.05, 5.9, 2.75, fill=PANEL if i == 0 else TEAL, line=WHITE)
    pill(s, x + 0.3, 2.82, 2.6, 0.42, lbl)
    text(s, x + 0.35, 3.45, 5.2, 2.2, [f"•  {b}" for b in body], size=13.5, after=9)
nb = card(s, ML, 6.05, CW, 0.7, fill=PANEL, line=GOLD)
text(s, 0, 0, 0, 0, ["**Belum ada data** berapa chat yang biasanya menjadi pesanan [ISI TIM: konfirmasi]. Karena itu program dimulai dengan mengenal tim, dan angka awal ini menjadi pembanding di akhir."], size=12.5, anchor="m", box=nb)

# 4. Yang ingin dicapai
s = slide("Yang ingin dicapai", "Dari kebiasaan yang sering terjadi ke cara kerja yang sama untuk seluruh tim")
grid(s, ML, 1.95, [CW / 2, CW / 2], [
    ["Chat dibalas dengan daftar harga, lalu calon pelanggan berhenti membalas", "Chat dibuka dengan pertanyaan tentang kebutuhan keluarga, lalu ditawarkan satu paket yang sesuai"],
    ["Setiap CS membalas dengan caranya sendiri", "Seluruh tim memakai lima langkah chat yang sama"],
    ["Calon pelanggan yang bilang nanti dulu jarang dihubungi lagi", "Setiap calon pelanggan punya jadwal follow-up yang tercatat"],
    ["Target bulanan terasa jauh dari pekerjaan harian", "Setiap CS tahu berapa chat dan pesanan yang perlu dicapai per hari"],
    ["Supervisor melihat hasil di akhir bulan", "Supervisor memantau setiap hari lewat rapat 10 menit dan catatan tim"],
], header=["Yang sering terjadi", "Yang dituju setelah program"], row_h=0.78, size=13, first_bold=False)
text(s, ML, 6.45, CW, 0.4, ["Kondisi Al Kautsar yang sebenarnya akan kami pastikan pada tahap mengenal tim."], size=11, color=MUTED)

# 5. Tujuan
s = slide("Tujuan", "Setelah program, tim CS dan Supervisor mampu:")
for i, t in enumerate([
    "Setiap CS tahu target hariannya sendiri: berapa chat yang ditangani dan berapa pesanan yang didapat.",
    "CS menanyakan kebutuhan keluarga sebelum memberi harga.",
    "CS menawarkan satu paket yang sesuai dan menjawab keraguan pelanggan dengan tenang.",
    "CS menindaklanjuti calon pelanggan sesuai jadwal sampai memesan atau jelas menolak.",
    "Supervisor membagi target ke setiap CS, memimpin rapat harian singkat, dan membimbing CS dari chat nyata.",
]):
    y = 1.85 + i * 0.95
    shape(s, ML, y, CW, 0.8, fill=PANEL, line=TEAL, lw=1.25, r=0.12)
    circle(s, ML + 0.2, y + 0.12, 0.56, str(i + 1))
    text(s, ML + 1.0, y, CW - 1.3, 0.8, [t], size=14.5, anchor="m")

# 6. Alur program
s = slide("Alur program", "Empat tahap selama sekitar enam minggu")
tahap = [
    ("Mengenal tim", "9 - 13 Nov 2026, online", "Kuesioner singkat, contoh chat yang berhasil dan gagal, data penjualan sebulan terakhir, obrolan 30 menit dengan pemilik", "Materi memakai kasus Al Kautsar sendiri"),
    ("Workshop", "Pekan 16 - 21 Nov 2026, 4 jam", "Latihan menulis chat, bermain peran, dan menyusun jadwal follow-up dengan contoh nyata", "Kartu saku, contoh chat, jawaban keraguan"),
    ("Pendampingan", "4 minggu lewat WhatsApp", "Materi singkat tiga kali seminggu, pemeriksaan chat setiap Jumat, bimbingan pribadi untuk Supervisor", "Empat rekap mingguan"),
    ("Laporan", "Paling lambat 5 hari kerja", "Perbandingan kondisi awal dan akhir, catatan untuk setiap CS, saran bulan berikutnya", "Laporan akhir untuk pemilik"),
]
w = (CW - 0.6) / 4
for i, (judul, waktu, isi, hasil) in enumerate(tahap):
    x = ML + i * (w + 0.2)
    card(s, x, 1.85, w, 3.55, fill=PANEL, line=TEAL)
    circle(s, x + 0.2, 2.02, 0.5, str(i + 1), size=13)
    text(s, x + 0.82, 2.0, w - 0.95, 0.6, [(judul, 15, True, WHITE), (waktu, 10.5, True, GOLD)], after=1)
    text(s, x + 0.2, 2.8, w - 0.4, 1.9, [isi], size=11.5, color=SOFT)
    pill(s, x + 0.15, 4.75, w - 0.3, 0.48, hasil, size=10)
c = card(s, ML, 5.6, CW, 1.15, fill=PANEL, line=GOLD)
text(s, 0, 0, 0, 0, ["**Mengapa satu kali kelas ditambah pendampingan satu bulan?** Kemampuan closing terbentuk saat membalas chat sungguhan, bukan di kelas. Workshop menyamakan cara kerja seluruh tim. Setelah itu kami memeriksa chat asli setiap minggu dan memberi masukan, sehingga perbaikan terjadi pada pekerjaan sehari-hari."], size=12.5, anchor="m", box=c)

# 7. Gambaran workshop
s = slide("Gambaran workshop", "Enam sesi, sebagian besar waktunya untuk praktik")
sesi_ringkas = [
    ("08.45 - 09.15", "Target bulanan menjadi pegangan harian", "Target harian setiap CS"),
    ("09.15 - 09.50", "Bertanya dulu, baru memberi harga", "Daftar pertanyaan tim"),
    ("09.50 - 10.30", "Menyusun chat penawaran lima langkah", "Contoh chat versi tim"),
    ("10.45 - 11.30", "Menjawab keraguan pelanggan", "Kumpulan jawaban terbaik"),
    ("11.30 - 12.05", "Follow-up sampai memesan", "Jadwal dan contoh pesan follow-up"),
    ("12.05 - 12.30", "Siap menjalani pendampingan", "Catatan calon pelanggan, komitmen, kartu saku"),
]
w = (CW - 0.4) / 3
for i, (jam, judul, hasil) in enumerate(sesi_ringkas):
    x, y = ML + (i % 3) * (w + 0.2), 1.9 + (i // 3) * 2.2
    card(s, x, y, w, 2.0, fill=TEAL)
    text(s, x + 0.22, y + 0.18, w - 0.4, 0.3, [("SESI " + str(i + 1) if i < 5 else "PENUTUP", 10.5, True, GOLD)])
    text(s, x + 0.22, y + 0.45, w - 0.4, 0.8, [judul], size=15, bold=True)
    text(s, x + 0.22, y + 1.15, w - 0.4, 0.3, [jam + " WIB"], size=10.5, color=SOFT)
    pill(s, x + 0.15, y + 1.45, w - 0.3, 0.4, hasil, size=10)
text(s, ML, 6.42, CW, 0.4, ["Bahan latihan diambil dari chat Al Kautsar sendiri yang sudah disamarkan, sehingga peserta berlatih dengan kasus yang mereka temui setiap hari."], size=11.5, color=MUTED)

# 8 - 13. Rincian sesi
SESI = [
    ("Sesi 1", "Target bulanan menjadi pegangan harian", "08.45 - 09.15 WIB, 30 menit",
     "Cara menghitung berapa chat yang perlu ditangani dan berapa pesanan yang perlu didapat setiap hari supaya target bulanan tercapai.",
     ["Trainer menampilkan perjalanan seorang calon pelanggan, dari chat pertama sampai membayar lunas, dengan angka tim Al Kautsar sendiri.",
      "Sebelum angkanya dibuka, setiap CS menebak berapa dari 10 chat yang biasanya menjadi pesanan. Tebakan dibandingkan dengan angka sebenarnya.",
      "Setiap CS menghitung target hariannya di lembar hitung sederhana, lalu saling memeriksa dengan teman sebelah."],
     "Lembar hitung, kalkulator di ponsel, kertas plano, spidol.",
     "Setiap CS tahu jumlah chat dan pesanan yang perlu dicapai per hari."),
    ("Sesi 2", "Bertanya dulu, baru memberi harga", "09.15 - 09.50 WIB, 35 menit",
     "Cara menggali kebutuhan keluarga lewat chat sebelum mengirim harga, supaya penawaran tepat sasaran.",
     ["Permainan Pelanggan yang Tidak Terlihat. Satu peserta memakai penutup mata dan menebak paket yang diinginkan temannya hanya dengan bertanya. Begitulah keadaan CS sehari-hari: tidak melihat pelanggannya, jadi pertanyaan yang baik adalah cara utama memahami kebutuhan.",
      "Dua kelompok membedah tiga contoh chat nyata yang disamarkan, lalu menempelkan stiker di titik tempat calon pelanggan berhenti membalas.",
      "Latihan berpasangan. Satu orang berperan sebagai keluarga dengan kartu profil, satu sebagai CS yang memakai enam pertanyaan kunci. Peran ditukar setelah 5 menit."],
     "Penutup mata, kartu gambar paket, contoh chat tercetak, stiker penanda warna, kartu profil keluarga.",
     "Daftar pertanyaan yang disepakati tim untuk setiap chat baru."),
    ("Sesi 3", "Menyusun chat penawaran lima langkah", "09.50 - 10.30 WIB, 40 menit",
     "Alur chat lima langkah: sapa, gali kebutuhan, rekomendasikan satu paket, jawab keraguan, lalu ajak memesan.",
     ["Trainer menampilkan satu chat yang berhasil menjadi pesanan dan membahasnya langkah demi langkah.",
      "Peserta memilihkan satu paket untuk tiga contoh keluarga yang berbeda, lengkap dengan satu kalimat alasannya.",
      "Setiap CS menulis ulang satu chat nyata yang gagal, lalu bertukar dengan teman untuk dicek memakai daftar lima langkah. Dua hasil terbaik dibacakan."],
     "Contoh chat tercetak, kartu profil keluarga, daftar paket dan harga Al Kautsar, ponsel peserta.",
     "Contoh chat lima langkah versi tim Al Kautsar."),
    ("Sesi 4", "Menjawab keraguan pelanggan", "10.45 - 11.30 WIB, 45 menit",
     "Pola akui, tanya, jawab, ajak untuk empat keraguan yang paling sering muncul: harga, ingin membandingkan, menunda, dan menunggu keputusan keluarga.",
     ["Trainer mengenalkan pola menjawab dengan satu contoh untuk setiap keraguan. Diskon diletakkan sebagai pilihan terakhir.",
      "Bermain peran bertiga: CS, pelanggan yang memegang kartu keraguan, dan pengamat. Tiga putaran sehingga setiap orang mencoba semua peran. Supervisor ikut mengamati.",
      "Jawaban terbaik dari setiap kelompok dikumpulkan menjadi pegangan bersama tim."],
     "Kartu keraguan pelanggan, pengatur waktu dan bel, lembar pengamatan, kertas plano.",
     "Kumpulan jawaban terbaik untuk empat keraguan pelanggan."),
    ("Sesi 5", "Follow-up sampai memesan", "11.30 - 12.05 WIB, 35 menit",
     "Kapan dan bagaimana menghubungi kembali calon pelanggan yang belum memutuskan, lewat chat maupun telepon.",
     ["Peserta menyusun jadwal follow-up untuk tiga calon pelanggan contoh, dihitung dari chat pertama dan tanggal aqiqah.",
      "Setiap CS menulis tiga pesan follow-up: pengingat ringan, info penguat, dan ajakan memesan.",
      "Latihan berpasangan menelepon calon pelanggan yang tidak membalas chat, masing-masing dua menit."],
     "Kalender kertas, catatan tempel, ponsel peserta, pengatur waktu.",
     "Jadwal follow-up serta contoh pesan dan percakapan telepon."),
    ("Penutup", "Siap menjalani pendampingan", "12.05 - 12.30 WIB, 25 menit",
     "Cara mencatat calon pelanggan setiap hari dan aturan main pendampingan selama satu bulan.",
     ["Setiap CS mencoba mengisi catatan calon pelanggan di Google Sheets lewat ponselnya.",
      "Setiap CS menuliskan tiga kebiasaan yang akan diterapkan selama sebulan. Supervisor menyimpan catatan ini untuk dicek setiap minggu.",
      "Sesi ditutup dengan kuis singkat, survei kepuasan, dan pembagian kartu saku CS."],
     "Ponsel peserta, kartu komitmen, kartu saku CS.",
     "Catatan calon pelanggan siap dipakai dan tiga komitmen dari setiap CS."),
]
for kode, judul, waktu, belajar, kegiatan, alat, hasil in SESI:
    s = slide(f"Rincian {kode.lower()}  •  {waktu}", f"{kode}. {judul}")
    # kiri: yang dipelajari
    c = card(s, ML, 1.85, 5.15, 2.35, fill=PANEL, line=TEAL)
    text(s, ML + 0.25, 2.02, 4.7, 0.3, [("YANG DIPELAJARI", 10.5, True, GOLD)])
    text(s, ML + 0.25, 2.38, 4.7, 1.75, [belajar], size=13.5)
    # kiri bawah: alat dan media, hasil
    c = card(s, ML, 4.35, 2.5, 2.35, fill=TEAL)
    text(s, ML + 0.22, 4.5, 2.1, 0.3, [("ALAT DAN MEDIA", 10, True, GOLD)])
    text(s, ML + 0.22, 4.85, 2.1, 1.8, [alat], size=11.5)
    c = card(s, ML + 2.65, 4.35, 2.5, 2.35, fill=GOLD, line=None)
    text(s, ML + 2.87, 4.5, 2.1, 0.3, [("HASIL", 10, True, NAVY)])
    text(s, ML + 2.87, 4.85, 2.1, 1.8, [hasil], size=12, bold=True, color=NAVY)
    # kanan: kegiatan
    x0, w0 = ML + 5.4, CW - 5.4
    card(s, x0, 1.85, w0, 4.85, fill=PANEL, line=TEAL)
    text(s, x0 + 0.25, 2.02, w0 - 0.5, 0.3, [("KEGIATANNYA", 10.5, True, GOLD)])
    y = 2.45
    for i, k in enumerate(kegiatan):
        circle(s, x0 + 0.25, y, 0.42, str(i + 1), size=12)
        tb = text(s, x0 + 0.85, y - 0.02, w0 - 1.15, 1.4, [k], size=12.5, spacing=1.12)
        lines = max(1, round(len(k) / 62 + 0.49))
        y += 0.32 * lines + 0.42

# 14. Kartu saku
s = slide("Contoh alat yang dibawa pulang", "Kartu saku CS: lima langkah di samping ponsel kerja")
picture(s, "kartu-saku-depan.png", 6.2, 1.75, h=5.05)
picture(s, "kartu-saku-belakang.png", 9.85, 1.75, h=5.05)
text(s, ML, 1.85, 5.2, 4.8, [
    "Setiap CS menerima satu kartu saku berukuran A6.",
    "**Sisi depan:** lima langkah chat closing beserta contoh kalimat dalam bentuk chat.",
    "**Sisi belakang:** enam pertanyaan sebelum memberi harga, cara menjawab empat keraguan pelanggan, dan jadwal follow-up.",
    ("Isi final disusun dari chat dan daftar paket Al Kautsar setelah tahap mengenal tim.", 12, False, MUTED),
], size=14.5, after=14)

# 15. Pendampingan
s = slide("Pendampingan satu bulan", "Ritme tetap setiap minggu, fokusnya bertambah")
ritme = [("Senin", "Pendamping dan Supervisor membahas rekap, menentukan satu fokus perbaikan"),
         ("Senin, Rabu, Jumat", "Materi singkat dan tantangan praktik di grup CS"),
         ("Setiap hari", "CS mencatat calon pelanggan. Supervisor memimpin rapat 10 menit"),
         ("Jumat", "Pendamping memeriksa 3 chat acak dari setiap CS dan mengirim rekap mingguan")]
w = (CW - 0.6) / 4
for i, (hari, isi) in enumerate(ritme):
    x = ML + i * (w + 0.2)
    card(s, x, 1.85, w, 1.55, fill=TEAL)
    text(s, x + 0.2, 1.98, w - 0.4, 0.3, [(hari, 12.5, True, GOLD)])
    text(s, x + 0.2, 2.35, w - 0.4, 1.0, [isi], size=11.5)
grid(s, ML, 3.6, [1.6, (CW - 1.6) / 2, (CW - 1.6) / 2], [
    ["Minggu 1", "Menyapa, menggali kebutuhan, dan rajin mencatat calon pelanggan", "Membagi target tim ke setiap CS dan memulai rapat harian 10 menit"],
    ["Minggu 2", "Memperbaiki langkah yang paling sering terlewat pada pemeriksaan minggu pertama", "Bimbingan pribadi dengan setiap CS memakai contoh chatnya sendiri"],
    ["Minggu 3", "Menjawab keraguan dan follow-up tepat waktu", "Membaca penyebab target meleset: jumlah chat, cara membalas, atau follow-up"],
    ["Minggu 4", "Mengajak memesan dan merapikan seluruh lima langkah", "Menyusun target dan kebiasaan tim untuk bulan berikutnya"],
], header=["Minggu", "Fokus tim CS", "Fokus Supervisor"], row_h=0.66, size=12)

# 16. Cara mengukur hasil
s = slide("Cara kami mengukur hasil", "Tiga titik pemeriksaan hasil")
ukur = [("Hari workshop", "Kuis singkat di awal dan akhir sesi, serta hasil latihan menulis chat", "Nilai kuis naik, dan sebagian besar CS bisa menulis chat lima langkah dengan lengkap"),
        ("Setiap minggu", "Contoh chat nyata yang kami pilih acak dan catatan follow-up tim", "Makin banyak chat mengikuti lima langkah. Pada minggu ke-4, minimal 7 dari 10 chat"),
        ("Akhir bulan", "Persentase chat yang menjadi DP atau lunas, dibandingkan dengan sebelum program", "Target disepakati setelah kondisi awal diketahui [ISI TIM: target]")]
w = (CW - 0.4) / 3
for i, (kapan, lihat, tanda) in enumerate(ukur):
    x = ML + i * (w + 0.2)
    card(s, x, 1.85, w, 3.75, fill=PANEL, line=TEAL)
    pill(s, x + 0.2, 1.65, 2.2, 0.42, kapan)
    text(s, x + 0.25, 2.3, w - 0.5, 0.3, [("YANG KAMI LIHAT", 10, True, GOLD)])
    text(s, x + 0.25, 2.62, w - 0.5, 1.2, [lihat], size=12.5)
    text(s, x + 0.25, 3.85, w - 0.5, 0.3, [("TANDA BERHASIL", 10, True, GOLD)])
    text(s, x + 0.25, 4.17, w - 0.5, 1.3, [tanda], size=12.5, bold=True)
c = card(s, ML, 5.85, CW, 0.9, fill=PANEL, line=GOLD)
text(s, 0, 0, 0, 0, ["**Catatan jujur soal batas.** Penjualan juga dipengaruhi jumlah calon pelanggan dari iklan, harga, dan musim. Karena itu yang kami bandingkan adalah persentase chat yang menjadi pesanan, bukan hanya total omzet. Kami tidak menjanjikan kenaikan penjualan dalam angka tertentu."], size=12, anchor="m", box=c)

# 17. Yang dibawa pulang
s = slide("Yang dibawa pulang", "Tujuh hasil yang langsung dipakai tim")
items = [("Target harian setiap CS", "Pegangan jumlah chat dan pesanan per hari, dicek di rapat harian"),
         ("Daftar pertanyaan dan contoh chat", "Cara membalas yang sama untuk seluruh CS"),
         ("Jawaban keraguan pelanggan", "Siap pakai, terus ditambah selama pendampingan"),
         ("Jadwal dan pesan follow-up", "Calon pelanggan tidak terlewat"),
         ("Kartu saku CS", "Pengingat lima langkah di samping ponsel kerja"),
         ("Catatan calon pelanggan", "Google Sheets, dasar rekap mingguan dan keputusan Supervisor"),
         ("Rekap mingguan dan laporan akhir", "Perkembangan tim dan saran untuk bulan berikutnya")]
w = (CW - 0.6) / 4
for i, (judul, guna) in enumerate(items):
    x, y = ML + (i % 4) * (w + 0.2), 1.9 + (i // 4) * 2.35
    card(s, x, y, w, 2.15, fill=TEAL)
    text(s, x + 0.2, y + 0.2, w - 0.4, 0.8, [judul], size=14, bold=True)
    text(s, x + 0.2, y + 1.05, w - 0.4, 1.0, [guna], size=11.5, color=WHITE)

# 18. Susunan acara
s = slide("Susunan acara workshop", "Rundown 4 jam, 08.30 - 12.30 WIB")
grid(s, ML, 1.85, [2.0, 1.45, 5.6, CW - 9.05], [
    ["08.15 - 08.30", "15 menit", "Registrasi dan pengalihan chat", "Tim Sanggabiz"],
    ["08.30 - 08.45", "15 menit", "Pembukaan oleh pemilik dan kuis awal", "Pemilik, trainer"],
    ["08.45 - 09.15", "30 menit", "**Sesi 1.** Target bulanan menjadi pegangan harian", "Trainer"],
    ["09.15 - 09.50", "35 menit", "**Sesi 2.** Bertanya dulu, baru memberi harga", "Trainer"],
    ["09.50 - 10.30", "40 menit", "**Sesi 3.** Menyusun chat penawaran lima langkah", "Trainer"],
    ["10.30 - 10.45", "15 menit", "Istirahat", ""],
    ["10.45 - 11.30", "45 menit", "**Sesi 4.** Menjawab keraguan pelanggan", "Trainer, Supervisor sebagai pengamat"],
    ["11.30 - 12.05", "35 menit", "**Sesi 5.** Follow-up sampai memesan", "Trainer"],
    ["12.05 - 12.30", "25 menit", "**Penutup.** Siap menjalani pendampingan", "Trainer, pendamping"],
], header=["Waktu (WIB)", "Durasi", "Kegiatan", "Pemandu"], row_h=0.44, size=12)
text(s, ML, 6.45, CW, 0.4, ["Jam dapat digeser mengikuti jam sepi chat. Urutan dan durasi setiap sesi tetap sama. Selama workshop, chat dialihkan ke pesan otomatis atau petugas cadangan."], size=11, color=MUTED)

# 19. Investasi
s = slide("Investasi", "Skema kemitraan untuk acara Sanggabiz 7 November 2026")
for i, (lbl, nilai, ket) in enumerate([("NILAI PROGRAM", "Rp 7.500.000", "Mengenal tim, workshop 4 jam, pendampingan 4 minggu, kartu saku, dan laporan akhir"),
                                        ("NILAI KEMITRAAN", "Rp 5.500.000", "Dibayar dengan konsumsi dan biaya tunai di bawah ini")]):
    x = ML + i * 6.1
    c = card(s, x, 1.85, 5.9, 1.65, fill=TEAL if i == 0 else GOLD, line=None if i else WHITE)
    col = WHITE if i == 0 else NAVY
    text(s, x + 0.3, 2.0, 5.3, 1.4, [(lbl, 10.5, True, GOLD if i == 0 else NAVY), (nilai, 26, True, col), (ket, 11.5, False, col)], after=3)
w = (CW - 0.4) / 3
for i, (lbl, nilai, ket) in enumerate([
    ("Konsumsi acara Sanggabiz", "Rp 3.500.000", ["Makan dan snack untuk 50 orang, 7 November 2026.", "Menu dan jumlah disepakati bersama."]),
    ("Biaya pelatihan tunai", "Rp 2.000.000", ["Rp 1.000.000 saat konfirmasi, paling lambat 5 November 2026.", "Rp 1.000.000 setelah workshop."]),
    ("Dukungan publikasi", "Tanpa biaya", ["Izin dokumentasi dan testimoni untuk publikasi Sanggabiz.", "[ISI TIM: pertahankan atau hapus]"]),
]):
    x = ML + i * (w + 0.2)
    card(s, x, 3.75, w, 2.45, fill=PANEL, line=TEAL)
    text(s, x + 0.25, 3.92, w - 0.5, 2.2, [(lbl.upper(), 10, True, GOLD), (nilai, 19, True, WHITE)] + [(k, 11.5, False, SOFT) for k in ket], after=5)
text(s, ML, 6.42, CW, 0.4, ["Nilai konsumsi mengikuti harga jual menu dan jumlah yang disepakati. Belum termasuk pajak bila berlaku dan biaya perjalanan ke luar DIY. Data Al Kautsar dijaga kerahasiaannya."], size=10.5, color=MUTED)

# 20. Yang disiapkan
s = slide("Ketentuan", "Yang perlu disiapkan Al Kautsar dan yang di luar program")
for i, (lbl, isi) in enumerate([
    ("Disiapkan Al Kautsar", ["Contoh chat dan data penjualan paling lambat tiga hari sebelum workshop.", "Seluruh CS dan Supervisor ikut workshop penuh selama 4 jam.", "Ruang, layar atau TV, dan colokan listrik.", "**Setiap CS mencatat calon pelanggan setiap hari selama empat minggu.** Catatan ini dasar rekap dan laporan.", "Satu orang manajemen untuk memutuskan target dan pembagian penjualan per CS."]),
    ("Di luar program ini", ["Pengelolaan iklan dan jumlah calon pelanggan yang masuk.", "Pembelian atau pemasangan aplikasi CRM berbayar.", "Penetapan skema komisi. Kami memberi masukan, keputusan ada di manajemen.", "Pendampingan lebih dari empat minggu."]),
]):
    x, w = (ML, 7.0) if i == 0 else (ML + 7.2, CW - 7.2)
    card(s, x, 2.05, w, 4.6, fill=PANEL if i == 0 else TEAL, line=WHITE)
    pill(s, x + 0.3, 1.82, 3.0, 0.44, lbl)
    text(s, x + 0.3, 2.5, w - 0.6, 4.0, [f"•  {t}" for t in isi], size=13, after=10)

# 21. Trainer dan Sanggabiz
s = slide("Tim dan Sanggabiz", "Trainer, pendamping, dan Sanggabiz")
card(s, ML, 1.85, 6.0, 4.85, fill=PANEL, line=TEAL)
text(s, ML + 0.3, 2.0, 5.4, 0.3, [("TRAINER DAN PENDAMPING", 10.5, True, GOLD)])
text(s, ML + 0.3, 2.4, 5.4, 4.2, [
    "[ISI TIM: nama dan gelar]",
    "[ISI TIM: jabatan dan instansi]",
    ("Pengalaman penjualan atau CS: [ISI TIM: lama pengalaman, jenis usaha, ukuran tim]", 12),
    ("Pengalaman melatih: [ISI TIM: program dan klien yang relevan]", 12),
    ("**Kriteria kami:** pernah menjual atau memimpin tim penjualan lewat chat dan telepon, pernah melatih tim CS atau penjualan, dan terbiasa membaca angka penjualan sederhana.", 12, False, SOFT),
], size=14, after=10)
x0 = ML + 6.2
text(s, x0, 1.9, CW - 6.2, 1.4, ["Sanggabiz menyediakan layanan department-as-a-service: keuangan, sumber daya manusia, layanan pelanggan, pemasaran, manajemen proyek, administrasi, dan operasional. Layanan pelanggan termasuk pekerjaan yang kami jalankan sehari-hari untuk klien."], size=12.5, color=SOFT)
for i, (big, small) in enumerate([("400+", "proyek dan layanan"), ("500+", "pakar dan trainer"), ("6.000+", "mitra engagement")]):
    w = (CW - 6.2 - 0.4) / 3
    x = x0 + i * (w + 0.2)
    c = card(s, x, 3.45, w, 1.3, fill=TEAL)
    text(s, 0, 0, 0, 0, [(big, 22, True, GOLD), (small, 10.5, True, WHITE)], align="c", anchor="m", box=c, after=2)
fr = shape(s, x0 - 0.04, 4.96, CW - 6.2 + 0.08, 1.78, fill=WHITE)
picture(s, "foto-pelatihan-1.jpg", x0, 5.0, w=(CW - 6.2) / 2 - 0.05, h=1.7)
picture(s, "foto-pelatihan-2.jpg", x0 + (CW - 6.2) / 2 + 0.05, 5.0, w=(CW - 6.2) / 2 - 0.05, h=1.7)

# 22. Langkah berikutnya
s = slide("Langkah berikutnya", "Siap memulai bersama tim Aqiqah Al Kautsar", footer=True)
langkah = [("s.d. 5 Nov", "Konfirmasi kerja sama, pembayaran pertama, menu dan jumlah konsumsi"),
           ("7 Nov", "Makan dan snack 50 orang untuk acara Sanggabiz"),
           ("9 - 13 Nov", "Mengenal tim"),
           ("16 - 21 Nov", "Workshop 4 jam dan pembayaran kedua"),
           ("23 Nov - 18 Des", "Pendampingan empat minggu"),
           ("Setelahnya", "Laporan akhir, paling lambat 5 hari kerja")]
w = (CW - 1.0) / 6
for i, (tgl, isi) in enumerate(langkah):
    x = ML + i * (w + 0.2)
    card(s, x, 1.95, w, 2.6, fill=PANEL, line=TEAL)
    circle(s, x + w / 2 - 0.25, 2.1, 0.5, str(i + 1), size=13)
    text(s, x + 0.15, 2.75, w - 0.3, 0.4, [tgl], size=12.5, bold=True, color=GOLD, align="c")
    text(s, x + 0.15, 3.2, w - 0.3, 1.3, [isi], size=11, align="c")
picture(s, "logo_white.png", ML, 4.95, w=2.2)
for i, t in enumerate(["www.sanggabiz.com", "partnership@sanggabiz.com", "WhatsApp 0877-7413-4288"]):
    pl = shape(s, ML + i * (CW / 3 + 0.0) + (0.1 if i else 0), 5.65, CW / 3 - 0.2, 0.5, fill=PANEL, line=WHITE, lw=1.25, r=0.25)
    text(s, 0, 0, 0, 0, [t], size=12.5, bold=True, align="c", anchor="m", box=pl)
text(s, ML, 6.35, CW, 0.3, ["Kontak program: [ISI TIM: nama, jabatan, nomor WhatsApp]"], size=11.5, color=SOFT)

prs.save(OUT)
print("ditulis:", os.path.abspath(OUT), "slide:", len(prs.slides))
