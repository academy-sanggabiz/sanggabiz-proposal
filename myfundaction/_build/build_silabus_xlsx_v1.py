"""Membuat silabus xlsx pelatihan AI Agent MyFundAction dari silabus_data.py."""
import os
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import silabus_data_v1 as d

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "silabus", "v1 Silabus Pelatihan AI Agent - MyFundAction.xlsx")

TEAL = "15908F"
TEAL_M = "D7ECEC"
ZEBRA = "F2F8F9"
GREY = "F2F2F2"
CYAN = "34BDCF"
FONT = "Arial"

thin = Side(style="thin", color="000000")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
WRAP_C = Alignment(wrap_text=True, vertical="center", horizontal="center")


def judul(ws, teks, sub=None, lebar=8):
    ws["A1"] = teks
    ws["A1"].font = Font(name=FONT, size=14, bold=True, color=TEAL)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name=FONT, size=10, italic=False, color="555555")
    ws.sheet_view.showGridLines = False


def kepala(ws, baris, kolom_list):
    for i, k in enumerate(kolom_list, 1):
        c = ws.cell(baris, i, k)
        c.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=TEAL)
        c.alignment = WRAP_C
        c.border = BORDER


def sel(ws, r, c, v, bold=False, fill=None, align=WRAP, color="000000", size=10):
    x = ws.cell(r, c, v)
    x.font = Font(name=FONT, size=size, bold=bold, color=color)
    x.alignment = align
    x.border = BORDER
    if fill:
        x.fill = PatternFill("solid", fgColor=fill)
    return x


