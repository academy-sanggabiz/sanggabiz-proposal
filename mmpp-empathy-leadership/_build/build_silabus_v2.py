"""Pembuat v2 Kurikulum dan Silabus PT MMPP (gaya slide landscape 16:9), versi 1 hari.

Arsip v2. v1 (2 hari) dibuat ulang dengan build_silabus_v1.py.

Gaya mengikuti reference/gaya-silabus/ (deck MyFundAction): judul dua warna,
logo Sanggabiz dalam kapsul teal, tabel berkepala teal, kaki halaman kontak.

Pemakaian: python3 mmpp-empathy-leadership/_build/build_silabus_v2.py
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
LOGO = ROOT / "assets" / "logo-sanggabiz-putih.png"
OUT = ROOT.parent / "silabus" / (
    "v2 Kurikulum dan Silabus 1 Hari - Communication and Teamwork Leadership "
    "Based on Empathy - PT MMPP.pptx"
)
FOOT_RIGHT = "PT MMPP | v2, 26 November 2026"

INK = RGBColor(0x1D, 0x1D, 0x1F)
TEAL = RGBColor(0x0E, 0x8A, 0x8A)
TEAL_H = RGBColor(0x15, 0x90, 0x8F)
TEAL_D = RGBColor(0x0D, 0x5C, 0x5B)
TEAL_L = RGBColor(0xD7, 0xEC, 0xEC)
ROW_ALT = RGBColor(0xF2, 0xF8, 0xF9)
CYAN = RGBColor(0x33, 0xBC, 0xCF)
BLUE = RGBColor(0x00, 0x71, 0xCE)
GREY = RGBColor(0xD9, 0xD9, 0xD9)
GREY_T = RGBColor(0x55, 0x55, 0x55)
GREY_F = RGBColor(0x99, 0x99, 0x99)
PINK = RGBColor(0xE2, 0xA9, 0xF1)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)
FONT = "Arial"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


# ---------- alat bantu ----------
def _run(p, text, size=10, bold=False, color=INK, italic=False):
    r = p.add_run()
    r.text = text
    f = r.font
    f.name = FONT
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = color
    return r


def text(slide, x, y, w, h, parts, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         spacing=None):
    """parts: list paragraf. Tiap paragraf: str atau list (teks, opsi)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.03))
    fill_tf(tf, parts, align, spacing)
    return tb


def fill_tf(tf, parts, align=PP_ALIGN.LEFT, spacing=None, default=None):
    default = default or {}
    first = True
    for para in parts:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        if spacing:
            p.space_after = Pt(spacing)
        runs = para if isinstance(para, list) else [(para, {})]
        for t, opt in runs:
            o = dict(default)
            o.update(opt)
            _run(p, t, **o)


def box(slide, x, y, w, h, fill, shape=MSO_SHAPE.RECTANGLE, line=None,
        parts=None, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, shadow=False):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(0.75)
    if not shadow:
        s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.12
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right"):
        setattr(tf, m, Inches(0.08))
    for m in ("margin_top", "margin_bottom"):
        setattr(tf, m, Inches(0.04))
    if parts:
        fill_tf(tf, parts, align)
    return s


def line(slide, x1, y1, x2, y2, color=BLACK, width=0.75):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    return c


def page(black, teal, sub=None):
    s = prs.slides.add_slide(BLANK)
    text(s, 0.55, 0.32, 10.0, 0.6, [[(black + "  ", {"size": 24, "bold": True}),
                                    (teal, {"size": 24, "bold": True, "color": TEAL})]])
    if sub:
        text(s, 0.55, 0.9, 10.0, 0.4, [[(sub, {"size": 12, "color": GREY_T})]])
    box(s, 10.78, 0.34, 2.0, 0.5, TEAL_H, MSO_SHAPE.ROUNDED_RECTANGLE)
    s.shapes[-1].adjustments[0] = 0.5
    s.shapes.add_picture(str(LOGO), Inches(11.06), Inches(0.45), Inches(1.44), Inches(0.28))
    line(s, 0.55, 7.0, 12.78, 7.0)
    text(s, 0.55, 7.05, 12.23, 0.3, [[
        ("WhatsApp 0877-7413-4288     www.sanggabiz.com     partnership@sanggabiz.com",
         {"size": 8, "color": GREY_T}),
        ("          " + FOOT_RIGHT, {"size": 8, "color": GREY_F})]])
    return s


def table(slide, x, y, widths, header, rows, size=9, head_size=10, row_h=0.3,
          head_h=0.32, styles=None, merge_first=None):
    """rows: list baris, sel berupa str atau list paragraf (lihat fill_tf).
    styles: dict kolom -> dict opsi (bold, color, align, fill)."""
    styles = styles or {}
    nr, nc = len(rows) + 1, len(widths)
    gt = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(widths)),
                                Inches(head_h + row_h * len(rows)))
    t = gt.table
    tblPr = t._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for i, w in enumerate(widths):
        t.columns[i].width = Inches(w)
    t.rows[0].height = Inches(head_h)
    for i in range(1, nr):
        t.rows[i].height = Inches(row_h)
    for j, h in enumerate(header):
        c = t.cell(0, j)
        c.fill.solid()
        c.fill.fore_color.rgb = TEAL_H
        c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.text_frame.word_wrap = True
        fill_tf(c.text_frame, [[(h, {"size": head_size, "bold": True, "color": WHITE})]],
                PP_ALIGN.CENTER)
    for i, r in enumerate(rows, start=1):
        for j, val in enumerate(r):
            c = t.cell(i, j)
            st = styles.get(j, {})
            c.fill.solid()
            c.fill.fore_color.rgb = st.get("fill", WHITE if i % 2 else ROW_ALT)
            c.vertical_anchor = st.get("anchor", MSO_ANCHOR.MIDDLE)
            for m in ("margin_left", "margin_right"):
                setattr(c, m, Inches(0.06))
            for m in ("margin_top", "margin_bottom"):
                setattr(c, m, Inches(0.04))
            c.text_frame.word_wrap = True
            parts = val if isinstance(val, list) else [val]
            base = {"size": st.get("size", size), "bold": st.get("bold", False),
                    "color": st.get("color", INK)}
            fill_tf(c.text_frame, [p if isinstance(p, list) else [(p, {})] for p in parts],
                    st.get("align", PP_ALIGN.LEFT), default=base)
    if merge_first:
        for a, b in merge_first:
            top = t.cell(a, 0)
            top.merge(t.cell(b, 0))
    _borders(t)
    return t


