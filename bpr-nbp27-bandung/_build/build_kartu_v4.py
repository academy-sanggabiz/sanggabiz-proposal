"""Kartu Saku Isyarat v4: desain kartu v2 dengan 20 gambar contoh dari pengguna. PDF dan PPTX yang bisa diedit.

Gambar dari foto-isyarat-contoh/ (dipotong oleh potong_foto_contoh.py). Gambar ini contoh dan belum diperiksa
pengguna Tuli, jadi setiap foto diberi label "contoh" dan kaki kartu menyebutnya.
PPTX disusun dari ukuran elemen di HTML (ukur.js), jadi tata letaknya sama dengan PDF. Semua teks dan kotak bisa
diedit, foto bisa diganti (klik kanan, Ganti Gambar).

Pemakaian (dari folder _build):
  python3 -I potong_foto_contoh.py
  python3 build_kartu_v4.py
"""
import json
import subprocess
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Pt
from gaya import BUILD, ROOT
from build_kartu import CSS, KAT, KATA, NAVY, TEAL, sisi_depan, sisi_belakang, ikon, foto_untuk
from ilustrasi import ilus
from build_pptx import px

HTML = BUILD / "html"
TMP = BUILD / "tmp"
IKON = BUILD / "assets" / "ikon-kartu"
FOTO_CONTOH = BUILD / "foto-isyarat-contoh"
LOGO_PUTIH = BUILD / "assets" / "logo_putih.png"
NAMA = "02 Kartu Saku Isyarat Perbankan v4 - foto contoh"
KETERANGAN = ("Gambar isyarat ini contoh dan belum diperiksa pengguna Tuli. "
              "Cocokkan dengan pengajar BISINDO sebelum dipakai di loket.")
TAG = "contoh"
LAYANAN = [("setor", "Setor"), ("tarik", "Tarik"), ("saldo", "Cek saldo"), ("rekening", "Buka rekening"), ("buku", "Cetak buku"), ("kartu", "Kartu ATM")]
JAWABAN = [("ya", "Ya"), ("tidak", "Tidak"), ("ulang", "Ulangi"), ("tunggu", "Tunggu"), ("selesai", "Selesai")]
TIPS = [
    ("lambai", "Tarik perhatian", "Lambaikan tangan pelan di depan nasabah atau ketuk meja."),
    ("matahari", "Wajah terlihat jelas", "Berhadapan, wajah terkena cahaya, mulut tidak tertutup."),
    ("pena", "Tulis angkanya", "Nominal dan nomor rekening selalu ditulis atau ditunjuk."),
    ("mata", "Tatap nasabah", "Bila ada juru bahasa isyarat, tetap bicara kepada nasabah."),
    ("papan", "Kalimat pendek", "Satu informasi per kalimat. Tanyakan cara yang diinginkan nasabah."),
]
C = lambda h: RGBColor.from_string(h.lstrip("#"))
PUTIH = C("FFFFFF")
F_JUDUL, F_ISI = "Montserrat", "Inter"

SEL_KEPALA = {"kepala": ".kepala", "h1": ".kepala h1", "sub": ".kepala p", "logo": ".kepala .kanan img", "kanan": ".kepala .kanan"}
SEL_DEPAN = dict(SEL_KEPALA, pita=".pita span", ubin=".ubin", foto=".ubin .foto", lencana=".ubin .lencana",
                 tag=".ubin .tagfoto", kata=".ubin .kata", kaki=".kaki span")
SEL_BELAKANG = dict(SEL_KEPALA, judul=".judul-k", judul_i=".judul-k i", tombol=".tombol > div", tombol_svg=".tombol > div > svg",
                    tombol_teks=".tombol > div > span", konf=".konf > div", konf_svg=".konf > div > svg", konf_teks=".konf > div > span",
                    pad=".pad > div", tulis=".tulis", tip_ik=".tips .ik", tip_b=".tips b", tip_teks=".tips > div > span:last-child",
                    contoh=".contoh", lab=".contoh .lab", lab_sub=".contoh .lab span", c=".contoh .c", sama=".contoh .sama",
                    hasil=".contoh .hasil", kaki=".kaki span")


