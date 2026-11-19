#!/usr/bin/env python3
"""Membuat workbook latihan AR dan Income Audit hotel (versi peserta dan versi kunci pengajar).
Semua data adalah rekaan untuk latihan. Jalankan: python3 build_workbook.py"""
import datetime as dt
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = Path(__file__).resolve().parent.parent / "assets"
NAVY, GOLD, INPUT = "0B396D", "FFC00C", "FFF8D6"
thin = Side(style="thin", color="C9D2DE")
BORD = Border(top=thin, bottom=thin, left=thin, right=thin)
RP = '#,##0;[Red]-#,##0'
D = dt.date

TARIF = {  # kode: (Standard, Deluxe, Suite), nett sebelum service dan pajak
    "RACK": (450000, 600000, 1000000), "CORP": (380000, 500000, 850000),
    "OTA": (420000, 560000, 900000), "COMP": (0, 0, 0), "HU": (0, 0, 0)}
TIPE = ["Standard", "Deluxe", "Suite"]
# kamar, tipe, kode tarif, tarif terposting, persetujuan
KAMAR = []
def add(rooms, tipe, codes, posted_over=None, appr=None):
    posted_over = posted_over or {}; appr = appr or {}
    for r, c in zip(rooms, codes):
        std = TARIF[c][TIPE.index(tipe)]
        KAMAR.append((r, tipe, c, posted_over.get(r, std), appr.get(r, "-")))
add(range(101, 115), "Standard",
    ["RACK","RACK","CORP","CORP","CORP","OTA","OTA","OTA","OTA","RACK","HU","RACK","CORP","OTA"],
    {105: 450000, 109: 380000}, {111: "Ya, GM"})
add(range(201, 213), "Deluxe",
    ["RACK","RACK","RACK","CORP","CORP","CORP","COMP","OTA","OTA","OTA","RACK","CORP"],
    {203: 560000}, {207: "Tidak ada"})
add(range(301, 305), "Suite", ["RACK","CORP","OTA","RACK"])

FNB = [  # outlet, penjualan POS, bayar langsung, transfer kamar (POS), transfer kamar (PMS)
    ("Restoran", 6850000, 4640000, 2210000, 2210000),
    ("Bar", 1870000, 1460000, 410000, 460000),
    ("Room Service", 2640000, 1100000, 1540000, 1440000)]
TENDER = [  # metode, PMS, bukti, nama bukti
    ("Tunai", 9250000, 9215000, "Setoran kasir (hitung fisik)"),
    ("Kartu debit dan kredit", 7800000, 7650000, "Batch settlement EDC"),
    ("QRIS", 2150000, 2150000, "Mutasi QRIS"),
    ("Transfer bank", 1600000, 1600000, "Mutasi rekening"),
    ("Transfer ke city ledger", 6045000, 5540000, "Daftar transfer CL berotorisasi")]

ASOF = D(2026, 12, 10)
PEL = [  # nama, jenis, term hari, limit
    ("PT Maju Bersama", "Korporasi", 30, 25000000),
    ("CV Cahaya Wisata", "Agen perjalanan", 14, 15000000),
    ("Dinas Pendidikan Kab. Contoh", "Instansi", 45, 40000000),
    ("PT Samudra Logistik", "Korporasi", 30, 20000000),
    ("OTA Sampel", "OTA", 30, 50000000),
    ("Yayasan Tunas", "Event", 14, 10000000)]
