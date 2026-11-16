"""Pembantu python-docx untuk aset MyFundAction: gaya teal, tabel garis hitam tipis, stabilo ISI TIM."""
import os
import re

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(HERE, "assets", "logo_white.png")
TEAL = RGBColor(0x15, 0x90, 0x8F)
TEAL_T = RGBColor(0x0E, 0x8A, 0x8A)
INK = RGBColor(0x1D, 0x1D, 0x1F)
MUTED = RGBColor(0x55, 0x55, 0x55)
FONT = "Arial"


def _shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def _borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement(f"w:{edge}")
        e.set(qn("w:val"), "single")
        e.set(qn("w:sz"), "4")
        e.set(qn("w:color"), "000000")
        b.append(e)
    tblPr.append(b)


def dokumen(judul, sub, landscape=False):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(10.5)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(4)
    st.paragraph_format.line_spacing = 1.15
    for lvl, size in ((1, 15), (2, 12.5), (3, 11)):
        h = doc.styles[f"Heading {lvl}"]
        h.font.name = FONT
        h.font.size = Pt(size)
        h.font.bold = True
        h.font.color.rgb = TEAL if lvl < 3 else INK
        h.element.rPr.rFonts.set(qn("w:asciiTheme"), FONT) if False else None
        rf = h.element.rPr.find(qn("w:rFonts"))
        if rf is None:
            rf = OxmlElement("w:rFonts")
            h.element.rPr.append(rf)
        for a in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
            rf.set(qn(a), FONT)
        for a in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
            if rf.get(qn(a)) is not None:
                del rf.attrib[qn(a)]
        h.paragraph_format.space_before = Pt(12 if lvl == 1 else 8)
        h.paragraph_format.space_after = Pt(4)
    sec = doc.sections[0]
    if landscape:
        sec.orientation = WD_ORIENT.LANDSCAPE
        sec.page_width, sec.page_height = sec.page_height, sec.page_width
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.6)
    # kepala: pita teal dengan logo
    hp = sec.header.paragraphs[0]
    hp.text = ""
    t = sec.header.add_table(1, 2, sec.page_width - sec.left_margin - sec.right_margin)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c0, c1 = t.rows[0].cells
    _shade(c0, "15908F")
    _shade(c1, "15908F")
    r = c0.paragraphs[0].add_run()
    r.add_picture(LOGO, height=Cm(0.55))
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rr = p1.add_run("MyFundAction  |  Pelatihan AI Agent  |  2026")
    rr.font.size = Pt(8.5)
    rr.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    rr.font.name = FONT
    fp = sec.footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = fp.add_run("WhatsApp 0877-7413-4288   |   www.sanggabiz.com   |   partnership@sanggabiz.com")
    fr.font.size = Pt(8)
    fr.font.color.rgb = MUTED
    # judul
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(judul)
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = TEAL
    if sub:
        p = doc.add_paragraph()
        r = p.add_run(sub)
        r.font.size = Pt(10.5)
        r.font.color.rgb = MUTED
    return doc


ISI = re.compile(r"(\[ISI TIM:[^\]]*\]|`[^`]+`|\*\*[^*]+\*\*)")


def para(doc, teks, size=None, bold=False, italic=False, color=None, align=None, style=None, after=None):
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    tambah(p, teks, size=size, bold=bold, italic=italic, color=color)
    if align == "c":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def tambah(p, teks, size=None, bold=False, italic=False, color=None):
    """Teks dengan **tebal**, `kode`, dan [ISI TIM: ...] berstabilo kuning."""
    for bag in ISI.split(teks):
        if not bag:
            continue
        r = p.add_run()
        if bag.startswith("[ISI TIM:"):
            r.text = bag
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW
            r.bold = True
        elif bag.startswith("`"):
            r.text = bag[1:-1]
            r.font.name = "Courier New"
            r._element.rPr.rFonts.set(qn("w:hAnsi"), "Courier New")
            r.font.color.rgb = RGBColor(0x0E, 0x5E, 0x5D)
        elif bag.startswith("**"):
            r.text = bag[2:-2]
            r.bold = True
        else:
            r.text = bag
            r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = color
    return p


_HITUNG = [0]


_PUTUS = [False]


def h(doc, teks, lvl=1):
    _HITUNG[0] = 0
    p = doc.add_heading(teks, level=lvl)
    if _PUTUS[0]:
        p.paragraph_format.page_break_before = True
        _PUTUS[0] = False
    return p


def butir(doc, items, nomor=False):
    """Daftar. Nomor berlanjut sampai judul berikutnya."""
    for t in items:
        if nomor:
            _HITUNG[0] += 1
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Cm(0.75)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            tambah(p, f"{_HITUNG[0]}.\t" + t)
            p.paragraph_format.tab_stops.add_tab_stop(Cm(0.75))
        else:
            p = doc.add_paragraph(style="List Bullet")
            tambah(p, t)
        p.paragraph_format.space_after = Pt(2)


def kode(doc, teks):
    """Blok perintah atau prompt, huruf monospace, latar abu."""
    t = doc.add_table(rows=1, cols=1)
    _borders(t)
    c = t.rows[0].cells[0]
    _shade(c, "F2F8F9")
    c.paragraphs[0].text = ""
    for i, baris in enumerate(teks.split("\n")):
        p = c.paragraphs[0] if i == 0 else c.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(baris if baris else " ")
        r.font.name = "Courier New"
        r._element.rPr.rFonts.set(qn("w:hAnsi"), "Courier New")
        r.font.size = Pt(9)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def tabel(doc, kolom, baris, lebar=None, size=9.5, kepala_teal=False, tinggi=None):
    t = doc.add_table(rows=1, cols=len(kolom))
    _borders(t)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, k in enumerate(kolom):
        c = t.rows[0].cells[i]
        _shade(c, "15908F" if kepala_teal else "F2F2F2")
        p = c.paragraphs[0]
        r = p.add_run(k)
        r.bold = True
        r.font.size = Pt(size)
        if kepala_teal:
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    for row in baris:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            c = cells[i]
            c.paragraphs[0].text = ""
            lines = v if isinstance(v, list) else [v]
            for j, ln in enumerate(lines):
                p = c.paragraphs[0] if j == 0 else c.add_paragraph()
                p.paragraph_format.space_after = Pt(1)
                tambah(p, str(ln), size=size, bold=(i == 0 and not isinstance(v, list) and len(kolom) > 2 and len(str(ln)) < 40))
    if tinggi:
        for row in t.rows[1:]:
            row.height = Cm(tinggi)
    if lebar:
        t.autofit = False
        grid = t._tbl.tblGrid
        for i, gc in enumerate(grid.findall(qn("w:gridCol"))):
            gc.set(qn("w:w"), str(int(lebar[i] * 567)))
        for row in t.rows:
            for i, w in enumerate(lebar):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def kotak_isian(doc, label, tinggi_baris=3):
    t = doc.add_table(rows=1, cols=1)
    _borders(t)
    c = t.rows[0].cells[0]
    p = c.paragraphs[0]
    r = p.add_run(label)
    r.font.size = Pt(9)
    r.font.color.rgb = MUTED
    for _ in range(tinggi_baris):
        c.add_paragraph().paragraph_format.space_after = Pt(14)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def pindah_halaman(doc):
    """Judul berikutnya mulai di halaman baru."""
    _PUTUS[0] = True
