"""Membuat deck silabus dan alat bantu dua pelatihan pest control.

Bentuk halaman mengikuti deck acuan `reference/format-standar/05-silabus-dan-alat-bantu-IHT-Asia-Pramulia.pptx`
(kepala logo, garis ungu, judul kapital Montserrat, tabel teal, kartu alur, slide contoh alat bantu).

Pemakaian:
    python3 pest-control/_build/build_alat_bantu.py   (lembar kerja Excel)
    python3 pest-control/_build/build_deck.py         (deck ini, memakai gambar di _build/assets)
"""
import re
from pathlib import Path

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "_build" / "assets"
OUT = ROOT / "proposal" / "v1 Silabus dan Alat Bantu - Customer Retention dan Sales Leadership - Pest Control.pptx"

KLIEN = "[ISI TIM: nama perusahaan]"

TEAL = "15908F"
CYAN = "34BDCF"
NAVY = "13314F"
KARTU = "145B78"
UNGU = "8B5CF6"
TEKS = "111111"
ABU = "333333"
MONT = "Montserrat"
INTER = "Inter"

X0 = 609600
W0 = 10972800

prs = Presentation()
prs.slide_width = Emu(12192000)
prs.slide_height = Emu(6858000)
BLANK = prs.slide_layouts[6]


# ---------------------------------------------------------------------------
# Dasar teks
# ---------------------------------------------------------------------------
def pecah_isi_tim(teks):
    """Memecah teks agar bagian [ISI TIM: ...] diberi stabilo kuning."""
    hasil = []
    for bagian in re.split(r"(\[ISI TIM:[^\]]*\])", teks):
        if bagian:
            hasil.append((bagian, bagian.startswith("[ISI TIM")))
    return hasil


def tulis_run(p, teks, size, bold=False, italic=False, color=TEKS, font=INTER):
    for isi, stabilo in pecah_isi_tim(teks):
        r = p.add_run()
        r.text = isi
        f = r.font
        f.size = Emu(int(size * 127))  # size dalam seperseratus poin
        f.bold = bold
        f.italic = italic
        f.color.rgb = RGBColor.from_string(color)
        f.name = font
        if stabilo:
            rpr = r._r.get_or_add_rPr()
            hl = etree.SubElement(rpr, qn("a:highlight"))
            clr = etree.SubElement(hl, qn("a:srgbClr"))
            clr.set("val", "FFFF00")
            sf = rpr.find(qn("a:solidFill"))
            sf.addnext(hl)


def paragraf(tf, runs, align=PP_ALIGN.LEFT, spacing=1.1, pertama=False):
    p = tf.paragraphs[0] if pertama else tf.add_paragraph()
    p.alignment = align
    p.line_spacing = spacing
    for r in runs:
        teks, size = r[0], r[1]
        opsi = r[2] if len(r) > 2 else {}
        tulis_run(p, teks, size, **opsi)
    return p


def kotak_teks(slide, x, y, w, h, daftar, anchor=MSO_ANCHOR.TOP, autofit=True):
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    if autofit:
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    for i, (runs, align, spacing) in enumerate(daftar):
        paragraf(tf, runs, align, spacing, pertama=(i == 0))
    return tb


def bentuk(slide, jenis, x, y, w, h, isi, garis=None, tebal=None):
    s = slide.shapes.add_shape(jenis, Emu(x), Emu(y), Emu(w), Emu(h))
    if jenis == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.08
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor.from_string(isi)
    if garis:
        s.line.color.rgb = RGBColor.from_string(garis)
        s.line.width = Emu(tebal or 12700)
    else:
        s.line.fill.background()
    st = s._element.find(qn("p:style"))
    if st is not None:
        s._element.remove(st)
    return s


# ---------------------------------------------------------------------------
# Kerangka halaman
# ---------------------------------------------------------------------------
def halaman(judul, sub):
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(str(ASSET / "logo_warna.png"), Emu(X0), Emu(257175), Emu(1444803), Emu(285750))
    kotak_teks(s, 10477500, 295275, 1104900, 228600,
               [([("2026", 1300, {"bold": True, "font": MONT})], PP_ALIGN.RIGHT, 1.1)])
    bentuk(s, MSO_SHAPE.RECTANGLE, X0, 790575, W0, 19050, UNGU)
    kotak_teks(s, X0, 990600, W0, 381000,
               [([(judul, 2250, {"bold": True, "font": MONT})], PP_ALIGN.CENTER, 1.1)])
    kotak_teks(s, X0, 1352550, W0, 190500,
               [([(sub, 1000, {"color": ABU})], PP_ALIGN.CENTER, 1.1)])
    bentuk(s, MSO_SHAPE.RECTANGLE, X0, 6257925, W0, 14287, "222222")
    for x, ikon, teks, w in ((609600, "wa.png", "0877-7413-4288", 2000250),
                             (5095875, "web.png", "www.sanggabiz.com", 2000250),
                             (8858250, "mail.png", "partnership@sanggabiz.com", 2724150)):
        bentuk(s, MSO_SHAPE.OVAL, x, 6438900, 247650, 247650, CYAN)
        s.shapes.add_picture(str(ASSET / ikon), Emu(x + 47625), Emu(6486525), Emu(152400), Emu(152400))
        kotak_teks(s, x + 333375, 6467475, w, 190500,
                   [([(teks, 1050, {"bold": True, "font": MONT})], PP_ALIGN.LEFT, 1.1)],
                   anchor=MSO_ANCHOR.MIDDLE)
    return s


def catatan(s, y, h, label, isi):
    bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, X0, y, W0, h, "FBF3FE", "E2A9F1", 9525)
    kotak_teks(s, 800100, y + 54864, 10591800, h - 109728,
               [([(label + " ", 1050, {"bold": True}), (isi, 1050)], PP_ALIGN.LEFT, 1.2)],
               anchor=MSO_ANCHOR.MIDDLE)


def kartu(s, x, y, w, h, judul, butir, size=1050, spasi=1.6):
    bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, "FFFFFF", "D6E4E7", 12700)
    bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, 419100, KARTU)
    bentuk(s, MSO_SHAPE.RECTANGLE, x, y + 228600, w, 190500, KARTU)
    kotak_teks(s, x + 128016, y, w - 256033, 419100,
               [([(judul, 1150, {"bold": True, "color": "FFFFFF", "font": MONT})], PP_ALIGN.LEFT, 1.1)],
               anchor=MSO_ANCHOR.MIDDLE)
    kotak_teks(s, x + 128016, y + 571500, w - 256033, h - 640080,
               [([("•  ", size, {"bold": True, "color": TEAL}), (b, size)], PP_ALIGN.LEFT, spasi) for b in butir])