def _borders(t):
    from pptx.oxml.ns import qn
    from lxml import etree
    for row in t.rows:
        for c in row.cells:
            tcPr = c._tc.get_or_add_tcPr()
            for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                ln = etree.SubElement(tcPr, qn(tag), w="9525")
                sf = etree.SubElement(ln, qn("a:solidFill"))
                etree.SubElement(sf, qn("a:srgbClr"), val="000000")


# ---------- 1. sampul ----------
s = prs.slides.add_slide(BLANK)
box(s, 0, 0, 13.333, 7.5, TEAL_D)
box(s, 0, 0, 0.35, 7.5, CYAN)
s.shapes.add_picture(str(LOGO), Inches(0.9), Inches(0.8), Inches(2.78), Inches(0.55))
text(s, 0.9, 2.2, 11.0, 0.5, [[("KURIKULUM DAN SILABUS", {"size": 14, "bold": True, "color": CYAN})]])
text(s, 0.9, 2.7, 11.5, 1.6, [[("Communication & Teamwork Leadership Based on Empathy",
                                {"size": 36, "bold": True, "color": WHITE})]])
text(s, 0.9, 4.3, 11.0, 0.5, [[("Pelatihan in-house satu hari untuk para pemimpin: mendengar, "
                                "memberi umpan balik, memimpin percakapan sulit, dan membangun "
                                "tim yang aman untuk bicara", {"size": 16, "color": WHITE})]])
text(s, 0.9, 5.7, 11.0, 0.9, [[("Disiapkan untuk PT Makassar Mega Putra Prima", {"size": 13, "color": WHITE})],
                              [("November 2026", {"size": 13, "color": WHITE})]])

# ---------- 2. kebutuhan dan hasil ----------
s = page("Kebutuhan dan", "Hasil yang Diharapkan",
         "Diambil dari kebutuhan pelatihan yang disampaikan PT MMPP, November 2026")


def numbered_panel(slide, x, title, color, items):
    box(slide, x, 1.45, 5.95, 0.5, color,
        parts=[[(title, {"size": 12, "bold": True, "color": WHITE})]])
    box(slide, x, 1.95, 5.95, 4.75, WHITE, line=GREY)
    for k, it in enumerate(items):
        y = 2.1 + k * 0.9
        box(slide, x + 0.2, y + 0.08, 0.42, 0.42, color, MSO_SHAPE.OVAL,
            parts=[[(str(k + 1), {"size": 10, "bold": True, "color": WHITE})]])
        text(slide, x + 0.75, y, 5.0, 0.85, [[(it, {"size": 11})]], anchor=MSO_ANCHOR.MIDDLE)


numbered_panel(s, 0.55, "Kebutuhan PT MMPP", TEAL_H, [
    "Memperkuat keterampilan komunikasi para pemimpin",
    "Membangun pola pikir kolaboratif di dalam dan antartim",
    "Mengembangkan kemampuan memimpin dengan pendekatan berbasis empati",
    "Pelatihan luring dan privat, khusus karyawan PT MMPP",
    "Januari sampai Maret 2027 di Makassar atau Jakarta, dalam satu paket dengan tempat",
])
numbered_panel(s, 6.75, "Yang bisa dikerjakan peserta setelah pelatihan", BLUE, [
    "Mendengar sampai paham isi dan perasaan anggota tim sebelum menanggapi",
    "Memberi umpan balik dengan model SBI tanpa menjatuhkan martabat orang",
    "Memimpin percakapan sulit dengan Alur Percakapan Empatik, skor minimal 6 dari 8",
    "Membaca skor rasa aman psikologis timnya dan menyusun norma tim",
    "Menjalankan rencana aksi 30 hari yang dipantau lewat survei anggota tim",
])

# ---------- 3. riset pendukung ----------
s = page("Mengapa", "Empati dalam Memimpin",
         "Empati adalah keterampilan kerja yang bisa dilatih dan diukur. Empat temuan riset yang menjadi dasar program")
cards = [
    ("6.731 manajer, 38 negara",
     "Manajer yang dinilai bawahannya lebih empatik dinilai atasannya berkinerja lebih baik. "
     "Pengaruh empati lebih besar di budaya dengan jarak kekuasaan tinggi.",
     "Center for Creative Leadership, 2016"),
    ("76% dan 32%",
     "Karyawan dengan pemimpin senior yang sangat empatik merasa terlibat 76 persen, "
     "dibanding 32 persen pada pemimpin yang kurang empatik. Survei 889 karyawan.",
     "Catalyst, 2021"),
    ("51 tim kerja",
     "Rasa aman psikologis berkaitan dengan perilaku belajar tim, dan perilaku belajar "
     "berkaitan dengan kinerja tim. Studi di perusahaan manufaktur.",
     "Edmondson, Administrative Science Quarterly, 1999"),
    ("Faktor pertama dari lima",
     "Riset Google atas tim-timnya sendiri menempatkan rasa aman psikologis sebagai faktor "
     "paling mendasar dari lima ciri tim yang efektif.",
     "Google, Project Aristotle, 2016"),
]
for k, (big, body, src) in enumerate(cards):
    x = 0.55 + k * 3.1
    box(s, x, 1.45, 2.95, 3.3, ROW_ALT, MSO_SHAPE.ROUNDED_RECTANGLE, line=GREY)
    text(s, x + 0.15, 1.6, 2.65, 0.8, [[(big, {"size": 18, "bold": True, "color": TEAL})]])
    text(s, x + 0.15, 2.4, 2.65, 1.7, [[(body, {"size": 11})]])
    box(s, x + 0.15, 4.15, 2.65, 0.45, PINK, MSO_SHAPE.ROUNDED_RECTANGLE,
        parts=[[(src, {"size": 8.5, "bold": True})]])
