"""Membuat versi PPTX yang bisa diedit (untuk PowerPoint dan unggah ke Canva).

Semua teks, tabel, dan bentuk dibuat sebagai objek asli, bukan gambar halaman. Gambar hanya untuk logo,
ikon kontak, dan tangkapan aset. Font: Montserrat (judul) dan Inter (isi), keduanya ada di Canva.
Isi diambil dari silabus.py dan build_proposal.py supaya sama dengan versi PDF.

Pemakaian (dari folder _build, setelah build_proposal.py dijalankan):
  python3 build_pptx.py
"""
import json
import subprocess
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Pt
from PIL import Image
from gaya import BUILD, ROOT
from silabus import KIT, RINGKAS, MODUL, HASIL
from build_proposal import DESK, SINGKAT, SLUG, IKON, HTML

NAMA = "v1 Silabus dan Aset Pelatihan - IHT Layanan Inklusif PT BPR NBP 27.pptx"
LOGO = BUILD / "assets" / "logo_warna.png"
SLIDE = ROOT / "proposal" / "aset-slide"
IKON_DIR = BUILD / "assets" / "ikon"

C = lambda h: RGBColor.from_string(h.lstrip("#"))
TEAL, TEAL_MUDA, CYAN, NAVY = C("15908F"), C("D7ECEC"), C("34BDCF"), C("13314F")
UNGU, UNGU_MUDA, UNGU_GARIS = C("E2A9F1"), C("FBF3FE"), C("8B5CF6")
HITAM, ABU_TEKS, PUTIH, BARIS_GENAP, GARIS = C("111111"), C("333333"), C("FFFFFF"), C("F2F8F9"), C("C9D6DA")
JUDUL_FONT, ISI_FONT = "Montserrat", "Inter"


def px(v):
    return Emu(int(v * 9525))


def ikon_png():
    """Ikon kontak putih transparan dari SVG yang sama dengan versi PDF."""
    IKON_DIR.mkdir(parents=True, exist_ok=True)
    jobs = []
    for k, svg in IKON.items():
        big = svg.replace('width="15" height="15"', 'width="96" height="96"')
        h = HTML / f"ikon-{k}.html"
        h.write_text(f"<html><body style='margin:0;background:transparent'>{big}</body></html>")
        jobs.append({"html": str(h), "png": str(IKON_DIR / f"{k}.png"), "width": 96, "height": 96, "scale": 1, "transparent": True})
    j = BUILD / "jobs_ikon.json"
    j.write_text(json.dumps(jobs))
    subprocess.run(["node", str(BUILD / "render.js"), str(j)], check=True, capture_output=True)


