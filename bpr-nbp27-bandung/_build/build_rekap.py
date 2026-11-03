"""Membuat aset 11: Rekap Nilai dan Rubrik (Excel) dengan rumus otomatis.

Tim cukup mengetik jawaban peserta dan skor rubrik. Nilai, kenaikan, N-gain, status, dan grafik terhitung sendiri.
Isi awal adalah data contoh (sama dengan draf laporan aset 10) dan dihapus sebelum dipakai.
Pemakaian: python3 build_rekap.py
"""
import random
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from gaya import ROOT

KUNCI = ["B", "A", "C", "B", "A", "C", "B", "A", "C", "B", "Benar", "Salah", "Benar", "Salah", "Benar"]
PESERTA = [("Peserta 1", "Frontliner", 8, 13), ("Peserta 2", "Frontliner", 9, 14), ("Peserta 3", "Frontliner", 7, 12),
           ("Peserta 4", "Frontliner", 10, 14), ("Peserta 5", "Frontliner", 6, 11), ("Peserta 6", "Frontliner", 9, 13),
           ("Peserta 7", "Kasie Operasional", 11, 15), ("Peserta 8", "Kasie Operasional", 10, 14),
           ("Peserta 9", "Lainnya", 7, 12), ("Peserta 10", "Lainnya", 8, 13)]
TEAL = PatternFill("solid", fgColor="15908F")
MUDA = PatternFill("solid", fgColor="D7ECEC")
KUNING = PatternFill("solid", fgColor="FFF200")
PUTIH = Font(bold=True, color="FFFFFF")
TIPIS = Border(*(Side(style="thin", color="B0BEC5"),) * 4)
random.seed(27)


def kepala(ws, row, vals):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row, i, v)
        c.fill, c.font, c.border = TEAL, PUTIH, TIPIS
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")


def jawab(benar):
    idx = set(random.sample(range(15), benar))
    out = []
    for i, k in enumerate(KUNCI):
        if i in idx:
            out.append(k)
        elif k in ("Benar", "Salah"):
            out.append("Salah" if k == "Benar" else "Benar")
        else:
            out.append(random.choice([x for x in "ABC" if x != k]))
    return out


wb = Workbook()

# Lembar Petunjuk
ws = wb.active
ws.title = "Petunjuk"
teks = [
    ("Rekap Nilai dan Rubrik, IHT Layanan Inklusif PT BPR NBP 27", True),
    ("Isi awal adalah DATA CONTOH. Hapus isi sel kuning di lembar Jawaban dan Rubrik sebelum dipakai.", True),
    ("1. Lembar Jawaban: ketik jawaban tiap peserta (A, B, C, Benar, Salah) untuk pre-test dan post-test.", False),
    ("2. Lembar Nilai terisi otomatis: nilai 0 sampai 100, kenaikan, N-gain, dan status post-test 80 atau lebih.", False),
    ("3. Lembar Rubrik: ketik skor 1 sampai 3 per aspek dan skenario. Rata-rata di bawah 2,5 berwarna merah muda.", False),
    ("4. Lembar Grafik dipakai langsung di laporan evaluasi (aset 10).", False),
    ("N-gain = (post - pre) / (100 - pre). Dipakai untuk membandingkan kenaikan peserta yang nilai awalnya berbeda.", False),
]
for i, (t, b) in enumerate(teks, 1):
    ws.cell(i, 1, t).font = Font(bold=b, size=13 if i == 1 else 11)
ws["A2"].fill = KUNING
ws.column_dimensions["A"].width = 110

# Lembar Jawaban
wj = wb.create_sheet("Jawaban")
wj["A1"] = "Kunci jawaban"
wj["A1"].font = Font(bold=True)
for i, k in enumerate(KUNCI):
    c = wj.cell(1, 4 + i, k)
    c.fill, c.font = MUDA, Font(bold=True)
kepala(wj, 2, ["No", "Nama", "Tes"] + [f"S{i}" for i in range(1, 16)] + ["Benar", "Nilai"])
r = 3
for no, (nama, jab, pre, post) in enumerate(PESERTA, 1):
    for tes, nb in (("Pre", pre), ("Post", post)):
        wj.cell(r, 1, no)
        wj.cell(r, 2, nama)
        wj.cell(r, 3, tes)
        for i, v in enumerate(jawab(nb)):
            c = wj.cell(r, 4 + i, v)
            c.fill = KUNING
        wj.cell(r, 19, f"=SUMPRODUCT(--(D{r}:R{r}=$D$1:$R$1))")
        wj.cell(r, 20, f"=ROUND(S{r}*100/15,1)")
        for col in range(1, 21):
            wj.cell(r, col).border = TIPIS
        r += 1