def statistik(s, y, kotak):
    lebar_k = 3568700
    for i, (angka, label, teks) in enumerate(kotak):
        x = X0 + i * (lebar_k + 133350)
        bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, lebar_k, 590550, "ECF6F7")
        kotak_teks(s, x + 133350, y + 76200, 1238250, 438150,
                   [([(angka, 1600, {"bold": True, "color": TEAL, "font": MONT})], PP_ALIGN.LEFT, 1.1),
                    ([(label, 750, {"bold": True, "color": NAVY, "font": MONT})], PP_ALIGN.LEFT, 1.1)],
                   anchor=MSO_ANCHOR.MIDDLE)
        kotak_teks(s, x + 1428750, y + 57150, 2025650, 476250,
                   [([(teks, 860)], PP_ALIGN.LEFT, 1.15)], anchor=MSO_ANCHOR.MIDDLE)


# ---------------------------------------------------------------------------
# Tabel
# ---------------------------------------------------------------------------
def isi_sel(cell, paragraf_sel, fill):
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor.from_string(fill)
    cell.margin_left = cell.margin_right = Emu(57150)
    cell.margin_top = cell.margin_bottom = Emu(38100)
    tf = cell.text_frame
    tf.word_wrap = True
    for i, runs in enumerate(paragraf_sel):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        for r in runs:
            opsi = r[2] if len(r) > 2 else {}
            tulis_run(p, r[0], r[1], **opsi)
        # Ukuran akhir paragraf disamakan agar sel kosong tidak memakai 18 pt bawaan.
        end = etree.SubElement(p._p, qn("a:endParaRPr"))
        end.set("sz", str(runs[0][1]))


def tabel(s, x, y, lebar_kolom, tinggi_baris, baris, isi_baris):
    """baris: daftar baris, tiap baris daftar sel, tiap sel daftar paragraf (daftar run)."""
    gf = s.shapes.add_table(len(baris), len(lebar_kolom), Emu(x), Emu(y),
                            Emu(sum(lebar_kolom)), Emu(sum(tinggi_baris)))
    t = gf.table
    t.first_row = False
    t.horz_banding = False
    for i, w in enumerate(lebar_kolom):
        t.columns[i].width = Emu(w)
    for i, h in enumerate(tinggi_baris):
        t.rows[i].height = Emu(h)
    for r, sel_baris in enumerate(baris):
        for c, isi in enumerate(sel_baris):
            isi_sel(t.cell(r, c), isi, isi_baris(r, c))
    return t


def kepala_tabel(labels, size=910):
    return [[[(l, size, {"bold": True, "color": "FFFFFF"})]] for l in labels]


# ---------------------------------------------------------------------------
# Jenis halaman
# ---------------------------------------------------------------------------
def halaman_ringkasan_program(judul, sub, pengantar, kotak, rundown):
    s = halaman(judul, sub)
    kotak_teks(s, 1809750, 1562100, 8572500, 342900,
               [([(pengantar, 980)], PP_ALIGN.CENTER, 1.2)])
    statistik(s, 2019300, kotak)
    baris = [kepala_tabel(["Waktu (WIB)", "Kegiatan", "Yang terjadi"], 819)]
    jeda = []
    for i, (w, k, y) in enumerate(rundown, 1):
        if y is None:
            jeda.append(i)
            baris.append([[[(w, 819, {"italic": True, "color": "777777"})]],
                          [[(k, 819, {"bold": True, "italic": True, "color": "777777"})]],
                          [[("", 819)]]])
        else:
            baris.append([[[(w, 819)]], [[(k, 819, {"bold": True})]], [[(y, 819)]]])

    def warna(r, c):
        if r == 0:
            return TEAL
        return "FAFAFA" if r in jeda else "FFFFFF"

    tabel(s, X0, 2743200, [1316736, 4169664, 5486400], [228600] + [228600] * len(rundown), baris, warna)
    return s


def halaman_alur(judul, sub, sesi, kasus):
    s = halaman(judul, sub)
    w = 2633472
    for i, (j, butir) in enumerate(sesi):
        kartu(s, 612648 + i * 2779776, 1676400, w, 2697480, j, butir)
    catatan(s, 4553712, 868680, "Kasus pelatihan.", kasus)
    return s


def sel_topik(no, judul, waktu):
    return [[(f"Topik {no}", 919, {"bold": True, "color": TEAL, "font": MONT})],
            [(judul, 1000, {"bold": True, "color": NAVY, "font": MONT})],
            [(waktu, 819, {"color": "335555"})]]


def sel_label(pasangan, size=860):
    return [[(lbl + " ", size, {"bold": True, "color": TEAL}), (isi, size)] for lbl, isi in pasangan]


def halaman_sesi(judul, topik):
    s = halaman(judul, "Tujuan, yang dipelajari, kegiatan peserta di Zoom, dan hasil yang bisa diukur.")
    baris = [kepala_tabel(["Topik", "Tujuan dan yang dipelajari", "Kegiatan peserta", "Alat dan media", "Hasil"])]
    for t in topik:
        dipelajari = [[("Tujuan: ", 860, {"bold": True, "color": TEAL}), (t["tujuan"], 860)]]
        dipelajari += [[("• " + b, 860)] for b in t["materi"]]
        kegiatan = [[("• " + b, 860)] for b in t["kegiatan"]]
        baris.append([
            sel_topik(t["no"], t["judul"], t["waktu"]),
            dipelajari,
            kegiatan,
            sel_label([("Alat:", t["alat"]), ("Media:", t["media"])]),
            sel_label([("Output:", t["output"]), ("Ukuran:", t["ukuran"])]),
        ])

    def warna(r, c):
        if r == 0:
            return TEAL
        if c == 0:
            return "D7ECEC"
        return "FFFFFF" if r % 2 else "F2F8F9"

    tabel(s, X0, 1638300, [1600200, 2651760, 3474720, 1554480, 1691640], [228600, 2020000, 2020000], baris, warna)
    return s


def halaman_hasil(judul, sub, kolom, fasilitator):
    s = halaman(judul, sub)
    for i, (j, butir) in enumerate(kolom):
        kartu(s, X0 + i * 3714750, 1676400, 3543300, 2857500, j, butir)
    catatan(s, 4705350, 666750, "Satu trainer dan satu host Zoom sepanjang hari.", fasilitator)
    return s


