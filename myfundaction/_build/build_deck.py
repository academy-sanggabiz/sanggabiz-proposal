"""Slide kurikulum dan silabus pelatihan AI Agent MyFundAction.

Mengikuti FORMAT-STANDAR-PROPOSAL.md tipe 1 varian slide per bab (keluarga warna teal).
Isi diambil dari silabus_data.py.
"""
import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

import silabus_data as d

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "proposal", "v2 Kurikulum dan Silabus - Pelatihan AI Agent MyFundAction.pptx")
LOGO = os.path.join(HERE, "assets", "logo_white.png")

TEAL = "15908F"
TEAL_T = "0E8A8A"
TEAL_M = "D7ECEC"
ZEBRA = "F2F8F9"
CYAN = "34BDCF"
BLUE = "0071CE"
GREY = "D9D9D9"
GREY_L = "F2F2F2"
LILAC = "E2A9F1"
INK = "1D1D1F"
MUTED = "555555"
FONT = "Arial"

SW, SH = 13.333, 7.5
ML = 0.55


def rgb(h):
    return RGBColor.from_string(h)


prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)


def teks(slide, x, y, w, h, isi, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    baris = isi if isinstance(isi, list) else [isi]
    for i, b in enumerate(baris):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        runs = b if isinstance(b, list) else [(b, bold, color)]
        for t, bb, cc in runs:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = bb
            r.font.italic = italic
            r.font.name = FONT
            r.font.color.rgb = rgb(cc)
    return tb


def kotak(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(fill)
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.75)
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s


def isi_kotak(s, baris, size=11, color=INK, bold=False, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE):
    tf = s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.vertical_anchor = anchor
    baris = baris if isinstance(baris, list) else [baris]
    for i, b in enumerate(baris):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        runs = b if isinstance(b, list) else [(b, bold, color)]
        for t, bb, cc in runs:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = bb
            r.font.name = FONT
            r.font.color.rgb = rgb(cc)


def garis(slide, x1, y1, x2, y2, color="000000", w=0.75, panah=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(w)
    if panah:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
    return c


def kerangka(judul_hitam, judul_teal=None, sub=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    runs = [(judul_hitam, True, INK)]
    if judul_teal:
        runs.append(("  " + judul_teal, True, TEAL_T))
    teks(s, ML, 0.32, 10.6, 0.6, [runs], size=24)
    if sub:
        teks(s, ML, 0.9, 10.6, 0.4, sub, size=12, color=MUTED)
    # logo di kanan atas dalam pil teal
    pil = kotak(s, SW - ML - 2.0, 0.34, 2.0, 0.5, TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    s.shapes.add_picture(LOGO, Inches(SW - ML - 1.0 - 0.72), Inches(0.45), height=Inches(0.285))
    # kaki
    garis(s, ML, SH - 0.5, SW - ML, SH - 0.5, "000000", 0.75)
    teks(s, ML, SH - 0.45, SW - 2 * ML, 0.3,
         [[("WhatsApp 0877-7413-4288", False, MUTED), ("     www.sanggabiz.com", False, MUTED), ("     partnership@sanggabiz.com", False, MUTED),
           (f"          {d.PROGRAM['klien']} | {d.PROGRAM['versi']}", False, "999999")]], size=9)
    return s


def tabel(slide, x, y, w, kolom, lebar_kol, baris, size=9, tinggi_kepala=0.4, tinggi_baris=None):
    n = len(baris) + 1
    shp = slide.shapes.add_table(n, len(kolom), Inches(x), Inches(y), Inches(w), Inches(tinggi_kepala + 0.5 * len(baris)))
    tbl = shp.table
    tblPr = tbl._tbl.tblPr
    for attr in ("bandRow", "firstRow"):
        tblPr.set(attr, "0")
    sty = tblPr.find(qn("a:tableStyleId"))
    if sty is not None:
        sty.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"  # No Style, Table Grid
    for i, wv in enumerate(lebar_kol):
        tbl.columns[i].width = Inches(wv)
    tbl.rows[0].height = Inches(tinggi_kepala)
    for c, k in enumerate(kolom):
        cell = tbl.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = rgb(TEAL)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        r = tf.paragraphs[0].add_run()
        r.text = k
        r.font.size = Pt(size + 1)
        r.font.bold = True
        r.font.name = FONT
        r.font.color.rgb = rgb("FFFFFF")
    for ri, row in enumerate(baris, 1):
        if tinggi_baris:
            tbl.rows[ri].height = Inches(tinggi_baris[ri - 1])
        for c, v in enumerate(row):
            cell = tbl.cell(ri, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(ZEBRA if ri % 2 == 0 else "FFFFFF")
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            item = v if isinstance(v, dict) else {"t": v}
            lines = item["t"] if isinstance(item["t"], list) else [item["t"]]
            for li, ln in enumerate(lines):
                p = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                p.alignment = item.get("align", PP_ALIGN.LEFT)
                r = p.add_run()
                r.text = ln
                r.font.size = Pt(item.get("size", size))
                r.font.bold = item.get("bold", False)
                r.font.italic = item.get("italic", False)
                r.font.name = FONT
                r.font.color.rgb = rgb(item.get("color", INK))
    return tbl


def gabung_kolom_pertama(tbl, awal, akhir, judul, fokus):
    c = tbl.cell(awal, 0)
    if akhir > awal:
        c.merge(tbl.cell(akhir, 0))
    c.fill.solid()
    c.fill.fore_color.rgb = rgb(TEAL_M)
    tf = c.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    r = p.add_run()
    r.text = judul
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = rgb(TEAL_T)
    p2 = tf.add_paragraph()
    p2.space_before = Pt(6)
    r2 = p2.add_run()
    r2.text = "Fokus: " + fokus
    r2.font.size = Pt(9)
    r2.font.italic = True
    r2.font.name = FONT
    r2.font.color.rgb = rgb(INK)


# ---------- 1. Sampul ----------
s = prs.slides.add_slide(prs.slide_layouts[6])
kotak(s, 0, 0, SW, SH, "0D5C5B")
kotak(s, 0, 0, 0.35, SH, CYAN)
s.shapes.add_picture(LOGO, Inches(0.9), Inches(0.8), height=Inches(0.55))
teks(s, 0.9, 2.2, 11, 0.5, "KURIKULUM DAN SILABUS", size=16, bold=True, color=CYAN)
teks(s, 0.9, 2.7, 11.5, 1.6, d.PROGRAM["judul"], size=40, bold=True, color="FFFFFF")
teks(s, 0.9, 4.25, 11, 0.5, "Dari dasar AI dan Claude sampai menjalankan AI Agent dengan Hermes", size=18, color="E6F4F4")
teks(s, 0.9, 5.6, 11, 0.9, [f"Disiapkan untuk {d.PROGRAM['klien']}", "November 2026"], size=14, color="FFFFFF")

# ---------- 2. Kebutuhan dan hasil ----------
s = kerangka("Kebutuhan dan", "Hasil yang Diharapkan", "Diambil dari rapat bersama tim MyFundAction, 14 November 2026")
kebutuhan = [
    "Tim CRM tertarik memakai AI Agent setelah mengenal Hermes, tetapi belum tahu langkah awalnya",
    "Peserta bukan programmer, jadi materi dimulai dari dasar dan praktik dibuat bertahap",
    "Kualitas hasil AI berbeda antara tim Indonesia, Malaysia, dan Australia, terutama dalam menyusun prompt",
    "Penerapan awal di CRM, iklan, marketing, dan analisis untuk program Palestina, masjid, dan air bersih",
    "Peserta kurang dari 10 orang, luring di Jakarta dengan kemungkinan peserta daring dari Malaysia dan Australia",
]
hasil = [
    "Memakai Claude untuk tugas kerja dan memeriksa hasilnya",
    "Menulis prompt dengan 6 unsur yang sama di ketiga negara, diukur dengan rubrik 0 sampai 12",
    "Memasang Hermes dan menjalankan agen pertama lewat Telegram dengan pengaturan aman",
    "Menjalankan agen untuk segmentasi donatur, brief iklan, dan laporan kampanye mingguan",
    "Membawa pulang draf Standar Prompt MFA dan rencana agen 30 hari",
]
for i, (jdl, items, warna) in enumerate([("Kebutuhan MyFundAction", kebutuhan, TEAL), ("Yang bisa dikerjakan peserta setelah pelatihan", hasil, BLUE)]):
    x = ML + i * 6.2
    k = kotak(s, x, 1.45, 5.95, 0.5, warna)
    isi_kotak(k, jdl, size=13, bold=True, color="FFFFFF")
    kotak(s, x, 1.95, 5.95, 4.75, "FFFFFF", line=GREY)
    for j, t in enumerate(items):
        y = 2.1 + j * 0.9
        o = kotak(s, x + 0.2, y + 0.08, 0.42, 0.42, warna, shape=MSO_SHAPE.OVAL)
        isi_kotak(o, str(j + 1), size=11, bold=True, color="FFFFFF")
        teks(s, x + 0.75, y, 5.0, 0.85, t, size=12, anchor=MSO_ANCHOR.MIDDLE)

# ---------- 3. Alur program dan metode ----------
s = kerangka("Alur Program", "dan Metode", "Enam tahap dari asesmen kebutuhan sampai laporan. Metode: ADDIE, andragogi, Bloom, Kirkpatrick")
lebar_k = (SW - 2 * ML - 5 * 0.18) / 6
for i, (n, t, k, h) in enumerate(d.ALUR):
    x = ML + i * (lebar_k + 0.18)
    box = kotak(s, x, 1.5, lebar_k, 3.55, GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    o = kotak(s, x + lebar_k / 2 - 0.25, 1.62, 0.5, 0.5, "33BCCF", shape=MSO_SHAPE.OVAL)
    isi_kotak(o, n, size=14, bold=True, color="FFFFFF")
    teks(s, x + 0.08, 2.2, lebar_k - 0.16, 0.65, t, size=11, bold=True, align=PP_ALIGN.CENTER)
    teks(s, x + 0.08, 2.85, lebar_k - 0.16, 2.1, k, size=9, align=PP_ALIGN.LEFT)
    lab = kotak(s, x + 0.08, 5.15, lebar_k - 0.16, 0.6, LILAC, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    isi_kotak(lab, h, size=9, bold=True)
    if i < 5:
        garis(s, x + lebar_k + 0.01, 3.3, x + lebar_k + 0.17, 3.3, TEAL, 1.5, panah=True)
y = 5.95
for i, (m, ket) in enumerate(d.METODE):
    x = ML + i * 3.08
    teks(s, x, y, 2.95, 0.9, [[(m + ": ", True, TEAL_T), (ket, False, INK)]], size=9)

# ---------- 4-7. Kurikulum per bab ----------
kelompok = [(0, 1), (1, 2), (2, 3), (3, 5), (5, 6), (6, 7)]
for a, b in kelompok:
    mods = d.MODUL[a:b]
    nama = ", ".join(m["kode"] for m in mods)
    s = kerangka("Materi & Silabus", " dan ".join(f"{m['kode']} {m['judul']}" for m in mods) if len(mods) == 1 else " dan ".join(f"{m['kode']} {m['judul'].replace('Introduction to ', '')}" for m in mods))
    rows, spans, tinggi_b = [], [], []
    for m in mods:
        awal = len(rows) + 1
        for t in m["topik"]:
            ntop = sum(len(mm["topik"]) for mm in mods)
            nchar = sum(len(o) for mm in mods for tt in mm["topik"] for o in tt["outline"])
            fs = 12 if (ntop <= 2 and nchar < 650) else (10.5 if ntop <= 2 else (11 if (ntop <= 3 and nchar < 1000) else 10))
            cpl = 62 * 9 / fs
            rows.append([
                "",
                {"t": f"{t['kode']} {t['judul']}", "bold": True, "size": fs + 1},
                {"t": ["\u2022 " + o for o in t["outline"]], "size": fs},
                {"t": t["tujuan"], "size": fs},
                {"t": [t["format"], f"{t['menit']} menit"], "bold": True, "color": TEAL_T, "align": PP_ALIGN.CENTER, "size": fs},
            ])
            tinggi_b.append(max(0.6, 0.19 * fs / 9 * max(len(t["outline"]) + sum(int(len(o) // cpl) for o in t["outline"]), int(len(t["tujuan"]) // (cpl * 0.72)) + 1) + 0.15))
        spans.append((awal, len(rows), f"{m['kode']} {m['judul']}", m["fokus"]))
    if sum(tinggi_b) > 5.3:
        tinggi_b = [h * 5.3 / sum(tinggi_b) for h in tinggi_b]
    tbl = tabel(s, ML, 1.2, SW - 2 * ML, ["Modul & fokus", "Topik", "Outline materi", "Tujuan pembelajaran", "Format"],
                [2.2, 2.0, 4.2, 2.75, SW - 2 * ML - 2.2 - 2.0 - 4.2 - 2.75], rows, tinggi_baris=tinggi_b)
    for awal, akhir, jdl, fokus in spans:
        gabung_kolom_pertama(tbl, awal, akhir, jdl, fokus)

# ---------- 8. Dua skema ----------
s = kerangka("Dua Skema", "Pelaksanaan", f"Isi dan menit tiap modul sama di kedua skema: {d.total_menit_inti()} menit tatap muka inti")
# Skema A
x0 = ML
k = kotak(s, x0, 1.4, 5.7, 0.5, GREY_L, line="000000")
isi_kotak(k, [[("Skema A", True, INK), ("  intensif 1 hari, 08.30 - 17.00 WIB", False, INK)]], size=12)
ra = [r for r in d.SKEMA_A["rundown"] if r[2] not in ("Registrasi dan cek laptop",)]
rows = [[{"t": f"{a} - {b}", "size": 9}, {"t": kg, "size": 9, "bold": kg.startswith("M")}] for a, b, kg, _ in ra]
tabel(s, x0, 1.95, 5.7, ["Waktu", "Kegiatan"], [1.35, 4.35], rows, size=9, tinggi_kepala=0.3, tinggi_baris=[0.27] * len(rows))
# Skema B
x1 = ML + 6.0
k = kotak(s, x1, 1.4, SW - ML - x1, 0.5, TEAL)
isi_kotak(k, [[("Skema B (rekomendasi)", True, "FFFFFF"), ("  4 sesi x 2 jam, 09.00 - 11.00 WIB", False, "FFFFFF")]], size=12)
for i, sesi in enumerate(d.SKEMA_B["sesi"]):
    y = 2.0 + i * 0.86
    box = kotak(s, x1, y, SW - ML - x1, 0.76, ZEBRA if i % 2 else "FFFFFF", line=GREY)
    mods = [r[2] for r in sesi["rundown"] if r[2].startswith("M")]
    teks(s, x1 + 0.12, y + 0.05, 2.6, 0.66, sesi["nama"].replace(": ", "\n"), size=10, bold=True, color=TEAL_T, anchor=MSO_ANCHOR.MIDDLE)
    lb = kotak(s, SW - ML - 1.0, y + 0.2, 0.88, 0.36, LILAC, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.4)
    isi_kotak(lb, sesi["bentuk"], size=9, bold=True)
    teks(s, x1 + 2.8, y + 0.05, SW - ML - x1 - 3.9, 0.66, mods + ([r[2] for r in sesi["rundown"] if r[2] in ("Pre-test", "Post-test")]), size=9, anchor=MSO_ANCHOR.MIDDLE)
alasan = [
    "Jeda antarsesi memberi waktu latihan di pekerjaan nyata dan menyelesaikan instalasi Hermes yang tertunda",
    "Dua jam di pagi WIB masih jam kerja di Kuala Lumpur dan Sydney, sehingga tim lintas negara ikut semua modul",
    "Sesi 1 tidak membutuhkan instalasi, jadi bisa digelar luring pada 17 November 2026 bila jadwal itu dipertahankan",
]
teks(s, x1, 5.5, SW - ML - x1, 0.3, "Alasan rekomendasi", size=11, bold=True, color=TEAL_T)
teks(s, x1, 5.8, SW - ML - x1, 1.2, ["• " + a for a in alasan], size=9)

# ---------- 8b. Bentuk pelaksanaan Skema B ----------
s = kerangka("Skema B:", "Luring dan Daring per Sesi", "Peserta Malaysia dan Australia selalu daring. " + d.SKEMA_B["platform"].replace(" [ISI TIM: konfirmasi platform dengan MFA]", ""))
rows = []
for nama, bentuk, ket in [(x["nama"], x["bentuk"], x["ket_bentuk"]) for x in d.SKEMA_B["sesi"]] + d.SKEMA_B["klinik"]:
    rows.append([{"t": nama, "bold": True, "size": 11}, {"t": bentuk, "bold": True, "color": TEAL_T, "align": PP_ALIGN.CENTER, "size": 12}, {"t": ket, "size": 11}])
tabel(s, ML, 1.45, SW - 2 * ML, ["Sesi", "Bentuk", "Siapa di mana"], [3.3, 1.3, SW - 2 * ML - 4.6], rows, size=11, tinggi_baris=[0.78] * len(rows))
teks(s, ML, 6.55, SW - 2 * ML, 0.4, "Luring: tim Jakarta wajib di ruang kelas.   Hibrida: tim Jakarta boleh di ruang kelas atau dari laptop masing-masing.   Daring: semua lewat Google Meet.", size=10, bold=True, color=TEAL_T)

# ---------- 9. Standar Prompt MFA ----------
s = kerangka("Standar Prompt MFA", "untuk Tiga Negara", "Satu cara menulis prompt untuk tim Indonesia, Malaysia, dan Australia, diukur dengan rubrik yang sama")
w6 = (SW - 2 * ML - 5 * 0.15) / 6
for i, (u, en, arti, s0, s1, s2) in enumerate(d.RUBRIK):
    x = ML + i * (w6 + 0.15)
    top = kotak(s, x, 1.45, w6, 0.85, TEAL if i % 2 == 0 else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    isi_kotak(top, [[(u, True, "FFFFFF")], [(en, False, "E6F4F4")]], size=13)
    teks(s, x, 2.4, w6, 0.95, arti, size=10, align=PP_ALIGN.CENTER)
    lab = kotak(s, x, 3.35, w6, 0.95, GREY_L, line=GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    isi_kotak(lab, [[("Skor 2: ", True, TEAL_T), (s2, False, INK)]], size=9, align=PP_ALIGN.LEFT)
contoh = [
    [("Contoh prompt 6 unsur (dipendekkan): ", True, TEAL_T)],
    [("Konteks: ", True, INK), ("Kami tim marketing MyFundAction Australia. Program pembangunan masjid paling banyak direspons donatur Australia.", False, INK)],
    [("Tugas: ", True, INK), ("Tulis 3 variasi teks iklan Facebook untuk program masjid.", False, INK)],
    [("Bahan: ", True, INK), ("<data> lokasi, kebutuhan dana, dan progres dari laporan program </data>", False, INK)],
    [("Aturan: ", True, INK), ("Bahasa Inggris Australia, nada hangat, jangan menulis angka yang tidak ada di <data>.", False, INK)],
    [("Contoh: ", True, INK), ("<contoh> dua iklan yang pernah berhasil </contoh>", False, INK)],
    [("Format: ", True, INK), ("Tabel: judul maksimal 40 karakter, teks utama maksimal 125 karakter, ajakan.", False, INK)],
]
kotak(s, ML, 4.5, 8.2, 2.35, "FFFFFF", line=GREY)
teks(s, ML + 0.15, 4.58, 7.9, 2.2, contoh, size=10)
k = kotak(s, ML + 8.45, 4.5, SW - 2 * ML - 8.45, 2.35, TEAL_M)
isi_kotak(k, [
    [("Cara mengukur penyelarasan", True, TEAL_T)],
    [("Pre-test dan post-test memuat satu tugas prompt yang dinilai dengan rubrik ini. Skor dibandingkan per peserta dan per negara.", False, INK)],
    [("Target post-test: rata-rata minimal 9 dari 12, selisih antarnegara tidak lebih dari 2 poin.", True, INK)],
], size=10, align=PP_ALIGN.LEFT)

# ---------- 10. Lingkungan latihan Hermes ----------
s = kerangka("Lingkungan Latihan", "Hermes Agent", "Tiga agen contoh di satu grup Telegram. Semua pesan ke donatur melewati pemeriksaan manusia")
# tim
tm = kotak(s, ML, 2.9, 2.0, 1.2, BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
isi_kotak(tm, [[("Tim MFA", True, "FFFFFF")], [("CRM dan marketing", False, "FFFFFF")]], size=12)
tg = kotak(s, ML + 2.6, 2.9, 2.1, 1.2, CYAN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
isi_kotak(tg, [[("Grup Telegram", True, "FFFFFF")], [("hanya anggota terdaftar", False, "FFFFFF")]], size=12)
garis(s, ML + 2.0, 3.5, ML + 2.6, 3.5, INK, 1.5, panah=True)
agen = [
    ("Agen Analis", "Membaca data kampanye, menghitung biaya per donasi, laporan tiap Senin"),
    ("Agen Iklan", "Menyusun brief dan variasi teks iklan per negara dari temuan Analis"),
    ("Agen CRM", "Mengelompokkan donatur dan menyusun draf pesan tindak lanjut"),
]
for i, (n, ket) in enumerate(agen):
    y = 1.45 + i * 1.5
    a = kotak(s, ML + 5.4, y, 3.4, 1.25, GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    isi_kotak(a, [[(n, True, TEAL_T)], [(ket, False, INK)]], size=10)
    garis(s, ML + 4.7, 3.5, ML + 5.4, y + 0.62, INK, 1.0, panah=True)
srv = kotak(s, ML + 9.4, 1.45, SW - 2 * ML - 9.4, 2.15, "FFFFFF", line=TEAL)
isi_kotak(srv, [
    [("Server latihan Hermes", True, TEAL_T)],
    [("3 profil, masing-masing dengan SOUL.md, memori, skill, dan jadwal sendiri", False, INK)],
    [("Model lewat kunci API latihan dengan batas belanja", False, INK)],
], size=10)
cek = kotak(s, ML + 9.4, 3.85, SW - 2 * ML - 9.4, 2.4, LILAC, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
isi_kotak(cek, [
    [("Pengaturan aman", True, INK)],
    [("Persetujuan perintah aktif, mode YOLO mati", False, INK)],
    [("Allowlist pengguna Telegram", False, INK)],
    [("Batas belanja API per peserta", False, INK)],
    [("Data latihan rekaan, bukan data donatur", False, INK)],
    [("Manusia memeriksa sebelum pesan keluar", False, INK)],
], size=10, align=PP_ALIGN.LEFT)
garis(s, ML + 8.8, 2.1, ML + 9.4, 2.1, INK, 1.0)
teks(s, ML, 6.3, 9, 0.6, "Peserta memasang Hermes di laptop sendiri di Modul 6. Server latihan dipakai untuk demo Modul 5, sebagai cadangan bila laptop belum siap, dan untuk latihan tiga agen di Modul 7.", size=10, color=MUTED)

# ---------- 11. Persiapan dan evaluasi ----------
s = kerangka("Persiapan Teknis", "dan Evaluasi")
rows = [[{"t": a, "align": PP_ALIGN.CENTER, "bold": True}, b, c] for a, b, c, _ in d.PERSIAPAN]
tabel(s, ML, 1.15, 7.4, ["Kapan", "Kegiatan", "Penanggung jawab"], [0.7, 4.4, 2.3], rows, size=9, tinggi_kepala=0.35, tinggi_baris=[0.5] * len(rows))
rows = [[{"t": a, "bold": True}, b, c] for a, b, c in d.EVALUASI]
tabel(s, ML + 7.65, 1.15, SW - 2 * ML - 7.65, ["Level Kirkpatrick", "Alat ukur", "Target"], [1.2, 1.85, SW - 2 * ML - 7.65 - 3.05], rows, size=9, tinggi_kepala=0.35)

# ---------- 12. Hasil dibawa pulang ----------
s = kerangka("Hasil yang", "Dibawa Pulang", "Setiap output dihasilkan di topik yang disebut")
half = (len(d.HASIL) + 1) // 2
for col, part in enumerate([d.HASIL[:half], d.HASIL[half:]]):
    rows = [[{"t": t, "align": PP_ALIGN.CENTER, "bold": True, "color": TEAL_T}, o] for o, t in part]
    tabel(s, ML + col * 6.2, 1.4, 5.95, ["Topik", "Output"], [0.9, 5.05], rows, size=10, tinggi_kepala=0.35, tinggi_baris=[0.6] * len(rows))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("tersimpan:", os.path.normpath(OUT))