box(s, 0.55, 4.95, 12.23, 1.75, WHITE, line=GREY, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT,
    parts=[
        [("Yang membuat program ini berbeda", {"size": 12, "bold": True, "color": TEAL})],
        [("Kasus nyata PT MMPP. ", {"size": 11, "bold": True}),
         ("Asesmen awal mengumpulkan percakapan sulit yang benar-benar dihadapi peserta. Tiga kasus terbanyak menjadi bahan role play.", {"size": 11})],
        [("Nilai lokal siri' na pacce. ", {"size": 11, "bold": True}),
         ("Pacce berarti ikut merasakan kesusahan orang lain, siri' berarti harga diri. Keduanya dipakai sebagai bahasa bersama untuk empati dan menjaga martabat saat menegur.", {"size": 11})],
        [("Terukur sebelum dan sesudah. ", {"size": 11, "bold": True}),
         ("Rubrik percakapan 0 sampai 8 dipakai di role play. Survei singkat oleh anggota tim diambil sebelum pelatihan dan 30 hari sesudahnya.", {"size": 11})],
    ])

# ---------- 4. alur program ----------
s = page("Alur Program", "dan Metode",
         "Enam tahap dari asesmen kebutuhan sampai laporan. Metode: ADDIE, andragogi, Bloom, Kirkpatrick")
steps = [
    ("Asesmen kebutuhan",
     "Formulir diri untuk peserta, survei singkat oleh 3 anggota tim tiap peserta, survei rasa aman tim 7 butir, wawancara 30 menit dengan 3 sampai 5 peserta dan atasannya",
     "Profil peserta dan 3 kasus utama"),
    ("Penyesuaian modul dan kasus",
     "Kasus role play, kalimat latihan, dan kartu peran disusun dari hasil asesmen. Modul disetujui HR PT MMPP sebelum dicetak",
     "Modul, kartu peran, lembar kerja"),
    ("Persiapan tempat",
     "Ruang kelas dengan meja kelompok 5 orang, ruang cukup untuk latihan bertiga, proyektor, flipchart, konsumsi",
     "Ruang dan bahan siap"),
    ("Pelatihan 1 hari",
     "Enam modul, 340 menit materi, 08.30 - 16.30. Pre-test di awal dan post-test di akhir",
     "Skor tes, rubrik, norma tim, rencana 30 hari"),
    ("Tindak lanjut 30 hari",
     "Survei anggota tim diulang di hari ke-30. Sesi daring 90 menit untuk berbagi penerapan dan kendala",
     "Skor survei sebelum dan sesudah"),
    ("Evaluasi dan laporan",
     "Analisis pre-test dan post-test, skor rubrik, survei kepuasan, perubahan skor survei tim, rekomendasi lanjutan",
     "Laporan akhir"),
]
for k, (ttl, body, out) in enumerate(steps):
    x = 0.55 + k * 2.07
    box(s, x, 1.5, 1.89, 3.55, GREY, MSO_SHAPE.ROUNDED_RECTANGLE)
    box(s, x + 0.69, 1.62, 0.5, 0.5, CYAN, MSO_SHAPE.OVAL,
        parts=[[(str(k + 1), {"size": 12, "bold": True, "color": WHITE})]])
    text(s, x + 0.08, 2.2, 1.73, 0.65, [[(ttl, {"size": 11, "bold": True})]], align=PP_ALIGN.CENTER)
    text(s, x + 0.08, 2.85, 1.73, 2.1, [[(body, {"size": 8.5})]])
    box(s, x + 0.08, 5.15, 1.73, 0.6, PINK, MSO_SHAPE.ROUNDED_RECTANGLE,
        parts=[[(out, {"size": 8.5, "bold": True})]])
    if k < 5:
        line(s, x + 1.9, 3.3, x + 2.06, 3.3, TEAL_H, 1.5)
methods = [
    ("ADDIE: ", "Alur program dari asesmen kebutuhan sampai evaluasi (tahap 1 sampai 6)"),
    ("Andragogi: ", "Peserta belajar dari kasusnya sendiri lewat role play dan refleksi, trainer berperan sebagai fasilitator"),
    ("Taksonomi Bloom revisi: ", "Tujuan tiap topik ditulis dengan kata kerja terukur, kode C2 sampai C6"),
    ("Kirkpatrick: ", "Evaluasi level 1 sampai 3: survei kepuasan, pre-test dan post-test, rubrik role play, survei tim 30 hari"),
]
for k, (a, b) in enumerate(methods):
    text(s, 0.55 + k * 3.08, 5.95, 2.95, 0.9, [[(a, {"size": 9, "bold": True, "color": TEAL}),
                                               (b, {"size": 9})]])

# ---------- 5. ringkasan program ----------
s = page("Ringkasan", "Program",
         "Satu hari tatap muka, 340 menit materi, ditambah tindak lanjut daring 90 menit di hari ke-30")
