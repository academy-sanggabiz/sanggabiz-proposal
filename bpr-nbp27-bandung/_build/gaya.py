"""Gaya bersama untuk kit dan halaman proposal BPR NBP 27."""
from pathlib import Path

BUILD = Path(__file__).resolve().parent
ROOT = BUILD.parent
FONTS = BUILD / "fonts"
LOGO = (BUILD / "assets" / "logo_warna.png").as_uri()

TEAL = "#15908F"
TEAL_MUDA = "#D7ECEC"
CYAN = "#34BDCF"
BIRU = "#0071CE"
UNGU = "#E2A9F1"
ABU = "#F2F2F2"

FONT_FACE = "\n".join(
    f"@font-face{{font-family:'Montserrat';src:url('{(FONTS / f'Montserrat-{n}.ttf').as_uri()}');font-weight:{w}}}"
    for n, w in (("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800))
)

KIT_CSS = FONT_FACE + f"""
@page {{ size: A4; margin: 16mm 15mm 16mm 15mm; }}
* {{ box-sizing: border-box; }}
body {{ font-family: 'Inter', sans-serif; font-size: 9.6pt; color: #1d1d1d; line-height: 1.42; margin: 0; }}
.kop {{ display:flex; justify-content:space-between; align-items:center; border-bottom: 1.5px solid {TEAL}; padding-bottom: 6px; margin-bottom: 14px; }}
.kop img {{ height: 22px; }}
.kop .ket {{ font-size: 8pt; color:#555; text-align:right; }}
.label {{ display:inline-block; background:{TEAL_MUDA}; color:{TEAL}; font-weight:700; font-size:7.6pt; padding:2px 8px; border-radius:10px; letter-spacing:.3px; text-transform:uppercase; }}
h1 {{ font-family:'Montserrat'; font-weight:800; font-size:17pt; color:#13314f; margin:8px 0 4px; }}
.sub {{ color:#444; margin:0 0 12px; }}
h2 {{ font-family:'Montserrat'; font-weight:700; font-size:12pt; color:{TEAL}; margin:16px 0 6px; padding-bottom:3px; border-bottom:1.5px solid {TEAL_MUDA}; break-after: avoid; }}
h3 {{ font-family:'Montserrat'; font-weight:700; font-size:10pt; color:#13314f; margin:10px 0 4px; break-after: avoid; }}
p {{ margin: 0 0 6px; }}
table {{ width:100%; border-collapse:collapse; margin: 4px 0 10px; font-size: 8.8pt; break-inside: auto; }}
th {{ background:{TEAL}; color:#fff; text-align:left; font-weight:600; padding:5px 6px; }}
td {{ border:1px solid #cfd8dc; padding:4px 6px; vertical-align:top; }}
tr {{ break-inside: avoid; }}
tr:nth-child(even) td {{ background:#F2F8F9; }}
td.b {{ font-weight:600; }}
.kotak {{ border:1px solid #cfd8dc; border-left:4px solid {TEAL}; background:#f7fbfb; padding:7px 10px; margin:6px 0 10px; break-inside: avoid; }}
.isi {{ background:#FFF200; padding:0 3px; font-weight:600; }}
.rekaan {{ color:#9a3412; font-weight:600; font-size:8pt; }}
.cek {{ display:inline-block; width:10px; height:10px; border:1px solid #333; margin-right:4px; vertical-align:-1px; }}
.garis {{ border-bottom:1px solid #999; display:inline-block; min-width:160px; height:12px; }}
.foto {{ border:1.5px dashed #9bb; height:54px; display:flex; align-items:center; justify-content:center; color:#7a9; font-size:7.5pt; text-align:center; background:#fbfdfd; }}
.dua {{ display:grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
.kartu {{ border:1.5px solid {TEAL}; border-radius:8px; padding:9px 11px; break-inside: avoid; margin-bottom:10px; }}
.kartu .judul {{ font-family:'Montserrat'; font-weight:700; color:{TEAL}; font-size:10.5pt; margin-bottom:4px; }}
ol, ul {{ margin: 2px 0 8px 0; padding-left: 18px; }}
li {{ margin-bottom: 2px; }}
.kecil {{ font-size:8pt; color:#555; }}
.pecah {{ break-before: page; }}
"""


def kit_html(judul, sub, label, isi, kop_ket="IHT Layanan Inklusif bagi Nasabah Disabilitas, PT BPR NBP 27"):
    return f"""<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{judul}</title>
<style>{KIT_CSS}</style></head><body>
<div class="kop"><img src="{LOGO}"><div class="ket">{kop_ket}<br>Bandung, 2026</div></div>
<span class="label">{label}</span>
<h1>{judul}</h1><p class="sub">{sub}</p>
{isi}
</body></html>"""


def tabel(kepala, baris, lebar=None):
    col = ""
    if lebar:
        col = "<colgroup>" + "".join(f'<col style="width:{w}">' for w in lebar) + "</colgroup>"
    th = "".join(f"<th>{k}</th>" for k in kepala)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in b) + "</tr>" for b in baris)
    return f"<table>{col}<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>"
