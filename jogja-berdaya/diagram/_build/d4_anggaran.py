import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

OUT = os.path.join(os.path.dirname(__file__), "..", "04-anggaran-mengikuti-proses.svg")
s = SVG(1200)
header(s, "Anggaran: ke mana uangnya pergi dan apa yang perlu diubah",
       "Baris anggaran di dokumen sumber dikelompokkan ulang menurut tahap kerja program, supaya tiap rupiah bisa ditelusuri ke satu pekerjaan. Angka asli tidak diubah.")

stages = [
    ("1. Diagnosis kebutuhan dan pemetaan", 5.0, 45, "#0E8A8A"),
    ("3. Kurikulum, rubrik, alat asesmen", 3.5, 24, "#2F6EA5"),
    ("4. Pelatihan (pelatih, bahan, konsumsi)", 20.0, 204, "#12304F"),
    ("5. Pendampingan dan penghubung kerja", 7.0, 102, "#E0A100"),
    ("6. Monev dan pelacakan 90 hari", 4.5, 30, "#7A5BA6"),
    ("7. Showcase dan laporan", 1.9, 21, "#5B6B7A"),
    ("2. Rekrutmen dan manajemen program (lintas tahap)", 6.0, 69, "#6FB7A8"),
    ("Contingency (baris cadangan)", 1.0, 0, "#B83227"),
]
tp = sum(a for _, a, _, _ in stages)
tf = sum(b for _, _, b, _ in stages)
assert abs(tp - 48.9) < 1e-9 and tf == 495, (tp, tf)

def pct(v, t): return f"{v / t * 100:.1f}".replace(".", ",")
def rp(v): return f"{v:.1f}".replace(".", ",")

y = section(s, 140, 1, "Pembagian biaya menurut tahap kerja")
for label, idx, total, unit in [("Pilot, Rp48,9 juta", 1, tp, "juta"), ("Program penuh, Rp495 juta", 2, tf, "juta")]:
    s.text(50, y, label, 15, NAVY, True)
    y += 24
    x = 50
    for st in stages:
        v = st[idx]
        if not v:
            continue
        w = 1100 * v / total
        s.rect(x, y, w, 36, st[3], "#fff", rx=0, sw=1)
        if w > 44:
            s.text(x + w / 2, y + 10, f"{pct(v, total)}%", 12.5, "#fff", True, "middle")
        x += w
    y += 56

# Tabel
s.rect(50, y, 1100, 32, NAVY, rx=6)
for t, hx in [("Tahap", 90), ("Pilot (Rp juta)", 600), ("Persen", 730), ("Penuh (Rp juta)", 830), ("Persen", 1000)]:
    s.text(hx, y + 8, t, 13.5, "#fff", True)