def teks(slide, x, y, w, h, isi, size=10, bold=False, color=HITAM, font=ISI_FONT, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, italic=False, spasi=1.1):
    """isi: str, atau daftar paragraf. Paragraf: str atau daftar run (teks, {opsi})."""
    tb = slide.shapes.add_textbox(px(x), px(y), px(w), px(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    paras = [isi] if isinstance(isi, str) else isi
    for i, p in enumerate(paras):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align
        para.line_spacing = spasi
        runs = p if isinstance(p, list) else [(p, {})]
        for t, o in runs:
            r = para.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", italic)
            f.color.rgb = o.get("color", color)
    return tb


def kotak(slide, x, y, w, h, fill=None, line=None, bentuk=MSO_SHAPE.RECTANGLE, lebar_garis=1):
    s = slide.shapes.add_shape(bentuk, px(x), px(y), px(w), px(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lebar_garis)
    s.shadow.inherit = False
    if bentuk == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = 0.08
    return s


def kerangka(prs, judul, sub):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(str(LOGO), px(64), px(27), height=px(30))
    teks(s, 1100, 31, 116, 24, "2026", size=13, bold=True, font=JUDUL_FONT, align=PP_ALIGN.RIGHT)
    kotak(s, 64, 83, 1152, 2, fill=UNGU_GARIS)
    teks(s, 64, 104, 1152, 40, judul, size=22.5, bold=True, font=JUDUL_FONT, align=PP_ALIGN.CENTER)
    teks(s, 64, 142, 1152, 20, sub, size=10, color=ABU_TEKS, align=PP_ALIGN.CENTER)
    kotak(s, 64, 657, 1152, 1.5, fill=C("222222"))
    kontak = [("wa", "0877-7413-4288", 64, PP_ALIGN.LEFT), ("web", "www.sanggabiz.com", 0, PP_ALIGN.CENTER),
              ("mail", "partnership@sanggabiz.com", 0, PP_ALIGN.RIGHT)]
    pos = [(64, 210), (535, 210), (930, 286)]
    for (k, t, _, _), (x, w) in zip(kontak, pos):
        kotak(s, x, 676, 26, 26, fill=CYAN, bentuk=MSO_SHAPE.OVAL)
        s.shapes.add_picture(str(IKON_DIR / f"{k}.png"), px(x + 5), px(681), px(16), px(16))
        teks(s, x + 35, 679, w, 20, t, size=10.5, bold=True, font=JUDUL_FONT, anchor=MSO_ANCHOR.MIDDLE)
    return s


def tabel(slide, x, y, w, kepala, baris, lebar, size=8.3, tinggi_kepala=24, tinggi_baris=20, kolom_tebal=()):
    t = slide.shapes.add_table(len(baris) + 1, len(kepala), px(x), px(y), px(w),
                               px(tinggi_kepala + tinggi_baris * len(baris))).table
    tot = sum(lebar)
    for i, l in enumerate(lebar):
        t.columns[i].width = px(w * l / tot)
    t.rows[0].height = px(tinggi_kepala)
    for r in range(1, len(baris) + 1):
        t.rows[r].height = px(tinggi_baris)
    tblPr = t._tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")

    def isi_sel(cell, nilai, fill, warna, tebal):
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
        for m, v in (("margin_left", 6), ("margin_right", 6), ("margin_top", 4), ("margin_bottom", 4)):
            setattr(cell, m, px(v))
        tf = cell.text_frame
        tf.word_wrap = True
        paras = nilai if isinstance(nilai, list) else [nilai]
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            runs = p if isinstance(p, list) else [(p, {})]
            for tx, o in runs:
                rr = para.add_run()
                rr.text = tx
                rr.font.name = o.get("font", ISI_FONT)
                rr.font.size = Pt(o.get("size", size))
                rr.font.bold = o.get("bold", tebal)
                rr.font.italic = o.get("italic", False)
                rr.font.color.rgb = o.get("color", warna)

    for c, k in enumerate(kepala):
        isi_sel(t.cell(0, c), k, TEAL, PUTIH, True)
    for r, b in enumerate(baris, 1):
        for c, v in enumerate(b):
            fill = BARIS_GENAP if r % 2 == 0 else PUTIH
            if isinstance(v, dict):
                fill = v.get("fill", fill)
                v = v["isi"]
            isi_sel(t.cell(r, c), v, fill, HITAM, c in kolom_tebal)
    return t


# ---------- halaman ----------
def hal_ringkas(prs):
    total = sum(r[2] for r in RINGKAS[2:])
    s = kerangka(prs, "SILABUS PELATIHAN: RINGKASAN SATU HARI",
                 "In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27, Bandung. 10 peserta, luring, 08.30 - 16.30 WIB.")
    pita = [
        [[("30", {"size": 17, "bold": True, "font": JUDUL_FONT, "color": TEAL}), (" menit teori dari ", {}), (f"{total} menit", {"bold": True}),
          (f" pembelajaran. Sisanya, {total-30} menit atau {round((total-30)*100/total)} persen, adalah praktik dan simulasi sesuai TOR.", {})]],
        [[("Metode. ", {"bold": True, "font": JUDUL_FONT, "color": NAVY}), ("Andragogi: peserta belajar dari kasus loket sendiri. Bloom revisi untuk tujuan tiap modul (C1 sampai C5). Kirkpatrick level 1 dan 2 untuk evaluasi, level 3 lewat rubrik di kantor.", {})]],
        [[("Tim di kelas. ", {"bold": True, "font": JUDUL_FONT, "color": NAVY}), ("1 trainer utama, 1 co-trainer Tuli untuk isyarat BISINDO, 1 peraga netra untuk pemanduan dan pembacaan slip.", {})]],
    ]
    w = (1152 - 20) / 3
    for i, p in enumerate(pita):
        x = 64 + i * (w + 10)
        kotak(s, x, 174, w, 70, fill=C("F4FAFB"))
        kotak(s, x, 174, 4, 70, fill=CYAN)
        teks(s, x + 14, 180, w - 24, 60, p, size=9, anchor=MSO_ANCHOR.MIDDLE, spasi=1.15)
    baris = [[j, s_, str(m), mt, h] for j, s_, m, mt, h in RINGKAS]
    baris.append(["", "Rehat kopi 10.15 - 10.30 dan 15.00 - 15.15, ishoma 12.00 - 13.00 (disediakan BPR)", "", "", ""])
    tabel(s, 64, 258, 1152, ["Waktu (WIB)", "Sesi", "Menit", "Metode", "Hasil"], baris, [11, 36, 6, 18, 29],
          size=8.6, tinggi_baris=22, kolom_tebal=(1,))


def hal_modul(prs, ms, ket):
    s = kerangka(prs, f"SILABUS PELATIHAN: {ket.upper()}",
                 "Tiap modul memuat tujuan berkode Bloom, outline materi, aktivitas per menit, alat, indikator, dan output. Nomor aset merujuk ke isi kit.")
    baris = []
    for m in ms:
        kiri = {"fill": TEAL_MUDA, "isi": [
            [(m["no"], {"bold": True, "font": JUDUL_FONT, "color": TEAL, "size": 9.5})],
            [(m["judul"], {"bold": True, "font": JUDUL_FONT, "color": NAVY, "size": 9})],
            [(m["jam"], {"size": 7.6, "color": C("335555")})],
            [(m["tujuan"], {"italic": True, "size": 7.9})]]}
        materi = [f"{i}. {x}" for i, x in enumerate(m["materi"], 1)]
        baris.append([kiri, materi, m["aktivitas"], m["alat"], m["indikator"], m["output"]])
    tabel(s, 64, 172, 1152, ["Modul, waktu, dan tujuan (Bloom)", "Outline materi", "Aktivitas di ruang pelatihan",
                             "Alat dan media", "Indikator capaian", "Output konkret"], baris, [17, 20, 30, 11, 11, 11],
          size=8, tinggi_baris=200)


def hal_hasil(prs):
    s = kerangka(prs, "HASIL YANG DIBAWA PULANG DAN EVALUASI",
                 "Semua output tiap modul dikumpulkan di sini, lalu diukur dengan empat level Kirkpatrick.")
    tabel(s, 64, 172, 628, ["Hasil", "Dari", "Dipakai untuk"], [list(h) for h in HASIL], [46, 20, 34], size=8.3, tinggi_baris=27)
    kp = [["1. Reaksi", "Survei 4 butir di lembar post-test", "Rata-rata minimal 4 dari 5"],
          ["2. Pembelajaran", "Pre-test dan post-test 15 soal, lembar praktik, rubrik Modul 6", "Post-test minimal 80, rubrik minimal 2,5 dari 3"],
          ["3. Perilaku", "Kasie memakai rubrik untuk tiga layanan pertama di kantor", "Diusulkan, dicatat BPR"],
          ["4. Dampak", "Log keluhan nasabah disabilitas dan hasil pemeriksaan", "Dipantau BPR, di luar paket"]]
    tabel(s, 716, 172, 500, ["Level", "Diukur dengan", "Target"], kp, [24, 42, 34], size=8.3, tinggi_baris=34, kolom_tebal=(0,))
    teks(s, 716, 352, 500, 90, "Laporan evaluasi dikirim paling lambat 7 hari kerja setelah pelatihan, berisi rekap nilai, dokumentasi foto dan video, "
         "dan rekomendasi perbaikan fasilitas layanan sesuai TOR bagian VI. Target angka adalah usulan kami dan dapat disesuaikan dengan BPR.",
         size=8.8, spasi=1.2)


def gambar(slide, path, x, y, w, h, potong_atas=False):
    """Menempatkan gambar di dalam kotak w x h. potong_atas: isi penuh lebar, sisa bawah dipotong."""
    im = Image.open(path)
    iw, ih = im.size
    if potong_atas:
        pic = slide.shapes.add_picture(str(path), px(x), px(y), px(w), px(w * ih / iw))
        tinggi = w * ih / iw
        if tinggi > h:
            pic.crop_bottom = 1 - h / tinggi
            pic.height = px(h)
        return pic
    sk = min(w / iw, h / ih)
    pw, ph = iw * sk, ih * sk
    return slide.shapes.add_picture(str(path), px(x + (w - pw) / 2), px(y + (h - ph) / 2), px(pw), px(ph))


def hal_kit(prs):
    s = kerangka(prs, "ASET PELATIHAN: ISI KIT",
                 "Disiapkan Sanggabiz untuk 10 peserta dan tim. Data nasabah di kit adalah rekaan dan dibuat khusus untuk layanan BPR.")
    cw, gap = (1152 - 5 * 10) / 6, 10
    for i, (no, nama, siapa, pakai) in enumerate(KIT):
        x = 64 + (i % 6) * (cw + gap)
        y = 176 + (i // 6) * 228
        kotak(s, x, y, cw, 216, fill=PUTIH, line=C("D6E4E7"), bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
        kotak(s, x + 1, y + 1, cw - 2, 96, fill=TEAL_MUDA)
        gambar(s, SLIDE / f"{no}-{SLUG[no]}.png", x + 6, y + 6, cw - 12, 91, potong_atas=True)
        teks(s, x + 8, y + 104, cw - 16, 106, [[(f"{int(no)}. {nama}", {"bold": True, "font": JUDUL_FONT, "color": TEAL, "size": 8.3})],
                                              f"{siapa}. {pakai}."], size=8, spasi=1.15)


def kol_aset(s, no, x):
    nama = SINGKAT.get(no, next(k[1] for k in KIT if k[0] == no))
    berkas = next((ROOT / "kit").glob(f"{no} *")).name
    apa, dipakai, bawa = DESK[no]
    w = 556
    kotak(s, x, 174, 34, 34, fill=CYAN, bentuk=MSO_SHAPE.OVAL)
    teks(s, x, 174, 34, 34, str(int(no)), size=11, bold=True, font=JUDUL_FONT, color=PUTIH, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    teks(s, x + 46, 174, w - 46, 34, nama, size=15, bold=True, font=JUDUL_FONT, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    kotak(s, x, 218, w, 262, fill=TEAL_MUDA)
    gambar(s, SLIDE / f"{no}-{SLUG[no]}.png", x + 9, 227, w - 18, 244)
    kotak(s, x, 489, w, 44, fill=UNGU_MUDA, line=UNGU, bentuk=MSO_SHAPE.ROUNDED_RECTANGLE, lebar_garis=0.75)
    teks(s, x + 10, 494, w - 20, 36, [[("Berkas di kit: ", {"bold": True}), (f"kit/{berkas}", {})],
                                     [("Gambar: ", {"bold": True}), (f"proposal/aset-slide/{no}-{SLUG[no]}.png", {})]],
         size=9.3, anchor=MSO_ANCHOR.MIDDLE, spasi=1.15)
    lab = {"bold": True, "color": TEAL}
    teks(s, x, 542, w, 108, [[("Apa ini. ", lab), (apa, {})], [("Dipakai di. ", lab), (dipakai, {})],
                             [("Dibawa pulang. ", lab), (bawa, {})]], size=9.6, spasi=1.15)


def hal_aset(prs, a, b, judul):
    s = kerangka(prs, f"ASET PELATIHAN: {judul}",
                 "Disiapkan Sanggabiz dan dibagikan ke peserta. Semua data nasabah rekaan, dibuat khusus untuk layanan BPR.")
    kol_aset(s, a, 70)
    kol_aset(s, b, 654)


def main():
    ikon_png()
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(1280), px(720)
    hal_ringkas(prs)
    for a, b, ket in ((0, 2, "Modul 1 dan 2"), (2, 4, "Modul 3 dan 4"), (4, 6, "Modul 5 dan 6")):
        hal_modul(prs, MODUL[a:b], ket)
    hal_hasil(prs)
    hal_kit(prs)
    for a, b, j in [("01", "02", "RINGKASAN REGULASI DAN KARTU ISYARAT"), ("03", "04", "LEMBAR PRAKTIK DAN SKENARIO"),
                    ("05", "06", "RUBRIK DAN TES"), ("07", "08", "FORMULIR SLIP DAN AUDIT AKSESIBILITAS"),
                    ("09", "10", "SERTIFIKAT DAN LAPORAN"), ("11", "00", "REKAP NILAI DAN PANDUAN FASILITATOR")]:
        hal_aset(prs, a, b, j)
    prs.core_properties.title = "Silabus dan Aset Pelatihan, IHT Layanan Inklusif PT BPR NBP 27"
    prs.core_properties.author = "Sanggabiz"
    out = ROOT / "proposal" / NAMA
    prs.save(out)
    print(out, len(prs.slides._sldIdLst), "slide")


if __name__ == "__main__":
    main()
