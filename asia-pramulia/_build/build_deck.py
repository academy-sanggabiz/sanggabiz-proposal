#!/usr/bin/env python3
"""Pembangun deck silabus dan alat bantu PT Asia Pramulia Tbk.

Bentuk halaman mengikuti standar silabus satu hari Sanggabiz
(reference/format-standar/05-silabus-satu-hari-rujukan.pptx). Skrip ini menyalin bentuk
dari berkas rujukan (kepala, kaki, tabel, kartu), lalu mengganti isinya. Halaman rujukan
dibuang di akhir, jadi font, warna, dan ukuran sama persis dengan standar.

Jalankan dari akar repo:
    python3 asia-pramulia/_build/build_deck.py
"""
import copy
import os

from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TPL = os.path.join(ROOT, "reference", "format-standar", "05-silabus-satu-hari-rujukan.pptx")
ASSET = os.path.join(ROOT, "asia-pramulia", "_build", "assets")
OUT = os.path.join(ROOT, "asia-pramulia", "proposal",
                   "Proposal Silabus dan Alat Bantu - IHT PT Asia Pramulia Tbk.pptx")

prs = Presentation(TPL)
REF = list(prs.slides)
R_RUNDOWN, R_MODUL, R_DIDAPAT, R_ASET = REF[0], REF[1], REF[4], REF[5]
N_REF = len(REF)
CHROME = 15  # logo, tahun, garis, judul, subjudul, garis bawah, tiga kontak


# ------------------------------------------------------------------ utilitas bentuk
def _next_id(slide):
    ids = [int(e.get("id")) for e in slide.shapes._spTree.iter(qn("p:cNvPr"))]
    return max(ids + [1]) + 1


def copy_shape(shape, dst):
    el = copy.deepcopy(shape._element)
    for blip in el.iter(qn("a:blip")):
        rid = blip.get(qn("r:embed"))
        part = shape.part.related_part(rid)
        blip.set(qn("r:embed"), dst.part.relate_to(part, RT.IMAGE))
    for c in el.iter(qn("p:cNvPr")):
        c.set("id", str(_next_id(dst)))
    dst.shapes._spTree.insert_element_before(el, "p:extLst")
    return dst.shapes[-1]


def new_slide(src, upto=None, skip=()):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    for i, sh in enumerate(src.shapes):
        if upto is not None and i >= upto:
            break
        if sh.name in skip:
            continue
        copy_shape(sh, s)
    return s


def find(slide, name):
    for sh in slide.shapes:
        if sh.name == name:
            return sh
    raise KeyError(name)


def move(sh, x=None, y=None, w=None, h=None):
    if x is not None:
        sh.left = Inches(x)
    if y is not None:
        sh.top = Inches(y)
    if w is not None:
        sh.width = Inches(w)
    if h is not None:
        sh.height = Inches(h)


# ------------------------------------------------------------------ utilitas teks
def _highlight(run_el):
    """Stabilo kuning untuk penanda [ISI TIM: ...] sesuai ATURAN-PENULISAN.md."""
    rpr = run_el.find(qn("a:rPr"))
    hl = rpr.makeelement(qn("a:highlight"), {})
    clr = hl.makeelement(qn("a:srgbClr"), {"val": "FFFF00"})
    hl.append(clr)
    latin = rpr.find(qn("a:latin"))
    if latin is not None:
        latin.addprevious(hl)
    else:
        rpr.append(hl)


def _split_isi_tim(p):
    for r in list(p.findall(qn("a:r"))):
        t = r.find(qn("a:t")).text or ""
        if "[ISI TIM" not in t:
            continue
        a = t.index("[ISI TIM")
        b = t.index("]", a) + 1
        parts = [(t[:a], False), (t[a:b], True), (t[b:], False)]
        prev = r
        for txt, mark in parts:
            if not txt:
                continue
            nr = copy.deepcopy(r)
            nr.find(qn("a:t")).text = txt
            if mark:
                _highlight(nr)
            prev.addnext(nr)
            prev = nr
        r.getparent().remove(r)


