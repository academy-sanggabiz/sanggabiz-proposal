"""Proposal v3 dalam PPTX yang bisa diedit (PowerPoint dan Canva).

Slide 1 sampai 5 sama dengan v2 (fungsi dari build_pptx_v2.py). Slide 6 memakai gambar Kartu Saku Isyarat v4.
Pemakaian (dari folder _build, setelah build_v3.py dan render-nya dijalankan):
  python3 build_pptx_v3.py
"""
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from gaya import ROOT
from build_pptx import px, teks, kotak, kerangka, ikon_png, TEAL, CYAN, PUTIH, JUDUL_FONT, C
from build_pptx_v2 import hal1, hal_modul, hal_didapat
from silabus_v2 import MODUL
from build_v3 import GAMBAR, KARTU_V3

NAMA = "v3 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pptx"


def hal_kartu(prs):
    s = kerangka(prs, "CONTOH ASET PELATIHAN: KARTU SAKU ISYARAT PERBANKAN",
                 "Salah satu yang dibawa pulang peserta. Disiapkan Sanggabiz untuk meja teller dan CS PT BPR NBP 27.")
    for nama, x, rot, lab, lx in (("depan", 122, -2.2, "Sisi depan: 20 isyarat loket", 140), ("belakang", 700, 2.0, "Sisi belakang: kartu tunjuk", 960)):
        pic = s.shapes.add_picture(str(GAMBAR[nama]), px(x), px(190), px(458), px(458 * 559 / 794))
        pic.rotation = rot
        kotak(s, lx, 172, 190, 22, fill=CYAN, bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        teks(s, lx, 172, 190, 22, lab, size=8.5, bold=True, font=JUDUL_FONT, color=PUTIH, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    kol = [("Apa ini", KARTU_V3["apa"], 1.25), ("Isyarat setempat", KARTU_V3["foto"], 1.0), ("Dipakai di", KARTU_V3["dipakai"], 0.9)]
    tot = sum(k[2] for k in kol)
    x = 64
    for j, t, r in kol:
        w = (1152 - 32) * r / tot
        kotak(s, x, 532, w, 112, fill=C("F6FAFB"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        teks(s, x + 13, 540, w - 26, 100, [[(j, {"bold": True, "font": JUDUL_FONT, "color": TEAL, "size": 9.5})], t], size=9.1, spasi=1.25)
        x += w + 16


def main():
    ikon_png()
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(1280), px(720)
    hal1(prs)
    for a, b in ((0, 2), (2, 4), (4, 6)):
        hal_modul(prs, MODUL[a:b], a + 1, b)
    hal_didapat(prs)
    hal_kartu(prs)
    prs.core_properties.title = "Silabus dan Contoh Aset, IHT Layanan Inklusif PT BPR NBP 27"
    prs.core_properties.author = "Sanggabiz"
    out = ROOT / "proposal" / NAMA
    prs.save(out)
    print(out)


if __name__ == "__main__":
    main()