table(s, 0.55, 1.4, [3.2, 5.3, 1.0, 2.73],
      ["Modul", "Topik", "Menit", "Hasil utama"],
      [
          ["M1 Empati dalam Kepemimpinan", "1.1 Empati di tempat kerja dan buktinya\n1.2 Pacce: empati dalam nilai lokal", "40", "Daftar perilaku siri' dan pacce"],
          ["M2 Mendengar untuk Memahami", "2.1 Tingkat mendengar dan penghambatnya\n2.2 Bertanya terbuka dan merefleksikan perasaan", "60", "Lembar cek praktik mendengar"],
          ["M3 Umpan Balik yang Menjaga Martabat", "3.1 Bahasa yang menjaga martabat\n3.2 Umpan balik dengan model SBI dan niat", "60", "Naskah umpan balik dari kasus nyata"],
          ["M4 Percakapan Sulit dengan Empati", "4.1 Alur Percakapan Empatik 4 langkah\n4.2 Role play kasus nyata", "90", "Skor rubrik percakapan 0 sampai 8"],
          ["M5 Tim yang Aman untuk Bicara", "5.1 Rasa aman psikologis dalam tim\n5.2 Norma tim", "60", "Draf norma tim"],
          ["M6 Rencana Aksi 30 Hari", "6.1 Profil empati dan rencana aksi", "30", "Rencana aksi 30 hari"],
          [[[("Jumlah materi", {"bold": True})]], "Di luar pembukaan, tes, dan penutupan (50 menit)", [[("340", {"bold": True})]], ""],
      ],
      size=10.5, row_h=0.6,
      styles={0: {"bold": True, "color": TEAL}, 2: {"align": PP_ALIGN.CENTER}})
text(s, 0.55, 6.25, 12.23, 0.6, [[(
    "Rancangan untuk satu kelas berisi paling banyak 24 peserta dengan satu trainer dan satu co-fasilitator. "
    "Jumlah kelas menyesuaikan jumlah peserta. Jam mengikuti waktu setempat. Kelas dibuat padat praktik: "
    "sekitar 240 dari 340 menit materi dipakai untuk latihan, role play, dan kerja kelompok.", {"size": 10, "color": GREY_T})]])

# ---------- 6 sampai 9. silabus per modul ----------
HEAD = ["Modul & fokus", "Topik", "Outline materi", "Tujuan pembelajaran", "Format"]
WID = [2.2, 2.0, 4.2, 2.75, 1.08]


def bullets(*items):
    return ["• " + i for i in items]


def module_block(slide, y, code, name, focus, topics, row_h):
    rows = []
    for k, (tt, outline, goal, fmt) in enumerate(topics):
        first = [[(f"{code} {name}", {"bold": True, "color": TEAL, "size": 11})],
                 [("Fokus: " + focus, {"italic": True, "size": 9.5, "color": GREY_T})]] if k == 0 else ""
        rows.append([first, [[(tt, {"bold": True, "size": 12})]], bullets(*outline), goal,
                     [[(fmt, {"bold": True, "color": TEAL})]]])
    return rows


def module_slide(title, blocks, row_h=1.2):
    """blocks: list (code, name, focus, topics). Beberapa modul boleh di satu slide."""
    s = page("Materi & Silabus", title)
    rows, merges, start = [], [], 1
    for code, name, focus, topics in blocks:
        r = module_block(s, 0, code, name, focus, topics, row_h)
        rows += r
        if len(r) > 1:
            merges.append((start, start + len(r) - 1))
        start += len(r)
    table(s, 0.55, 1.2, WID, HEAD, rows, size=10.5, row_h=row_h,
          styles={0: {"fill": TEAL_L}, 4: {"align": PP_ALIGN.CENTER}},
          merge_first=merges or None)
    return s


M1 = ("M1", "Empati dalam Kepemimpinan",
      "Peserta memandang empati sebagai keterampilan kerja yang bisa dilatih, diukur, dan tetap sejalan dengan standar kerja yang tinggi.",
      [
          ("1.1 Empati di tempat kerja dan buktinya",
           ["Tiga bentuk empati: memahami cara pandang orang (kognitif), ikut merasakan (afektif), dan tergerak membantu (kepedulian)",
            "Empati berbeda dengan setuju atau menurunkan target",
            "Data riset: CCL atas 6.731 manajer di 38 negara dan Catalyst 2021"],
           "C2 Menjelaskan tiga bentuk empati dan bedanya dengan sikap serba membolehkan, dengan contoh dari pekerjaannya sendiri",
           "Teori, Diskusi\n20 menit"),
          ("1.2 Pacce: empati dalam nilai lokal",
           ["Siri' na pacce: harga diri dan ikut merasakan kesusahan orang lain dalam komunitas",
            "Siri' di tempat kerja: menjaga martabat anggota tim saat menegur",
            "Pacce di tempat kerja: solidaritas yang tetap menuntut tanggung jawab",
            "Nilai serupa dari daerah asal peserta lain"],
           "C2 Mengaitkan nilai siri' na pacce dengan perilaku memimpin sehari-hari",
           "Diskusi kelompok\n20 menit"),
      ])
M2 = ("M2", "Mendengar untuk Memahami",
      "Peserta mendengar sampai paham isi dan perasaan lawan bicara sebelum menanggapi.",
      [
          ("2.1 Tingkat mendengar dan penghambatnya",
           ["Tiga tingkat mendengar: menunggu giliran bicara, mendengar isi, mendengar isi dan perasaan",
            "Penghambat: memotong, buru-buru memberi solusi, menghakimi, sibuk dengan ponsel",
            "Latihan mendengar 2 menit tanpa menyela"],
           "C3 Mempraktikkan mendengar tanpa menyela dan meringkas ulang isi pembicaraan dengan tepat",
           "Demo, Latihan berpasangan\n20 menit"),
          ("2.2 Bertanya terbuka dan merefleksikan perasaan",
           ["Pertanyaan terbuka: apa, bagaimana, ceritakan",
            "Refleksi isi dan refleksi perasaan (\"sepertinya Bapak kecewa karena...\"), lalu memberi jeda",
            "Praktik bertiga: pembicara, pendengar, dan pengamat dengan lembar cek, tiga putaran"],
           "C3 Menerapkan pertanyaan terbuka dan refleksi perasaan dalam percakapan 6 menit. C5 Menilai praktik rekan dengan lembar cek",
           "Praktik bertiga\n40 menit"),
      ])