def set_paras(txbody, items):
    """Ganti isi paragraf dengan tetap memakai format paragraf rujukan.

    items: daftar paragraf. Satu paragraf berupa str (satu run) atau list str (run berurutan).
    Paragraf ke-i memakai paragraf rujukan ke-i, atau paragraf rujukan terakhir bila kurang.
    """
    ps = txbody.findall(qn("a:p"))
    for p in ps:
        txbody.remove(p)
    for i, item in enumerate(items):
        p = copy.deepcopy(ps[min(i, len(ps) - 1)])
        runs = p.findall(qn("a:r"))
        texts = [item] if isinstance(item, str) else list(item)
        for r in runs:
            p.remove(r)
        if not runs:
            txbody.append(p)
            continue
        anchor = p.find(qn("a:endParaRPr"))
        for j, t in enumerate(texts):
            r = copy.deepcopy(runs[min(j, len(runs) - 1)])
            r.find(qn("a:t")).text = t
            if anchor is not None:
                anchor.addprevious(r)
            else:
                p.append(r)
        _split_isi_tim(p)
        txbody.append(p)


def set_text(shape, items):
    set_paras(shape.text_frame._txBody, items if isinstance(items, list) else [items])


def header(slide, judul, sub):
    set_text(find(slide, "TextBox 4"), judul)
    set_text(find(slide, "TextBox 5"), sub)


# ------------------------------------------------------------------ utilitas tabel
def rebuild_table(tbl_shape, rows, templates, widths=None):
    """rows: daftar (kunci_template, [isi sel]). Isi sel: str, list paragraf, atau dict."""
    tbl = tbl_shape.table._tbl
    trs = tbl.findall(qn("a:tr"))
    tpl = {k: copy.deepcopy(trs[i]) for k, i in templates.items()}
    for tr in trs[1:]:
        tbl.remove(tr)
    for key, cells in rows:
        tr = copy.deepcopy(tpl[key])
        for tc, val in zip(tr.findall(qn("a:tc")), cells):
            if val is None:
                continue
            bold = None
            if isinstance(val, dict):
                bold = val.get("bold")
                val = val["text"]
            set_paras(tc.find(qn("a:txBody")), val if isinstance(val, list) else [val])
            if bold is not None:
                for rpr in tc.iter(qn("a:rPr")):
                    rpr.set("b", "1" if bold else "0")
        tbl.append(tr)
    if widths:
        for gc, w in zip(tbl.find(qn("a:tblGrid")).findall(qn("a:gridCol")), widths):
            gc.set("w", str(int(Inches(w))))
    return tbl


def set_header_row(tbl_shape, labels):
    tr = tbl_shape.table._tbl.findall(qn("a:tr"))[0]
    for tc, lab in zip(tr.findall(qn("a:tc")), labels):
        set_paras(tc.find(qn("a:txBody")), [lab])


# ================================================================== HALAMAN 1: silabus satu hari
s = new_slide(R_RUNDOWN)
header(s, "SILABUS PELATIHAN: SATU HARI, SATU KASUS PABRIK",
       "In-House Training Pengembangan Kompetensi Karyawan, PT Asia Pramulia Tbk, Surabaya. "
       "[ISI TIM: jumlah] peserta, 08.00 - 16.30 WIB.")
set_text(find(s, "TextBox 16"),
         "Delapan topik dipelajari dalam satu alur kerja pabrik: rencana biaya dan jadwal, ketersediaan bahan, "
         "kondisi lantai produksi, lalu perbaikan. Setiap topik berisi paparan singkat dan latihan dengan alat bantu Sanggabiz.")