M, C_, DK, S_, O, Y = [p[0] for p in PEL]
INV = [  # no, pelanggan, tanggal, jumlah, dibayar
    ("INV-2608-0701", C_, D(2026,8,10), 3025000, 0),
    ("INV-2609-0901", M, D(2026,9,15), 8250000, 8250000),
    ("INV-2609-0902", C_, D(2026,9,18), 4620000, 0),
    ("INV-2609-0903", DK, D(2026,9,25), 12100000, 12100000),
    ("INV-2610-1001", M, D(2026,10,3), 6050000, 0),
    ("INV-2610-1002", S_, D(2026,10,7), 9680000, 4000000),
    ("INV-2610-1003", O, D(2026,10,10), 15400000, 15400000),
    ("INV-2610-1004", Y, D(2026,10,12), 3025000, 0),
    ("INV-2610-1005", C_, D(2026,10,20), 5445000, 0),
    ("INV-2610-1006", DK, D(2026,10,28), 18150000, 0),
    ("INV-2611-1101", M, D(2026,11,2), 7260000, 0),
    ("INV-2611-1102", S_, D(2026,11,5), 11495000, 0),
    ("INV-2611-1103", O, D(2026,11,9), 21780000, 0),
    ("INV-2611-1104", Y, D(2026,11,14), 2420000, 2420000),
    ("INV-2611-1105", C_, D(2026,11,20), 6655000, 0),
    ("INV-2611-1106", DK, D(2026,11,24), 9075000, 0),
    ("INV-2611-1107", M, D(2026,11,27), 3630000, 0),
    ("INV-2612-1201", S_, D(2026,12,1), 14520000, 0),
    ("INV-2612-1202", O, D(2026,12,4), 26620000, 0)]
BANK = [  # tanggal, uraian, jumlah, faktur (kunci), selisih (kunci), perlakuan (kunci)
    (D(2026,12,3), "PT MAJU BERSAMA INV 1001", 6050000, "INV-2610-1001", "Tidak ada", "Lunas. Aplikasikan ke INV-2610-1001."),
    (D(2026,12,4), "CAHAYA WISATA 0902", 4605000, "INV-2609-0902", "Kurang 15.000", "Potongan biaya transfer. Catat biaya bank 15.000, lunaskan faktur, atau tagih selisih sesuai kebijakan."),
    (D(2026,12,5), "SAMUDRA LOG", 12000000, "INV-2610-1002 dan sebagian INV-2611-1102", "Tanpa nomor faktur", "Konfirmasi ke pelanggan. Bila FIFO: lunasi INV-2610-1002 sisa 5.680.000, sisa 6.320.000 ke INV-2611-1102."),
    (D(2026,12,8), "DISDIK KAB CONTOH 1006", 18150000, "INV-2610-1006", "Tidak ada", "Lunas sebelum jatuh tempo. Aplikasikan."),
    (D(2026,12,9), "OTA SAMPEL SETTLEMENT NOV", 18513000, "INV-2611-1103", "Kurang 3.267.000", "Komisi OTA 15 persen dari 21.780.000. Dr Bank 18.513.000, Dr Komisi OTA 3.267.000, Cr City Ledger 21.780.000."),
    (D(2026,12,10), "TUNAS 1004", 3025000, "INV-2610-1004", "Tidak ada", "Lunas. Aplikasikan."),
    (D(2026,12,10), "TRF TANPA KETERANGAN", 1000000, "Belum teridentifikasi", "Tidak ada faktur", "Catat di akun dana belum teridentifikasi. Telusuri pengirim lewat bank dan front office.")]