M3 = ("M3", "Umpan Balik yang Menjaga Martabat",
      "Peserta memberi umpan balik tanpa menjatuhkan harga diri orang lain.",
      [
          ("3.1 Bahasa yang menjaga martabat",
           ["Memisahkan orang dari perilaku: \"laporan terlambat dua hari\" dan \"kamu tidak bisa diandalkan\"",
            "Teguran empat mata, pujian di depan tim",
            "Latihan mengubah 5 kalimat teguran dari kasus asesmen"],
           "C3 Mengubah kalimat teguran yang menyerang pribadi menjadi kalimat yang menyebut perilaku dan dampaknya",
           "Teori, Latihan berpasangan\n15 menit"),
          ("3.2 Umpan balik dengan model SBI dan niat",
           ["Model Situation-Behavior-Impact (CCL): situasi, perilaku yang terlihat, dampak",
            "Menambah pertanyaan tentang niat agar umpan balik menjadi dua arah",
            "Umpan balik untuk perilaku yang perlu diperbaiki dan yang perlu dipertahankan",
            "Praktik dengan kasus dari asesmen awal"],
           "C3 Menyusun dan menyampaikan umpan balik SBI dengan pertanyaan niat untuk satu kasus nyata",
           "Demo, Praktik berpasangan\n45 menit"),
      ])
M4 = ("M4", "Percakapan Sulit dengan Empati",
      "Peserta memimpin percakapan sulit dengan Alur Percakapan Empatik 4 langkah yang dinilai dengan rubrik 0 sampai 8.",
      [
          ("4.1 Alur Percakapan Empatik 4 langkah",
           ["Ciri percakapan sulit: taruhan tinggi, pendapat berbeda, emosi kuat",
            "Siapkan: pisahkan fakta dan tafsiran, tetapkan tujuan bersama",
            "Dengarkan: buka dengan fakta dan pertanyaan, refleksikan perasaan",
            "Akui: sebut kepentingan kedua pihak tanpa menyalahkan",
            "Sepakati: langkah, penanggung jawab, waktu, cara memantau"],
           "C3 Menyusun lembar persiapan percakapan sulit dengan 4 langkah untuk satu kasus sendiri",
           "Teori, Demo, Latihan individu\n30 menit"),
          ("4.2 Role play kasus nyata",
           ["Tiga kasus dari asesmen, misalnya target tidak tercapai, konflik antaranggota tim, keputusan yang tidak populer",
            "Tiap peserta menjadi pemimpin satu kali, 8 menit per putaran",
            "Pengamat memberi skor dengan rubrik 0 sampai 8"],
           "C3 Memimpin percakapan sulit 8 menit dengan Alur 4 langkah. C5 Menilai percakapan rekan dengan rubrik 0 sampai 8",
           "Role play bertiga\n60 menit"),
      ])
M5 = ("M5", "Tim yang Aman untuk Bicara",
      "Peserta membangun kebiasaan tim yang membuat anggota berani bertanya, mengaku salah, dan memberi usul.",
      [
          ("5.1 Rasa aman psikologis dalam tim",
           ["Definisi Edmondson (1999) dan temuan Project Aristotle Google",
            "Konflik tugas dan konflik hubungan dalam kolaborasi lintas fungsi",
            "Membaca skor survei 7 butir tim sendiri dari asesmen awal"],
           "C2 Menjelaskan rasa aman psikologis. C4 Menganalisis skor survei timnya dan menentukan butir terendah",
           "Teori, Analisis data tim\n25 menit"),
          ("5.2 Norma tim",
           ["Lima kesepakatan perilaku: rapat, beda pendapat, mengakui salah, saling bantu",
            "Perilaku pemimpin yang memberi contoh: mengakui tidak tahu, bertanya, berterima kasih atas kabar buruk",
            "Cara membawa norma ke rapat tim masing-masing"],
           "C6 Menyusun draf norma tim untuk dibahas di rapat tim masing-masing",
           "Praktik kelompok\n35 menit"),
      ])
M6 = ("M6", "Rencana Aksi 30 Hari",
      "Peserta memilih dua perilaku prioritas dan menyusun rencana yang bisa dipantau anggota timnya.",
      [
          ("6.1 Profil empati dan rencana aksi",
           ["Profil empati dari asesmen awal: skor diri dan skor dari 3 anggota tim",
            "Dua perilaku prioritas dan tindakan mingguan yang bisa diamati",
            "Cara memantau: catatan mingguan dan survei tim di hari ke-30",
            "Berbagi rencana dengan rekan sebagai mitra pengingat"],
           "C4 Membandingkan penilaian diri dengan penilaian tim. C6 Menyusun rencana aksi 30 hari dengan ukuran keberhasilan",
           "Refleksi, Praktik individu\n30 menit"),
      ])

module_slide("M1 dan M2", [M1, M2], row_h=1.15)
module_slide("M3 Umpan Balik yang Menjaga Martabat", [M3], row_h=2.0)
module_slide("M4 Percakapan Sulit dengan Empati", [M4], row_h=2.0)
module_slide("M5 dan M6", [M5, M6], row_h=1.2)

# ---------- 10 dan 11. aktivitas dan ukuran ----------
AHEAD = ["Topik", "Aktivitas di kelas (langkah dan menit)", "Alat dan media", "Output", "Ukuran keberhasilan"]
AWID = [0.75, 5.2, 1.9, 2.0, 2.38]


def activity_slide(teal, rows, row_h=0.9):
    s = page("Aktivitas", teal)
    table(s, 0.55, 1.2, AWID, AHEAD, rows, size=9.5, row_h=row_h,
          styles={0: {"bold": True, "color": TEAL, "align": PP_ALIGN.CENTER}})