for num_box, desc_box, angka, label, desc in [
    ("TextBox 18", "TextBox 19", "8 topik", "EMPAT SESI",
     "Delapan topik yang diminta dibahas dalam empat sesi mengikuti alur kerja pabrik."),
    ("TextBox 21", "TextBox 22", "1 kasus", "SEPANJANG HARI",
     "Satu order tutup botol 28 mm diikuti dari jadwal sampai perbaikan."),
    ("TextBox 24", "TextBox 25", "5 alat", "DIBAWA PULANG",
     "Lembar kerja Excel berisi kasus contoh, siap diisi data pabrik sendiri."),
]:
    set_text(find(s, num_box), [angka, label])
    set_text(find(s, desc_box), desc)
rebuild_table(find(s, "Table 26"), [
    ("a", ["08.00 - 08.15", "Pembukaan dan pre-test",
           "Peserta dibagi ke kelompok lintas fungsi, menerima buku kasus, dan mengerjakan 15 soal pre-test."]),
    ("b", ["08.15 - 08.30", "Kerangka perbaikan berkelanjutan",
           "PDCA dan delapan pemborosan sebagai cara melihat masalah sepanjang hari."]),
    ("a", ["08.30 - 10.00", "Sesi 1. Rencana: biaya dan jadwal produksi",
           "Menghitung biaya per unit, membaca beban mesin, dan memilih urutan order minggu ini."]),
    ("rehat", ["10.00 - 10.15", "Rehat kopi", ""]),
    ("b", ["10.15 - 11.45", "Sesi 2. Material: gudang dan inventori",
           "Mengecek akurasi stok, kelas ABC, titik pesan ulang, dan kecukupan resin untuk jadwal."]),
    ("rehat", ["11.45 - 12.45", "Istirahat, salat, dan makan siang", ""]),
    ("a", ["12.45 - 14.15", "Sesi 3. Lantai produksi: Gemba Walk dan OEE",
           "Mengamati satu area dengan checklist, lalu mencari loss terbesar dari data delapan shift."]),
    ("rehat", ["14.15 - 14.30", "Rehat kopi", ""]),
    ("b", ["14.30 - 16.00", "Sesi 4. Perbaikan: RCA, CAPA, dan kaizen",
           "Menelusuri akar penyebab short shot, menyusun CAPA dan kaizen, lalu menghitung dampaknya ke biaya."]),
    ("a", ["16.00 - 16.30", "Post-test, rencana tindak lanjut, dan penutupan",
           "Setiap peserta menulis rencana 30 hari untuk area kerjanya."]),
], {"a": 1, "b": 2, "rehat": 5})

# ================================================================== HALAMAN 2: alur satu kasus
s = new_slide(R_DIDAPAT)
header(s, "ALUR PELATIHAN: SATU KASUS, EMPAT SESI",
       "Hasil kerja satu sesi menjadi bahan sesi berikutnya. Seluruh hari membentuk satu siklus PDCA.")