def hdr(ws, row, heads, widths=None):
    for i, h in enumerate(heads, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = BORD
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[row].height = 32

def title(ws, text, sub=None):
    ws["A1"] = text; ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    if sub: ws["A2"] = sub; ws["A2"].font = Font(italic=True, color="5C5F66")

def put(ws, ref, val, fmt=None, key=True, kind="calc", bold=False):
    """kind=calc: isi hanya di versi kunci. kind=data: selalu diisi. kind=input: kosong kuning di peserta, isi di kunci."""
    c = ws[ref]
    if kind == "data" or key: c.value = val
    if kind == "input" or (kind == "calc" and not key):
        c.fill = PatternFill("solid", fgColor=INPUT)
    if fmt: c.number_format = fmt
    c.border = BORD; c.font = Font(bold=bold)
    return c

def build(key):
    wb = Workbook()
    # --- Petunjuk
    ws = wb.active; ws.title = "Petunjuk"
    title(ws, "Workbook Latihan AR dan Income Audit Hotel" + (" (KUNCI PENGAJAR)" if key else " (peserta)"),
          "Sanggabiz. Semua nama, angka, dan tanggal di berkas ini rekaan untuk latihan.")
    rows = [
        "Hotel Sampel: 50 kamar, hari kasus 10 Desember 2026.",
        "Sel berwarna kuning muda diisi peserta. Sel lain sudah berisi data soal." if not key else "Versi ini sudah berisi jawaban dan rumus. Jangan dibagikan ke peserta sebelum latihan selesai.",
        "Tarif kamar ditulis nett, sebelum service charge 10 persen dan pajak hotel 10 persen. Pajak dihitung dari tarif ditambah service. Besaran dan cara hitung di hotel Anda bisa berbeda. Ubah di sel parameter bila perlu.",
        "Kamar komplimen dan house use dipisahkan dari kamar terjual berbayar. Pakai kebijakan hotel Anda di tempat kerja.",
        "",
        "Lembar 1. IA-Tarif kamar: cek tarif terposting terhadap tarif seharusnya (Sesi 1, topik 1.3).",
        "Lembar 2. IA-Rekap: F&B ke kamar, penyelesaian per metode bayar, dan rasio kamar (Sesi 1, topik 1.3).",
        "Lembar 3. Invoice: templat dan contoh invoice (Sesi 2, topik 2.3 dan 2.4).",
        "Lembar 4. City Ledger: daftar faktur dan umur piutang (Sesi 3, topik 3.1).",
        "Lembar 5. Rekon Bank: mencocokkan mutasi bank dengan faktur (Sesi 3, topik 3.2).",
        "Lembar 6. Laporan AR: ringkasan piutang, DSO, dan limit kredit (Sesi 3, topik 3.3).",
    ]
    for i, t in enumerate(rows, 4): ws.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True)
    ws.column_dimensions["A"].width = 120

    # --- IA-Tarif
    ws = wb.create_sheet("IA-Tarif kamar")
    title(ws, "Pemeriksaan tarif kamar terposting, 10 Desember 2026", "Bandingkan tarif terposting di PMS dengan tarif seharusnya menurut kode tarif. Selisih positif berarti tamu ditagih lebih.")
    ws["A4"] = "Tabel tarif (nett)"; ws["A4"].font = Font(bold=True, color=NAVY)
    hdr(ws, 5, ["Kode tarif", "Standard", "Deluxe", "Suite"])
    for i, (k, v) in enumerate(TARIF.items(), 6):
        ws.cell(row=i, column=1, value=k).border = BORD
        for j, x in enumerate(v, 2):
            c = ws.cell(row=i, column=j, value=x); c.number_format = RP; c.border = BORD
    hdr(ws, 12, ["Kamar", "Tipe", "Kode tarif", "Tarif terposting PMS", "Tarif seharusnya", "Selisih", "Persetujuan tertulis", "Temuan (isi peserta)"],
        [12, 12, 12, 20, 18, 14, 20, 46])
    first = 13
    for n, (r, t, c, posted, appr) in enumerate(KAMAR):
        row = first + n
        put(ws, f"A{row}", r, kind="data"); put(ws, f"B{row}", t, kind="data"); put(ws, f"C{row}", c, kind="data")
        put(ws, f"D{row}", posted, RP, kind="data")
        put(ws, f"E{row}", f"=INDEX($B$6:$D$10,MATCH(C{row},$A$6:$A$10,0),MATCH(B{row},$B$5:$D$5,0))", RP, key)
        put(ws, f"F{row}", f"=D{row}-E{row}", RP, key)
        put(ws, f"G{row}", appr, kind="data")
        temuan = ""
        if r == 105: temuan = "Tamu korporasi ditagih tarif rack. Lebih tagih 70.000. Koreksi folio sebelum check-out."
        if r == 109: temuan = "Tarif OTA kurang 40.000 dari seharusnya. Selidiki alasan, kemungkinan diskon tanpa otorisasi."
        if r == 203: temuan = "Tarif rack diposting 560.000 padahal 600.000. Kurang 40.000, tidak ada persetujuan."
        if r == 207: temuan = "Kamar komplimen tanpa persetujuan tertulis. Minta bukti dari pimpinan."
        put(ws, f"H{row}", temuan, kind="input", key=key)
    last = first + len(KAMAR) - 1
    r0 = last + 2
    for i, (lab, f, fm) in enumerate([
        ("Jumlah kamar terisi", f"=COUNTA(A{first}:A{last})", "0"),
        ("Jumlah kamar komplimen dan house use", f'=COUNTIF(C{first}:C{last},"COMP")+COUNTIF(C{first}:C{last},"HU")', "0"),
        ("Kamar terjual berbayar", f"=B{r0}-B{r0+1}", "0"),
        ("Pendapatan kamar terposting (nett)", f"=SUM(D{first}:D{last})", RP),
        ("Pendapatan kamar seharusnya (nett)", f"=SUM(E{first}:E{last})", RP),
        ("Selisih bersih", f"=B{r0+3}-B{r0+4}", RP),
    ]):
        ws.cell(row=r0 + i, column=1, value=lab).font = Font(bold=True)
        put(ws, f"B{r0+i}", f, fm, key, kind="calc")
    ws.column_dimensions["A"].width = 38
    TAR = dict(first=first, last=last, r0=r0)

    # --- IA-Rekap
    ws = wb.create_sheet("IA-Rekap")
    title(ws, "Rekap income audit, 10 Desember 2026")
    ws["A3"] = "Parameter"; ws["A3"].font = Font(bold=True, color=NAVY)
    ws["A4"] = "Kamar tersedia"; ws["B4"] = 50; ws["A5"] = "Service charge"; ws["B5"] = 0.10; ws["A6"] = "Pajak hotel (dari tarif + service)"; ws["B6"] = 0.10
    ws["B5"].number_format = "0%"; ws["B6"].number_format = "0%"
    ws["A8"] = "A. F&B yang dipindahkan ke tagihan kamar"; ws["A8"].font = Font(bold=True, color=NAVY)
    hdr(ws, 9, ["Outlet", "Penjualan POS", "Dibayar langsung di outlet", "Dipindah ke kamar (POS)", "Dipindah ke kamar (PMS)", "Selisih PMS dikurangi POS", "Dugaan penyebab (isi peserta)"], [38, 18, 22, 22, 22, 22, 50])
    cause = {"Bar": "Posting ke kamar lebih besar 50.000 dari POS. Kemungkinan charge ganda atau salah nomor kamar. Cek struk dan folio.",
             "Room Service": "Posting kurang 100.000. Ada struk yang belum dipindah ke folio. Posting ulang dan cek apakah tamu sudah check-out."}
    for i, (o, a, b, c, d) in enumerate(FNB, 10):
        put(ws, f"A{i}", o, kind="data"); put(ws, f"B{i}", a, RP, kind="data"); put(ws, f"C{i}", b, RP, kind="data")
        put(ws, f"D{i}", c, RP, kind="data"); put(ws, f"E{i}", d, RP, kind="data")
        put(ws, f"F{i}", f"=E{i}-D{i}", RP, key); put(ws, f"G{i}", cause.get(o, "Cocok."), kind="input", key=key)
    ws["A13"] = "Jumlah"; ws["A13"].font = Font(bold=True)
    for col in "BCDEF": put(ws, f"{col}13", f"=SUM({col}10:{col}12)", RP, key, bold=True)
    ws["A15"] = "B. Penyelesaian per metode bayar"; ws["A15"].font = Font(bold=True, color=NAVY)
    hdr(ws, 16, ["Metode", "Menurut PMS", "Menurut bukti", "Selisih bukti dikurangi PMS", "Jenis bukti", "", "Dugaan penyebab dan tindak lanjut (isi peserta)"])
    tcause = {"Tunai": "Kurang kas 35.000. Minta kasir menjelaskan, cek void dan paid out. Bila tidak ada bukti, catat sebagai selisih kas sesuai kebijakan.",
              "Kartu debit dan kredit": "Batch EDC lebih rendah 150.000. Satu transaksi belum masuk batch atau batch ditutup sebelum transaksi terakhir. Cek slip EDC dan settlement besok.",
              "Transfer ke city ledger": "Transfer 505.000 tanpa otorisasi dan dokumen. Tahan sampai ada persetujuan dan pelanggan jelas. Jangan ditagihkan dulu."}
    for i, (m, a, b, n) in enumerate(TENDER, 17):
        put(ws, f"A{i}", m, kind="data"); put(ws, f"B{i}", a, RP, kind="data"); put(ws, f"C{i}", b, RP, kind="data")
        put(ws, f"D{i}", f"=C{i}-B{i}", RP, key); put(ws, f"E{i}", n, kind="data")
        put(ws, f"G{i}", tcause.get(m, "Cocok."), kind="input", key=key)
    ws["A22"] = "Jumlah"; ws["A22"].font = Font(bold=True)
    for col in "BCD": put(ws, f"{col}22", f"=SUM({col}17:{col}21)", RP, key, bold=True)
    ws["A24"] = "C. Rasio kamar"; ws["A24"].font = Font(bold=True, color=NAVY)
    labs = [("Kamar terjual berbayar", f"='IA-Tarif kamar'!B{TAR['r0']+2}", "0"),
            ("Pendapatan kamar terposting (nett)", f"='IA-Tarif kamar'!B{TAR['r0']+3}", RP),
            ("Okupansi (kamar terjual dibagi kamar tersedia)", "=B25/B4", "0.0%"),
            ("ARR (pendapatan kamar dibagi kamar terjual)", "=B26/B25", RP),
            ("RevPAR (pendapatan kamar dibagi kamar tersedia)", "=B26/B4", RP),
            ("Service charge dari pendapatan kamar", "=B26*B5", RP),
            ("Pajak hotel dari pendapatan kamar plus service", "=(B26+B30)*B6", RP),
            ("Tagihan kamar total (tarif, service, pajak)", "=B26+B30+B31", RP)]
    for i, (l, f, fm) in enumerate(labs, 25):
        ws.cell(row=i, column=1, value=l).font = Font(bold=True)
        put(ws, f"B{i}", f, fm, key)
    wb["IA-Rekap"].column_dimensions["A"].width = 48

    # --- Invoice
    ws = wb.create_sheet("Invoice")
    title(ws, "Templat invoice city ledger", "Isi sel kuning. Contoh kasus: PT Maju Bersama, 3 kamar Deluxe tarif CORP, 2 malam.")
    ws.column_dimensions["A"].width = 34
    for c, w in zip("BCDEF", [16, 10, 16, 18, 18]): ws.column_dimensions[c].width = w
    info = [("Nomor invoice", "INV-2612-1203", None), ("Tanggal invoice", D(2026, 12, 10), "dd mmmm yyyy"),
            ("Pelanggan", "PT Maju Bersama", None), ("Alamat dan NPWP", "[ISI TIM: data pelanggan]", None),
            ("Termin pembayaran (hari)", 30, "0"), ("Jatuh tempo", "=B5+B8", "dd mmmm yyyy"),
            ("Referensi (PO, voucher, nomor folio)", "PO-2025-118, Folio 8841", None),
            ("Service charge", 0.10, "0%"), ("Pajak hotel", 0.10, "0%")]
    for i, (l, v, fm) in enumerate(info, 4):
        ws.cell(row=i, column=1, value=l).font = Font(bold=True)
        kind = "calc" if isinstance(v, str) and v.startswith("=") else "data"
        put(ws, f"B{i}", v, fm, key, kind=kind)
    hdr(ws, 15, ["Uraian", "Tanggal menginap", "Malam", "Kamar", "Tarif nett per malam", "Jumlah nett"])
    ws["A16"] = "Kamar Deluxe, tarif CORP, 3 kamar"; ws["B16"] = "8-10 Des 2026"; ws["C16"] = 2; ws["D16"] = 3; ws["E16"] = 500000
    for c in "ABCDE": ws[f"{c}16"].border = BORD
    ws["E16"].number_format = RP
    put(ws, "F16", "=C16*D16*E16", RP, key)
    sumrows = [("Jumlah tarif nett", "=F16"), ("Service charge", "=F17*B11"), ("Pajak hotel", "=(F17+F18)*B12"), ("Total yang ditagih", "=F17+F18+F19")]
    for i, (l, f) in enumerate(sumrows, 17):
        ws.cell(row=i, column=5, value=l).font = Font(bold=True)
        put(ws, f"F{i}", f, RP, key, bold=(i == 20))
    ws["A22"] = "Pembayaran ke rekening: [ISI TIM: bank, nomor rekening, atas nama]"
    ws["A23"] = "Lampiran: salinan folio, PO atau voucher, daftar tamu."

    # --- City Ledger
    ws = wb.create_sheet("City Ledger")
    title(ws, "Daftar faktur city ledger")
    ws["A3"] = "Tanggal laporan"; ws["A3"].font = Font(bold=True); ws["B3"] = ASOF; ws["B3"].number_format = "dd mmmm yyyy"; ws["B3"].border = BORD
    hdr(ws, 5, ["No faktur", "Pelanggan", "Tanggal faktur", "Termin (hari)", "Jumlah", "Dibayar", "Sisa tagihan", "Jatuh tempo", "Hari lewat jatuh tempo", "Kelompok umur"],
        [18, 30, 15, 12, 16, 16, 16, 15, 16, 22])
    fr = 6
    for n, (no, pel, tgl, jml, byr) in enumerate(INV):
        r = fr + n
        put(ws, f"A{r}", no, kind="data"); put(ws, f"B{r}", pel, kind="data"); put(ws, f"C{r}", tgl, "dd-mmm-yyyy", kind="data")
        term = [p[2] for p in PEL if p[0] == pel][0]
        put(ws, f"D{r}", term, "0", kind="data")
        put(ws, f"E{r}", jml, RP, kind="data"); put(ws, f"F{r}", byr, RP, kind="data")
        put(ws, f"G{r}", f"=E{r}-F{r}", RP, key)
        put(ws, f"H{r}", f"=C{r}+D{r}", "dd-mmm-yyyy", key)
        put(ws, f"I{r}", f"=IF(G{r}=0,0,MAX(0,$B$3-H{r}))", "0", key)
        put(ws, f"J{r}", f'=IF(G{r}=0,"Lunas",IF(I{r}=0,"Belum jatuh tempo",IF(I{r}<=30,"1-30 hari",IF(I{r}<=60,"31-60 hari",IF(I{r}<=90,"61-90 hari","Lebih dari 90 hari")))))', None, key)
    lr = fr + len(INV) - 1
    ws.cell(row=lr + 1, column=2, value="Jumlah").font = Font(bold=True)
    for col in "EFG": put(ws, f"{col}{lr+1}", f"=SUM({col}{fr}:{col}{lr})", RP, key, bold=True)
    CL = dict(first=fr, last=lr)

    # --- Rekon Bank
    ws = wb.create_sheet("Rekon Bank")
    title(ws, "Mencocokkan mutasi bank dengan faktur", "Isi kolom kuning: faktur yang dicocokkan, selisih, dan perlakuan.")
    hdr(ws, 4, ["Tanggal", "Uraian mutasi bank", "Jumlah masuk", "Faktur yang dicocokkan", "Selisih terhadap sisa faktur", "Perlakuan dan jurnal"], [14, 34, 16, 34, 28, 80])
    for i, (tg, ur, jm, fk, sl, pl) in enumerate(BANK, 5):
        put(ws, f"A{i}", tg, "dd-mmm-yyyy", kind="data"); put(ws, f"B{i}", ur, kind="data"); put(ws, f"C{i}", jm, RP, kind="data")
        put(ws, f"D{i}", fk, kind="input", key=key); put(ws, f"E{i}", sl, kind="input", key=key); put(ws, f"F{i}", pl, kind="input", key=key)
        ws[f"F{i}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["B12"] = "Jumlah"; ws["B12"].font = Font(bold=True); put(ws, "C12", "=SUM(C5:C11)", RP, key, bold=True)

    # --- Laporan AR
    ws = wb.create_sheet("Laporan AR")
    title(ws, "Laporan piutang city ledger per 10 Desember 2026")
    hdr(ws, 4, ["Kelompok umur", "Sisa tagihan", "Persen dari total"], [38, 20, 20, 20, 20, 20])
    buckets = ["Belum jatuh tempo", "1-30 hari", "31-60 hari", "61-90 hari", "Lebih dari 90 hari"]
    f, l = CL["first"], CL["last"]
    for i, b in enumerate(buckets, 5):
        put(ws, f"A{i}", b, kind="data")
        put(ws, f"B{i}", f"=SUMIFS('City Ledger'!$G${f}:$G${l},'City Ledger'!$J${f}:$J${l},A{i})", RP, key)
        put(ws, f"C{i}", f"=B{i}/$B$10", "0.0%", key)
    ws["A10"] = "Total piutang"; ws["A10"].font = Font(bold=True); put(ws, "B10", "=SUM(B5:B9)", RP, key, bold=True); put(ws, "C10", "=SUM(C5:C9)", "0.0%", key)
    ws["A12"] = "Penjualan kredit 90 hari terakhir"; put(ws, "B12", f"=SUMIFS('City Ledger'!$E${f}:$E${l},'City Ledger'!$C${f}:$C${l},\">=\"&('City Ledger'!$B$3-90))", RP, key)
    ws["A13"] = "DSO (hari) = piutang dibagi penjualan kredit dikali 90"; put(ws, "B13", "=B10/B12*90", "0.0", key)
    ws["A14"] = "Persen piutang lewat jatuh tempo lebih dari 30 hari"; put(ws, "B14", "=SUM(B7:B9)/B10", "0.0%", key)
    ws["A16"] = "Piutang per pelanggan dan limit kredit"; ws["A16"].font = Font(bold=True, color=NAVY)
    hdr(ws, 17, ["Pelanggan", "Sisa tagihan", "Limit kredit", "Pemakaian limit", "Status limit", "Piutang lewat jatuh tempo"])
    for i, (nama, jenis, term, lim) in enumerate(PEL, 18):
        put(ws, f"A{i}", nama, kind="data")
        put(ws, f"B{i}", f"=SUMIFS('City Ledger'!$G${f}:$G${l},'City Ledger'!$B${f}:$B${l},A{i})", RP, key)
        put(ws, f"C{i}", lim, RP, kind="data")
        put(ws, f"D{i}", f"=B{i}/C{i}", "0%", key)
        put(ws, f"E{i}", f'=IF(B{i}>C{i},"Melebihi limit",IF(D{i}>=0.9,"Mendekati limit","Aman"))', None, key)
        put(ws, f"F{i}", f"=SUMIFS('City Ledger'!$G${f}:$G${l},'City Ledger'!$B${f}:$B${l},A{i},'City Ledger'!$I${f}:$I${l},\">0\")", RP, key)
    ws["A24"] = "Jumlah"; ws["A24"].font = Font(bold=True); put(ws, "B24", "=SUM(B18:B23)", RP, key, bold=True)
    ws["A26"] = "Rekomendasi tindakan (isi peserta)"; ws["A26"].font = Font(bold=True, color=NAVY)
    rek = ["CV Cahaya Wisata: melebihi limit dan ada faktur lebih dari 90 hari. Hentikan kredit baru, kirim surat peringatan, dan eskalasi ke manajer sales.",
           "PT Samudra Logistik: melebihi limit. Tahan booking baru dengan billing langsung sampai ada pelunasan, konfirmasi alokasi pembayaran 5 Desember.",
           "OTA Sampel: mendekati limit. Cocokkan settlement November dan Desember sebelum tagihan berikutnya."]
    for i in range(3):
        put(ws, f"A{27+i}", rek[i] if key else None, kind="input", key=key)
        ws.merge_cells(start_row=27+i, start_column=1, end_row=27+i, end_column=6)
        ws[f"A{27+i}"].alignment = Alignment(wrap_text=True, vertical="top"); ws.row_dimensions[27+i].height = 34

    for s in wb.worksheets:
        s.sheet_view.showGridLines = False
    return wb

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    build(False).save(OUT / "2 Workbook Latihan AR dan Income Audit Hotel (peserta).xlsx")
    build(True).save(OUT / "3 Workbook Latihan AR dan Income Audit Hotel (kunci pengajar).xlsx")
    print("selesai")
