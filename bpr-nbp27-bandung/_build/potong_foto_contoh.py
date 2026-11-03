"""Memotong 20 gambar isyarat dari gambar kartu yang dikirim pengguna (3 November 2026).

Sumber: ../sumber/Kartu isyarat dengan gambar dari pengguna - 3 November 2026.webp (1024 x 707 piksel).
Tulisan "FOTO ISYARAT" dan nomor yang menempel di gambar dihapus dengan inpainting, lalu gambar diperbesar 3 kali.
Hasil: foto-isyarat-contoh/NN-kata.jpg. Gambar ini contoh dan belum diperiksa pengguna Tuli.
Butuh: pip install opencv-python-headless
Pemakaian: python3 -I potong_foto_contoh.py
"""
import sys
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageFilter

BUILD = Path(__file__).resolve().parent
sys.path.insert(0, str(BUILD))
from build_kartu import KATA, slug  # noqa: E402

SUMBER = BUILD.parent / "sumber" / "Kartu isyarat dengan gambar dari pengguna - 3 November 2026.webp"
OUT = BUILD / "foto-isyarat-contoh"
KOLOM = [(39, 223), (235, 419), (432, 616), (627, 813), (824, 1009)]
BARIS = [143, 271, 399, 527]
TINGGI_FOTO = 78
KOTAK_NOMOR = (7, 9, 29, 23)    # x0, y0, x1, y1 relatif terhadap ubin, nomor 01 sampai 20
KOTAK_TAG = (100, 61, 178, 76)   # tulisan "FOTO ISYARAT"


def topeng_goresan(ubin, kotak, ambang=18):
    """Piksel di dalam kotak yang berbeda dari median sekitarnya: goresan huruf tipis, bukan tangan yang lebar."""
    x0, y0, x1, y1 = kotak
    median = cv2.medianBlur(ubin.astype(np.uint8), 11).astype(int)
    beda = np.abs(ubin - median).max(axis=2)
    m = np.zeros(ubin.shape[:2], bool)
    m[y0:y1, x0:x1] = beda[y0:y1, x0:x1] > ambang
    return m


def main():
    OUT.mkdir(exist_ok=True)
    im = np.asarray(Image.open(SUMBER).convert("RGB")).astype(int)
    for i, (kata, kat) in enumerate(KATA):
        x0, x1 = KOLOM[i % 5]
        y0 = BARIS[i // 5]
        ubin = im[y0:y0 + TINGGI_FOTO + 2, x0:x1].copy()
        topeng = topeng_goresan(ubin, KOTAK_TAG) | topeng_goresan(ubin, KOTAK_NOMOR, 14)
        # sudut atas yang putih di luar ubin bersudut bulat
        lum = ubin.mean(axis=2)
        for cx in (slice(0, 12), slice(ubin.shape[1] - 12, ubin.shape[1])):
            topeng[0:12, cx] |= lum[0:12, cx] > 249
        m = cv2.dilate(topeng.astype(np.uint8) * 255, np.ones((3, 3), np.uint8), iterations=2)
        bersih = cv2.inpaint(ubin.astype(np.uint8)[..., ::-1], m, 3, cv2.INPAINT_TELEA)[..., ::-1]
        foto = Image.fromarray(bersih[2:TINGGI_FOTO, 3:-3])
        foto = foto.resize((foto.width * 3, foto.height * 3), Image.LANCZOS)
        foto = foto.filter(ImageFilter.UnsharpMask(radius=1.4, percent=70, threshold=2))
        foto.save(OUT / f"{i + 1:02d}-{slug(kata)}.jpg", quality=92)
    print("20 foto contoh di", OUT)


if __name__ == "__main__":
    main()