card = ["Rounded Rectangle 16", "Rounded Rectangle 17", "Rectangle 18", "TextBox 19", "TextBox 20"]
alur = [
    ("Sesi 1. Rencana (Plan)", [
        "Topik: Budgeting dan Cost Control, Perencanaan dan Penjadwalan Produksi",
        "Pertanyaan: berapa biaya per unit, dan cukupkah kapasitas mesin minggu ini?",
        "Diteruskan: jadwal mingguan dan kebutuhan bahan"]),
    ("Sesi 2. Material (Do)", [
        "Topik: Warehouse Management, Pengendalian Inventori",
        "Pertanyaan: apakah bahan untuk jadwal itu ada, dan stoknya akurat?",
        "Diteruskan: item kritis dan selisih stok"]),
    ("Sesi 3. Lantai Produksi (Check)", [
        "Topik: Gemba Walk, OEE",
        "Pertanyaan: produksi berjalan, mengapa target tidak tercapai?",
        "Diteruskan: temuan Gemba dan loss terbesar"]),
    ("Sesi 4. Perbaikan (Act)", [
        "Topik: Problem Solving dan RCA, Continuous Improvement",
        "Pertanyaan: apa akar penyebabnya dan apa tindakannya?",
        "Kembali ke Sesi 1: dampak perbaikan ke biaya"]),
]
base = {n: find(s, n) for n in card}
W, GAP, X0 = 2.88, 0.16, 0.67
for k, (judul, butir) in enumerate(alur):
    x = X0 + k * (W + GAP)
    shapes = {n: (base[n] if k == 0 else copy_shape(base[n], s)) for n in card}
    move(shapes["Rounded Rectangle 16"], x=x, w=W, h=2.95)
    move(shapes["Rounded Rectangle 17"], x=x, w=W)
    move(shapes["Rectangle 18"], x=x, w=W)
    move(shapes["TextBox 19"], x=x + 0.14, w=W - 0.28)
    move(shapes["TextBox 20"], x=x + 0.14, w=W - 0.28, h=2.25)
    set_text(shapes["TextBox 19"], judul)
    set_text(shapes["TextBox 20"], [["•  ", b] for b in butir])
for n in ["Rounded Rectangle 21", "Rounded Rectangle 22", "Rectangle 23", "TextBox 24", "TextBox 25",
          "Rounded Rectangle 26", "Rounded Rectangle 27", "Rectangle 28", "TextBox 29", "TextBox 30"]:
    el = find(s, n)._element
    el.getparent().remove(el)
move(find(s, "Rounded Rectangle 31"), y=4.98, h=0.95)
move(find(s, "TextBox 32"), y=5.04, h=0.84)
set_text(find(s, "TextBox 32"), [[
    "Kasus pelatihan. ",
    "Pabrik contoh menerima order tutup botol 28 mm. Jadwal di mesin IM-01 tampak cukup, tetapi stok resin "
    "di gudang selisih, OEE hanya 69 persen, dan short shot berulang, sehingga biaya resin melewati anggaran. "
    "Semua data kasus disusun Sanggabiz untuk latihan, bukan data PT Asia Pramulia."]])