def html_sisi(isi):
    return f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{NAMA}</title><style>{CSS}</style></head><body>{isi}</body></html>'


def node(*args):
    subprocess.run(["node", *map(str, args)], check=True, cwd=BUILD, capture_output=True)


# ---------- ikon PNG transparan untuk PPTX ----------
def ikon_png():
    IKON.mkdir(parents=True, exist_ok=True)
    tr, _ = KAT["Transaksi"]
    kr, _ = KAT["Konfirmasi"]
    daftar = [(f"ilus-{i}", ilus(i, 50, 38), 50, 38) for i, _ in LAYANAN]
    daftar += [(f"konf-{i}", ikon(i, kr, 15, 2), 15, 15) for i, _ in JAWABAN]
    daftar += [(f"tip-{i}", ikon(i, TEAL, 17), 17, 17) for i, _, _ in TIPS]
    daftar += [("orang-putih", ikon("orang", "#fff", 13, 2.2), 13, 13)]
    jobs = []
    for nama, svg, w, h in daftar:
        p = HTML / f"ikon-{nama}.html"
        svg_blok = svg.replace("<svg ", '<svg style="display:block" ', 1)
        p.write_text(f"<html><body style='margin:0;background:transparent'>{svg_blok}</body></html>")
        jobs.append({"html": str(p), "png": str(IKON / f"{nama}.png"), "width": w, "height": h, "scale": 6, "transparent": True})
    (BUILD / "jobs_ikon_kartu.json").write_text(json.dumps(jobs))
    node("render.js", BUILD / "jobs_ikon_kartu.json")


# ---------- bantu PPTX ----------
def bentuk(s, b, fill=None, garis=None, tebal=1.0, radius=0, oval=False, putus=False):
    jenis = MSO_SHAPE.OVAL if oval else (MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE)
    sh = s.shapes.add_shape(jenis, px(b["x"]), px(b["y"]), px(b["w"]), px(b["h"]))
    st = sh._element.find(qn("p:style"))
    if st is not None:
        sh._element.remove(st)
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = C(fill)
    if garis is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = C(garis)
        sh.line.width = Pt(tebal)
        if putus:
            sh.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    if radius and not oval:
        sh.adjustments[0] = min(0.5, radius / max(1, min(b["w"], b["h"])))
    return sh


def tulis(s, b, runs, size, warna=NAVY, font=F_ISI, bold=False, rata=PP_ALIGN.LEFT, tengah=True, lebar_tambah=4, spasi=1.0, bungkus=True):
    """runs: str, atau daftar paragraf berisi daftar (teks, opsi)."""
    if not bungkus:
        lebar_tambah += 60  # teks satu baris: beri ruang cadangan supaya tidak pindah baris di aplikasi lain
    if rata == PP_ALIGN.CENTER:
        x = b["x"] - lebar_tambah / 2
    elif rata == PP_ALIGN.RIGHT:
        x = b["x"] - lebar_tambah
    else:
        x = b["x"]
    tb = s.shapes.add_textbox(px(x), px(b["y"]), px(b["w"] + lebar_tambah), px(b["h"]))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE if tengah else MSO_ANCHOR.TOP
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    paras = [[(runs, {})]] if isinstance(runs, str) else runs
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = rata
        p.line_spacing = spasi
        for t, o in para:
            r = p.add_run()
            r.text = t
            f = r.font
            f.name = o.get("font", font)
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.color.rgb = C(o.get("warna", warna))
    return tb


def alfa(sh, persen):
    """Transparansi isian bentuk, misalnya 86 berarti 86 persen tampak."""
    clr = sh.fill._xPr.find(qn("a:solidFill")).find(qn("a:srgbClr"))
    a = clr.makeelement(qn("a:alpha"), {"val": str(int(persen * 1000))})
    clr.append(a)


