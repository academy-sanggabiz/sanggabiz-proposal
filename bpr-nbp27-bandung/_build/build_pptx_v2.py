"""Proposal v2 dalam PPTX yang bisa diedit (PowerPoint dan Canva). Isi sama dengan build_v2.py.

Pemakaian (dari folder _build, setelah build_kartu.py dan build_pptx.py pernah dijalankan untuk ikon):
  python3 build_pptx_v2.py
"""
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from gaya import ROOT
from build_pptx import (px, teks, kotak, kerangka, tabel, ikon_png, TEAL, TEAL_MUDA, NAVY, PUTIH, CYAN, UNGU, UNGU_MUDA,
                        JUDUL_FONT, C)
from silabus_v2 import PEMBUKA, SOROTAN, RUNDOWN, MODUL, DIDAPAT, KARTU

SLIDE = ROOT / "proposal" / "aset-slide"
NAMA = "v2 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pptx"
B = {"bold": True}


def hal1(prs):
    s = kerangka(prs, "SILABUS PELATIHAN: SATU HARI PENUH PRAKTIK",
                 "In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27, Bandung. 10 peserta, 08.30 - 16.30 WIB.")
    teks(s, 190, 164, 900, 36, PEMBUKA, size=9.8, align=PP_ALIGN.CENTER, spasi=1.2)
    w = (1152 - 28) / 3
    for i, (a, b, c) in enumerate(SOROTAN):
        x = 64 + i * (w + 14)
        kotak(s, x, 212, w, 62, fill=C("ECF6F7"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        teks(s, x + 14, 220, 130, 46, [[(a, {"bold": True, "font": JUDUL_FONT, "color": TEAL, "size": 16})],
                                       [(b.upper(), {"bold": True, "font": JUDUL_FONT, "color": NAVY, "size": 7.5})]], anchor=MSO_ANCHOR.MIDDLE)
        teks(s, x + 150, 218, w - 162, 50, c, size=8.6, anchor=MSO_ANCHOR.MIDDLE, spasi=1.15)
    baris = []
    for j, k, t in RUNDOWN:
        if t:
            baris.append([j, k, t])
        else:
            f = C("FAFAFA")
            baris.append([{"fill": f, "isi": [[(j, {"italic": True, "color": C("777777")})]]},
                          {"fill": f, "isi": [[(k, {"italic": True, "color": C("777777")})]]}, {"fill": f, "isi": ""}])
    tabel(s, 64, 288, 1152, ["Waktu (WIB)", "Kegiatan", "Yang terjadi"], baris, [12, 38, 50], size=8.2, tinggi_baris=22, kolom_tebal=(1,))


def hal_modul(prs, ms, a, b):
    s = kerangka(prs, f"SILABUS PELATIHAN: MODUL {a} DAN {b}", "Apa yang dipelajari, apa yang dilakukan peserta, dan apa hasilnya.")
    baris = []
    for m in ms:
        kiri = {"fill": TEAL_MUDA, "isi": [[(m["no"], {"bold": True, "font": JUDUL_FONT, "color": TEAL, "size": 9.2})],
                                           [(m["judul"], {"bold": True, "font": JUDUL_FONT, "color": NAVY, "size": 10})],
                                           [(f'{m["jam"]} WIB', {"size": 8.2, "color": C("335555")})]]}
        lab = {"bold": True, "color": TEAL}
        baris.append([kiri, [f"• {x}" for x in m["dipelajari"]], [f"• {x}" for x in m["kegiatan"]],
                      [[("Alat: ", lab), (m["alat"], {})], [("Media: ", lab), (m["media"], {})]], m["hasil"]])
    tabel(s, 64, 172, 1152, ["Modul", "Yang dipelajari", "Kegiatan peserta", "Alat dan media", "Hasil"], baris,
          [16, 22, 32, 15, 15], size=9.1, tinggi_baris=200)


def hal_didapat(prs):
    s = kerangka(prs, "YANG DIDAPAT PT BPR NBP 27",
                 "Hasil yang bisa langsung dipakai di loket, dan bukti yang bisa ditunjukkan saat pemeriksaan OJK.")
    w = (1152 - 36) / 3
    for i, (j, xs) in enumerate(DIDAPAT):
        x = 64 + i * (w + 18)
        kotak(s, x, 176, w, 300, fill=PUTIH, line=C("D6E4E7"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        kotak(s, x, 176, w, 44, fill=C("145B78"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        kotak(s, x, 200, w, 20, fill=C("145B78"))
        teks(s, x + 16, 176, w - 32, 44, j, size=11.5, bold=True, font=JUDUL_FONT, color=PUTIH, anchor=MSO_ANCHOR.MIDDLE)
        teks(s, x + 16, 236, w - 32, 236, [[("\u2022  ", {"bold": True, "color": TEAL}), (t, {})] for t in xs], size=10.5, spasi=1.6)
    kotak(s, 64, 494, 1152, 70, fill=UNGU_MUDA, line=UNGU, bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
    teks(s, 84, 500, 1112, 58, [[("Dipandu langsung oleh penyandang disabilitas. ", B),
        ("Trainer utama berpengalaman di layanan perbankan, didampingi co-trainer Tuli untuk bahasa isyarat dan peraga netra untuk pemanduan "
         "dan pembacaan slip. Peserta belajar dari orang yang setiap hari menjadi nasabah.", {})]], size=10.5, anchor=MSO_ANCHOR.MIDDLE, spasi=1.2)


def hal_kartu(prs):
    s = kerangka(prs, "CONTOH ASET PELATIHAN: KARTU SAKU ISYARAT PERBANKAN",
                 "Salah satu yang dibawa pulang peserta. Disiapkan Sanggabiz untuk meja teller dan CS PT BPR NBP 27.")
    for nama, x, rot, lab, lx in (("depan", 122, -2.2, "Sisi depan: 20 isyarat loket", 140), ("belakang", 700, 2.0, "Sisi belakang: kartu tunjuk", 960)):
        pic = s.shapes.add_picture(str(SLIDE / f"v2-kartu-isyarat-{nama}.png"), px(x), px(190), px(458), px(458 * 559 / 794))
        pic.rotation = rot
        kotak(s, lx, 172, 190, 22, fill=CYAN, bentuk=MSO_SHAPE.ROUNDED_RECTANGLE)
        teks(s, lx, 172, 190, 22, lab, size=8.5, bold=True, font=JUDUL_FONT, color=PUTIH, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    kol = [("Apa ini", KARTU["apa"], 1.25), ("Isyarat setempat", KARTU["foto"], 1.0), ("Dipakai di", KARTU["dipakai"], 0.9)]
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