activity_slide("dan Ukuran Keberhasilan M1 sampai M3", [
    ["1.1", "1. Trainer menayangkan dua tanggapan pemimpin atas keluhan anggota tim, peserta memilih yang empatik (6)\n2. Penjelasan tiga bentuk empati dan data riset (8)\n3. Berpasangan, peserta menulis satu contoh tiap bentuk dari pekerjaannya (6)",
     "Slide, kartu kasus, lembar kerja", "Catatan tiga bentuk empati dengan contoh", "Tiap peserta menulis 3 contoh yang sesuai bentuknya"],
    ["1.2", "1. Trainer menjelaskan arti siri' na pacce dari sumber tertulis (5)\n2. Kelompok 4 orang menulis perilaku pemimpin yang mencerminkan dan yang melanggar siri' dan pacce (10)\n3. Dua kelompok membacakan hasil (5)",
     "Flipchart, kertas tempel, spidol", "Daftar perilaku siri' dan pacce di tempat kerja", "Tiap kelompok menulis minimal 4 perilaku yang dapat diamati"],
    ["2.1", "1. Trainer memperagakan dua cara mendengar keluhan yang sama bersama co-fasilitator (6)\n2. Penjelasan tingkat mendengar dan penghambatnya (6)\n3. Berpasangan: A bercerita 2 menit, B mendengar tanpa menyela lalu meringkas, bertukar peran (8)",
     "Slide, pengatur waktu", "Ringkasan lisan cerita rekan", "Minimal 80 persen pencerita menyatakan ringkasan rekannya tepat"],
    ["2.2", "1. Penjelasan pertanyaan terbuka dan refleksi dengan 6 contoh kalimat (7)\n2. Bertiga, 3 putaran x 10 menit: 6 menit percakapan, 4 menit umpan balik pengamat (30)\n3. Satu temuan dari tiap kelompok (3)",
     "Kartu topik percakapan, lembar cek pengamat", "Lembar cek pengamat 3 putaran", "Di putaran ketiga tiap peserta memakai minimal 2 pertanyaan terbuka dan 1 refleksi perasaan"],
    ["3.1", "1. Penjelasan memisahkan orang dan perilaku (5)\n2. Berpasangan menulis ulang 5 kalimat teguran rekaan dari kasus asesmen (10)",
     "Lembar 5 kalimat teguran", "5 kalimat teguran yang sudah diperbaiki", "Minimal 4 dari 5 kalimat menyebut perilaku dan dampak"],
    ["3.2", "1. Trainer memperagakan umpan balik tanpa struktur, lalu dengan SBI dan niat (8)\n2. Peserta menulis 1 naskah SBI dari kasusnya (10)\n3. Berpasangan menyampaikan naskah, penerima menanggapi, bertukar peran (20)\n4. Dua pasangan tampil, kelas memberi masukan (7)",
     "Lembar naskah SBI", "Naskah umpan balik untuk kasus nyata", "Naskah memuat situasi, perilaku yang terlihat, dampak, dan satu pertanyaan niat"],
], row_h=0.82)

activity_slide("dan Ukuran Keberhasilan M4 sampai M6", [
    ["4.1", "1. Peserta menulis satu percakapan sulit yang sedang atau akan dihadapinya (5)\n2. Penjelasan alur 4 langkah dan rubrik (10)\n3. Trainer memperagakan alur dengan relawan, kelas menilai dengan rubrik (7)\n4. Peserta mengisi lembar persiapan untuk kasusnya (8)",
     "Kartu Alur Percakapan Empatik, lembar persiapan", "Lembar persiapan percakapan sulit", "Fakta terpisah dari tafsiran, tujuan bersama dan usulan kesepakatan tertulis"],
    ["4.2", "1. Bertiga: pemimpin, anggota tim dengan kartu peran, pengamat. 3 putaran x 18 menit: 8 menit percakapan, 3 menit skor, 7 menit umpan balik (54)\n2. Trainer membahas bagian yang paling sering sulit dari lembar skor (6)",
     "Kartu peran, rubrik 0 sampai 8, pengatur waktu", "Skor rubrik dari pengamat", "Skor rata-rata putaran ketiga minimal 6 dari 8"],
    ["5.1", "1. Penjelasan rasa aman psikologis, konflik tugas dan konflik hubungan (10)\n2. Peserta membaca skor survei 7 butir timnya dari asesmen awal (5)\n3. Berpasangan membahas butir terendah dan penyebabnya (10)",
     "Laporan skor tim per peserta", "Skor rasa aman tim dan butir terendah", "Tiap peserta menyebut butir terendah dan satu penyebab yang mungkin"],
    ["5.2", "1. Trainer menunjukkan contoh norma tim (5)\n2. Peserta per unit kerja menyusun 5 norma (20)\n3. Galeri: kelompok lain memberi satu pertanyaan untuk tiap norma (10)",
     "Templat norma tim, flipchart", "Draf norma tim", "Tiap norma menyebut perilaku yang dapat diamati"],
    ["6.1", "1. Peserta membaca profil empati pribadi dari asesmen awal (5)\n2. Peserta mengisi kanvas rencana 30 hari (15)\n3. Berpasangan berbagi rencana dan menetapkan mitra pengingat (10)",
     "Profil empati cetak, kanvas rencana 30 hari", "Profil empati dan rencana aksi 30 hari", "Rencana memuat 2 perilaku, tindakan mingguan, dan ukuran yang bisa dilihat anggota tim"],
], row_h=0.98)

# ---------- 12. alat kerja ----------
s = page("Alur Percakapan", "Empatik 4 Langkah",
         "Satu alur untuk umpan balik, teguran, dan perbedaan pendapat, dinilai dengan rubrik 0 sampai 8")