def halaman_contoh(judul, gambar, samping):
    """gambar: daftar (label, path, x, y, lebar). samping: tiga (judul, isi)."""
    s = halaman(judul, "Lembar kerja Excel yang dipakai di kelas dan dibawa pulang peserta. "
                       "Angka di dalamnya adalah data kasus latihan.")
    for label, path, x, y, w in gambar:
        im = Image.open(path)
        h = int(w * im.height / im.width)
        lw = 260000 + len(label) * 62000
        bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, lw, 209550, CYAN)
        kotak_teks(s, x, y, lw, 209550,
                   [([(label, 850, {"bold": True, "color": "FFFFFF", "font": MONT})], PP_ALIGN.CENTER, 1.1)],
                   anchor=MSO_ANCHOR.MIDDLE)
        pic = s.shapes.add_picture(str(path), Emu(x), Emu(y + 256032), Emu(w), Emu(h))
        pic.line.color.rgb = RGBColor.from_string("D6E4E7")
        pic.line.width = Emu(9525)
    for i, (j, isi) in enumerate(samping):
        y = 1645920 + i * 1545336
        bentuk(s, MSO_SHAPE.ROUNDED_RECTANGLE, 8339327, y, 3246120, 1389888, "F6FAFB")
        kotak_teks(s, 8467344, y + 73152, 2990087, 1243584,
                   [([(j, 950, {"bold": True, "color": TEAL, "font": MONT})], PP_ALIGN.LEFT, 1.25),
                    ([(isi, 910)], PP_ALIGN.LEFT, 1.25)])
    return s


# ---------------------------------------------------------------------------
# Isi
# ---------------------------------------------------------------------------
def ringkasan_dua_program():
    s = halaman("DUA PELATIHAN DARING UNTUK TIM PEST CONTROL",
                f"Customer Retention Training dan Sales Leadership Training, {KLIEN}. "
                "Via Zoom, satu hari per pelatihan, 09.00 - 16.00 WIB.")
    data = [
        ("Peserta", "7 Retention Staff", "7 Sales Leader"),
        ("Fokus", "Customer relationship management, customer loyalty, complaint handling, dan strategi "
                  "mempertahankan pelanggan",
         "Sales team leadership, sales performance management, coaching dan mentoring, dan strategi "
         "pencapaian target penjualan"),
        ("Pertanyaan yang dijawab", "Pelanggan mana yang berisiko berhenti, dan apa yang kami lakukan minggu ini?",
         "Siapa di tim yang perlu dibantu, dengan cara apa, agar target tercapai?"),
        ("Kasus latihan", "24 pelanggan kontrak cabang contoh, termasuk kafe yang mengeluh kecoa tiga kali "
                          "dalam sebulan dan kontraknya habis bulan depan",
         "Lima sales cabang contoh di minggu ke-8 kuartal, dengan capaian tim 46 persen dari target"),
        ("Alat bantu Excel", "Skor Kesehatan Pelanggan, Kalkulator Retensi dan Nilai Pelanggan, Log Keluhan",
         "Dasbor Kinerja Tim Sales, Kalkulator Target ke Aktivitas, Rencana Coaching GROW"),
        ("Hasil utama", "Rencana retensi 30 hari untuk lima pelanggan prioritas, dari setiap peserta",
         "Rencana 30-60-90 hari untuk tim dan rencana coaching satu anggota tim, dari setiap peserta"),
        ("Tanggal", "[ISI TIM: tanggal, rencana 23 - 30 November 2026]",
         "[ISI TIM: tanggal, rencana 23 - 30 November 2026]"),
    ]
    baris = [kepala_tabel(["", "Customer Retention Training", "Sales Leadership Training"])]
    for a, b, c in data:
        baris.append([[[(a, 910, {"bold": True, "color": NAVY})]], [[(b, 910)]], [[(c, 910)]]])

    def warna(r, c):
        if r == 0:
            return TEAL
        if c == 0:
            return "D7ECEC"
        return "FFFFFF" if r % 2 else "F2F8F9"

    tabel(s, X0, 1676400, [2194560, 4389120, 4389120], [256032] + [301752] * len(data), baris, warna)
    catatan(s, 4389120, 1143000, "Kelas daring yang tetap praktik.",
            "Tujuh peserta per kelas, sehingga setiap orang mendapat giliran role play di breakout room. "
            "Peserta memakai laptop dengan kamera menyala dan headset, karena latihan memakai lembar kerja "
            "dan percakapan langsung. Akun Zoom, tautan, dan bahan disiapkan Sanggabiz dan dikirim H-1. "
            "Metode: tujuan tiap topik ditulis dengan kata kerja Taksonomi Bloom, kegiatan mengikuti prinsip "
            "andragogi (belajar dari kasus kerja peserta), dan evaluasi memakai level 1 dan 2 Kirkpatrick.")


RUNDOWN_RETENSI = [
    ("09.00 - 09.20", "Pembukaan, aturan kelas Zoom, dan pre-test",
     "Peserta menyebut satu keluhan pelanggan yang paling sering diterima, lalu mengerjakan 10 soal pre-test."),
    ("09.20 - 10.30", "Sesi 1. Mengenali pelanggan: CRM dan nilai pelanggan",
     "Menghitung retensi dan nilai pelanggan, lalu memberi skor kesehatan pada 24 pelanggan kasus."),
    ("10.30 - 10.40", "Jeda layar", None),
    ("10.40 - 12.00", "Sesi 2. Menjaga loyalitas pelanggan",
     "Memetakan momen rawan pelanggan restoran dan menyusun kalender kontak 12 bulan."),
    ("12.00 - 13.00", "Istirahat, salat, dan makan siang", None),
    ("13.00 - 14.20", "Sesi 3. Complaint handling dan service recovery",
     "Role play keluhan di breakout room, lalu menelusuri akar penyebab keluhan yang berulang."),
    ("14.20 - 14.30", "Jeda layar", None),
    ("14.30 - 15.40", "Sesi 4. Strategi mempertahankan pelanggan",
     "Role play telepon perpanjangan kontrak dengan keberatan harga, lalu menyusun rencana retensi 30 hari."),
    ("15.40 - 16.00", "Post-test, survei, dan penutupan",
     "Peserta mengerjakan post-test dan menyebut satu tindakan yang dilakukan besok pagi."),
]

