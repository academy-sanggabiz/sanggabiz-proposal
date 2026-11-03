"""Proposal v3 (PDF): sama dengan v2, tetapi halaman contoh aset memakai Kartu Saku Isyarat v4.

Kartu v4 berisi 20 gambar contoh dari pengguna (3 November 2026), berlabel "contoh" dan belum diperiksa pengguna Tuli.
Halaman 6 menjelaskan bahwa kartu peserta memakai foto dari co-trainer Tuli.
v2 tetap disimpan. Skrip v2 tidak diubah: halaman 1 sampai 5 diambil dari build_v2.susun().

Pemakaian (dari folder _build):
  python3 -I potong_foto_contoh.py && python3 build_kartu_v4.py
  python3 build_v3.py && node render.js jobs_v3.json && python3 build_v3.py --gabung
  python3 build_pptx_v3.py
"""
import json
import subprocess
import sys
from gaya import BUILD, ROOT
from build_proposal import halaman
from build_kartu import sisi_depan, sisi_belakang
from build_kartu_v4 import FOTO_CONTOH, KETERANGAN, TAG, html_sisi
from build_v2 import CSS2, susun as susun_v2
from silabus_v2 import KARTU

HTML = BUILD / "html"
HAL = BUILD / "halaman-v3"
SLIDE = ROOT / "proposal" / "aset-slide"
NAMA_PDF = "v3 Silabus dan Contoh Aset - IHT Layanan Inklusif PT BPR NBP 27.pdf"
GAMBAR = {s: SLIDE / f"v4-kartu-isyarat-{s}.png" for s in ("depan", "belakang")}
KARTU_V3 = dict(KARTU, foto=("Gambar isyarat di kartu contoh ini masih ilustrasi. Pada kartu yang dibagikan ke peserta, "
                             "foto isyarat diperagakan dan diperiksa co-trainer Tuli dari Bandung, sesuai isyarat nasabah setempat."))


def halaman_kartu():
    d, b = GAMBAR["depan"].as_uri(), GAMBAR["belakang"].as_uri()
    return halaman("CONTOH ASET PELATIHAN: KARTU SAKU ISYARAT PERBANKAN",
        "Salah satu yang dibawa pulang peserta. Disiapkan Sanggabiz untuk meja teller dan CS PT BPR NBP 27.",
        f'<div class="mock"><span class="lbl" style="left:80px">Sisi depan: 20 isyarat loket</span><img class="d" src="{d}">'
        f'<span class="lbl" style="right:80px">Sisi belakang: kartu tunjuk</span><img class="b" src="{b}"></div>'
        f'<div class="desk3"><div><b>Apa ini</b>{KARTU_V3["apa"]}</div><div><b>Isyarat setempat</b>{KARTU_V3["foto"]}</div>'
        f'<div><b>Dipakai di</b>{KARTU_V3["dipakai"]}</div></div>')


def main():
    HAL.mkdir(exist_ok=True)
    if "--gabung" in sys.argv:
        files = sorted(HAL.glob("hal-*.pdf"))
        out = ROOT / "proposal" / NAMA_PDF
        subprocess.run(["pdfunite", *map(str, files), str(out)], check=True)
        prev = ROOT / "preview" / "v3"
        prev.mkdir(parents=True, exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "72", "-png", str(out), str(prev / "hal")], check=True)
        print(out)
        return
    jobs = []
    # gambar kartu v4 untuk halaman 6, dirender lebih dulu
    for nama, isi in (("depan", sisi_depan(FOTO_CONTOH, KETERANGAN, TAG)), ("belakang", sisi_belakang())):
        h = HTML / f"kartu-v4-{nama}-slide.html"
        h.write_text(html_sisi(isi), encoding="utf8")
        jobs.append({"html": str(h), "png": str(GAMBAR[nama]), "width": 794, "height": 559, "scale": 3, "transparent": True})
    halaman_semua = susun_v2()[:5] + [halaman_kartu()]
    for i, h in enumerate(halaman_semua, 1):
        p = HTML / f"v3-hal-{i:02d}.html"
        p.write_text(f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Halaman {i}</title><style>{CSS2}</style></head><body>{h}</body></html>', encoding="utf8")
        jobs.append({"html": str(p), "pdf": str(HAL / f"hal-{i:02d}.pdf"), "width": 1280, "height": 720, "scale": 1})
    (BUILD / "jobs_v3.json").write_text(json.dumps(jobs, indent=1))
    print(len(halaman_semua), "halaman v3")


if __name__ == "__main__":
    main()
