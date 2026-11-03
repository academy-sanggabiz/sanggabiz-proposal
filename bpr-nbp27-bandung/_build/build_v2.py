"""Proposal v2 (PDF): silabus berbahasa sehari-hari dan satu contoh aset, kartu saku isyarat.

Mengikuti ATURAN-PROPOSAL.md bagian 9. v1 tetap disimpan sebagai arsip.
Pemakaian (dari folder _build):
  python3 build_kartu.py && node render.js jobs_kartu.json
  python3 build_v2.py && node render.js jobs_v2.json && python3 build_v2.py --gabung
"""
import json
import subprocess
import sys
from gaya import BUILD, ROOT, TEAL, TEAL_MUDA, CYAN
from build_proposal import CSS, halaman, dokumen
from build_kartu import ikon
from silabus_v2 import PEMBUKA, SOROTAN, RUNDOWN, MODUL, DIDAPAT, KARTU

HTML = BUILD / "html"
HAL = BUILD / "halaman-v2"
HAL.mkdir(exist_ok=True)
SLIDE = ROOT / "proposal" / "aset-slide"
NAMA_PDF = "v2 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pdf"

CSS2 = CSS + f"""
.lead {{ text-align:center; font-size:13px; color:#333; max-width:900px; margin:-6px auto 10px; line-height:1.5; }}
.sorot {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:14px; }}
.sorot > div {{ background:linear-gradient(135deg,#f2fafb,#e6f4f5); border-radius:12px; padding:9px 16px; display:flex; gap:14px; align-items:center; }}
.sorot .a {{ flex:none; width:122px; font-size:21px !important; }}
.sorot .a {{ font-family:'Montserrat'; font-weight:800; font-size:24px; color:{TEAL}; line-height:1; white-space:nowrap; }}
.sorot .a span {{ display:block; font-size:11px; font-weight:700; color:#13314f; letter-spacing:.4px; text-transform:uppercase; margin-top:3px; }}
.sorot p {{ margin:0; font-size:11.5px; line-height:1.4; color:#24394a; }}
tr.rehat td {{ background:#fafafa !important; color:#777; font-style:italic; }}
td.mod2 {{ background:{TEAL_MUDA} !important; width:16%; }}
td.mod2 .n {{ font-family:'Montserrat'; font-weight:700; color:{TEAL}; font-size:12px; }}
td.mod2 .j {{ font-family:'Montserrat'; font-weight:700; font-size:13px; color:#13314f; margin:3px 0 5px; line-height:1.25; }}
td.mod2 .w {{ font-size:11px; color:#355; }}
table.v2 {{ font-size:12.3px; line-height:1.45; }}
table.v2.rapat {{ font-size:11px; line-height:1.3; }}
table.v2.rapat td {{ padding:4px 9px !important; }}
table.v2 td {{ padding:7px 9px; }}
table.v2 ul {{ margin:0; padding-left:15px; }}
table.v2 li {{ margin-bottom:2px; }}
.am b {{ color:{TEAL}; font-weight:700; }}
.tiga {{ display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }}
.kartu-d {{ border-radius:14px; border:1.5px solid #d6e4e7; overflow:hidden; background:#fff; }}
.kartu-d .h {{ background:linear-gradient(115deg,#13314F,#145b78 60%,{TEAL}); color:#fff; padding:15px 18px; font-family:'Montserrat'; font-weight:700; font-size:16.5px; display:flex; gap:10px; align-items:center; }}
.kartu-d .h i {{ width:30px; height:30px; border-radius:50%; background:rgba(255,255,255,.18); display:flex; align-items:center; justify-content:center; }}
.kartu-d ul {{ list-style:none; margin:0; padding:10px 16px 12px; }}
.kartu-d li {{ display:flex; gap:10px; font-size:14px; line-height:1.45; padding:12px 0; border-bottom:1px dashed #e1eaec; }}
.kartu-d li:last-child {{ border-bottom:0; }}
.kartu-d li .titik {{ flex:none; width:9px; height:9px; border-radius:50%; background:{TEAL}; margin-top:6px; }}
.pandu {{ margin-top:20px; background:#fbf3fe; border:1px solid #E2A9F1; border-radius:12px; padding:16px 20px; font-size:14px; line-height:1.45; display:flex; gap:12px; align-items:center; }}
.mock {{ position:relative; height:338px; margin:6px 0 6px; }}
.mock img {{ position:absolute; width:458px; border-radius:16px; box-shadow:0 10px 28px rgba(19,49,79,.22), 0 2px 6px rgba(19,49,79,.12); }}
.mock .d {{ left:60px; top:14px; transform:rotate(-2.2deg); }}
.mock .b {{ right:60px; top:20px; transform:rotate(2deg); }}
.mock .lbl {{ position:absolute; top:-2px; font-family:'Montserrat'; font-weight:700; font-size:11px; color:#fff; background:{CYAN}; padding:3px 12px; border-radius:20px; z-index:2; }}
.desk3 {{ display:grid; grid-template-columns:1.25fr 1fr 0.9fr; gap:16px; font-size:12.2px; line-height:1.45; }}
.desk3 div {{ background:#f6fafb; border-radius:10px; padding:9px 13px; }}
.desk3 b {{ color:{TEAL}; font-family:'Montserrat'; display:block; margin-bottom:2px; }}
"""