SESI_RETENSI = [
    ("SILABUS CUSTOMER RETENTION: SESI 1. MENGENALI PELANGGAN", [
        dict(no=1, judul="Peran Retention Staff dan Nilai Pelanggan", waktu="09.20 - 09.50 WIB",
             tujuan="peserta mampu menghitung retention rate, churn, dan nilai seumur pelanggan.",
             materi=["Biaya mencari pelanggan baru dibanding menjaga pelanggan lama",
                     "Retention rate, churn rate, dan revenue churn",
                     "Nilai seumur pelanggan (CLV) untuk kontrak pest control",
                     "Tugas Retention Staff sepanjang masa kontrak"],
             kegiatan=["10 menit. Polling Zoom: berapa pelanggan cabang yang berhenti tahun lalu?",
                       "10 menit. Paparan rumus dengan contoh kontrak restoran.",
                       "10 menit. Peserta mengisi Kalkulator Retensi dan membaca nilai yang dipertaruhkan."],
             alat="Kalkulator Retensi dan Nilai Pelanggan", media="Presentasi, polling Zoom",
             output="angka retensi, churn, dan CLV cabang contoh.",
             ukuran="minimal 6 dari 7 peserta menghitung retensi dengan benar."),
        dict(no=2, judul="Customer Relationship Management: Data dan Skor Kesehatan", waktu="09.50 - 10.30 WIB",
             tujuan="peserta mampu mengklasifikasikan risiko pelanggan dari data layanan.",
             materi=["Data minimal per pelanggan: layanan, nilai kontrak, tanggal habis, PIC, kunjungan, keluhan",
                     "Segmen: residensial, komersial F&B, industri pangan, gudang",
                     "Tanda awal pelanggan akan berhenti",
                     "Skor kesehatan dan prioritas kontak"],
             kegiatan=["10 menit. Paparan tanda awal pelanggan berhenti.",
                       "20 menit. Tiga breakout room memeriksa 8 pelanggan masing-masing dan menebak statusnya "
                       "sebelum melihat skor.",
                       "10 menit. Kelompok membandingkan tebakan dengan skor dan membahas yang meleset."],
             alat="Skor Kesehatan Pelanggan", media="Presentasi, Google Sheets bersama",
             output="daftar 6 pelanggan merah dan 4 kuning, dibawa ke Sesi 2.",
             ukuran="setiap kelompok menjelaskan alasan untuk 2 pelanggan merah."),
    ]),
    ("SILABUS CUSTOMER RETENTION: SESI 2. MENJAGA LOYALITAS", [
        dict(no=3, judul="Pendorong Loyalitas Pelanggan Pest Control", waktu="10.40 - 11.20 WIB",
             tujuan="peserta mampu memetakan momen rawan dalam perjalanan pelanggan.",
             materi=["Yang dinilai pelanggan: hama terkendali, teknisi tepat jadwal, laporan jelas, bahan aman",
                     "Kebutuhan per segmen: dokumen audit untuk pabrik pangan dan restoran, rasa aman untuk rumah",
                     "Momen rawan: kunjungan pertama, keluhan pertama, kontrak hampir habis, kenaikan harga"],
             kegiatan=["10 menit. Peserta menulis di chat satu alasan pelanggan bertahan dan satu alasan berhenti.",
                       "20 menit. Breakout room memetakan perjalanan Restoran 01 di Zoom Whiteboard dan "
                       "menandai tiga momen rawan.",
                       "10 menit. Setiap kelompok mempresentasikan petanya."],
             alat="Templat peta perjalanan pelanggan", media="Presentasi, Zoom Whiteboard",
             output="peta perjalanan pelanggan dengan tiga momen rawan per kelompok.",
             ukuran="setiap momen rawan disertai satu tindakan Retention Staff."),
        dict(no=4, judul="Komunikasi Proaktif dan Program Loyalitas", waktu="11.20 - 12.00 WIB",
             tujuan="peserta mampu menyusun kalender kontak dan pesan untuk satu segmen pelanggan.",
             materi=["Survei kepuasan singkat sesudah kunjungan",
                     "Laporan tren hama bulanan untuk pelanggan komersial",
                     "Kontak musiman sesuai pola hama di wilayah layanan",
                     "Program rujukan dan etika pesan WhatsApp"],
             kegiatan=["10 menit. Trainer menunjukkan contoh pesan WhatsApp yang membantu dan yang mengganggu.",
                       "20 menit. Peserta menyusun kalender kontak 12 bulan dan dua templat pesan untuk satu segmen.",
                       "10 menit. Dua peserta membacakan pesannya, peserta lain memberi masukan."],
             alat="Templat kalender kontak 12 bulan", media="Presentasi, Google Docs",
             output="kalender kontak dan dua templat pesan per peserta.",
             ukuran="pesan menyebut nama pelanggan, layanan, dan satu ajakan yang jelas."),
    ]),
    ("SILABUS CUSTOMER RETENTION: SESI 3. MENANGANI KELUHAN", [
        dict(no=5, judul="Complaint Handling dengan Langkah HEARD", waktu="13.00 - 13.40 WIB",
             tujuan="peserta mampu menerapkan lima langkah HEARD saat menerima keluhan lewat telepon dan WhatsApp.",
             materi=["Keluhan yang sering muncul: hama muncul lagi, teknisi terlambat, bau atau noda, tagihan",
                     "HEARD: Hear, Empathize, Apologize, Resolve, Diagnose",
                     "Kalimat yang meredakan dan kalimat yang memancing marah",
                     "Hanya menjanjikan yang bisa dipenuhi tim operasional"],
             kegiatan=["10 menit. Trainer memeragakan satu telepon keluhan dua kali: cara keliru dan cara HEARD.",
                       "25 menit. Breakout room 2 sampai 3 orang: peran pelanggan dan Retention Staff bergantian "
                       "dengan tiga kartu kasus. Pengamat mengisi checklist HEARD.",
                       "5 menit. Temuan pengamat dibahas bersama."],
             alat="Kartu kasus keluhan, checklist HEARD", media="Presentasi, breakout room",
             output="checklist HEARD terisi untuk setiap peserta.",
             ukuran="setiap peserta menjalankan minimal 4 dari 5 langkah."),
        dict(no=6, judul="Service Recovery dan Akar Penyebab Keluhan", waktu="13.40 - 14.20 WIB",
             tujuan="peserta mampu menelusuri akar penyebab keluhan berulang dan menentukan tindakan pencegahan.",
             materi=["Batas waktu respons dan penyelesaian (SLA)",
                     "Koordinasi dengan teknisi dan tim operasional",
                     "Kunjungan ulang dan kompensasi yang wajar",
                     "5 Why untuk keluhan berulang, lalu konfirmasi penutupan ke pelanggan"],
             kegiatan=["10 menit. Peserta membaca Log Keluhan dan menghitung keluhan yang lewat batas waktu.",
                       "20 menit. Kelompok menelusuri tiga keluhan Kafe 05 dengan 5 Why.",
                       "10 menit. Setiap peserta menulis pesan penutupan keluhan untuk Kafe 05."],
             alat="Log Keluhan dan Service Recovery", media="Presentasi, Google Sheets bersama",
             output="akar penyebab dan tindakan pencegahan Kafe 05, dibawa ke Sesi 4.",
             ukuran="akar penyebab bisa ditindaklanjuti pelanggan atau teknisi."),
    ]),
    ("SILABUS CUSTOMER RETENTION: SESI 4. MEMPERTAHANKAN KONTRAK", [
        dict(no=7, judul="Percakapan Perpanjangan Kontrak", waktu="14.30 - 15.10 WIB",
             tujuan="peserta mampu menanggapi keberatan harga dan rencana berhenti dengan bukti nilai layanan.",
             materi=["Kontak perpanjangan 90, 60, dan 30 hari sebelum kontrak habis",
                     "Ringkasan nilai setahun: kunjungan, temuan, tren hama, audit yang lolos",
                     "Keberatan umum: harga pesaing, hama masih ada, pengelola baru",
                     "Pilihan sebelum kehilangan pelanggan: ubah frekuensi atau ruang lingkup",
                     "Mengajak kembali pelanggan yang sudah berhenti"],
             kegiatan=["10 menit. Paparan alur telepon perpanjangan dan contoh ringkasan nilai.",
                       "25 menit. Role play berpasangan: menelepon Kafe 05 yang membandingkan harga pesaing. "
                       "Trainer dan host Zoom berpindah room memberi masukan.",
                       "5 menit. Kelas memilih kalimat terbaik untuk skrip bersama."],
             alat="Skrip telepon perpanjangan kontrak", media="Presentasi, breakout room",
             output="skrip perpanjangan kontrak versi kelas.",
             ukuran="setiap peserta menanggapi keberatan harga tanpa langsung memberi potongan."),
        dict(no=8, judul="Rencana Retensi 30 Hari", waktu="15.10 - 15.40 WIB",
             tujuan="peserta mampu menyusun rencana tindakan untuk pelanggan prioritas.",
             materi=["Prioritas dari skor kesehatan dan tanggal habis kontrak",
                     "Satu tindakan, satu tanggal, satu penanggung jawab per pelanggan",
                     "Serah terima peluang tambah layanan ke tim sales",
                     "Angka yang dipantau: retensi bulanan dan keluhan berulang"],
             kegiatan=["20 menit. Setiap peserta menyusun rencana untuk 5 pelanggan prioritas 1 dari "
                       "Skor Kesehatan Pelanggan.",
                       "10 menit. Trainer memberi masukan pada dua rencana yang dibagikan di layar."],
             alat="Lembar rencana retensi 30 hari, Skor Kesehatan Pelanggan", media="Google Sheets",
             output="rencana retensi 30 hari per peserta.",
             ukuran="setiap rencana berisi 5 pelanggan dengan tindakan dan tanggal."),
    ]),
]

