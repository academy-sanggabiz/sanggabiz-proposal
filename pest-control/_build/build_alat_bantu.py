"""Membuat dua berkas alat bantu Excel untuk pelatihan pest control.

Pemakaian: python3 pest-control/_build/build_alat_bantu.py
Keluaran: pest-control/alat-bantu/*.xlsx

Semua data adalah data kasus latihan yang disusun Sanggabiz, bukan data klien.
Rumus ditulis sebagai rumus Excel hidup supaya peserta bisa mengganti data.
"""
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).resolve().parents[1] / "alat-bantu"
OUT.mkdir(exist_ok=True)

TEAL = "15908F"
NAVY = "13314F"
MUDA = "D7ECEC"
SELANG = "F2F8F9"
INPUT = "FFF7D6"
F = "Inter"

tipis = Side(style="thin", color="C9D6D9")
BORDER = Border(left=tipis, right=tipis, top=tipis, bottom=tipis)
RP = '"Rp" #,##0'
PCT = "0.0%"


def judul(ws, teks, sub):
    ws["A1"] = teks
    ws["A1"].font = Font(name=F, size=14, bold=True, color=NAVY)
    ws["A2"] = sub
    ws["A2"].font = Font(name=F, size=9, italic=True, color="555555")


def kepala(ws, row, labels, col=1):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        c.font = Font(name=F, size=9, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=TEAL)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = BORDER


def sel(ws, row, col, val, fmt=None, bold=False, fill=None, align="left", color="111111"):
    c = ws.cell(row=row, column=col, value=val)
    c.font = Font(name=F, size=9, bold=bold, color=color)
    c.border = BORDER
    c.alignment = Alignment(vertical="center", horizontal=align, wrap_text=True)
    if fmt:
        c.number_format = fmt
    if fill:
        c.fill = PatternFill("solid", fgColor=fill)
    return c


def lebar(ws, widths):
    for k, v in widths.items():
        ws.column_dimensions[k].width = v


def cetak(ws, area):
    ws.print_area = area
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_options.horizontalCentered = False
    ws.page_margins.left = ws.page_margins.right = 0.3
    ws.page_margins.top = ws.page_margins.bottom = 0.3