def lebar(ws, daftar):
    for i, w in enumerate(daftar, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def bernomor(items):
    return "\n".join(f"{i}. {t}" for i, t in enumerate(items, 1))


def aktivitas_teks(akt):
    out, mulai = [], 0
    for n, (menit, langkah) in enumerate(akt, 1):
        out.append(f"{n}. Menit {mulai}-{mulai + menit}: {langkah}")
        mulai += menit
    return "\n".join(out)


def tinggi(teks_list, lebar_list):
    """Perkiraan tinggi baris dari panjang teks per kolom."""
    maks = 1
    for t, w in zip(teks_list, lebar_list):
        if not t:
            continue
        n = 0
        for b in str(t).split("\n"):
            n += max(1, int(len(b) / max(w * 1.05, 1)) + 1)
        maks = max(maks, n)
    return min(409, maks * 13 + 6)


wb = Workbook()

# ---------- Ringkasan ----------
ws = wb.active
ws.title = "Ringkasan"
judul(ws, f"{d.PROGRAM['judul']}: {d.PROGRAM['klien']}", f"Silabus {d.PROGRAM['versi']}. Disusun Sanggabiz dari notulen rapat 14 November 2026")
lebar(ws, [26, 70, 16, 16])
r = 4
for k, v in [
    ("Klien", f"{d.PROGRAM['klien']} ({d.PROGRAM['kontak']})"),
    ("Peserta", d.PROGRAM["peserta"]),
    ("Level", d.PROGRAM["level"]),
    ("Bahasa", d.PROGRAM["bahasa"]),
    ("Durasi inti", f"{d.total_menit_inti()} menit tatap muka untuk 7 modul, sama di kedua skema"),
    ("Skema A", d.SKEMA_A["ringkas"]),
    ("Skema B (rekomendasi)", d.SKEMA_B["ringkas"]),
]:
    sel(ws, r, 1, k, bold=True, fill=GREY)
    sel(ws, r, 2, v)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    ws.row_dimensions[r].height = tinggi([v], [100])
    r += 1

r += 1
ws.cell(r, 1, "Modul dan durasi").font = Font(name=FONT, size=12, bold=True, color=TEAL)
r += 1
kepala(ws, r, ["Modul", "Fokus", "Topik", "Menit"])
r += 1
for m in d.MODUL:
    sel(ws, r, 1, f"{m['kode']} {m['judul']}\n({m['judul_id']})", bold=True, fill=TEAL_M)
    sel(ws, r, 2, m["fokus"])
    sel(ws, r, 3, ", ".join(t["kode"] for t in m["topik"]), align=WRAP_C)
    sel(ws, r, 4, d.menit_modul(m), align=WRAP_C)
    ws.row_dimensions[r].height = tinggi([m["fokus"], m["judul"] + m["judul_id"]], [68, 24])
    r += 1
sel(ws, r, 1, "Total", bold=True, fill=GREY)
sel(ws, r, 2, "")
sel(ws, r, 3, "")
sel(ws, r, 4, f"=SUM(D{r - len(d.MODUL)}:D{r - 1})", bold=True, align=WRAP_C)
r += 2

ws.cell(r, 1, "Metode").font = Font(name=FONT, size=12, bold=True, color=TEAL)
r += 1
kepala(ws, r, ["Metode", "Dipakai di"])
r += 1
for a, b in d.METODE:
    sel(ws, r, 1, a, bold=True, fill=GREY)
    sel(ws, r, 2, b)
    ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
    ws.row_dimensions[r].height = tinggi([b], [100])
    r += 1
r += 1
ws.cell(r, 1, "Catatan: Hermes Agent merilis versi baru hampir tiap minggu. Perintah di silabus dan panduan dicocokkan dengan dokumentasi resmi sehari sebelum pelatihan.").font = Font(name=FONT, size=9, color="555555")

# ---------- Silabus ----------
ws = wb.create_sheet("Silabus")
judul(ws, "Silabus per modul dan topik", "Aktivitas ditulis dengan menit di dalam topik. Menit topik sama di Skema A dan Skema B")
kol = ["Modul dan fokus", "Kode", "Topik", "Menit", "Tujuan pembelajaran (Bloom)", "Outline materi", "Aktivitas (menit, siapa, bahan)", "Alat dan media", "Output", "Ukuran keberhasilan", "Format"]
lb = [26, 6, 22, 7, 34, 44, 60, 30, 30, 32, 14]
lebar(ws, lb)
kepala(ws, 4, kol)
ws.freeze_panes = "C5"
r = 5
for m in d.MODUL:
    awal = r
    for i, t in enumerate(m["topik"]):
        fill = ZEBRA if i % 2 else None
        isi = [
            None, t["kode"], t["judul"], t["menit"], t["tujuan"], bernomor(t["outline"]),
            aktivitas_teks(t["aktivitas"]), t["alat"], t["output"], t["ukuran"], t["format"],
        ]
        for c, v in enumerate(isi, 1):
            if c == 1:
                continue
            al = WRAP_C if c in (2, 4) else WRAP
            sel(ws, r, c, v, bold=(c == 3), fill=fill, align=al, color=(TEAL if c == 11 else "000000"))
        ws.row_dimensions[r].height = tinggi(isi[1:], lb[1:])
        r += 1
    teks_m = f"{m['kode']} {m['judul']}\n{m['judul_id']}\n\nFokus: {m['fokus']}\n\nPrasyarat: {m['prasyarat']}"
    ws.merge_cells(start_row=awal, start_column=1, end_row=r - 1, end_column=1)
    sel(ws, awal, 1, teks_m, bold=False, fill=TEAL_M)
    ws.cell(awal, 1).font = Font(name=FONT, size=10, bold=True, color="0E6E6D")
    for rr in range(awal + 1, r):
        ws.cell(rr, 1).border = BORDER
        ws.cell(rr, 1).fill = PatternFill("solid", fgColor=TEAL_M)

# ---------- Rundown Skema A ----------
ws = wb.create_sheet("Rundown Skema A")
judul(ws, d.SKEMA_A["nama"], d.SKEMA_A["ringkas"])
lebar(ws, [10, 10, 9, 40, 60])
kepala(ws, 4, ["Mulai", "Selesai", "Menit", "Kegiatan", "Keterangan"])
r = 5
for a, b, k, ket in d.SKEMA_A["rundown"]:
    jeda = k in ("Rehat", "Ishoma")
    fill = GREY if jeda else None
    sel(ws, r, 1, a, align=WRAP_C, fill=fill)
    sel(ws, r, 2, b, align=WRAP_C, fill=fill)
    sel(ws, r, 3, f'=(VALUE(SUBSTITUTE(B{r},".",":"))-VALUE(SUBSTITUTE(A{r},".",":")))*1440', align=WRAP_C, fill=fill)
    sel(ws, r, 4, k, bold=k.startswith("M"), fill=fill)
    sel(ws, r, 5, ket, fill=fill)
    r += 1
sel(ws, r, 4, "Total menit di ruang (termasuk rehat)", bold=True, fill=GREY)
sel(ws, r, 3, f"=SUM(C5:C{r - 1})", bold=True, align=WRAP_C, fill=GREY)

# ---------- Rundown Skema B ----------
ws = wb.create_sheet("Rundown Skema B")
judul(ws, d.SKEMA_B["nama"] + " (rekomendasi)", d.SKEMA_B["ringkas"])
lebar(ws, [30, 10, 10, 9, 38, 56])
kepala(ws, 4, ["Sesi", "Mulai", "Selesai", "Menit", "Kegiatan", "Keterangan"])
r = 5
for s in d.SKEMA_B["sesi"]:
    awal = r
    for a, b, k, ket in s["rundown"]:
        sel(ws, r, 2, a, align=WRAP_C)
        sel(ws, r, 3, b, align=WRAP_C)
        sel(ws, r, 4, f'=(VALUE(SUBSTITUTE(C{r},".",":"))-VALUE(SUBSTITUTE(B{r},".",":")))*1440', align=WRAP_C)
        sel(ws, r, 5, k, bold=k.startswith("M"))
        sel(ws, r, 6, ket)
        ws.row_dimensions[r].height = tinggi([ket, k], [56, 38])
        r += 1
    ws.merge_cells(start_row=awal, start_column=1, end_row=r - 1, end_column=1)
    sel(ws, awal, 1, s["nama"], bold=True, fill=TEAL_M)
    for rr in range(awal + 1, r):
        ws.cell(rr, 1).border = BORDER
r += 1
ws.cell(r, 1, "Di antara sesi").font = Font(name=FONT, size=10, bold=True)
ws.cell(r, 2, d.SKEMA_B["antara"]).font = Font(name=FONT, size=10)

# ---------- Hasil dibawa pulang ----------
ws = wb.create_sheet("Hasil dibawa pulang")
judul(ws, "Hasil yang dibawa pulang", "Setiap output dihasilkan di topik yang disebut")
lebar(ws, [6, 70, 12])
kepala(ws, 4, ["No", "Output", "Topik"])
for i, (o, t) in enumerate(d.HASIL, 1):
    sel(ws, 4 + i, 1, i, align=WRAP_C)
    sel(ws, 4 + i, 2, o)
    sel(ws, 4 + i, 3, t, align=WRAP_C)

# ---------- Evaluasi ----------
ws = wb.create_sheet("Evaluasi")
judul(ws, "Evaluasi (Kirkpatrick) dan rubrik prompt")
lebar(ws, [22, 30, 30, 30, 30, 30])
kepala(ws, 4, ["Level", "Alat ukur", "Target"])
r = 5
for a, b, c in d.EVALUASI:
    sel(ws, r, 1, a, bold=True, fill=GREY)
    sel(ws, r, 2, b)
    sel(ws, r, 3, c)
    ws.row_dimensions[r].height = tinggi([b, c], [30, 30])
    r += 1
r += 1
ws.cell(r, 1, "Rubrik 6 unsur prompt (skor 0 sampai 12)").font = Font(name=FONT, size=12, bold=True, color=TEAL)
r += 1
kepala(ws, r, ["Unsur (English)", "Arti", "Skor 0", "Skor 1", "Skor 2"])
r += 1
for u, en, arti, s0, s1, s2 in d.RUBRIK:
    sel(ws, r, 1, f"{u} ({en})", bold=True, fill=GREY)
    for c, v in enumerate([arti, s0, s1, s2], 2):
        sel(ws, r, c, v)
    ws.row_dimensions[r].height = tinggi([arti, s0, s1, s2], [30] * 4)
    r += 1

# ---------- Persiapan teknis ----------
ws = wb.create_sheet("Persiapan teknis")
judul(ws, "Persiapan teknis sebelum pelatihan", "H = hari pelaksanaan. Untuk Skema B, H adalah sesi 1, kecuali butir Hermes yang mengacu ke sesi 3")
lebar(ws, [8, 60, 30, 30])
kepala(ws, 4, ["Kapan", "Kegiatan", "Penanggung jawab", "Bahan"])
for i, row in enumerate(d.PERSIAPAN, 5):
    for c, v in enumerate(row, 1):
        sel(ws, i, c, v, align=WRAP_C if c == 1 else WRAP)

# ---------- Alur program ----------
ws = wb.create_sheet("Alur program")
judul(ws, "Alur program (proses bisnis)", "Anggaran nanti mengikuti tahap ini (ATURAN-PROPOSAL bagian 4a)")
lebar(ws, [6, 34, 70, 36])
kepala(ws, 4, ["No", "Tahap", "Kegiatan", "Hasil"])
for i, (n, t, k, h) in enumerate(d.ALUR, 5):
    sel(ws, i, 1, n, align=WRAP_C)
    sel(ws, i, 2, t, bold=True)
    sel(ws, i, 3, k)
    sel(ws, i, 4, h)
    ws.row_dimensions[i].height = tinggi([k, h], [70, 36])

for w in wb.worksheets:
    w.page_setup.orientation = "landscape"
    w.page_setup.fitToWidth = 1
    w.sheet_properties.pageSetUpPr.fitToPage = True
    w.page_setup.fitToHeight = 0

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("tersimpan:", os.path.normpath(OUT))