RUNDOWN_SALES = [
    ("09.00 - 09.20", "Pembukaan, aturan kelas Zoom, dan pre-test",
     "Peserta menyebut satu tantangan terbesar memimpin tim sales, lalu mengerjakan 10 soal pre-test."),
    ("09.20 - 10.30", "Sesi 1. Memimpin tim sales",
     "Menilai pemakaian waktu Sales Leader, lalu memilih gaya kepemimpinan untuk lima sales kasus."),
    ("10.30 - 10.40", "Jeda layar", None),
    ("10.40 - 12.00", "Sesi 2. Sales performance management",
     "Membaca dasbor tim untuk menemukan titik macet, lalu berlatih umpan balik SBI."),
    ("12.00 - 13.00", "Istirahat, salat, dan makan siang", None),
    ("13.00 - 14.20", "Sesi 3. Coaching dan mentoring",
     "Role play coaching dengan model GROW, lalu menyusun rencana coaching empat minggu."),
    ("14.20 - 14.30", "Jeda layar", None),
    ("14.30 - 15.40", "Sesi 4. Strategi pencapaian target",
     "Memecah target menjadi aktivitas mingguan, lalu menyusun rencana 30-60-90 hari untuk tim."),
    ("15.40 - 16.00", "Post-test, survei, dan penutupan",
     "Peserta mengerjakan post-test dan menyebut satu kebiasaan baru yang dimulai minggu depan."),
]