# ---------------------------------------------------------------------------
# 1. Alat bantu Customer Retention
# ---------------------------------------------------------------------------
def retensi():
    wb = Workbook()

    # Lembar Pelanggan: skor kesehatan dan prioritas
    ws = wb.active
    ws.title = "Pelanggan"
    judul(ws, "Skor Kesehatan Pelanggan dan Prioritas Kontak",
          "Data kasus latihan: 24 pelanggan kontrak cabang contoh. Sel kuning diisi peserta, sel lain dihitung otomatis.")
    ws["A3"] = "Tanggal acuan"
    ws["A3"].font = Font(name=F, size=9, bold=True)
    sel(ws, 3, 3, date(2026, 11, 25), "d mmm yyyy", fill=INPUT)
    kol = ["Kode", "Pelanggan", "Segmen", "Layanan", "Nilai kontrak per bulan",
           "Habis kontrak", "Sisa hari", "Keluhan 3 bulan", "Kunjungan terjadwal",
           "Kunjungan terlaksana", "Ketepatan kunjungan", "Telat bayar (hari)",
           "Skor kepuasan (1-5)", "Skor kesehatan", "Status", "Prioritas kontak"]
    kepala(ws, 5, kol)
    data = [
        ("PLG-01", "Restoran 01", "Komersial F&B", "Pest control umum", 2_500_000, date(2027, 1, 10), 1, 6, 6, 0, 5),
        ("PLG-02", "Hotel 02", "Komersial F&B", "Pest control dan rodent", 6_500_000, date(2027, 2, 28), 3, 12, 10, 21, 3),
        ("PLG-03", "Pabrik Roti 03", "Industri pangan", "Pest control dan rodent", 9_000_000, date(2026, 12, 31), 2, 12, 11, 0, 3),
        ("PLG-04", "Gudang 04", "Gudang dan logistik", "Rodent control", 3_000_000, date(2027, 6, 30), 0, 3, 3, 0, 4),
        ("PLG-05", "Kafe 05", "Komersial F&B", "Pest control umum", 1_500_000, date(2026, 12, 20), 4, 6, 5, 35, 2),
        ("PLG-06", "Rumah Tinggal 06", "Residensial", "Anti rayap (garansi)", 450_000, date(2027, 8, 15), 1, 1, 1, 0, 4),
        ("PLG-07", "Kantor 07", "Perkantoran", "Pest control umum", 2_000_000, date(2027, 3, 31), 0, 6, 6, 0, 5),
        ("PLG-08", "Klinik 08", "Kesehatan", "Pest control umum", 1_800_000, date(2027, 1, 31), 1, 6, 5, 10, 4),
        ("PLG-09", "Supermarket 09", "Ritel", "Pest control dan rodent", 5_500_000, date(2027, 1, 15), 3, 12, 9, 0, 3),
        ("PLG-10", "Sekolah 10", "Pendidikan", "Fogging dan pest control", 1_200_000, date(2027, 5, 31), 0, 3, 3, 0, 5),
        ("PLG-11", "Apartemen 11", "Residensial", "Pest control umum", 4_000_000, date(2026, 12, 15), 2, 6, 6, 18, 3),
        ("PLG-12", "Restoran 12", "Komersial F&B", "Pest control umum", 2_200_000, date(2027, 4, 30), 0, 6, 6, 0, 4),
        ("PLG-13", "Pabrik Minuman 13", "Industri pangan", "Pest control dan rodent", 8_000_000, date(2027, 9, 30), 1, 12, 12, 0, 4),
        ("PLG-14", "Gudang 14", "Gudang dan logistik", "Fumigasi dan rodent", 3_500_000, date(2027, 1, 5), 2, 3, 2, 0, 3),
        ("PLG-15", "Rumah Tinggal 15", "Residensial", "Pest control umum", 350_000, date(2026, 12, 10), 1, 3, 3, 40, 3),
        ("PLG-16", "Hotel 16", "Komersial F&B", "Pest control dan rodent", 7_000_000, date(2027, 7, 31), 0, 12, 12, 0, 5),
        ("PLG-17", "Kafe 17", "Komersial F&B", "Pest control umum", 1_300_000, date(2027, 2, 14), 2, 6, 4, 0, 3),
        ("PLG-18", "Kantor 18", "Perkantoran", "Pest control umum", 1_700_000, date(2027, 10, 31), 0, 6, 6, 0, 4),
        ("PLG-19", "Rumah Sakit 19", "Kesehatan", "Pest control dan rodent", 6_000_000, date(2027, 1, 20), 1, 12, 12, 7, 4),
        ("PLG-20", "Ruko 20", "Ritel", "Pest control umum", 900_000, date(2027, 3, 15), 1, 3, 3, 0, 4),
        ("PLG-21", "Pabrik Snack 21", "Industri pangan", "Pest control dan rodent", 7_500_000, date(2027, 2, 1), 2, 12, 12, 0, 4),
        ("PLG-22", "Rumah Tinggal 22", "Residensial", "Anti rayap (garansi)", 500_000, date(2028, 4, 30), 0, 1, 1, 0, 5),
        ("PLG-23", "Restoran 23", "Komersial F&B", "Pest control umum", 2_800_000, date(2026, 12, 28), 1, 6, 6, 0, 4),
        ("PLG-24", "Gudang 24", "Gudang dan logistik", "Rodent control", 2_600_000, date(2027, 4, 15), 0, 3, 3, 0, 4),
    ]
    r0 = 6
    for i, d in enumerate(data):
        r = r0 + i
        fill = SELANG if i % 2 else None
        for c, v in enumerate(d[:4], 1):
            sel(ws, r, c, v, fill=fill)
        sel(ws, r, 5, d[4], RP, fill=INPUT)
        sel(ws, r, 6, d[5], "d mmm yyyy", fill=INPUT, align="center")
        sel(ws, r, 7, f"=F{r}-$C$3", "0", fill=fill, align="center")
        sel(ws, r, 8, d[6], "0", fill=INPUT, align="center")
        sel(ws, r, 9, d[7], "0", fill=INPUT, align="center")
        sel(ws, r, 10, d[8], "0", fill=INPUT, align="center")
        sel(ws, r, 11, f"=IF(I{r}=0,1,J{r}/I{r})", "0%", fill=fill, align="center")
        sel(ws, r, 12, d[9], "0", fill=INPUT, align="center")
        sel(ws, r, 13, d[10], "0", fill=INPUT, align="center")
        # Skor 100 dikurangi: keluhan 15 per kasus (maks 45), kunjungan terlewat,
        # telat bayar, dan kepuasan rendah.
        sel(ws, r, 14,
            f"=MAX(0,ROUND(100-MIN(45,H{r}*15)-(1-K{r})*60"
            f"-IF(L{r}>30,15,IF(L{r}>14,8,0))-(5-M{r})*7,0))",
            "0", bold=True, fill=fill, align="center")
        sel(ws, r, 15, f'=IF(N{r}<50,"Merah",IF(N{r}<75,"Kuning","Hijau"))', bold=True, fill=fill, align="center")
        sel(ws, r, 16,
            f'=IF(AND(O{r}="Merah",G{r}<=90),"1. Minggu ini",'
            f'IF(OR(O{r}="Merah",AND(O{r}="Kuning",G{r}<=90)),"2. Bulan ini","3. Kontak rutin"))',
            fill=fill)
    rn = r0 + len(data) - 1
    merah = PatternFill("solid", fgColor="F8D7DA")
    kuning = PatternFill("solid", fgColor="FFF3CD")
    hijau = PatternFill("solid", fgColor="D4EDDA")
    rng = f"O{r0}:O{rn}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Merah"'], fill=merah))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Kuning"'], fill=kuning))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Hijau"'], fill=hijau))
    ws.conditional_formatting.add(f"P{r0}:P{rn}", FormulaRule(formula=[f'LEFT(P{r0},1)="1"'], fill=merah))

    rs = rn + 2
    ringkas = [
        ("Pelanggan berstatus merah", f'=COUNTIF(O{r0}:O{rn},"Merah")', "0"),
        ("Pelanggan berstatus kuning", f'=COUNTIF(O{r0}:O{rn},"Kuning")', "0"),
        ("Nilai kontrak per tahun pelanggan merah", f'=SUMIF(O{r0}:O{rn},"Merah",E{r0}:E{rn})*12', RP),
        ("Kontrak habis dalam 60 hari", f'=COUNTIF(G{r0}:G{rn},"<=60")', "0"),
        ("Harus dihubungi minggu ini", f'=COUNTIF(P{r0}:P{rn},"1*")', "0"),
    ]
    for i, (lbl, f, fmt) in enumerate(ringkas):
        sel(ws, rs + i, 1, lbl, bold=True, fill=MUDA)
        ws.merge_cells(start_row=rs + i, start_column=1, end_row=rs + i, end_column=3)
        sel(ws, rs + i, 4, f, fmt, bold=True, align="right")
    rk = rs + len(ringkas) + 1
    ws.cell(row=rk, column=1, value=(
        "Cara membaca skor: mulai dari 100, dikurangi 15 per keluhan (paling banyak 45), dikurangi kunjungan yang tidak "
        "terlaksana, telat bayar (lebih dari 14 hari 8 poin, lebih dari 30 hari 15 poin), dan kepuasan di bawah 5 "
        "(7 poin per angka). Di bawah 50 merah, 50 sampai 74 kuning. Bobot ini contoh untuk latihan dan bisa diubah tim.")
    ).font = Font(name=F, size=8, italic=True, color="555555")
    lebar(ws, {"A": 8, "B": 17, "C": 17, "D": 21, "E": 14, "F": 12, "G": 7, "H": 8, "I": 9,
               "J": 10, "K": 10, "L": 8, "M": 9, "N": 10, "O": 8, "P": 14})
    ws.row_dimensions[5].height = 38
    ws.freeze_panes = "C6"
    cetak(ws, f"A1:P{rs + len(ringkas) - 1}")

    # Lembar Retensi: angka retensi dan nilai pelanggan
    ws = wb.create_sheet("Retensi")
    judul(ws, "Kalkulator Retensi dan Nilai Pelanggan",
          "Angka satu tahun cabang contoh. Ganti sel kuning dengan data perusahaan sendiri.")
    kepala(ws, 4, ["Masukan", "Nilai", "Keterangan"])
    masukan = [
        ("Pelanggan aktif awal tahun", 220, "0", "Jumlah kontrak aktif pada 1 Januari"),
        ("Pelanggan baru selama tahun ini", 64, "0", "Kontrak baru dari tim sales"),
        ("Pelanggan aktif akhir tahun", 236, "0", "Jumlah kontrak aktif pada 31 Desember"),
        ("Pendapatan berulang per bulan di awal tahun", 520_000_000, RP, "Total nilai kontrak per bulan dari pelanggan lama"),
        ("Pendapatan hilang dari pelanggan berhenti", 78_000_000, RP, "Nilai per bulan kontrak yang tidak diperpanjang"),
        ("Pendapatan turun karena kontrak dikurangi", 15_000_000, RP, "Frekuensi atau area layanan dikurangi"),
        ("Pendapatan tambahan dari pelanggan lama", 36_000_000, RP, "Tambah layanan, misalnya rodent atau anti rayap"),
        ("Rata-rata nilai kontrak per bulan", 2_400_000, RP, "Per pelanggan"),
        ("Margin kotor layanan", 0.35, "0%", "Setelah bahan, tenaga teknisi, dan transport"),
    ]
    for i, (a, b, fmt, c) in enumerate(masukan):
        r = 5 + i
        sel(ws, r, 1, a, bold=True)
        sel(ws, r, 2, b, fmt, fill=INPUT, align="right")
        sel(ws, r, 3, c, color="555555")
    kepala(ws, 15, ["Hasil", "Nilai", "Rumus"])
    hasil = [
        ("Customer retention rate", "=(B7-B6)/B5", PCT, "(pelanggan akhir - pelanggan baru) / pelanggan awal"),
        ("Churn rate per tahun", "=1-B16", PCT, "1 - retention rate"),
        ("Churn rate per bulan (perkiraan)", "=1-(1-B17)^(1/12)", "0.00%", "Churn tahunan diubah ke bulanan"),
        ("Revenue churn", "=(B9+B10)/B8", PCT, "(pendapatan hilang + turun) / pendapatan awal"),
        ("Net revenue retention", "=(B8-B9-B10+B11)/B8", PCT, "Di atas 100% berarti pelanggan lama tumbuh"),
        ("Rata-rata lama berlangganan (bulan)", "=1/B18", "0", "1 / churn bulanan"),
        ("Nilai seumur pelanggan (CLV)", "=B12*B13*B21", RP, "Nilai kontrak x margin x lama berlangganan"),
        ("Pelanggan yang perlu dipertahankan tambahan untuk retensi 90%", "=MAX(0,ROUNDUP(0.9*B5-(B7-B6),0))", "0",
         "Selisih ke target retensi 90%"),
        ("Laba kotor per tahun dari tambahan itu", "=B23*B12*B13*12", RP, "Nilai yang dipertaruhkan setiap tahun"),
    ]
    for i, (a, f, fmt, c) in enumerate(hasil):
        r = 16 + i
        sel(ws, r, 1, a, bold=True, fill=MUDA)
        sel(ws, r, 2, f, fmt, bold=True, align="right")
        sel(ws, r, 3, c, color="555555")
    lebar(ws, {"A": 46, "B": 18, "C": 52})
    cetak(ws, "A1:C24")

    # Lembar Log Keluhan
    ws = wb.create_sheet("Log Keluhan")
    judul(ws, "Log Keluhan dan Service Recovery",
          "Contoh 10 keluhan satu bulan. Batas respons dan batas selesai adalah contoh, sesuaikan dengan SLA perusahaan.")
    ws["A3"] = "Batas respons (menit)"
    ws["A3"].font = Font(name=F, size=9, bold=True)
    sel(ws, 3, 4, 60, "0", fill=INPUT, align="center")
    ws["F3"] = "Batas selesai (hari)"
    ws["F3"].font = Font(name=F, size=9, bold=True)
    sel(ws, 3, 8, 2, "0", fill=INPUT, align="center")
    kol = ["No", "Tanggal", "Kode", "Kategori", "Saluran", "Menit sampai direspons",
           "Respons tepat waktu", "Hari sampai selesai", "Selesai tepat waktu",
           "Akar penyebab", "Tindakan pencegahan", "Status"]
    kepala(ws, 5, kol)
    log = [
        (date(2026, 11, 2), "PLG-05", "Hama muncul lagi", "WhatsApp", 45, 1, "Sisa makanan di dapur malam hari", "Jadwal sanitasi bersama pelanggan", "Selesai"),
        (date(2026, 11, 3), "PLG-02", "Jadwal teknisi", "Telepon", 120, 2, "Teknisi pengganti tidak tahu lokasi", "Catatan lokasi di aplikasi jadwal", "Selesai"),
        (date(2026, 11, 6), "PLG-11", "Bau atau noda", "Email", 30, 1, "Bahan semprot dipakai saat penghuni ada", "Pemberitahuan H-1 ke penghuni", "Selesai"),
        (date(2026, 11, 9), "PLG-05", "Hama muncul lagi", "WhatsApp", 90, 3, "Celah saluran air belum ditutup", "Rekomendasi perbaikan fisik tertulis", "Selesai"),
        (date(2026, 11, 10), "PLG-15", "Tagihan", "Telepon", 50, 4, "Faktur dikirim ke alamat lama", "Perbarui data PIC tagihan", "Selesai"),
        (date(2026, 11, 13), "PLG-09", "Hama muncul lagi", "Email", 40, 2, "Tikus masuk dari area bongkar muat", "Tambah stasiun umpan di luar gedung", "Selesai"),
        (date(2026, 11, 16), "PLG-17", "Sikap petugas", "WhatsApp", 75, 1, "Teknisi tidak melapor ke PIC", "Lapor masuk dan keluar ke PIC", "Selesai"),
        (date(2026, 11, 18), "PLG-03", "Hama muncul lagi", "Telepon", 20, 3, "Lalat dari tempat sampah terbuka", "Temuan dicatat di laporan audit", "Proses"),
        (date(2026, 11, 20), "PLG-14", "Jadwal teknisi", "Email", 150, 2, "Jadwal bentrok dengan fumigasi", "Kalender bersama tim operasional", "Proses"),
        (date(2026, 11, 21), "PLG-05", "Hama muncul lagi", "WhatsApp", 35, 1, "Belum diketahui", "Kunjungan ulang dan inspeksi", "Proses"),
    ]
    for i, d in enumerate(log):
        r = 6 + i
        fill = SELANG if i % 2 else None
        sel(ws, r, 1, i + 1, fill=fill, align="center")
        sel(ws, r, 2, d[0], "d mmm", fill=fill, align="center")
        sel(ws, r, 3, d[1], fill=fill, align="center")
        sel(ws, r, 4, d[2], fill=fill)
        sel(ws, r, 5, d[3], fill=fill)
        sel(ws, r, 6, d[4], "0", fill=INPUT, align="center")
        sel(ws, r, 7, f'=IF(F{r}<=$D$3,"Ya","Tidak")', fill=fill, align="center")
        sel(ws, r, 8, d[5], "0", fill=INPUT, align="center")
        sel(ws, r, 9, f'=IF(H{r}<=$H$3,"Ya","Tidak")', fill=fill, align="center")
        sel(ws, r, 10, d[6], fill=fill)
        sel(ws, r, 11, d[7], fill=fill)
        sel(ws, r, 12, d[8], fill=fill, align="center")
    ws.conditional_formatting.add("G6:G15", CellIsRule(operator="equal", formula=['"Tidak"'], fill=merah))
    ws.conditional_formatting.add("I6:I15", CellIsRule(operator="equal", formula=['"Tidak"'], fill=merah))
    kepala(ws, 17, ["Ringkasan", "", "", "Nilai"])
    ws.merge_cells("A17:C17")
    ring = [
        ("Keluhan tercatat", "=COUNTA(C6:C15)", "0"),
        ("Respons tepat waktu", '=COUNTIF(G6:G15,"Ya")/COUNTA(G6:G15)', "0%"),
        ("Selesai tepat waktu", '=COUNTIF(I6:I15,"Ya")/COUNTA(I6:I15)', "0%"),
        ("Kategori terbanyak: hama muncul lagi", '=COUNTIF(D6:D15,"Hama muncul lagi")', "0"),
        ("Keluhan berulang dari PLG-05", '=COUNTIF(C6:C15,"PLG-05")', "0"),
    ]
    for i, (a, f, fmt) in enumerate(ring):
        r = 18 + i
        sel(ws, r, 1, a, bold=True, fill=MUDA)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        sel(ws, r, 4, f, fmt, bold=True, align="right")
    dv = DataValidation(type="list", formula1='"Hama muncul lagi,Jadwal teknisi,Bau atau noda,Tagihan,Sikap petugas,Lainnya"')
    ws.add_data_validation(dv)
    dv.add("D6:D60")
    lebar(ws, {"A": 5, "B": 8, "C": 8, "D": 16, "E": 10, "F": 10, "G": 9, "H": 9, "I": 9,
               "J": 30, "K": 30, "L": 8})
    ws.row_dimensions[5].height = 38
    cetak(ws, "A1:L22")

    p = OUT / "Alat Bantu Customer Retention - Pest Control.xlsx"
    wb.save(p)
    return p