# ================================================================== HALAMAN 3 sampai 6: rincian sesi
SESI = [
    ("SESI 1. RENCANA", [
        ("Topik 1", "Budgeting, Cost Control dan Cost Efficiency", "08.30 - 09.05 WIB",
         ["Biaya bahan baku, tenaga kerja langsung, dan overhead",
          "Biaya tetap dan biaya variabel",
          "Biaya per unit sebagai dasar anggaran",
          "Titik kendali biaya: scrap, energi, lembur, perawatan"],
         ["Paparan struktur biaya dengan contoh tutup botol.",
          "Kelompok menghitung biaya per unit lini tutup botol dari data kasus.",
          "Kelompok menandai dua akun yang paling mudah membengkak dan alasannya."],
         "Kalkulator Anggaran dan Varians", "Presentasi, buku kasus",
         "Peserta bisa membaca struktur biaya dan biaya per unit lini produksinya."),
        ("Topik 2", "Perencanaan dan Penjadwalan Produksi", "09.05 - 10.00 WIB",
         ["Alur dari permintaan sampai jadwal harian",
          "Jam mesin dari jumlah, cavity, waktu siklus, dan setup",
          "Aturan prioritas: FIFO, tenggat terdekat, waktu proses terpendek"],
         ["Peserta menghitung jam mesin satu order dengan tangan.",
          "Kelompok membaca beban tujuh order di tiga mesin.",
          "Kelompok mengubah urutan order dan membandingkan jumlah order terlambat.",
          "Jadwal terpilih diubah menjadi kebutuhan resin dan karton."],
         "Kalkulator Kapasitas dan Jadwal", "Presentasi, buku kasus",
         "Jadwal mingguan dan daftar kebutuhan bahan, dibawa ke Sesi 2."),
    ]),
    ("SESI 2. MATERIAL", [
        ("Topik 3", "Warehouse Management", "10.15 - 10.55 WIB",
         ["Alur gudang dari penerimaan sampai pengiriman",
          "Kode lokasi, FIFO, dan FEFO",
          "Cycle count dan akurasi stok"],
         ["Paparan alur gudang bahan baku plastik dengan denah contoh.",
          "Kelompok membaca hasil cycle count delapan item dan akurasi stoknya.",
          "Kelompok menelusuri penyebab selisih stok resin PP."],
         "Kalkulator Inventori dan Gudang", "Presentasi, denah gudang contoh",
         "Peserta bisa membaca akurasi stok dan menelusuri penyebab selisih."),
        ("Topik 4", "Pengendalian Inventori", "10.55 - 11.45 WIB",
         ["Bahan baku, bahan pembantu, dan bahan pelengkap",
          "Analisis ABC",
          "Stok pengaman dan titik pemesanan ulang",
          "Sisa bahan baku di area mesin"],
         ["Kelompok menebak item kelas A, lalu mencocokkan dengan hasil ABC.",
          "Kelompok mencari item di bawah titik pemesanan ulang dan mengecek resin untuk jadwal Sesi 1.",
          "Kelompok menandai surat perintah produksi dengan bahan tidak terlacak."],
         "Kalkulator Inventori dan Gudang", "Presentasi, buku kasus",
         "Daftar item kritis dan keputusan pemesanan, dibawa ke Sesi 3."),
    ]),
    ("SESI 3. LANTAI PRODUKSI", [
        ("Topik 5", "Gemba Walk", "12.45 - 13.20 WIB",
         ["Gemba: melihat langsung di tempat kerja",
          "Lima area amatan: keselamatan, 5S, aliran material, kondisi mesin, informasi visual",
          "Bertanya kepada proses, bukan menyalahkan orang"],
         ["Paparan tujuan dan etika walk.",
          "Kelompok mengamati satu area lini atau gudang dengan checklist. Bila izin tidak ada, memakai foto dan video area.",
          "Kelompok menulis tiga temuan beserta pertanyaannya."],
         "Checklist Gemba lima area", "Presentasi, foto dan video area produksi",
         "Tiga temuan Gemba per kelompok."),
        ("Topik 6", "OEE (Overall Equipment Effectiveness)", "13.20 - 14.15 WIB",
         ["OEE = Availability x Performance x Quality",
          "Enam big losses",
          "Membaca loss terbesar dari data shift"],
         ["Peserta menghitung OEE satu shift dengan tangan, lalu mencocokkan di kalkulator.",
          "Kelompok menebak loss terbesar dari delapan shift, lalu mencocokkan.",
          "Kelompok menghubungkan loss terbesar dengan temuan Gemba."],
         "Kalkulator OEE", "Presentasi, buku kasus",
         "Loss terbesar mesin IM-01 dan dugaan penyebabnya, dibawa ke Sesi 4."),
    ]),
    ("SESI 4. PERBAIKAN", [
        ("Topik 7", "Problem Solving, Analytical Thinking dan RCA", "14.30 - 15.30 WIB",
         ["Alur pemecahan masalah dari data sampai verifikasi",
          "Pareto, Fishbone, dan 5 Why",
          "CAPA: tindakan korektif dan pencegahan"],
         ["Kelompok memilih cacat dominan dengan Pareto.",
          "Kelompok menggambar Fishbone di kertas plano.",
          "Kelompok menelusuri short shot dengan 5 Why sampai akar penyebab.",
          "Kelompok menulis satu CAPA dengan PIC, tenggat, dan bukti hasil."],
         "Pareto, 5 Why, dan CAPA", "Presentasi, kertas plano, sticky note",
         "Akar penyebab dan satu CAPA per kelompok."),
        ("Topik 8", "Continuous Improvement Mindset", "08.15 - 08.30 dan 15.30 - 16.00 WIB",
         ["PDCA dan delapan pemborosan",
          "Kaizen: perbaikan kecil oleh pelaksana",
          "Menghitung dampak perbaikan ke biaya"],
         ["Pagi: PDCA dan delapan pemborosan sebagai kerangka hari ini.",
          "Tiap peserta menulis satu usulan kaizen di kartu.",
          "Kelompok menghitung penghematan dari CAPA dan membandingkannya dengan anggaran Sesi 1."],
         "Kartu usulan kaizen, Kalkulator Anggaran dan Varians", "Presentasi",
         "Usulan kaizen per peserta dan perkiraan penghematan per tahun."),
    ]),
]
for judul, baris in SESI:
    s = new_slide(R_MODUL)
    header(s, "SILABUS PELATIHAN: " + judul, "Apa yang dipelajari, apa yang dilakukan peserta, dan apa hasilnya.")
    tb = find(s, "Table 16")
    set_header_row(tb, ["Topik", "Yang dipelajari", "Kegiatan peserta", "Alat dan media", "Hasil"])
    rows = []
    for k, (lab, nama, jam, pelajari, kegiatan, alat, media, hasil) in enumerate(baris):
        rows.append(("a" if k == 0 else "b", [
            [lab, nama, jam],
            ["• " + t for t in pelajari],
            ["• " + t for t in kegiatan],
            [["Alat: ", alat], ["Media: ", media]],
            hasil,
        ]))
    rebuild_table(tb, rows, {"a": 1, "b": 2})