SESI_SALES = [
    ("SILABUS SALES LEADERSHIP: SESI 1. MEMIMPIN TIM SALES", [
        dict(no=1, judul="Peran Sales Leader: Hasil Lewat Tim", waktu="09.20 - 09.50 WIB",
             tujuan="peserta mampu membedakan pekerjaan Sales Leader dari pekerjaan sales dan menilai "
                    "pemakaian waktunya sendiri.",
             materi=["Dari penjual terbaik menjadi pemimpin tim",
                     "Pembagian waktu: coaching, review, kunjungan bersama, administrasi, menjual sendiri",
                     "Ritme tim: briefing harian, review pipeline mingguan, review bulanan",
                     "Risiko mengambil alih closing anggota tim"],
             kegiatan=["10 menit. Polling Zoom: berapa persen waktu minggu lalu dipakai untuk menjual sendiri?",
                       "10 menit. Paparan peran dan ritme tim.",
                       "10 menit. Peserta menulis jadwal ritme tim untuk satu minggu."],
             alat="Templat ritme tim mingguan", media="Presentasi, polling Zoom",
             output="jadwal ritme tim satu minggu per peserta.",
             ukuran="jadwal memuat minimal satu slot coaching per anggota tim."),
        dict(no=2, judul="Situational Leadership: Gaya untuk Tiap Anggota Tim", waktu="09.50 - 10.30 WIB",
             tujuan="peserta mampu memilih gaya kepemimpinan sesuai kompetensi dan komitmen anggota tim.",
             materi=["Kompetensi dan komitmen sebagai ukuran kesiapan",
                     "Empat gaya: directing, coaching, supporting, delegating",
                     "Tanda gaya yang keliru: terlalu mengatur atau terlalu melepas",
                     "Gaya berubah saat tugas berubah"],
             kegiatan=["10 menit. Paparan empat gaya dengan contoh sales pest control.",
                       "20 menit. Breakout room menilai kompetensi dan komitmen lima sales kasus dari kartu "
                       "profil, lalu memilih gaya.",
                       "10 menit. Hasil kelompok dibandingkan di Dasbor Tim."],
             alat="Dasbor Kinerja Tim Sales, kolom gaya", media="Presentasi, kartu profil sales",
             output="gaya kepemimpinan untuk lima sales kasus, dibawa ke Sesi 2.",
             ukuran="setiap pilihan gaya disertai satu alasan dari data atau perilaku."),
    ]),
    ("SILABUS SALES LEADERSHIP: SESI 2. MENGELOLA KINERJA", [
        dict(no=3, judul="Indikator Kinerja dan Pipeline Penjualan", waktu="10.40 - 11.20 WIB",
             tujuan="peserta mampu menganalisis dasbor tim untuk menemukan tahap penjualan yang macet.",
             materi=["Alur penjualan pest control: leads, survei lokasi, penawaran, kontrak",
                     "Indikator aktivitas (leading) dan indikator hasil (lagging)",
                     "Konversi antartahap dan cakupan pipeline",
                     "Kontrak berulang dan pekerjaan sekali, misalnya anti rayap pra-konstruksi"],
             kegiatan=["10 menit. Paparan alur penjualan dan cara membaca konversi.",
                       "20 menit. Kelompok membaca Dasbor Tim dan menulis titik macet tiap sales sebelum "
                       "melihat kolom Titik macet.",
                       "10 menit. Kelompok membandingkan jawaban dengan hasil kalkulator."],
             alat="Dasbor Kinerja Tim Sales", media="Presentasi, Google Sheets bersama",
             output="titik macet dan dugaan penyebab untuk lima sales.",
             ukuran="minimal 4 dari 5 titik macet sesuai data."),
        dict(no=4, judul="Review Kinerja dan Umpan Balik", waktu="11.20 - 12.00 WIB",
             tujuan="peserta mampu memberi umpan balik dengan model SBI dalam pertemuan one-on-one.",
             materi=["Struktur one-on-one mingguan 20 menit",
                     "SBI: Situation, Behavior, Impact",
                     "Umpan balik apresiasi dan umpan balik perbaikan",
                     "Menangani kinerja di bawah target secara bertahap"],
             kegiatan=["10 menit. Trainer memeragakan umpan balik SBI kepada Sales B.",
                       "20 menit. Peserta berpasangan bergantian memberi umpan balik SBI kepada Sales B dan Sales E.",
                       "10 menit. Kelas membahas kalimat yang paling jelas."],
             alat="Lembar SBI dan agenda one-on-one", media="Presentasi, breakout room",
             output="dua umpan balik SBI tertulis per peserta.",
             ukuran="setiap umpan balik menyebut perilaku yang teramati, tidak menilai sifat orang."),
    ]),
    ("SILABUS SALES LEADERSHIP: SESI 3. COACHING DAN MENTORING", [
        dict(no=5, judul="Coaching dengan Model GROW", waktu="13.00 - 13.45 WIB",
             tujuan="peserta mampu memandu percakapan coaching dengan model GROW.",
             materi=["Beda coaching, mentoring, training, dan memberi arahan",
                     "GROW: Goal, Reality, Options, Will",
                     "Pertanyaan terbuka dan mendengarkan",
                     "Kapan coaching tidak tepat dipakai"],
             kegiatan=["10 menit. Trainer memeragakan coaching kepada Sales C yang sering kalah harga.",
                       "30 menit. Breakout room 2 sampai 3 orang: peran Sales Leader, sales, dan pengamat "
                       "bergantian. Pengamat menghitung pertanyaan terbuka dan mencatat komitmen.",
                       "5 menit. Temuan pengamat dibahas bersama."],
             alat="Kartu kasus coaching, checklist GROW", media="Presentasi, breakout room",
             output="catatan GROW untuk satu percakapan per peserta.",
             ukuran="setiap percakapan berakhir dengan komitmen yang punya tanggal."),
        dict(no=6, judul="Mentoring di Lapangan dan Rencana Pengembangan", waktu="13.45 - 14.20 WIB",
             tujuan="peserta mampu menyusun rencana coaching dan mentoring empat minggu untuk satu anggota tim.",
             materi=["Kunjungan bersama: sebelum, selama, dan sesudah kunjungan",
                     "Mentoring sales baru: pengetahuan hama, metode layanan, dan garansi",
                     "Meninjau rekaman telepon dan dokumen penawaran",
                     "Rencana pengembangan empat minggu"],
             kegiatan=["10 menit. Paparan alur kunjungan bersama dengan contoh survei lokasi gudang.",
                       "20 menit. Peserta mengisi Rencana Coaching untuk Sales D atau satu anggota timnya sendiri.",
                       "5 menit. Dua peserta membacakan rencananya."],
             alat="Rencana Coaching GROW", media="Presentasi, Google Sheets",
             output="rencana coaching empat minggu per peserta.",
             ukuran="rencana memuat sasaran terukur dan jadwal cek mingguan."),
    ]),
    ("SILABUS SALES LEADERSHIP: SESI 4. MENCAPAI TARGET", [
        dict(no=7, judul="Memecah Target Menjadi Aktivitas", waktu="14.30 - 15.05 WIB",
             tujuan="peserta mampu menghitung aktivitas mingguan yang dibutuhkan untuk mencapai target.",
             materi=["Target nilai kontrak dibagi rata-rata nilai kontrak",
                     "Mundur dari kontrak ke penawaran, survei lokasi, dan leads",
                     "Aktivitas per sales per minggu",
                     "Dampak kenaikan konversi pada beban aktivitas"],
             kegiatan=["10 menit. Peserta menghitung satu contoh dengan tangan.",
                       "15 menit. Peserta mengisi Kalkulator Target ke Aktivitas dengan data kasus, lalu "
                       "mengubah konversi penawaran.",
                       "10 menit. Diskusi: mana yang lebih realistis, menambah leads atau menaikkan konversi."],
             alat="Kalkulator Target ke Aktivitas", media="Presentasi, Google Sheets",
             output="aktivitas mingguan per sales untuk target kasus.",
             ukuran="semua peserta mendapat angka yang sama dengan kalkulator."),
        dict(no=8, judul="Rencana 30-60-90 Hari untuk Tim", waktu="15.05 - 15.40 WIB",
             tujuan="peserta mampu menyusun rencana pencapaian target untuk timnya sendiri.",
             materi=["Memilih segmen: restoran dan hotel, pabrik pangan, gudang, perumahan dan pengembang",
                     "Peluang dari pelanggan lama: tambah layanan dan rujukan, bersama Retention Staff",
                     "Pola musiman permintaan di wilayah layanan",
                     "Ritme review dan kompetisi tim"],
             kegiatan=["20 menit. Setiap peserta menyusun rencana 30-60-90 hari: segmen, aktivitas, gaya per "
                       "anggota tim, dan jadwal review.",
                       "15 menit. Tiga peserta presentasi 3 menit, peserta lain memberi satu masukan."],
             alat="Lembar rencana 30-60-90 hari", media="Presentasi, Google Docs",
             output="rencana 30-60-90 hari per peserta.",
             ukuran="rencana memuat angka aktivitas mingguan dari Topik 7."),
    ]),
]

CARA_MEMASTIKAN = ["Pre-test dan post-test dengan soal yang sama (Kirkpatrick level 2)",
                   "Role play dinilai pengamat dengan checklist",
                   "Survei kepuasan peserta (Kirkpatrick level 1)",
                   "Laporan dikirim paling lambat 7 hari kerja setelah pelatihan"]