def isi_bentuk(sh, teks, size, warna, font=F_JUDUL, bold=True):
    tf = sh.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = teks
    r.font.name, r.font.size, r.font.bold = font, Pt(size), bold
    r.font.color.rgb = C(warna)


def gambar(s, path, b, potong_vertikal=0.3, bulat_atas=False):
    pic = s.shapes.add_picture(str(path), px(b["x"]), px(b["y"]), px(b["w"]), px(b["h"]))
    iw, ih = Image.open(path).size
    r_img, r_kot = iw / ih, b["w"] / b["h"]
    if r_img > r_kot:
        sisa = 1 - r_kot / r_img
        pic.crop_left = pic.crop_right = sisa / 2
    elif r_img < r_kot:
        sisa = 1 - r_img / r_kot
        pic.crop_top, pic.crop_bottom = sisa * potong_vertikal, sisa * (1 - potong_vertikal)
    if bulat_atas:
        pic.auto_shape_type = MSO_SHAPE.ROUND_2_SAME_RECTANGLE
    return pic


def kepala(s, u, judul, sub):
    k = u["kepala"][0]
    sh = bentuk(s, k)
    sh.fill.gradient()
    sh.fill.gradient_angle = 25
    st = sh.fill.gradient_stops
    st[0].color.rgb, st[0].position = C(NAVY), 0.0
    st[1].color.rgb, st[1].position = C(TEAL), 1.0
    tulis(s, u["h1"][0], judul, 17.25, "#FFFFFF", F_JUDUL, True, lebar_tambah=30, bungkus=False)
    tulis(s, u["sub"][0], sub, 8.6, "#FFFFFF", lebar_tambah=30, bungkus=False)
    lg = u["logo"][0]
    s.shapes.add_picture(str(LOGO_PUTIH), px(lg["x"]), px(lg["y"]), px(lg["w"]), px(lg["h"]))
    kn = u["kanan"][0]["teks"]
    b = dict(kn, x=kn["x"] - 40, w=kn["w"] + 40)
    tulis(s, b, "PT BPR NBP 27, Bandung", 7.5, "#FFFFFF", rata=PP_ALIGN.RIGHT, lebar_tambah=0, bungkus=False)


def depan(prs, u):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kepala(s, u, "Kartu Saku Isyarat Perbankan", "20 isyarat BISINDO yang paling sering dipakai di loket")
    for b, (nama, (tua, muda)) in zip(u["pita"], KAT.items()):
        sh = bentuk(s, b, fill=muda, radius=b["h"] / 2)
        isi_bentuk(sh, nama.upper(), 7.1, tua, F_ISI)
    for i, (k, kat) in enumerate(KATA):
        tua, muda = KAT[kat]
        bentuk(s, u["ubin"][i], fill="#FFFFFF", garis=muda, tebal=1.05, radius=12)
        f = foto_untuk(i + 1, k, FOTO_CONTOH)
        fb = u["foto"][i]
        if f:
            gambar(s, f, fb, bulat_atas=True)
        else:
            bentuk(s, fb, fill=muda)
        lb = u["lencana"][i]
        isi_bentuk(bentuk(s, lb, fill=tua, radius=8), f"{i + 1:02d}", 7.5, "#FFFFFF")
        if u["tag"]:
            tg = u["tag"][i]
            sh = bentuk(s, tg, fill="#FFFFFF", radius=8)
            alfa(sh, 86)
            isi_bentuk(sh, TAG.upper(), 4.9, tua, F_ISI)
        tulis(s, u["kata"][i], k, 9, NAVY, F_JUDUL, True, rata=PP_ALIGN.CENTER)
    kk = u["kaki"]
    tulis(s, dict(kk[0], w=kk[0]["w"] + 10), KETERANGAN, 7.1, "#4b6070", lebar_tambah=0, bungkus=False)
    tulis(s, dict(kk[1], x=kk[1]["x"] - 20, w=kk[1]["w"] + 20), "Balik kartu untuk kartu tunjuk", 7.1, "#4b6070",
          rata=PP_ALIGN.RIGHT, lebar_tambah=0, bungkus=False)