# ================================================================== HALAMAN 7: yang didapat
s = new_slide(R_DIDAPAT)
header(s, "YANG DIDAPAT PT ASIA PRAMULIA",
       "Hasil yang bisa langsung dipakai di area kerja, dan bukti yang bisa ditunjukkan kepada manajemen.")
for judul_box, isi_box, judul, butir in [
    ("TextBox 19", "TextBox 20", "Untuk peserta", [
        "Paham delapan topik dalam satu alur kerja pabrik",
        "Pernah mencoba setiap alat dengan kasus pabrik plastik",
        "Lima lembar kerja Excel yang bisa diisi data sendiri",
        "Sertifikat perorangan yang menyebut delapan topik"]),
    ("TextBox 24", "TextBox 25", "Untuk supervisor dan manajemen", [
        "Rencana tindak lanjut 30 hari dari setiap peserta",
        "Daftar CAPA dan usulan kaizen hasil kelompok",
        "Laporan evaluasi: nilai pre-test dan post-test, foto kegiatan, catatan fasilitator",
        "Pemantauan tindak lanjut 30 hari sesudah pelatihan"]),
    ("TextBox 29", "TextBox 30", "Cara kami memastikan hasilnya", [
        "Pre-test dan post-test dengan soal yang sama",
        "Hasil kerja kelompok diperiksa fasilitator di setiap sesi",
        "Survei kepuasan peserta",
        "Laporan dikirim paling lambat 7 hari kerja setelah pelatihan"]),
]:
    set_text(find(s, judul_box), judul)
    set_text(find(s, isi_box), [["•  ", b] for b in butir])
set_text(find(s, "TextBox 32"), [[
    "Dua fasilitator sepanjang hari. ",
    "Satu berlatar produksi dan gudang, satu berlatar biaya dan perencanaan, sehingga setiap kelompok "
    "didampingi saat latihan. [ISI TIM: nama dan pengalaman fasilitator]"]])

# ================================================================== HALAMAN 8: toolkit
s = new_slide(R_RUNDOWN, skip={"TextBox 16"} | {f"Rounded Rectangle {n}" for n in (17, 20, 23)}
              | {f"TextBox {n}" for n in (18, 19, 21, 22, 24, 25)})
header(s, "TOOLKIT SANGGABIZ: ALAT BANTU BELAJAR",
       "Alat yang disiapkan untuk pelatihan ini. Lembar kerja Excel dibawa pulang peserta.")