def program_retensi():
    halaman_ringkasan_program(
        "SILABUS CUSTOMER RETENTION TRAINING",
        f"Untuk Retention Staff {KLIEN}. 7 peserta, via Zoom, 09.00 - 16.00 WIB.",
        "Delapan topik dipelajari mengikuti siklus kerja Retention Staff: mengenali pelanggan, menjaga loyalitas, "
        "menangani keluhan, lalu mempertahankan kontrak. Setiap topik berisi paparan singkat dan latihan dengan "
        "data kasus pest control.",
        [("8 topik", "EMPAT SESI", "Empat sesi mengikuti siklus kerja retensi, dari data pelanggan sampai "
                                   "perpanjangan kontrak."),
         ("7 peserta", "SATU KELAS ZOOM", "Setiap peserta mendapat giliran role play keluhan dan telepon "
                                          "perpanjangan."),
         ("3 alat", "DIBAWA PULANG", "Lembar kerja Excel berisi kasus contoh, siap diisi data pelanggan sendiri.")],
        RUNDOWN_RETENSI)
    halaman_alur(
        "ALUR PELATIHAN: SATU DAFTAR PELANGGAN, EMPAT SESI",
        "Hasil kerja satu sesi menjadi bahan sesi berikutnya, dari data pelanggan sampai rencana retensi.",
        [("Sesi 1. Mengenali Pelanggan",
          ["Topik: Nilai pelanggan, CRM dan skor kesehatan",
           "Pertanyaan: pelanggan mana yang paling berisiko berhenti?",
           "Diteruskan: daftar pelanggan merah dan kuning"]),
         ("Sesi 2. Menjaga Loyalitas",
          ["Topik: Pendorong loyalitas, komunikasi proaktif",
           "Pertanyaan: kapan pelanggan mulai ragu, dan kapan kami harus hadir?",
           "Diteruskan: kalender kontak dan templat pesan"]),
         ("Sesi 3. Menangani Keluhan",
          ["Topik: Langkah HEARD, service recovery",
           "Pertanyaan: bagaimana keluhan selesai dan tidak terulang?",
           "Diteruskan: akar penyebab dan tindakan pencegahan"]),
         ("Sesi 4. Mempertahankan Kontrak",
          ["Topik: Percakapan perpanjangan, rencana retensi 30 hari",
           "Pertanyaan: apa yang kami katakan saat pelanggan membandingkan harga?",
           "Kembali ke Sesi 1: skor kesehatan dipantau tiap bulan"])],
        "Cabang contoh melayani 24 pelanggan kontrak, dari rumah tinggal sampai pabrik roti. Kafe 05 sudah tiga kali "
        "mengeluh kecoa bulan ini, telat bayar 35 hari, dan kontraknya habis 20 Desember. Hotel 02 kecewa karena dua "
        f"kunjungan teknisi terlewat. Semua data kasus disusun Sanggabiz untuk latihan, bukan data {KLIEN}.")
    for judul, topik in SESI_RETENSI:
        halaman_sesi(judul, topik)
    halaman_hasil(
        "HASIL CUSTOMER RETENTION TRAINING",
        "Yang bisa langsung dipakai Retention Staff, dan bukti yang bisa ditunjukkan kepada manajemen.",
        [("Untuk peserta", ["Cara menghitung retensi, churn, dan nilai pelanggan",
                            "Pengalaman role play keluhan dan telepon perpanjangan",
                            "Tiga lembar kerja Excel yang bisa diisi data sendiri",
                            "Sertifikat elektronik perorangan"]),
         ("Untuk supervisor dan manajemen", ["Rencana retensi 30 hari dari setiap peserta",
                                             "Skrip perpanjangan kontrak dan templat pesan hasil kelas",
                                             "Laporan evaluasi: pre-test dan post-test, tangkapan layar "
                                             "kegiatan, catatan trainer"]),
         ("Cara kami memastikan hasilnya", CARA_MEMASTIKAN)],
        "Trainer berpengalaman di layanan pelanggan dan retensi kontrak B2B. Host mengatur breakout room, polling, "
        "dan kehadiran, sehingga trainer bisa fokus pada latihan. [ISI TIM: nama dan pengalaman trainer]")


def program_sales():
    halaman_ringkasan_program(
        "SILABUS SALES LEADERSHIP TRAINING",
        f"Untuk Sales Leader {KLIEN}. 7 peserta, via Zoom, 09.00 - 16.00 WIB.",
        "Delapan topik dipelajari mengikuti pekerjaan mingguan Sales Leader: memimpin tim, mengelola kinerja, "
        "melatih anggota tim, lalu mengejar target. Setiap topik berisi paparan singkat dan latihan dengan data "
        "tim sales pest control.",
        [("8 topik", "EMPAT SESI", "Empat sesi mengikuti pekerjaan Sales Leader, dari membaca tim sampai "
                                   "rencana target."),
         ("7 peserta", "SATU KELAS ZOOM", "Setiap peserta berlatih coaching dan memberi umpan balik di "
                                          "breakout room."),
         ("3 alat", "DIBAWA PULANG", "Lembar kerja Excel berisi data tim contoh, siap diisi data tim sendiri.")],
        RUNDOWN_SALES)
    halaman_alur(
        "ALUR PELATIHAN: SATU TIM SALES, EMPAT SESI",
        "Hasil kerja satu sesi menjadi bahan sesi berikutnya, dari membaca tim sampai rencana target.",
        [("Sesi 1. Memimpin Tim",
          ["Topik: Peran Sales Leader, Situational Leadership",
           "Pertanyaan: siapa yang butuh arahan, siapa yang cukup diberi kepercayaan?",
           "Diteruskan: gaya kepemimpinan per anggota tim"]),
         ("Sesi 2. Mengelola Kinerja",
          ["Topik: Indikator kinerja dan pipeline, umpan balik",
           "Pertanyaan: di tahap mana penjualan tiap orang macet?",
           "Diteruskan: titik macet per sales"]),
         ("Sesi 3. Coaching dan Mentoring",
          ["Topik: Coaching GROW, mentoring di lapangan",
           "Pertanyaan: bagaimana membantu sales tanpa mengambil alih pekerjaannya?",
           "Diteruskan: rencana coaching empat minggu"]),
         ("Sesi 4. Mencapai Target",
          ["Topik: Target ke aktivitas, rencana 30-60-90 hari",
           "Pertanyaan: berapa aktivitas per minggu yang dibutuhkan, dan dari segmen mana?",
           "Kembali ke Sesi 2: dasbor dipakai di review mingguan"])],
        "Tim cabang contoh berisi lima sales dan berada di minggu ke-8 dari 13 minggu kuartal. Capaian tim baru "
        "46 persen dari target Rp 1,2 miliar. Sales B rajin survei tetapi jarang mengirim penawaran, Sales C sering "
        "kalah harga, Sales D masih baru, dan aktivitas Sales E menurun. Semua data kasus disusun Sanggabiz untuk "
        f"latihan, bukan data {KLIEN}.")
    for judul, topik in SESI_SALES:
        halaman_sesi(judul, topik)
    halaman_hasil(
        "HASIL SALES LEADERSHIP TRAINING",
        "Yang bisa langsung dipakai Sales Leader, dan bukti yang bisa ditunjukkan kepada manajemen.",
        [("Untuk peserta", ["Cara memilih gaya kepemimpinan per anggota tim",
                            "Pengalaman role play coaching GROW dan umpan balik SBI",
                            "Tiga lembar kerja Excel yang bisa diisi data tim sendiri",
                            "Sertifikat elektronik perorangan"]),
         ("Untuk manajemen", ["Rencana 30-60-90 hari dari setiap Sales Leader",
                              "Rencana coaching empat minggu untuk satu anggota tim",
                              "Laporan evaluasi: pre-test dan post-test, tangkapan layar kegiatan, "
                              "catatan trainer"]),
         ("Cara kami memastikan hasilnya", CARA_MEMASTIKAN)],
        "Trainer berpengalaman memimpin tim penjualan B2B dan melatih coaching. Host mengatur breakout room, "
        "polling, dan kehadiran, sehingga trainer bisa fokus pada latihan. [ISI TIM: nama dan pengalaman trainer]")


