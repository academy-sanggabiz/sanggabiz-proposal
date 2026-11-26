"""Pembuat v3 Kurikulum dan Silabus PT MMPP (gaya slide landscape 16:9), versi 1 hari dengan visual SVG
dan contoh modul. Jalankan build_visual.py dan build_modul_contoh.py lebih dulu.

v1 (2 hari): build_silabus_v1.py. v2 (1 hari, tanpa visual): build_silabus_v2.py.

Gaya mengikuti reference/gaya-silabus/ (deck MyFundAction): judul dua warna,
logo Sanggabiz dalam kapsul teal, tabel berkepala teal, kaki halaman kontak.

Pemakaian: python3 mmpp-empathy-leadership/_build/build_silabus.py
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
    "v3 Kurikulum dan Silabus 1 Hari - Communication and Teamwork Leadership "
    "Based on Empathy - PT MMPP.pptx"
)
FOOT_RIGHT = "PT MMPP | v3, 26 November 2026"

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


# ---------- visual SVG ----------
VIS = ROOT / "visual"


def vis(slide, name, x, y, w, h):
    """Sisipkan visual: PNG sebagai cadangan, SVG asli untuk PowerPoint 2016 ke atas."""
    from PIL import Image
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    from pptx.opc.package import Part
    from pptx.opc.packuri import PackURI
    from pptx.oxml.ns import qn
    from lxml import etree
    png = VIS / f"{name}.png"
    pw, ph = Image.open(png).size
    k = min(w / pw, h / ph)
    dw, dh = pw * k, ph * k
    pic = slide.shapes.add_picture(str(png), Inches(x + (w - dw) / 2), Inches(y), Inches(dw), Inches(dh))
    svg_path = VIS / f"{name}.svg"
    if svg_path.exists():
        part = Part(PackURI(f"/ppt/media/{name}.svg"), "image/svg+xml", slide.part.package,
                    svg_path.read_bytes())
        rid = slide.part.relate_to(part, RT.IMAGE)
        blip = pic._element.find(".//" + qn("a:blip"))
        ext_lst = etree.SubElement(blip, qn("a:extLst"))
        ext = etree.SubElement(ext_lst, qn("a:ext"), uri="{96DAC541-7B7A-43D3-8B79-37D633B846F1}")
        svgb = etree.SubElement(ext, "{http://schemas.microsoft.com/office/drawing/2016/SVG/main}svgBlip",
                                nsmap={"asvg": "http://schemas.microsoft.com/office/drawing/2016/SVG/main"})
        svgb.set(qn("r:embed"), rid)
    return pic


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
         "Tiga tujuan di brief PT MMPP, enam modul, dan yang bisa dikerjakan peserta setelah pelatihan")
vis(s, "01-kebutuhan-ke-hasil", 0.55, 1.4, 12.23, 5.5)

# ---------- 3. riset pendukung ----------
s = page("Mengapa", "Empati dalam Memimpin",
         "Empati adalah keterampilan kerja yang bisa dilatih dan diukur. Empat temuan riset yang menjadi dasar program")
vis(s, "02-riset", 0.55, 1.35, 12.23, 5.6)

# ---------- 4. alur program ----------
s = page("Alur Program", "dan Metode",
         "Enam tahap dari asesmen kebutuhan sampai laporan. Metode: ADDIE, backward design, andragogi, Bloom, Kirkpatrick")
vis(s, "03-alur-program", 0.55, 1.4, 12.23, 5.55)

# ---------- 5. ringkasan program ----------
s = page("Ringkasan", "Program",
         "Satu hari tatap muka, enam modul, 340 menit materi. Tiga perempat waktu materi dipakai untuk praktik")
vis(s, "04-ringkasan-modul", 0.55, 1.35, 12.23, 5.6)

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
vis(s, "06-alur-percakapan", 0.55, 1.35, 12.23, 5.6)

# ---------- 13. rundown ----------
s = page("Rundown", "Satu Hari",
         "08.30 - 16.30 waktu setempat. 340 menit materi, 50 menit pembukaan, tes, dan penutupan, 90 menit istirahat")
vis(s, "05-peta-hari", 0.55, 1.35, 12.23, 5.6)

# ---------- 14. persiapan ----------
s = page("Persiapan", "Sebelum dan Sesudah Pelatihan",
         "Sepuluh titik kerja dari rapat awal sampai laporan akhir, dengan penanggung jawabnya")
vis(s, "07-persiapan", 0.55, 1.35, 12.23, 5.6)

# ---------- 15. evaluasi ----------
s = page("Evaluasi", "Kirkpatrick Level 1 sampai 3",
         "Apa yang diukur, targetnya, dan kapan diukur")
vis(s, "08-evaluasi", 0.55, 1.35, 12.23, 5.6)

# ---------- 16. hasil yang dibawa pulang ----------
s = page("Hasil yang", "Dibawa Pulang", "Setiap output dihasilkan di topik yang tertulis di pojok kartu")
vis(s, "09-hasil", 0.55, 1.4, 12.23, 5.5)

# ---------- 17. standar minimal modul ----------
s = page("Standar Minimal", "Modul Sanggabiz",
         "Delapan bagian yang selalu ada di setiap modul peserta. Dua contoh di slide berikut memenuhi kedelapannya")
vis(s, "10-standar-modul", 0.55, 1.4, 12.23, 4.3)
box(s, 0.55, 5.85, 12.23, 0.9, TEAL_L, MSO_SHAPE.ROUNDED_RECTANGLE, align=PP_ALIGN.LEFT, parts=[
    [("Cara kami menyusun modul untuk PT MMPP: ", {"size": 11, "bold": True, "color": TEAL_D}),
     ("kerangka dan konsep disiapkan sebelum asesmen. Kasus, kalimat latihan, dan kartu peran diisi dari hasil "
      "asesmen awal, lalu disetujui HR PT MMPP pada H-7.", {"size": 11})]])


def contoh_slide(teal, sub, pages, captions, facts):
    s = page("Contoh Modul", teal, sub)
    n = len(pages)
    gw = 2.75
    gap = (9.3 - n * gw) / (n - 1)
    for k, (pg, cap) in enumerate(zip(pages, captions)):
        x = 0.55 + k * (gw + gap)
        box(s, x - 0.03, 1.42, gw + 0.06, 3.95, GREY)
        s.shapes.add_picture(str(VIS / pg), Inches(x), Inches(1.45), Inches(gw), Inches(3.89))
        text(s, x, 5.42, gw, 0.6, [[(cap, {"size": 9.5, "color": GREY_T})]], align=PP_ALIGN.CENTER)
    fx = 10.05
    for k, (big, small) in enumerate(facts):
        y = 1.45 + k * 1.02
        box(s, fx, y, 2.73, 0.9, ROW_ALT if k else TEAL_H, MSO_SHAPE.ROUNDED_RECTANGLE, align=PP_ALIGN.LEFT,
            parts=[[(big, {"size": 15, "bold": True, "color": WHITE if not k else TEAL_D})],
                   [(small, {"size": 9.5, "color": WHITE if not k else GREY_T})]])
    box(s, 0.55, 6.15, 12.23, 0.65, RGBColor(0xF6, 0xE5, 0xFB), MSO_SHAPE.ROUNDED_RECTANGLE,
        align=PP_ALIGN.LEFT, parts=[[("Status: CONTOH. ", {"size": 10, "bold": True}),
                                     ("Kasus dan kalimat latihan masih rekaan dan diganti dengan hasil asesmen awal. "
                                      "Dokumen lengkap (docx dan PDF) disertakan terpisah.", {"size": 10})]])


contoh_slide("M3 Umpan Balik yang Menjaga Martabat",
             "Modul peserta dan catatan fasilitator, A4, 8 halaman",
             ["hal-m3-01.png", "hal-m3-04.png", "hal-m3-05.png"],
             ["Sampul dengan status dokumen", "Konsep SBI dan niat dengan contoh lengkap",
              "Lembar kerja 3.1: menulis ulang kalimat teguran"],
             [("8 halaman", "Modul peserta dan catatan fasilitator"),
              ("2 lembar kerja", "Kalimat teguran dan naskah SBI"),
              ("1 lembar cek", "Dipakai pasangan saat praktik"),
              ("60 menit", "Alur menit di catatan fasilitator")])
contoh_slide("M4 Percakapan Sulit dengan Empati",
             "Modul peserta dan catatan fasilitator, A4, 10 halaman",
             ["hal-m4-05.png", "hal-m4-07.png", "hal-m4-08.png"],
             ["Contoh percakapan lengkap dengan skor per langkah", "Kartu peran pemimpin dan anggota tim",
              "Rubrik pengamat 0 sampai 8 untuk 3 putaran"],
             [("10 halaman", "Modul peserta dan catatan fasilitator"),
              ("1 lembar persiapan", "Untuk kasus milik peserta"),
              ("Rubrik 0 sampai 8", "Target minimal 6 di putaran ketiga"),
              ("90 menit", "Termasuk role play 3 putaran")])

# ---------- 20. rujukan ----------
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