tb = find(s, "Table 26")
move(tb, y=1.79)
set_header_row(tb, ["Alat", "Isi", "Bentuk"])
B = lambda t: {"text": t, "bold": True}
N = lambda t: {"text": t, "bold": False}
alat = [
    ("Kalkulator OEE", "OEE per shift dan per mesin, enam big losses, dan loss terbesar", "Excel"),
    ("Pareto, 5 Why, dan CAPA", "Pareto jenis cacat dengan grafik, formulir 5 Why, dan daftar CAPA", "Excel"),
    ("Kalkulator Anggaran dan Varians", "Anggaran dari volume produksi, varians dengan anggaran fleksibel, dan dampak perbaikan ke biaya", "Excel"),
    ("Kalkulator Inventori dan Gudang", "Analisis ABC, stok pengaman dan titik pesan ulang, cycle count, dan sisa bahan baku", "Excel"),
    ("Kalkulator Kapasitas dan Jadwal", "Beban mesin, urutan order dan keterlambatan, dan kebutuhan bahan dari jadwal", "Excel"),
    ("Buku kasus", "Cerita pabrik contoh dan data awal setiap sesi", "Cetak"),
    ("Checklist Gemba Walk", "Lima area amatan dan kolom temuan", "Cetak"),
    ("Kartu usulan kaizen", "Kondisi sebelum, usulan, perkiraan hasil, dan penanggung jawab", "Cetak"),
    ("Lembar rencana tindak lanjut", "Rencana 30 hari setiap peserta untuk area kerjanya", "Cetak"),
    ("Pre-test, post-test, dan survei", "Soal yang sama di awal dan akhir, dan survei kepuasan peserta", "Formulir daring"),
]
rebuild_table(tb, [("a" if i % 2 == 0 else "b", [B(n), N(isi), N(bt)]) for i, (n, isi, bt) in enumerate(alat)],
              {"a": 1, "b": 2}, widths=[3.1, 7.2, 1.7])
note_box = copy_shape(find(R_DIDAPAT, "Rounded Rectangle 31"), s)
note_txt = copy_shape(find(R_DIDAPAT, "TextBox 32"), s)
move(note_box, y=4.65, h=1.0)
move(note_txt, y=4.71, h=0.9)
set_text(note_txt, [[
    "Data contoh. ",
    "Angka di setiap lembar kerja disusun Sanggabiz untuk latihan. Bila PT Asia Pramulia berkenan memberi data "
    "yang sudah dianonimkan, data contoh kami ganti agar latihan lebih dekat ke pekerjaan peserta. Materi lanjutan "
    "untuk belajar mandiri tersedia di LMS Sanggabiz. [ISI TIM: konfirmasi fitur dan harga LMS]"]])

