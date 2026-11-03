"""Proposal v4: silabus, contoh aset (kartu v4), dan rincian anggaran dalam satu dokumen. PDF dan Excel.

Halaman 1 sampai 6 sama dengan v3. Halaman 7 rincian anggaran dari anggaran.py.
v1 sampai v3 tetap disimpan. Skrip v3 tidak diubah.
Pemakaian (dari folder _build, setelah build_v3.py pernah dijalankan untuk gambar kartu):
  python3 build_v4.py && node render.js jobs_v4.json && python3 build_v4.py --gabung
  python3 build_pptx_v4.py
"""
import json
import subprocess
import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from gaya import BUILD, ROOT, TEAL, TEAL_MUDA
from build_proposal import halaman
from build_v2 import CSS2, susun as susun_v2
from build_v3 import halaman_kartu
from anggaran import BARIS, TERMASUK, DARI_BPR, CATATAN_KLIEN, hitung, jumlah, rp, vol

HTML = BUILD / "html"
HAL = BUILD / "halaman-v4"
NAMA = "v4 Proposal Silabus, Contoh Aset, dan Anggaran - IHT Layanan Inklusif PT BPR NBP 27"
JUDUL_ANGGARAN = "RINCIAN ANGGARAN"
SUB_ANGGARAN = "Satu paket untuk 10 peserta sesuai TOR bagian VII. Harga sudah termasuk pajak."

CSS4 = CSS2 + f"""
.ang {{ display:grid; grid-template-columns: 1fr 330px; gap:22px; }}
table.agg {{ font-size:9.9px; line-height:1.2; }}
table.agg th {{ padding:5px 7px; font-size:10px; }}
table.agg td {{ padding:2.6px 7px !important; }}
table.agg tr.sub td, table.agg tr.total td {{ text-align:left; }}
table.agg tr.sub td.n, table.agg tr.total td.n {{ text-align:right; }}
table.agg td.n {{ text-align:right; white-space:nowrap; }}
table.agg tr.tahap td {{ background:{TEAL_MUDA} !important; font-family:'Montserrat'; font-weight:700; color:#13314f; font-size:9.8px; padding:2px 7px !important; }}
table.agg tr.sub td {{ background:#fff !important; font-weight:700; font-size:10.4px; padding:4px 7px !important; }}
table.agg tr.total td {{ background:#13314f !important; color:#fff; font-family:'Montserrat'; font-weight:800; font-size:11px; padding:5px 7px !important; }}
.panel {{ display:flex; flex-direction:column; gap:9px; }}
.panel .k {{ border-radius:12px; padding:9px 13px; font-size:10.6px; line-height:1.38; }}
.panel .k b.j {{ font-family:'Montserrat'; display:block; font-size:12px; margin-bottom:5px; color:#13314f; }}
.panel ul {{ margin:0; padding-left:15px; }}
.panel li {{ margin-bottom:2px; }}
.total-besar {{ background:linear-gradient(115deg,#13314F,#145b78 60%,{TEAL}); color:#fff; }}
.total-besar .a {{ font-family:'Montserrat'; font-weight:800; font-size:22px; margin:1px 0; }}
"""


def halaman_anggaran():
    d, fee, total = hitung()
    rows, no, tahap = "", 0, None
    for b in BARIS:
        if b[0] != tahap:
            tahap = b[0]
            rows += f'<tr class="tahap"><td colspan="5">{tahap}</td></tr>'
        no += 1
        rows += (f'<tr><td class="n">{no}</td><td>{b[1]}</td><td class="n">{vol(b[2])} {b[3]}</td>'
                 f'<td class="n">{rp(b[4])}</td><td class="n">{rp(jumlah(b))}</td></tr>')
    rows += f'<tr class="sub"><td></td><td colspan="3">Jumlah biaya langsung</td><td class="n">{rp(d)}</td></tr>'
    rows += f'<tr class="sub"><td></td><td colspan="3">Fee 10 persen</td><td class="n">{rp(fee)}</td></tr>'
    rows += f'<tr class="total"><td></td><td colspan="3">Total, sudah termasuk pajak</td><td class="n">{rp(total)}</td></tr>'
    tabel = ('<table class="agg"><thead><tr><th style="width:4%">No</th><th>Uraian</th><th style="width:15%">Volume</th>'
             '<th style="width:13%">Harga satuan (Rp)</th><th style="width:13%">Jumlah (Rp)</th></tr></thead>'
             f'<tbody>{rows}</tbody></table>')
    li = lambda xs: "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"
    panel = (f'<div class="panel"><div class="k total-besar">Total paket<div class="a">Rp {rp(total)}</div>'
             'Sudah termasuk pajak, di dalam pagu TOR Rp 10.000.000 sampai Rp 11.000.000.</div>'
             f'<div class="k" style="background:#F6FAFB;border:1px solid #DCE8EC"><b class="j">Sudah termasuk</b>{li(TERMASUK)}</div>'
             f'<div class="k" style="background:#fbf3fe;border:1px solid #E2A9F1"><b class="j">Disediakan PT BPR NBP 27</b>{li(DARI_BPR)}</div>'
             f'<div class="k" style="background:#fff;border:1px dashed #9fb3bf">{CATATAN_KLIEN}</div></div>')
    return halaman(JUDUL_ANGGARAN, SUB_ANGGARAN, f'<div class="ang"><div>{tabel}</div>{panel}</div>')