wj.column_dimensions["B"].width = 14
for col in range(4, 19):
    wj.column_dimensions[L(col)].width = 7
wj.freeze_panes = "D3"

# Lembar Nilai
wn = wb.create_sheet("Nilai")
kepala(wn, 1, ["No", "Nama", "Jabatan", "Pre", "Post", "Naik", "N-gain", "Post 80 atau lebih"])
for i, (nama, jab, _, _) in enumerate(PESERTA):
    rr = i + 2
    pre_r, post_r = 3 + 2 * i, 4 + 2 * i
    vals = [i + 1, nama, jab, f"=Jawaban!T{pre_r}", f"=Jawaban!T{post_r}", f"=E{rr}-D{rr}",
            f'=IF(D{rr}=100,"",ROUND((E{rr}-D{rr})/(100-D{rr}),2))', f'=IF(E{rr}>=80,"Ya","Belum")']
    for c, v in enumerate(vals, 1):
        wn.cell(rr, c, v).border = TIPIS
n = len(PESERTA) + 1
s = n + 1
wn.cell(s, 2, "Rata-rata").font = Font(bold=True)
for col in "DEFG":
    wn[f"{col}{s}"] = f"=ROUND(AVERAGE({col}2:{col}{n}),1)"
    wn[f"{col}{s}"].font = Font(bold=True)
wn[f"H{s}"] = f'=COUNTIF(H2:H{n},"Ya")&" dari "&COUNTA(B2:B{n})'
wn[f"H{s}"].font = Font(bold=True)
for col, w in zip("ABCDEFGH", (5, 14, 20, 8, 8, 8, 9, 18)):
    wn.column_dimensions[col].width = w

# Lembar Rubrik
wr = wb.create_sheet("Rubrik")
aspek = ["Menyambut", "Bicara kepada nasabah", "Cara komunikasi", "Mobilitas", "Pembacaan dokumen", "Legalitas", "Kerahasiaan", "Penanganan keluhan"]
kepala(wr, 1, ["Aspek", "S1 Pintu masuk", "S2 Pembukaan rekening", "S3 Setoran teller", "S4 Cap jempol", "S5 Keluhan", "Rata-rata aspek"])
contoh = [[3, 3, 3, 2, 3], [3, 2, 3, 2, 3], [2, 3, 3, None, 2], [3, None, None, None, 3], [None, 2, 3, 3, None],
          [None, 3, 2, 3, None], [None, 3, 2, 3, 2], [None, None, None, None, 3]]
for i, (a, sk) in enumerate(zip(aspek, contoh), 2):
    wr.cell(i, 1, a).border = TIPIS
    for j, v in enumerate(sk, 2):
        c = wr.cell(i, j, v)
        c.fill, c.border = KUNING, TIPIS
    wr.cell(i, 7, f'=IFERROR(ROUND(AVERAGE(B{i}:F{i}),2),"")').border = TIPIS
last = len(aspek) + 1
wr.cell(last + 1, 1, "Rata-rata skenario").font = Font(bold=True)
for j in range(2, 8):
    col = L(j)
    wr.cell(last + 1, j, f'=IFERROR(ROUND(AVERAGE({col}2:{col}{last}),2),"")').font = Font(bold=True)
merah = PatternFill("solid", fgColor="F8C8D0")
wr.conditional_formatting.add(f"B{last+1}:G{last+1}", CellIsRule(operator="lessThan", formula=["2.5"], fill=merah))
wr.conditional_formatting.add(f"G2:G{last}", CellIsRule(operator="lessThan", formula=["2.5"], fill=merah))
wr.column_dimensions["A"].width = 22
for col in "BCDEFG":
    wr.column_dimensions[col].width = 15

# Lembar Grafik
wg = wb.create_sheet("Grafik")
ch = BarChart()
ch.type = "bar"
ch.title = "Nilai pre-test dan post-test per peserta (data contoh)"
ch.y_axis.title = "Nilai"
ch.y_axis.scaling.min, ch.y_axis.scaling.max = 0, 100
ch.add_data(Reference(wn, min_col=4, max_col=5, min_row=1, max_row=n), titles_from_data=True)
ch.set_categories(Reference(wn, min_col=2, min_row=2, max_row=n))
ch.height, ch.width = 11, 20
wg.add_chart(ch, "A1")

out = ROOT / "kit" / "11 Rekap Nilai dan Rubrik.xlsx"
wb.save(out)
print(out)