langkah = [
    ("Siapkan", "Pisahkan fakta dan tafsiran. Tetapkan tujuan yang sama-sama diinginkan",
     "Fakta tertulis terpisah dari tafsiran, tujuan bersama jelas"),
    ("Dengarkan", "Buka dengan fakta dan satu pertanyaan terbuka. Refleksikan perasaan, beri jeda",
     "Pertanyaan terbuka dan minimal satu refleksi perasaan"),
    ("Akui", "Sebut kepentingan dan kekhawatiran kedua pihak tanpa menyalahkan",
     "Kepentingan kedua pihak disebut, martabat lawan bicara terjaga"),
    ("Sepakati", "Tutup dengan langkah yang jelas dan cara memantaunya",
     "Langkah, penanggung jawab, waktu, dan cara memantau disebut"),
]
for k, (nm, desc, sk) in enumerate(langkah):
    x = 0.55 + k * 3.1
    box(s, x, 1.45, 2.95, 0.75, TEAL_H if k % 2 == 0 else BLUE, MSO_SHAPE.ROUNDED_RECTANGLE,
        parts=[[(f"{k + 1}  {nm}", {"size": 14, "bold": True, "color": WHITE})]])
    text(s, x + 0.1, 2.28, 2.75, 0.85, [[(desc, {"size": 10})]], align=PP_ALIGN.CENTER)
    box(s, x, 3.15, 2.95, 0.85, ROW_ALT, MSO_SHAPE.ROUNDED_RECTANGLE, line=GREY,
        align=PP_ALIGN.LEFT, parts=[[("Skor 2: ", {"size": 9, "bold": True, "color": TEAL}),
                                     (sk, {"size": 9})]])
box(s, 0.55, 4.25, 8.2, 2.55, WHITE, line=GREY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, parts=[
    [("Contoh rekaan: supervisor dan staf administrasi gudang", {"size": 10.5, "bold": True, "color": TEAL})],
    [("Siapkan: ", {"size": 10, "bold": True}),
     ("Fakta: laporan stok terlambat 3 kali bulan ini. Tafsiran saya: dia kurang peduli. Tujuan bersama: laporan tepat waktu tanpa lembur berlebihan.", {"size": 10})],
    [("Dengarkan: ", {"size": 10, "bold": True}),
     ("\"Laporan stok tiga kali terlambat bulan ini. Bagaimana keadaannya dari sisi kamu?\"", {"size": 10})],
    [("Akui: ", {"size": 10, "bold": True}),
     ("\"Jadi data dari gudang sering baru masuk sore, dan kamu kesal karena kamu yang ditegur. Saya juga perlu laporan itu untuk rapat pagi.\"", {"size": 10})],
    [("Sepakati: ", {"size": 10, "bold": True}),
     ("\"Besok saya bicara dengan kepala gudang supaya data masuk jam 14.00. Jumat kamu kabari saya apakah berjalan.\"", {"size": 10})],
])
box(s, 9.0, 4.25, 3.78, 2.55, TEAL_L, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, parts=[
    [("Cara memakai rubrik", {"size": 10.5, "bold": True, "color": TEAL})],
    [("Tiap langkah diberi skor 0, 1, atau 2. Pengamat mengisi rubrik di role play topik 4.2, tiga putaran. Peserta membawa pulang kartu alur ini untuk dipakai di tempat kerja.", {"size": 9.5})],
    [("Target: skor rata-rata minimal 6 dari 8 di putaran ketiga role play.", {"size": 9.5, "bold": True})],
])

# ---------- 13. rundown ----------
s = page("Rundown", "Satu Hari",
         "08.30 - 16.30 waktu setempat. 390 menit kegiatan: 340 menit materi, 50 menit pembukaan, tes, dan penutupan")
day = [
    ("08.30 - 08.45", "Pembukaan, tujuan pelatihan, kesepakatan kelas"),
    ("08.45 - 08.55", "Pre-test"),
    ("08.55 - 09.35", "M1 Empati dalam Kepemimpinan"),
    ("09.35 - 10.35", "M2 Mendengar untuk Memahami"),
    ("10.35 - 10.50", "Rehat"),
    ("10.50 - 11.50", "M3 Umpan Balik yang Menjaga Martabat"),
    ("11.50 - 12.50", "Ishoma"),
    ("12.50 - 14.20", "M4 Percakapan Sulit dengan Empati"),
    ("14.20 - 14.35", "Rehat"),
    ("14.35 - 15.35", "M5 Tim yang Aman untuk Bicara"),
    ("15.35 - 16.05", "M6 Rencana Aksi 30 Hari"),
    ("16.05 - 16.15", "Post-test"),
    ("16.15 - 16.30", "Survei kepuasan, penutupan, sertifikat"),
]
box(s, 0.55, 1.4, 6.6, 0.45, TEAL_H, parts=[[("Hari pelatihan", {"size": 11, "bold": True, "color": WHITE})]])
table(s, 0.55, 1.9, [1.5, 5.1], ["Waktu", "Kegiatan"],
      [[t, [[(k, {"bold": not k.startswith(("Rehat", "Ishoma"))})]]] for t, k in day],
      size=10, row_h=0.33, head_h=0.28)
box(s, 7.45, 1.4, 5.33, 0.45, BLUE, parts=[[("Sebelum dan sesudah hari pelatihan", {"size": 11, "bold": True, "color": WHITE})]])
for k, (ttl, body) in enumerate([
    ("H-18 sampai H-10  Asesmen awal",
     "Formulir diri, survei 3 anggota tim, survei rasa aman tim, wawancara 3 sampai 5 peserta. Hasilnya menjadi kasus role play dan profil empati, sehingga waktu kelas tidak terpakai untuk mengumpulkan kasus."),
    ("H+30  Tindak lanjut daring, 90 menit",
     "Peserta berbagi hasil rencana aksi, membahas kendala, dan menerima skor survei tim kedua. Survei diisi 3 anggota tim tiap peserta pada minggu sebelumnya."),
]):
    y = 1.95 + k * 1.7
    box(s, 7.45, y, 5.33, 1.55, ROW_ALT, line=GREY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, parts=[
        [(ttl, {"size": 11, "bold": True, "color": TEAL})],
        [(body, {"size": 10.5})]])