# ---------------------------------------------------------------------------
# 2. Alat bantu Sales Leadership
# ---------------------------------------------------------------------------
def sales():
    wb = Workbook()
    ws = wb.active
    ws.title = "Dasbor Tim"
    judul(ws, "Dasbor Kinerja Tim Sales dan Gaya Kepemimpinan",
          "Data kasus latihan: lima sales cabang contoh, kuartal berjalan minggu ke-8 dari 13. Sel kuning diisi Sales Leader.")
    kol = ["Sales", "Target kuartal", "Nilai kontrak tercapai", "Capaian", "Leads", "Survei lokasi",
           "Penawaran", "Kontrak baru", "Leads ke survei", "Survei ke penawaran", "Penawaran ke kontrak",
           "Pipeline terbuka", "Cakupan pipeline", "Titik macet", "Kompetensi (1-4)", "Komitmen (1-4)",
           "Gaya yang disarankan"]
    kepala(ws, 4, kol)
    tim = [
        ("Sales A", 300_000_000, 214_000_000, 60, 30, 24, 9, 260_000_000, 4, 4),
        ("Sales B", 250_000_000, 92_000_000, 72, 38, 12, 4, 120_000_000, 3, 2),
        ("Sales C", 250_000_000, 105_000_000, 48, 26, 22, 4, 310_000_000, 2, 2),
        ("Sales D", 150_000_000, 28_000_000, 25, 8, 6, 2, 60_000_000, 1, 4),
        ("Sales E", 250_000_000, 118_000_000, 30, 14, 11, 5, 90_000_000, 4, 2),
    ]
    r0 = 5
    for i, d in enumerate(tim):
        r = r0 + i
        fill = SELANG if i % 2 else None
        sel(ws, r, 1, d[0], bold=True, fill=fill)
        sel(ws, r, 2, d[1], RP, fill=INPUT, align="right")
        sel(ws, r, 3, d[2], RP, fill=INPUT, align="right")
        sel(ws, r, 4, f"=C{r}/B{r}", "0%", bold=True, fill=fill, align="center")
        for c, v in zip(range(5, 9), d[3:7]):
            sel(ws, r, c, v, "0", fill=INPUT, align="center")
        sel(ws, r, 9, f"=IFERROR(F{r}/E{r},0)", "0%", fill=fill, align="center")
        sel(ws, r, 10, f"=IFERROR(G{r}/F{r},0)", "0%", fill=fill, align="center")
        sel(ws, r, 11, f"=IFERROR(H{r}/G{r},0)", "0%", fill=fill, align="center")
        sel(ws, r, 12, d[7], RP, fill=INPUT, align="right")
        sel(ws, r, 13, f"=IFERROR(L{r}/MAX(1,B{r}-C{r}),0)", '0.0"x"', fill=fill, align="center")
        # Titik macet: tahap yang paling jauh di bawah rata-rata tim (di bawah 85 persen rata-rata).
        mn = f"MIN(I{r}/$I$11,J{r}/$J$11,K{r}/$K$11)"
        sel(ws, r, 14,
            f'=IF(E{r}<0.7*AVERAGE($E${r0}:$E${r0 + 4}),"Aktivitas leads rendah",'
            f'IF({mn}>=0.85,"Tidak ada yang menonjol",'
            f'IF(I{r}/$I$11={mn},"Leads ke survei",'
            f'IF(J{r}/$J$11={mn},"Survei ke penawaran","Penawaran ke kontrak"))))',
            fill=fill)
        sel(ws, r, 15, d[8], "0", fill=INPUT, align="center")
        sel(ws, r, 16, d[9], "0", fill=INPUT, align="center")
        sel(ws, r, 17,
            f'=IF(O{r}>=3,IF(P{r}>=3,"Delegating","Supporting"),IF(P{r}>=3,"Directing","Coaching"))',
            bold=True, fill=fill, align="center")
    rn = r0 + 4
    rt = 11
    sel(ws, rt - 1, 1, "")
    sel(ws, rt, 1, "Tim", bold=True, fill=MUDA)
    for c in "BCEFGHL":
        sel(ws, rt, " ABCDEFGHIJKLMNOPQ".index(c), f"=SUM({c}{r0}:{c}{rn})",
            RP if c in "BCL" else "0", bold=True, fill=MUDA, align="right" if c in "BCL" else "center")
    sel(ws, rt, 4, f"=C{rt}/B{rt}", "0%", bold=True, fill=MUDA, align="center")
    sel(ws, rt, 9, f"=F{rt}/E{rt}", "0%", bold=True, fill=MUDA, align="center")
    sel(ws, rt, 10, f"=G{rt}/F{rt}", "0%", bold=True, fill=MUDA, align="center")
    sel(ws, rt, 11, f"=H{rt}/G{rt}", "0%", bold=True, fill=MUDA, align="center")
    sel(ws, rt, 13, f"=L{rt}/MAX(1,B{rt}-C{rt})", '0.0"x"', bold=True, fill=MUDA, align="center")
    for c in (14, 15, 16, 17):
        sel(ws, rt, c, "", fill=MUDA)
    for c in range(1, 18):
        ws.cell(row=10, column=c).border = Border()
    ws.conditional_formatting.add(f"D{r0}:D{rn}", CellIsRule(operator="lessThan", formula=["0.5"],
                                                             fill=PatternFill("solid", fgColor="F8D7DA")))
    ws.conditional_formatting.add(f"M{r0}:M{rn}", CellIsRule(operator="lessThan", formula=["2"],
                                                             fill=PatternFill("solid", fgColor="FFF3CD")))
    ws["A13"] = ("Waktu kuartal berjalan 8 dari 13 minggu (62%). Cakupan pipeline = pipeline terbuka dibagi sisa target. "
                 "Gaya mengikuti Situational Leadership: kompetensi dan komitmen 1 sampai 4 dinilai Sales Leader.")
    ws["A13"].font = Font(name=F, size=8, italic=True, color="555555")
    ws["A14"] = ("Kompetensi 3-4 dan komitmen 3-4: Delegating. Kompetensi 3-4, komitmen 1-2: Supporting. "
                 "Kompetensi 1-2, komitmen 3-4: Directing. Keduanya 1-2: Coaching.")
    ws["A14"].font = Font(name=F, size=8, italic=True, color="555555")
    lebar(ws, {"A": 9, "B": 16, "C": 16, "D": 8, "E": 7, "F": 7, "G": 10, "H": 8, "I": 8, "J": 10,
               "K": 10, "L": 14, "M": 9, "N": 19, "O": 10, "P": 10, "Q": 12})
    ws.row_dimensions[4].height = 40
    cetak(ws, "A1:Q14")

    # Lembar Target ke Aktivitas
    ws = wb.create_sheet("Target ke Aktivitas")
    judul(ws, "Kalkulator Target ke Aktivitas",
          "Memecah target nilai kontrak menjadi aktivitas mingguan per sales. Sel kuning diisi Sales Leader.")
    kepala(ws, 4, ["Masukan", "Nilai", "Keterangan"])
    masukan = [
        ("Target nilai kontrak baru per bulan", 300_000_000, RP, "Untuk satu tim"),
        ("Rata-rata nilai satu kontrak baru", 12_000_000, RP, "Rata-rata residensial dan komersial"),
        ("Konversi leads ke survei lokasi", 0.50, "0%", "Dari dasbor tim, lembar Dasbor Tim kolom I"),
        ("Konversi survei ke penawaran", 0.65, "0%", "Lembar Dasbor Tim kolom J"),
        ("Konversi penawaran ke kontrak", 0.30, "0%", "Lembar Dasbor Tim kolom K"),
        ("Jumlah sales di tim", 5, "0", ""),
        ("Minggu kerja per bulan", 4, "0", ""),
    ]
    for i, (a, b, fmt, c) in enumerate(masukan):
        r = 5 + i
        sel(ws, r, 1, a, bold=True)
        sel(ws, r, 2, b, fmt, fill=INPUT, align="right")
        sel(ws, r, 3, c, color="555555")
    kepala(ws, 13, ["Kebutuhan per bulan", "Tim", "Per sales per minggu", "Bila konversi penawaran ke kontrak naik 5 poin"])
    langkah = [
        ("Kontrak baru", "=ROUNDUP(B5/B6,0)", "=B14/$B$10/$B$11", "=B14"),
        ("Penawaran", "=ROUNDUP(B14/B9,0)", "=B15/$B$10/$B$11", "=ROUNDUP(D14/(B9+0.05),0)"),
        ("Survei lokasi", "=ROUNDUP(B15/B8,0)", "=B16/$B$10/$B$11", "=ROUNDUP(D15/B8,0)"),
        ("Leads", "=ROUNDUP(B16/B7,0)", "=B17/$B$10/$B$11", "=ROUNDUP(D16/B7,0)"),
    ]
    for i, (a, t, w, s) in enumerate(langkah):
        r = 14 + i
        sel(ws, r, 1, a, bold=True, fill=MUDA)
        sel(ws, r, 2, t, "0", bold=True, align="center")
        sel(ws, r, 3, w, "0.0", align="center")
        sel(ws, r, 4, s, "0", align="center")
    sel(ws, 19, 1, "Leads yang tidak perlu dicari bila konversi naik", bold=True, fill=MUDA)
    sel(ws, 19, 2, "=B17-D17", "0", bold=True, align="center")
    ws.merge_cells("C19:D19")
    sel(ws, 19, 3, "Penawaran yang menonjolkan nilai layanan menaikkan konversi dan mengurangi leads yang harus dicari.", color="555555")
    lebar(ws, {"A": 44, "B": 18, "C": 22, "D": 30})
    ws.row_dimensions[13].height = 30
    cetak(ws, "A1:D19")

    # Lembar Rencana Coaching
    ws = wb.create_sheet("Rencana Coaching")
    judul(ws, "Rencana Coaching GROW dan Catatan 1-on-1",
          "Satu baris untuk satu anggota tim. Baris pertama contoh untuk Sales C dari data kasus.")
    kol = ["Sales", "Gaya", "Goal (sasaran 4 minggu)", "Reality (fakta dan data)",
           "Options (pilihan yang dibahas)", "Will (komitmen dan tanggal)", "Cek minggu 1", "Cek minggu 2",
           "Cek minggu 3", "Cek minggu 4"]
    kepala(ws, 4, kol)
    contoh = ["Sales C", "Coaching",
              "Konversi penawaran ke kontrak naik dari 18% ke 30%",
              "22 penawaran, 4 kontrak. Kalah harga di 3 dari 5 penawaran yang dicek",
              "Penawaran dua pilihan paket, presentasi hasil survei, ajak Sales Leader di penawaran besar",
              "Pakai format penawaran dua paket mulai Senin. Joint visit Kamis",
              "", "", "", ""]
    for c, v in enumerate(contoh, 1):
        sel(ws, 5, c, v, fill=SELANG)
    for r in range(6, 10):
        for c in range(1, 11):
            sel(ws, r, c, "", fill=INPUT if c > 2 else None)
    for c, s in zip("ABCDEFGHIJ", (9, 10, 24, 26, 30, 24, 10, 10, 10, 10)):
        ws.column_dimensions[c].width = s
    ws.row_dimensions[4].height = 30
    ws.row_dimensions[5].height = 48
    cetak(ws, "A1:J9")

    p = OUT / "Alat Bantu Sales Leadership - Pest Control.xlsx"
    wb.save(p)
    return p


if __name__ == "__main__":
    for p in (retensi(), sales()):
        print("ditulis:", p)
