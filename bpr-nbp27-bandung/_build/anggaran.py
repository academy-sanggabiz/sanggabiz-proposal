"""Anggaran IHT Layanan Inklusif PT BPR NBP 27. Satu sumber untuk PDF, PPTX, dan Excel.

Disusun dari proses bisnis program (ATURAN-PROPOSAL.md bagian 4a), harga dari STANDAR-HARGA.md, pagu dari TOR bagian VII
(Rp 10.000.000 sampai Rp 11.000.000 all-in, 10 peserta). Tempat dan konsumsi disediakan BPR, jadi tidak ada barisnya.
Tanda sumber: [R] [P] [E] [PP] seperti STANDAR-HARGA.md bagian 0. Alasan harga di luar rentang ada di 08-CATATAN-TIM.md.
"""

PAGU_BAWAH, PAGU_ATAS = 10_000_000, 11_000_000
FEE = 0.10

# (tahap, uraian, volume, satuan, harga satuan, tanda sumber)
BARIS = [
    ("Persiapan dan koordinasi", "Manajer proyek: koordinasi BPR, persiapan, dokumentasi, laporan", 0.075, "orang-bulan", 8_000_000, "[P][E]"),
    ("Modul dan kit", "Penyesuaian modul dan kit dengan SOP layanan PT BPR NBP 27", 1, "paket", 1_000_000, "[E]"),
    ("Modul dan kit", "Cetak kit peserta: modul ringkas, kartu saku isyarat laminasi, lembar praktik", 10, "set", 75_000, "[PP][E]"),
    ("Pelaksanaan", "Trainer utama, layanan perbankan inklusif", 6, "jam", 750_000, "[R][PP]"),
    ("Pelaksanaan", "Co-trainer Tuli, bahasa isyarat BISINDO", 1, "hari", 600_000, "[E]"),
    ("Pelaksanaan", "Peraga netra, pemanduan dan pembacaan slip", 1, "hari", 600_000, "[E]"),
    ("Pelaksanaan", "Sewa kursi roda untuk praktik", 1, "unit", 150_000, "[E]"),
    ("Pelaksanaan", "Penutup mata untuk praktik pemanduan", 10, "buah", 10_000, "[E]"),
    ("Pelaksanaan", "Papan tulis genggam dan spidol", 5, "set", 25_000, "[E]"),
    ("Pelaksanaan", "Bantalan tinta untuk simulasi cap jempol", 3, "buah", 15_000, "[E]"),
    ("Pelaksanaan", "Lakban warna penanda rute praktik", 2, "gulung", 15_000, "[E]"),
    ("Pelaksanaan", "Transport tim ke lokasi pelatihan", 4, "orang", 100_000, "[E]"),
    ("Evaluasi dan laporan", "Pre-test, post-test, lembar pengamatan praktik, dan survei kepuasan", 1, "paket", 350_000, "[E]"),
    ("Evaluasi dan laporan", "Laporan evaluasi: rekap nilai, foto, rekomendasi perbaikan fasilitas", 1, "paket", 600_000, "[E]"),
    ("Evaluasi dan laporan", "Sertifikat perorangan, cetak dan elektronik", 10, "lembar", 7_500, "[E]"),
]

TERMASUK = [
    "Honor trainer utama, co-trainer Tuli, dan peraga netra",
    "Penyesuaian materi dengan SOP layanan BPR",
    "Kit cetak untuk 10 peserta, termasuk kartu saku isyarat",
    "Perlengkapan praktik: kursi roda, penutup mata, papan tulis, bantalan tinta",
    "Transport tim ke lokasi",
    "Pre-test, post-test, sertifikat, dan laporan evaluasi",
]
DARI_BPR = [
    "Ruang rapat ber-AC, proyektor, dan sound system",
    "Makan siang dan dua kali rehat kopi untuk peserta dan tim",
]
CATATAN_KLIEN = ("Tim pelaksana dipilih dari Bandung dan sekitarnya, jadi tidak ada biaya menginap. "
                 "Dokumentasi foto dikerjakan manajer proyek, jadi tidak ada biaya fotografer terpisah.")


def jumlah(b):
    return round(b[2] * b[4])


def hitung():
    d = sum(jumlah(b) for b in BARIS)
    fee = round(d * FEE)
    return d, fee, d + fee


def rp(x):
    return f"{x:,.0f}".replace(",", ".")


def vol(v):
    return f"{v:g}".replace(".", ",")


if __name__ == "__main__":
    d, fee, total = hitung()
    for b in BARIS:
        print(f"{b[0][:12]:12} {b[1][:60]:60} {vol(b[2]):>6} {b[3]:12} {rp(b[4]):>10} {rp(jumlah(b)):>11}")
    print("Biaya langsung", rp(d), "| Fee", rp(fee), "| Total", rp(total), "| dalam pagu:", PAGU_BAWAH <= total <= PAGU_ATAS)
    print("Bila PKP dan PPN termasuk: PPN", rp(round(total * 11 / 111)), "| biaya langsung bersih", rp(round(total / 1.11 / 1.1)))