y += 32
for i, (n, a, b, c) in enumerate(stages):
    s.rect(50, y, 1100, 32, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    s.rect(62, y + 10, 14, 14, c, None, rx=3)
    s.text(90, y + 8, n, 13.5, INK, maxw=500)
    s.text(600, y + 8, rp(a), 13.5, INK)
    s.text(730, y + 8, pct(a, tp), 13.5, INK)
    s.text(830, y + 8, rp(b) if b else "tidak ada", 13.5, INK)
    s.text(1000, y + 8, pct(b, tf) if b else "-", 13.5, INK)
    y += 32
s.rect(50, y, 1100, 34, TEALBG, None, rx=0)
s.text(90, y + 9, "Total", 14, NAVY, True)
s.text(600, y + 9, rp(tp), 14, NAVY, True); s.text(730, y + 9, "100,0", 14, NAVY, True)
s.text(830, y + 9, rp(tf), 14, NAVY, True); s.text(1000, y + 9, "100,0", 14, NAVY, True)
y += 52

# Bacaan
y = section(s, y, 2, "Apa yang bisa dibaca dari pembagian ini (analisis kami)")
y += card(s, 50, y, 1100, "Pelatihan memakai sekitar 41 persen di kedua ukuran",
          "Pilot 40,9 persen dan program penuh 41,2 persen. Proporsinya sama di kedua ukuran, jadi susunan kelompok terbesar konsisten.",
          fill=GRAYBG, bar=NAVY) + 12
y += card(s, 50, y, 1100, "Pendampingan dan penghubung kerja lebih sedikit di pilot",
          "Pilot menyisihkan 14,3 persen untuk tahap ini, program penuh 20,6 persen. Padahal titik cek paling berat, G5 (minimal 4 dari 20 mendapat kerja atau tugas berbayar), bergantung pada tahap ini. Perlu dicek apakah Rp7,0 juta cukup untuk mendampingi 20 peserta dan 4 UMKM selama proyek dan pelacakan. Ini pertanyaan untuk tim, bukan temuan harga.",
          fill=YELBG, stroke=YEL, bar=YEL) + 12
y += card(s, 50, y, 1100, "Baris cadangan hanya ada di pilot",
          "Contingency Rp1,0 juta (2,0 persen) tidak sesuai aturan Sanggabiz. Aturannya satu baris Fee 10 persen dari biaya langsung dan tidak ada baris cadangan lain.",
          fill=REDBG, stroke=RED, bar=RED) + 38

# Fee
y = section(s, y, 3, "Bentuk yang sesuai aturan: biaya langsung ditambah Fee 10 persen (hitungan ilustrasi pilot)")
bars = [
    ("Sekarang", [(48.9, NAVY, "Seluruh baris termasuk Contingency 1,0: Rp48,9 juta")], "Tidak ada baris Fee."),
    ("Opsi A: total tetap", [(44.4545, NAVY, "Biaya langsung Rp44,45 juta"), (4.4455, GRN, "Fee 4,45")], "Total tetap Rp48,9 juta. Biaya langsung perlu dikurangi sekitar Rp4,45 juta."),
    ("Opsi B: biaya langsung tetap", [(48.9, NAVY, "Biaya langsung Rp48,9 juta"), (4.89, GRN, "Fee 4,89")], "Total naik menjadi Rp53,79 juta."),
]
sc = 800 / 53.79
for name, segs, note in bars:
    s.text(50, y + 9, name, 13.5, NAVY, True, maxw=170)
    x = 230
    for v, c, lab in segs:
        w = v * sc
        s.rect(x, y, w, 30, c, "#fff", rx=0)
        if w > 90:
            s.text(x + w / 2, y + 8, lab, 12, "#fff", True, "middle")
        else:
            s.text(x + w / 2, y + 8, lab.replace("Fee ", "Fee "), 11, "#fff", True, "middle") if w > 40 else None
        x += w
    y += 36
    s.text(230, y, note, 12.5, MUTED, maxw=900)
    y += 28
y += 4
y += s.text(50, y, "Untuk program penuh: bila Rp495 juta dipertahankan sebagai total, biaya langsung Rp450 juta dan Fee Rp45 juta. Bila biaya langsung Rp495 juta dipertahankan, total menjadi Rp544,5 juta. Tim memutuskan arahnya. Hitungan ini belum dicek ke rentang harga di STANDAR-HARGA.md dan belum memuat pajak (status PKP Sanggabiz belum diisi).", 12.5, MUTED, maxw=1100)
y += 30

# Pecah baris
y = section(s, y, 4, "Cara memecah baris gabungan (contoh bentuk, harga diisi tim)")
cols = [("Komponen", 50, 330), ("Volume", 380, 140), ("Satuan", 520, 140), ("Harga satuan", 660, 200), ("Jumlah", 860, 290)]
s.rect(50, y, 1100, 32, NAVY, rx=6)
for n, x, w in cols:
    s.text(x + 12, y + 8, n, 13.5, "#fff", True)
y += 32
ex = [("Cetak modul peserta", "20", "orang"), ("Kit pelatihan peserta", "20", "set"), ("Konsumsi peserta", "[ISI TIM]", "porsi"), ("Transport lokal pendamping", "[ISI TIM]", "kali")]
for i, (a, b, c) in enumerate(ex):
    s.rect(50, y, 1100, 32, GRAYBG if i % 2 == 0 else "#fff", None, rx=0)
    for (n, x, w), v in zip(cols, [a, b, c, "[ISI TIM]", "volume kali harga"]):
        mark = "[ISI TIM" in v
        if mark:
            s.rect(x + 8, y + 6, len(v) * 7.4 + 8, 20, YEL, None, rx=3)
        s.text(x + 12, y + 8, v, 13, INK)
    y += 32
y += 12
y += s.text(50, y, "Baris gabungan sekarang: \"Materi, transport, konsumsi, training kit\" Rp5.500.000. Setelah dipecah, jumlah seluruh barisnya harus tetap sama dengan angka yang disepakati, dan tiap harga satuan berada di rentang STANDAR-HARGA.md.", 12.5, MUTED, maxw=1100)
y += 24
s.text(50, y, "Sumber angka: proposal strategis (bagian 10) dan executive proposal pilot (bagian 08), 22 November 2026. Pengelompokan ke tahap adalah usulan kami.", 12.5, MUTED, maxw=1100)
y += 40
s.save(OUT, y, "Anggaran Jogja Berdaya menurut tahap kerja", "Pembagian biaya pilot dan program penuh per tahap kerja, hasil bacaan, dan bentuk anggaran dengan Fee 10 persen.")
print("ok", y)