def ul(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def susun():
    hal = []
    sor = "".join(f'<div><div class="a">{a}<span>{b}</span></div><p>{c}</p></div>' for a, b, c in SOROTAN)
    rows = ""
    for j, k, t in RUNDOWN:
        cls = ' class="rehat"' if not t else ""
        rows += f"<tr{cls}><td style='white-space:nowrap;width:12%'>{j}</td><td style='width:38%'><b>{k}</b></td><td>{t}</td></tr>"
    hal.append(halaman("SILABUS PELATIHAN: SATU HARI PENUH PRAKTIK",
        "In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27, Bandung. 10 peserta, 08.30 - 16.30 WIB.",
        f'<p class="lead">{PEMBUKA}</p><div class="sorot">{sor}</div>'
        f'<table class="v2 rapat"><thead><tr><th>Waktu (WIB)</th><th>Kegiatan</th><th>Yang terjadi</th></tr></thead><tbody>{rows}</tbody></table>'))

    def baris(m):
        return (f'<tr><td class="mod2"><div class="n">{m["no"]}</div><div class="j">{m["judul"]}</div><div class="w">{m["jam"]} WIB</div></td>'
                f'<td style="width:22%">{ul(m["dipelajari"])}</td><td style="width:32%">{ul(m["kegiatan"])}</td>'
                f'<td class="am" style="width:15%"><b>Alat:</b> {m["alat"]}<br><b>Media:</b> {m["media"]}</td><td style="width:15%">{m["hasil"]}</td></tr>')

    for a, b in ((0, 2), (2, 4), (4, 6)):
        hal.append(halaman(f"SILABUS PELATIHAN: MODUL {a+1} DAN {b}",
            "Apa yang dipelajari, apa yang dilakukan peserta, dan apa hasilnya.",
            '<table class="v2"><thead><tr><th>Modul</th><th>Yang dipelajari</th><th>Kegiatan peserta</th><th>Alat dan media</th><th>Hasil</th></tr></thead><tbody>'
            + "".join(baris(m) for m in MODUL[a:b]) + "</tbody></table>"))

    ik = ["orang", "rekening", "saldo"]
    kol = ""
    for (j, xs), i in zip(DIDAPAT, ik):
        li = "".join(f'<li><span class="titik"></span><span>{x}</span></li>' for x in xs)
        kol += f'<div class="kartu-d"><div class="h"><i>{ikon(i, "#fff", 17, 2)}</i>{j}</div><ul>{li}</ul></div>'
    hal.append(halaman("YANG DIDAPAT PT BPR NBP 27",
        "Hasil yang bisa langsung dipakai di loket, dan bukti yang bisa ditunjukkan saat pemeriksaan OJK.",
        f'<div class="tiga">{kol}</div><div class="pandu">{ikon("orang", TEAL, 26, 1.8)}<span><b>Dipandu langsung oleh penyandang disabilitas.</b> '
        'Trainer utama berpengalaman di layanan perbankan, didampingi co-trainer Tuli untuk bahasa isyarat dan peraga netra untuk pemanduan '
        'dan pembacaan slip. Peserta belajar dari orang yang setiap hari menjadi nasabah.</span></div>'))

    d = (SLIDE / "v2-kartu-isyarat-depan.png").as_uri()
    b = (SLIDE / "v2-kartu-isyarat-belakang.png").as_uri()
    hal.append(halaman("CONTOH ASET PELATIHAN: KARTU SAKU ISYARAT PERBANKAN",
        "Salah satu yang dibawa pulang peserta. Disiapkan Sanggabiz untuk meja teller dan CS PT BPR NBP 27.",
        f'<div class="mock"><span class="lbl" style="left:80px">Sisi depan: 20 isyarat loket</span><img class="d" src="{d}">'
        f'<span class="lbl" style="right:80px">Sisi belakang: kartu tunjuk</span><img class="b" src="{b}"></div>'
        f'<div class="desk3"><div><b>Apa ini</b>{KARTU["apa"]}</div><div><b>Isyarat setempat</b>{KARTU["foto"]}</div><div><b>Dipakai di</b>{KARTU["dipakai"]}</div></div>'))
    return hal


def main():
    if "--gabung" in sys.argv:
        files = sorted(HAL.glob("hal-*.pdf"))
        out = ROOT / "proposal" / NAMA_PDF
        subprocess.run(["pdfunite", *map(str, files), str(out)], check=True)
        prev = ROOT / "preview" / "v2"
        prev.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "72", "-png", str(out), str(prev / "hal")], check=True)
        print(out)
        return
    jobs = []
    for i, h in enumerate(susun(), 1):
        p = HTML / f"v2-hal-{i:02d}.html"
        p.write_text(f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Halaman {i}</title><style>{CSS2}</style></head><body>{h}</body></html>', encoding="utf8")
        jobs.append({"html": str(p), "pdf": str(HAL / f"hal-{i:02d}.pdf"), "width": 1280, "height": 720, "scale": 1})
    (BUILD / "jobs_v2.json").write_text(json.dumps(jobs, indent=1))
    print(len(jobs), "halaman v2")


if __name__ == "__main__":
    main()