# ================================================================== HALAMAN 9 sampai 11: contoh alat
ASET_SKIP = {"Picture 16", "Picture 19", "Rounded Rectangle 20", "TextBox 21"}
CONTOH = [
    ("KALKULATOR OEE",
     [("Lembar OEE: data per shift", "oee-lembar-oee.png"), ("Lembar Loss: enam big losses", "oee-lembar-loss.png")],
     [("Apa ini", "Lembar kerja Excel dengan rumus hidup. Peserta mengisi data per shift, lalu kalkulator menghitung "
                  "Availability, Performance, Quality, OEE, dan enam big losses."),
      ("Data kasus", "Delapan shift dua mesin injeksi. Loss terbesar ternyata kecepatan turun, bukan kerusakan, "
                     "jadi peserta belajar membaca data sebelum menebak."),
      ("Dipakai di", "Sesi 3. Sesudah pelatihan, berkas yang sama bisa diisi data mesin PT Asia Pramulia.")]),
    ("PARETO, 5 WHY, DAN CAPA",
     [("Lembar Pareto: cacat terbanyak", "pareto-lembar-pareto.png"), ("Lembar CAPA: daftar tindakan", "pareto-lembar-capa.png")],
     [("Apa ini", "Tiga lembar dalam satu berkas: Pareto jenis cacat dengan grafik, formulir 5 Why, dan daftar CAPA "
                  "dengan status dan penanda terlambat."),
      ("Data kasus", "Short shot pada tutup botol 28 mm di mesin IM-01. Akar penyebabnya, langkah menyalakan dryer "
                     "resin tidak ada di checklist awal shift."),
      ("Dipakai di", "Sesi 4. Daftar CAPA bisa langsung dipakai sebagai daftar tindakan di area kerja.")]),
    ("KALKULATOR KAPASITAS DAN JADWAL",
     [("Lembar Order: urutan dan keterlambatan", "jadwal-lembar-order.png"),
      ("Lembar Kebutuhan Bahan: dari jadwal ke resin", "jadwal-lembar-kebutuhan-bahan.png")],
     [("Apa ini", "Menghitung jam mesin, beban mesin dibanding kapasitas, hari selesai, dan status terlambat. "
                  "Lembar Kebutuhan Bahan mengubah jadwal menjadi kebutuhan resin dan karton."),
      ("Data kasus", "Tujuh order di tiga mesin. Urutan awal membuat tiga order terlambat dan resin HDPE tidak cukup. "
                     "Mengubah urutan mengubah hasilnya."),
      ("Dipakai di", "Sesi 1, lalu kebutuhan bahan dibawa ke Sesi 2.")]),
]
from PIL import Image

for judul, gambar, info in CONTOH:
    s = new_slide(R_ASET, skip=ASET_SKIP)
    header(s, "CONTOH ALAT BANTU: " + judul,
           "Lembar kerja Excel yang dipakai di kelas dan dibawa pulang peserta. Angka di dalamnya adalah data kasus latihan.")
    chip_box, chip_txt = find(s, "Rounded Rectangle 17"), find(s, "TextBox 18")
    y = 1.80
    LEFT, MAXW = 0.67, 8.25
    for k, (label, fn) in enumerate(gambar):
        cb = chip_box if k == 0 else copy_shape(chip_box, s)
        ct = chip_txt if k == 0 else copy_shape(chip_txt, s)
        cw = 0.35 + 0.062 * len(label)
        move(cb, x=LEFT, y=y, w=cw)
        move(ct, x=LEFT, y=y, w=cw)
        set_text(ct, label)
        y += 0.28
        path = os.path.join(ASSET, fn)
        iw, ih = Image.open(path).size
        h = MAXW * ih / iw
        pic = s.shapes.add_picture(path, Inches(LEFT), Inches(y), Inches(MAXW), Inches(h))
        pic.line.color.rgb = RGBColor(0xD6, 0xE4, 0xE7)
        pic.line.width = Pt(0.75)
        y += h + 0.14
    boxes = [("Rounded Rectangle 22", "TextBox 23"), ("Rounded Rectangle 24", "TextBox 25"),
             ("Rounded Rectangle 26", "TextBox 27")]
    BX, BW, BH, BY, BG = 9.12, 3.55, 1.52, 1.80, 0.17
    for k, ((bn, tn), (head_txt, body)) in enumerate(zip(boxes, info)):
        by = BY + k * (BH + BG)
        move(find(s, bn), x=BX, y=by, w=BW, h=BH)
        move(find(s, tn), x=BX + 0.14, y=by + 0.08, w=BW - 0.28, h=BH - 0.16)
        set_text(find(s, tn), [head_txt, body])

# ------------------------------------------------------------------ buang halaman rujukan
sld = prs.slides._sldIdLst
for el in list(sld)[:N_REF]:
    prs.part.drop_rel(el.get(qn("r:id")))
    sld.remove(el)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("tersimpan:", OUT)