def belakang(prs, u):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kepala(s, u, "Kartu Tunjuk untuk Nasabah", "Nasabah menunjuk, petugas mengonfirmasi dengan isyarat atau tulisan")
    tr, _ = KAT["Transaksi"]
    kr, km = KAT["Konfirmasi"]
    nr, _ = KAT["Nominal"]
    judul = [("Saya ingin", tr, "1"), ("Jawaban", kr, "3"), ("Jumlahnya", nr, "2"), ("Untuk petugas", TEAL, None)]
    for (t, w, n), jb, ji in zip(judul, u["judul"], u["judul_i"]):
        sh = bentuk(s, ji, fill=w, oval=True)
        if n:
            isi_bentuk(sh, n, 7.9, "#FFFFFF")
        else:
            m = 13
            s.shapes.add_picture(str(IKON / "orang-putih.png"), px(ji["x"] + (ji["w"] - m) / 2), px(ji["y"] + (ji["h"] - m) / 2), px(m), px(m))
        tulis(s, jb["teks"], t, 9.4, NAVY, F_JUDUL, True, lebar_tambah=10, bungkus=False)
    for (i, t), b, sv, tx in zip(LAYANAN, u["tombol"], u["tombol_svg"], u["tombol_teks"]):
        bentuk(s, b, fill="#FFFFFF", garis="#CFE6E3", tebal=1.05, radius=11)
        s.shapes.add_picture(str(IKON / f"ilus-{i}.png"), px(sv["x"]), px(sv["y"]), px(sv["w"]), px(sv["h"]))
        tulis(s, tx, t, 8.5, NAVY, F_JUDUL, True, lebar_tambah=6)
    for (i, t), b, sv, tx in zip(JAWABAN, u["konf"], u["konf_svg"], u["konf_teks"]):
        bentuk(s, b, fill=km, radius=b["h"] / 2)
        s.shapes.add_picture(str(IKON / f"konf-{i}.png"), px(sv["x"]), px(sv["y"]), px(sv["w"]), px(sv["h"]))
        tulis(s, tx, t, 7.9, NAVY, F_JUDUL, True, lebar_tambah=6, bungkus=False)
    for b in u["pad"]:
        sh = bentuk(s, b, fill="#FDF1DC", garis="#F1C879", tebal=1.0, radius=10)
        isi_bentuk(sh, b["isi"], 9 if len(b["isi"]) > 1 else 12.75, "#8a5a00")
    tb = u["tulis"][0]
    sh = bentuk(s, tb, garis="#9fb3bf", tebal=1.2, radius=11, putus=True)
    tulis(s, dict(tb, x=tb["x"] + 9, y=tb["y"] + 6, w=tb["w"] - 18, h=24), "Tulis di sini dengan spidol. Kartu dilaminasi, bisa dihapus.",
          6.75, "#7b8d98", tengah=False, lebar_tambah=0)
    for (i, j, t), ik, bb, tx in zip(TIPS, u["tip_ik"], u["tip_b"], u["tip_teks"]):
        bentuk(s, ik, fill="#E3F5F9", radius=9)
        m = 17
        s.shapes.add_picture(str(IKON / f"tip-{i}.png"), px(ik["x"] + (ik["w"] - m) / 2), px(ik["y"] + (ik["h"] - m) / 2), px(m), px(m))
        kotak_teks = dict(x=bb["x"], y=bb["y"], w=tx["w"], h=tx["y"] + tx["h"] - bb["y"])
        tulis(s, kotak_teks, [[(j, {"font": F_JUDUL, "bold": True, "size": 8, "warna": NAVY})], [(t, {})]], 7.7, "#24394a",
              tengah=False, lebar_tambah=3, spasi=1.05)
    bentuk(s, u["contoh"][0], fill="#F6FAFB", garis="#DCE8EC", tebal=1.0, radius=14)
    lab = u["lab"][0]
    tulis(s, dict(lab, w=lab["w"] + 8), [[("Contoh menunjuk nominal", {"font": F_JUDUL, "bold": True, "size": 8.25, "warna": NAVY})],
                                         [("Tunjuk berurutan dari kiri ke kanan", {"size": 7.1, "warna": "#5b6f7c"})]], 7.1, tengah=True, lebar_tambah=0)
    for b in u["c"]:
        sh = bentuk(s, b, fill="#FDF1DC", garis="#F1C879", tebal=1.0, radius=9)
        isi_bentuk(sh, b["isi"], 8.25 if len(b["isi"]) > 1 else 11.25, "#8a5a00")
    tulis(s, u["sama"][0], "=", 13.5, "#9fb3bf", F_JUDUL, True, rata=PP_ALIGN.CENTER)
    hs = u["hasil"][0]
    tulis(s, dict(hs, x=hs["x"] - 20, w=hs["w"] + 20), "Rp 2.750.000", 15, TEAL, F_JUDUL, True, rata=PP_ALIGN.RIGHT, lebar_tambah=0, bungkus=False)
    kk = u["kaki"]
    tulis(s, dict(kk[0], w=kk[0]["w"] + 10), "Disiapkan Sanggabiz untuk In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas.",
          7.1, "#4b6070", lebar_tambah=0, bungkus=False)
    tulis(s, dict(kk[1], x=kk[1]["x"] - 20, w=kk[1]["w"] + 20), "sanggabiz.com", 7.1, TEAL, bold=True, rata=PP_ALIGN.RIGHT,
          lebar_tambah=0, bungkus=False)