def excel():
    """Rincian anggaran dengan rumus, supaya mudah diubah tim."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Anggaran"
    teal = PatternFill("solid", fgColor="15908F")
    muda = PatternFill("solid", fgColor="D7ECEC")
    tipis = Border(*(Side(style="thin", color="B0BEC5"),) * 4)
    ws["A1"] = "Rincian Anggaran IHT Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Satu paket untuk 10 peserta. Harga sudah termasuk pajak. Pagu TOR Rp 10.000.000 sampai Rp 11.000.000."
    kepala = ["No", "Tahap", "Uraian", "Volume", "Satuan", "Harga satuan (Rp)", "Jumlah (Rp)", "Sumber harga"]
    for i, k in enumerate(kepala, 1):
        c = ws.cell(4, i, k)
        c.fill, c.font, c.border = teal, Font(bold=True, color="FFFFFF"), tipis
        c.alignment = Alignment(wrap_text=True, vertical="center")
    r = 5
    for no, b in enumerate(BARIS, 1):
        vals = [no, b[0], b[1], b[2], b[3], b[4], f"=ROUND(D{r}*F{r},0)", b[5]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(r, i, v)
            c.border = tipis
            if i in (6, 7):
                c.number_format = "#,##0"
            if i == 3:
                c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    akhir = r - 1
    ringkas = [("Jumlah biaya langsung", f"=SUM(G5:G{akhir})"), ("Fee 10 persen", f"=ROUND(G{r}*0.1,0)"),
               ("Total, sudah termasuk pajak", f"=G{r}+G{r + 1}"), ("Di dalam pagu TOR?", f'=IF(AND(G{r + 2}>=10000000,G{r + 2}<=11000000),"Ya","Tidak")')]
    for j, (label, f) in enumerate(ringkas):
        ws.cell(r + j, 3, label).font = Font(bold=True)
        c = ws.cell(r + j, 7, f)
        c.font, c.number_format = Font(bold=True), "#,##0"
        if j == 2:
            for col in range(1, 9):
                ws.cell(r + j, col).fill = muda
    for col, w in zip("ABCDEFGH", (5, 22, 62, 9, 12, 16, 16, 13)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    out = ROOT / "proposal" / f"{NAMA} - rincian anggaran.xlsx"
    wb.save(out)
    return out


def main():
    HAL.mkdir(exist_ok=True)
    if "--gabung" in sys.argv:
        files = sorted(HAL.glob("hal-*.pdf"))
        out = ROOT / "proposal" / f"{NAMA}.pdf"
        subprocess.run(["pdfunite", *map(str, files), str(out)], check=True)
        prev = ROOT / "preview" / "v4"
        prev.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "72", "-png", str(out), str(prev / "hal")], check=True)
        print(out)
        print(excel())
        return
    semua = susun_v2()[:5] + [halaman_kartu(), halaman_anggaran()]
    jobs = []
    for i, h in enumerate(semua, 1):
        p = HTML / f"v4-hal-{i:02d}.html"
        p.write_text(f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Halaman {i}</title><style>{CSS4}</style></head><body>{h}</body></html>', encoding="utf8")
        jobs.append({"html": str(p), "pdf": str(HAL / f"hal-{i:02d}.pdf"), "width": 1280, "height": 720, "scale": 1})
    (BUILD / "jobs_v4.json").write_text(json.dumps(jobs, indent=1))
    print(len(semua), "halaman v4")


if __name__ == "__main__":
    main()