def toolkit():
    s = halaman("TOOLKIT SANGGABIZ: ALAT BANTU BELAJAR",
                "Alat yang disiapkan untuk dua pelatihan. Lembar kerja Excel dibawa pulang peserta.")
    data = [
        ("Skor Kesehatan Pelanggan", "Skor 0 sampai 100 per pelanggan dari keluhan, kunjungan, pembayaran, dan "
                                     "kepuasan, lalu prioritas kontak", "Retention", "Excel"),
        ("Kalkulator Retensi dan Nilai Pelanggan", "Retention rate, churn, revenue churn, net revenue retention, "
                                                   "dan CLV", "Retention", "Excel"),
        ("Log Keluhan dan Service Recovery", "Ketepatan respons dan penyelesaian, akar penyebab, dan tindakan "
                                             "pencegahan", "Retention", "Excel"),
        ("Kartu kasus dan checklist HEARD", "Tiga kasus keluhan pest control dan checklist pengamat",
         "Retention", "PDF"),
        ("Skrip perpanjangan dan templat pesan", "Alur telepon 90, 60, dan 30 hari, dan templat WhatsApp",
         "Retention", "PDF"),
        ("Dasbor Kinerja Tim Sales", "Capaian, konversi antartahap, cakupan pipeline, titik macet, dan gaya "
                                     "kepemimpinan per sales", "Sales Leader", "Excel"),
        ("Kalkulator Target ke Aktivitas", "Target nilai kontrak menjadi kontrak, penawaran, survei, dan leads "
                                           "per sales per minggu", "Sales Leader", "Excel"),
        ("Rencana Coaching GROW", "Sasaran, fakta, pilihan, komitmen, dan cek mingguan per anggota tim",
         "Sales Leader", "Excel"),
        ("Kartu profil sales dan lembar SBI", "Profil lima sales kasus, checklist GROW, dan format umpan balik "
                                              "SBI", "Sales Leader", "PDF"),
        ("Lembar rencana tindak lanjut", "Rencana retensi 30 hari dan rencana 30-60-90 hari", "Keduanya", "PDF"),
        ("Pre-test, post-test, dan survei", "10 soal yang sama di awal dan akhir, dan survei kepuasan peserta",
         "Keduanya", "Formulir daring"),
    ]
    baris = [kepala_tabel(["Alat", "Isi", "Pelatihan", "Bentuk"], 860)]
    for a, b, c, d in data:
        baris.append([[[(a, 860, {"bold": True})]], [[(b, 860)]], [[(c, 860)]], [[(d, 860)]]])

    def warna(r, c):
        if r == 0:
            return TEAL
        return "FFFFFF" if r % 2 else "F2F8F9"

    tabel(s, X0, 1636776, [2834640, 5852160, 1188720, 1097280], [228600] * (len(data) + 1), baris, warna)
    catatan(s, 4480560, 822960, "Data contoh.",
            f"Angka di setiap lembar kerja disusun Sanggabiz untuk latihan. Bila {KLIEN} berkenan memberi data yang "
            "sudah dianonimkan, data contoh kami ganti agar latihan lebih dekat ke pekerjaan peserta. Semua berkas "
            "dikirim ke peserta paling lambat H-1 bersama tautan Zoom.")


def contoh_alat():
    halaman_contoh(
        "CONTOH ALAT BANTU: SKOR KESEHATAN PELANGGAN",
        [("Lembar Pelanggan: skor kesehatan dan prioritas kontak", ASSET / "retensi-lembar-1.png",
          612648, 1645920, 7543800)],
        [("Apa ini", "Lembar kerja Excel dengan rumus hidup. Peserta mengisi data layanan setiap pelanggan, lalu "
                     "lembar ini menghitung skor kesehatan, status merah, kuning, atau hijau, dan prioritas kontak."),
         ("Data kasus", "24 pelanggan kontrak cabang contoh. Enam berstatus merah dengan nilai kontrak "
                        "Rp 267,6 juta per tahun, dan lima harus dihubungi minggu ini."),
         ("Dipakai di", f"Sesi 1 dan Sesi 4. Sesudah pelatihan, bobot skor bisa disesuaikan dan diisi data "
                        f"pelanggan {KLIEN}.")])
    halaman_contoh(
        "CONTOH ALAT BANTU: LOG KELUHAN DAN SERVICE RECOVERY",
        [("Lembar Log Keluhan: respons, penyelesaian, akar penyebab", ASSET / "retensi-lembar-3.png",
          612648, 1645920, 7543800)],
        [("Apa ini", "Mencatat setiap keluhan, menghitung apakah respons dan penyelesaian memenuhi batas waktu, "
                     "dan menyimpan akar penyebab serta tindakan pencegahan."),
         ("Data kasus", "10 keluhan dalam satu bulan. Respons tepat waktu baru 60 persen, dan Kafe 05 mengeluh "
                        "tiga kali dengan masalah yang sama."),
         ("Dipakai di", "Sesi 3. Batas waktu respons dan penyelesaian bisa diganti sesuai SLA perusahaan.")])
    halaman_contoh(
        "CONTOH ALAT BANTU: DASBOR TIM DAN TARGET KE AKTIVITAS",
        [("Lembar Dasbor Tim: kinerja dan gaya kepemimpinan", ASSET / "sales-lembar-1.png",
          612648, 1645920, 7543800),
         ("Lembar Target ke Aktivitas", ASSET / "sales-lembar-2.png", 612648, 3840480, 3657600)],
        [("Apa ini", "Dasbor menghitung capaian, konversi, cakupan pipeline, titik macet, dan gaya kepemimpinan "
                     "per sales. Kalkulator memecah target menjadi aktivitas mingguan."),
         ("Data kasus", "Capaian tim 46 persen di minggu ke-8. Untuk target Rp 300 juta per bulan, tiap sales "
                        "butuh 13 leads per minggu. Bila konversi penawaran naik 5 poin, tim butuh 38 leads lebih "
                        "sedikit per bulan."),
         ("Dipakai di", "Sesi 1, 2, dan 4. Sesudah pelatihan, dasbor dipakai di review pipeline mingguan.")])


if __name__ == "__main__":
    ringkasan_dua_program()
    program_retensi()
    program_sales()
    toolkit()
    contoh_alat()
    OUT.parent.mkdir(exist_ok=True)
    prs.save(OUT)
    print("ditulis:", OUT, len(prs.slides), "slide")
