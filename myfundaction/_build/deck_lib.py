"""Pembantu python-pptx bersama untuk deck MyFundAction (gaya teal format standar)."""
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
OUT = os.path.join(HERE, "..", "proposal", "v1 Kurikulum dan Silabus - Pelatihan AI Agent MyFundAction.pptx")
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


def new_prs():
    p = Presentation()
    p.slide_width = Inches(SW)
    p.slide_height = Inches(SH)
    return p


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


def kerangka(prs, judul_hitam, judul_teal=None, sub=None, label=None):
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
           (f"          {label or d.PROGRAM['klien'] + ' | ' + d.PROGRAM['versi']}", False, "999999")]], size=9)
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
