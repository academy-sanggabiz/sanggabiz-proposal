"""Proposal v4 dalam PPTX yang bisa diedit: slide 1 sampai 6 sama dengan v3, slide 7 rincian anggaran (tabel asli).

Pemakaian (dari folder _build, setelah build_v3.py pernah dijalankan untuk gambar kartu):
  python3 build_pptx_v4.py
"""
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR
from gaya import ROOT
from build_pptx import px, teks, kotak, kerangka, tabel, ikon_png, TEAL, TEAL_MUDA, NAVY, PUTIH, JUDUL_FONT, UNGU, UNGU_MUDA, C
from build_pptx_v2 import hal1, hal_modul, hal_didapat
from build_pptx_v3 import hal_kartu
from silabus_v2 import MODUL
from anggaran import BARIS, TERMASUK, DARI_BPR, CATATAN_KLIEN, hitung, jumlah, rp, vol
from build_v4 import NAMA, JUDUL_ANGGARAN, SUB_ANGGARAN


def hal_anggaran(prs):
    s = kerangka(prs, JUDUL_ANGGARAN, SUB_ANGGARAN)
    d, fee, total = hitung()
    baris, tahap, no = [], None, 0
    for b in BARIS:
        if b[0] != tahap:
            tahap = b[0]
            sel = {"fill": TEAL_MUDA, "isi": [[(tahap, {"bold": True, "font": JUDUL_FONT, "color": NAVY})]]}
            kosong = {"fill": TEAL_MUDA, "isi": " "}
            baris.append([kosong, sel, kosong, kosong, kosong])
        no += 1
        baris.append([str(no), b[1], f"{vol(b[2])} {b[3]}", rp(b[4]), rp(jumlah(b))])
    tebal = lambda t: [[(t, {"bold": True})]]
    baris.append([" ", tebal("Jumlah biaya langsung"), " ", " ", tebal(rp(d))])
    baris.append([" ", tebal("Fee 10 persen"), " ", " ", tebal(rp(fee))])
    tot = lambda t: {"fill": NAVY, "isi": [[(t, {"bold": True, "color": PUTIH, "font": JUDUL_FONT})]]}
    baris.append([tot(" "), tot("Total, sudah termasuk pajak"), tot(" "), tot(" "), tot(rp(total))])
    t = tabel(s, 64, 170, 800, ["No", "Uraian", "Volume", "Harga satuan (Rp)", "Jumlah (Rp)"], baris, [5, 52, 15, 14, 14],
              size=7.4, tinggi_kepala=20, tinggi_baris=19)
    from pptx.enum.text import PP_ALIGN
    for r in range(1, len(baris) + 1):
        for c in (0, 2, 3, 4):
            for p in t.cell(r, c).text_frame.paragraphs:
                p.alignment = PP_ALIGN.RIGHT
        for c in range(5):
            cell = t.cell(r, c)
            cell.margin_top = cell.margin_bottom = px(2)
    # panel kanan
    x, w = 888, 328
    kotak(s, x, 170, w, 100, fill=C("145B78"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
    teks(s, x + 16, 178, w - 32, 86, [[("Total paket", {"size": 8.5})], [(f"Rp {rp(total)}", {"bold": True, "font": JUDUL_FONT, "size": 17})],
                                      [("Sudah termasuk pajak, di dalam pagu TOR Rp 10.000.000 sampai Rp 11.000.000.", {"size": 8})]],
         size=8.5, color=PUTIH, anchor=MSO_ANCHOR.MIDDLE, spasi=1.15)
    kotak(s, x, 282, w, 156, fill=C("F6FAFB"), line=C("DCE8EC"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
    teks(s, x + 14, 290, w - 28, 142, [[("Sudah termasuk", {"bold": True, "font": JUDUL_FONT, "size": 9, "color": NAVY})]]
         + [f"• {t}" for t in TERMASUK], size=8, spasi=1.2)
    kotak(s, x, 450, w, 82, fill=UNGU_MUDA, line=UNGU, bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
    teks(s, x + 14, 458, w - 28, 68, [[("Disediakan PT BPR NBP 27", {"bold": True, "font": JUDUL_FONT, "size": 9, "color": NAVY})]]
         + [f"• {t}" for t in DARI_BPR], size=8, spasi=1.2)
    kotak(s, x, 544, w, 92, fill=PUTIH, line=C("9FB3BF"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
    teks(s, x + 14, 552, w - 28, 78, CATATAN_KLIEN, size=8, spasi=1.2, anchor=MSO_ANCHOR.MIDDLE)


def main():
    ikon_png()
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(1280), px(720)
    hal1(prs)
    for a, b in ((0, 2), (2, 4), (4, 6)):
        hal_modul(prs, MODUL[a:b], a + 1, b)
    hal_didapat(prs)
    hal_kartu(prs)
    hal_anggaran(prs)
    prs.core_properties.title = "Proposal Silabus, Contoh Aset, dan Anggaran, IHT Layanan Inklusif PT BPR NBP 27"
    prs.core_properties.author = "Sanggabiz"
    out = ROOT / "proposal" / f"{NAMA}.pptx"
    prs.save(out)
    print(out)


if __name__ == "__main__":
    main()