def main():
    TMP.mkdir(exist_ok=True)
    d = sisi_depan(FOTO_CONTOH, KETERANGAN, TAG)
    b = sisi_belakang()
    p_full, p_d, p_b = HTML / "kartu-v4.html", HTML / "kartu-v4-depan.html", HTML / "kartu-v4-belakang.html"
    p_full.write_text(html_sisi(d + b), encoding="utf8")
    p_d.write_text(html_sisi(d), encoding="utf8")
    p_b.write_text(html_sisi(b), encoding="utf8")
    prev = ROOT / "preview"
    jobs = [{"html": str(p_full), "pdf": str(ROOT / "kit" / f"{NAMA}.pdf"), "width": 794, "height": 559},
            {"html": str(p_d), "png": str(prev / "kartu-v4-depan.png"), "width": 794, "height": 559, "scale": 2.5, "transparent": True},
            {"html": str(p_b), "png": str(prev / "kartu-v4-belakang.png"), "width": 794, "height": 559, "scale": 2.5, "transparent": True}]
    (BUILD / "jobs_kartu_v4.json").write_text(json.dumps(jobs, indent=1))
    node("render.js", BUILD / "jobs_kartu_v4.json")
    ukur = [{"nama": "depan", "html": str(p_d), "width": 794, "height": 559, "selectors": SEL_DEPAN},
            {"nama": "belakang", "html": str(p_b), "width": 794, "height": 559, "selectors": SEL_BELAKANG}]
    (TMP / "ukur_v4.json").write_text(json.dumps(ukur))
    node("ukur.js", TMP / "ukur_v4.json", TMP / "ukuran_v4.json")
    u = json.loads((TMP / "ukuran_v4.json").read_text())
    ikon_png()
    prs = Presentation()
    prs.slide_width, prs.slide_height = px(794), px(559)
    depan(prs, u["depan"])
    belakang(prs, u["belakang"])
    prs.core_properties.title = "Kartu Saku Isyarat Perbankan v4"
    prs.core_properties.author = "Sanggabiz"
    out = ROOT / "kit" / f"{NAMA}.pptx"
    prs.save(out)
    print(out)


if __name__ == "__main__":
    main()