# ---------- 14. persiapan dan evaluasi ----------
s = page("Persiapan", "dan Evaluasi")
table(s, 0.55, 1.15, [0.75, 4.35, 2.3], ["Kapan", "Kegiatan", "Penanggung jawab"], [
    ["H-21", "Rapat awal: jumlah peserta, jadwal, kota, daftar peserta dan atasannya", "PT MMPP dan Sanggabiz"],
    ["H-18", "Asesmen awal dikirim: formulir diri, survei 3 anggota tim, survei rasa aman tim", "Sanggabiz, disebarkan HR PT MMPP"],
    ["H-14", "Wawancara 30 menit dengan 3 sampai 5 peserta dan atasannya", "Trainer"],
    ["H-10", "Rekap asesmen, pemilihan 3 kasus utama, profil empati per peserta", "Sanggabiz"],
    ["H-7", "Modul, kartu peran, dan lembar kerja disetujui", "HR PT MMPP"],
    ["H-3", "Cetak bahan, konfirmasi ruang, konsumsi, dan daftar hadir", "Sanggabiz"],
    ["H-1", "Penataan ruang: meja kelompok 5 orang, proyektor, flipchart, pengeras suara", "Sanggabiz dan pihak tempat"],
    ["H+30", "Survei tim kedua dan sesi tindak lanjut daring", "Sanggabiz"],
    ["H+40", "Laporan akhir diserahkan", "Sanggabiz"],
], size=10, row_h=0.52, styles={0: {"bold": True, "align": PP_ALIGN.CENTER}})
table(s, 8.2, 1.15, [1.2, 1.85, 1.53], ["Level Kirkpatrick", "Alat ukur", "Target"], [
    [[[("Level 1 Reaksi", {"bold": True})]], "Survei kepuasan 8 butir di akhir pelatihan", "Rata-rata minimal 4 dari 5"],
    [[[("Level 2 Pembelajaran", {"bold": True})]], "Pre-test dan post-test 10 soal kasus pilihan ganda. Rubrik 0 sampai 8 di role play topik 4.2",
     "Skor tes rata-rata naik. Rubrik rata-rata minimal 6 dari 8 di putaran ketiga"],
    [[[("Level 3 Perilaku", {"bold": True})]], "Survei 3 anggota tim per peserta sebelum pelatihan dan di hari ke-30: 8 butir perilaku empatik dan 7 butir rasa aman tim",
     "Skor dua perilaku prioritas naik pada minimal separuh peserta"],
], size=9.5, row_h=1.35)
text(s, 8.2, 5.65, 4.58, 1.2, [[(
    "Level 4 (dampak bisnis) tidak kami janjikan karena perubahan angka bisnis dalam 30 hari "
    "dipengaruhi banyak hal di luar pelatihan. Bila PT MMPP memiliki data seperti tingkat keluar "
    "karyawan atau hasil survei keterlibatan, data itu bisa dibandingkan pada periode berikutnya.",
    {"size": 9.5, "color": GREY_T})]])

# ---------- 15. hasil yang dibawa pulang ----------
s = page("Hasil yang", "Dibawa Pulang", "Setiap output dihasilkan di topik yang disebut")
left = [
    ["1.1", "Catatan tiga bentuk empati dengan contoh dari pekerjaan"],
    ["1.2", "Daftar perilaku siri' dan pacce di tempat kerja"],
    ["2.2", "Lembar cek pengamat praktik mendengar"],
    ["3.1", "5 kalimat teguran yang sudah diperbaiki"],
    ["3.2", "Naskah umpan balik SBI untuk kasus nyata"],
    ["4.1", "Lembar persiapan percakapan sulit dan kartu Alur 4 langkah"],
]
right = [
    ["4.2", "Skor rubrik percakapan sulit dari pengamat"],
    ["5.1", "Skor rasa aman tim dan butir terendah"],
    ["5.2", "Draf norma tim untuk rapat tim"],
    ["6.1", "Profil empati diri dan tim"],
    ["6.1", "Rencana aksi 30 hari dengan mitra pengingat"],
    ["H+30", "Skor survei tim sebelum dan sesudah"],
]
st = {0: {"bold": True, "color": TEAL, "align": PP_ALIGN.CENTER}}
table(s, 0.55, 1.4, [0.9, 5.05], ["Topik", "Output"], left, size=11, row_h=0.7, styles=st)
table(s, 6.75, 1.4, [0.9, 5.05], ["Topik", "Output"], right, size=11, row_h=0.7, styles=st)

# ---------- 16. rujukan ----------
s = page("Rujukan", "", "Sumber data dan model yang dipakai di kurikulum ini")
refs = [
    "Gentry, W. A., Weber, T. J., dan Sadri, G. (2016). Empathy in the Workplace: A Tool for Effective Leadership. Center for Creative Leadership. doi.org/10.35613/ccl.2016.1070",
    "Catalyst (2021). Empathic Leaders Drive Employee Engagement and Innovation. Rilis media dan laporan The Power of Empathy in Times of Crisis and Beyond. catalyst.org",
    "Edmondson, A. (1999). Psychological Safety and Learning Behavior in Work Teams. Administrative Science Quarterly, 44(2), 350-383. doi.org/10.2307/2666999",
    "Google re:Work (2016). Guide: Understand Team Effectiveness (Project Aristotle). Diliput World Economic Forum, Maret 2016",
    "Center for Creative Leadership. Situation-Behavior-Impact (SBI) Feedback Tool. ccl.org",
    "Siri' na pacce: Good News From Indonesia, 21 Mei 2025, dan kajian nilai siri' na pacce di repositori Universitas Hasanuddin",
    "Anderson, L. W. dan Krathwohl, D. R. (2001). A Taxonomy for Learning, Teaching, and Assessing. Kirkpatrick, D. L. dan Kirkpatrick, J. D. (2006). Evaluating Training Programs, edisi 3",
]
text(s, 0.55, 1.4, 12.23, 5.3, [[(f"{k + 1}.  " + r, {"size": 12})] for k, r in enumerate(refs)], spacing=10)

OUT.parent.mkdir(parents=True, exist_ok=True)
prs.save(OUT)
print("Tersimpan:", OUT)
