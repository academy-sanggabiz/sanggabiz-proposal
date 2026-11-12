"""Membuat gambar lembar kerja Excel untuk slide contoh alat bantu.

Pemakaian: python3 pest-control/_build/render_gambar.py
Butuh LibreOffice (soffice) dan pdftoppm. Locale id_ID dipakai agar angka memakai titik ribuan.
"""
import os
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
ASSET = ROOT / "_build" / "assets"
BERKAS = {
    "Alat Bantu Customer Retention - Pest Control.xlsx": "retensi-lembar",
    "Alat Bantu Sales Leadership - Pest Control.xlsx": "sales-lembar",
}

env = dict(os.environ, LANG="id_ID.UTF-8", LC_ALL="id_ID.UTF-8")
with tempfile.TemporaryDirectory() as tmp:
    for nama, awalan in BERKAS.items():
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp,
                        str(ROOT / "alat-bantu" / nama)], check=True, env=env, capture_output=True)
        pdf = Path(tmp) / nama.replace(".xlsx", ".pdf")
        subprocess.run(["pdftoppm", "-r", "220", "-png", str(pdf), str(Path(tmp) / awalan)], check=True)
        for png in sorted(Path(tmp).glob(awalan + "-*.png")):
            im = Image.open(png).convert("RGB")
            kotak = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
            pad = 20
            im = im.crop((max(0, kotak[0] - pad), max(0, kotak[1] - pad),
                          min(im.width, kotak[2] + pad), min(im.height, kotak[3] + pad)))
            im.save(ASSET / png.name)
            print("ditulis:", ASSET / png.name, im.size)
