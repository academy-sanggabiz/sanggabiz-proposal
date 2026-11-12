#!/usr/bin/env python3
"""Pembuat kalkulator Excel untuk pelatihan PT Asia Pramulia Tbk.

Jalankan: python3 buat_kalkulator.py <folder keluaran>
Semua angka contoh adalah data rekaan fasilitator untuk latihan. Bukan data PT Asia Pramulia.
Rumus ditulis sebagai rumus Excel hidup, jadi peserta bisa mengganti data dengan data sendiri.
"""
import sys
from datetime import date
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else "."

NAVY = "0B396D"
INPUT_FILL = PatternFill("solid", fgColor="DDEBF7")
HEAD_FILL = PatternFill("solid", fgColor=NAVY)
CALC_FILL = PatternFill("solid", fgColor="F2F2F2")
NOTE_FILL = PatternFill("solid", fgColor="FFF2CC")
THIN = Side(style="thin", color="999999")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WHITE_BOLD = Font(bold=True, color="FFFFFF")
BOLD = Font(bold=True)

CONTOH = ("Data di berkas ini adalah data contoh rekaan fasilitator untuk latihan. "
          "Bukan data PT Asia Pramulia. Ganti dengan data pabrik sendiri.")


def head(ws, row, labels, col=1, height=45):
    for i, t in enumerate(labels):
        c = ws.cell(row=row, column=col + i, value=t)
        c.fill = HEAD_FILL
        c.font = WHITE_BOLD
        c.alignment = Alignment(wrap_text=True, horizontal="center", vertical="center")
        c.border = BORDER
    ws.row_dimensions[row].height = height


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=14, color=NAVY)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, color="666666")


def box(ws, rng, fill=None, fmt=None, wrap=False):
    for row in ws[rng]:
        for c in row:
            c.border = BORDER
            if fill:
                c.fill = fill
            if fmt:
                c.number_format = fmt
            if wrap:
                c.alignment = Alignment(wrap_text=True, vertical="top")


def widths(ws, ws_widths):
    for col, w in ws_widths.items():
        ws.column_dimensions[col].width = w


def panduan(wb, judul, bagian):
    """bagian: daftar (judul_bagian, [baris teks])."""
    ws = wb.active
    ws.title = "Panduan"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 110
    ws["B1"] = judul
    ws["B1"].font = Font(bold=True, size=16, color=NAVY)
    ws["B2"] = "Sanggabiz, pelatihan PT Asia Pramulia Tbk. Baca lembar ini dulu, lalu pindah ke lembar kerja."
    ws["B2"].font = Font(italic=True, color="666666")
    r = 4
    ws.cell(row=r, column=2, value="Warna sel").font = Font(bold=True, color=NAVY, size=12)
    r += 1
    ws.cell(row=r, column=2, value="Biru muda: sel isian. Isi atau ganti dengan data Anda.").fill = INPUT_FILL
    r += 1
    ws.cell(row=r, column=2, value="Abu-abu: sel hasil hitungan. Jangan diketik, isinya dihitung otomatis.").fill = CALC_FILL
    r += 2
    for judul_b, baris in bagian:
        ws.cell(row=r, column=2, value=judul_b).font = Font(bold=True, color=NAVY, size=12)
        r += 1
        for t in baris:
            c = ws.cell(row=r, column=2, value=t)
            c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = max(15, 15 * (len(t) // 105 + 1))
            r += 1
        r += 1
    c = ws.cell(row=r, column=2, value=CONTOH)
    c.fill = NOTE_FILL
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 32
    return ws


def dropdown(ws, rng, options):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(rng)


# ---------------------------------------------------------------- 1. OEE
def kalkulator_oee():
    wb = Workbook()
    panduan(wb, "Kalkulator OEE (Overall Equipment Effectiveness)", [
        ("Untuk apa", [
            "Menghitung OEE per shift dan per mesin, lalu menunjukkan loss terbesar dari enam big losses. "
            "Dipakai di Sesi 4 (OEE) dan bisa dipakai harian di lantai produksi sesudah pelatihan.",
        ]),
        ("Cara memakai", [
            "1. Buka lembar OEE. Satu baris berisi satu shift satu mesin.",
            "2. Isi sel biru: tanggal, mesin, waktu terjadwal, istirahat terencana, tiga jenis downtime, waktu siklus ideal, cavity, output total, dan dua jenis reject.",
            "3. Kolom abu-abu menghitung Availability, Performance, Quality, dan OEE. Kolom loss mengubah semua kerugian menjadi menit.",
            "4. Buka lembar Loss. Di sana ada OEE gabungan semua baris, ranking enam big losses, dan nama loss terbesar.",
            "5. Ambil loss terbesar, lalu telusuri penyebabnya dengan 5 Why (lihat kalkulator Pareto dan CAPA).",
        ]),
        ("Arti istilah", [
            "Waktu terjadwal: lama shift dalam menit. Istirahat terencana: istirahat dan briefing yang memang dijadwalkan. Selisihnya disebut waktu produksi terencana.",
            "Kerusakan: mesin berhenti karena rusak. Setup dan penyesuaian: ganti cetakan, ganti material, penyetelan awal. Henti kecil: berhenti singkat, misalnya produk nyangkut atau sensor, biasanya di bawah 10 menit.",
            "Waktu siklus ideal: waktu tercepat satu siklus cetak menurut standar mesin dan cetakan, dalam detik. Cavity: jumlah pcs yang tercetak dalam satu siklus. Output total dihitung per pcs hasil cetak, termasuk yang reject.",
            "Availability = waktu jalan dibagi waktu produksi terencana. Performance = (waktu siklus ideal x output total / cavity) dibagi waktu jalan. Quality = output baik dibagi output total. OEE = ketiganya dikalikan.",
        ]),
        ("Enam big losses di berkas ini", [
            "Kerusakan, setup dan penyesuaian, dan henti kecil diisi langsung. Kecepatan turun dihitung dari selisih waktu jalan dan waktu ideal. Reject proses dan reject start-up diubah ke menit dengan waktu siklus ideal.",
        ]),
        ("Cara membaca hasil", [
            "Nilai OEE 85 persen sering disebut sebagai tolok ukur kelas dunia dalam literatur TPM (Nakajima). Tiap pabrik perlu menentukan target sendiri sesuai jenis produk dan mesin.",
            "Bila Performance lebih dari 100 persen, waktu siklus ideal yang diisi terlalu lambat. Periksa standarnya.",
        ]),
        ("Batas kalkulator", [
            "Hasilnya hanya sebaik data yang diisi. Pencatatan downtime harus jujur dan konsisten antar shift. Kalkulator tidak menentukan sebab kerusakan.",
        ]),
    ])
    ws = wb.create_sheet("OEE")
    title(ws, "OEE per shift per mesin", CONTOH)
    labels = ["Tanggal", "Mesin", "Waktu terjadwal (menit)", "Istirahat terencana (menit)",
              "Kerusakan (menit)", "Setup dan penyesuaian (menit)", "Henti kecil (menit)",
              "Waktu siklus ideal (detik per siklus)", "Cavity (pcs per siklus)", "Output total (pcs)",
              "Reject proses (pcs)", "Reject start-up (pcs)",
              "Waktu produksi terencana (menit)", "Waktu jalan (menit)", "Availability",
              "Performance", "Quality", "OEE",
              "Loss kecepatan (menit)", "Loss reject proses (menit)", "Loss reject start-up (menit)",
              "Waktu ideal output baik (menit)"]
    head(ws, 4, labels, height=62)
    # IM-01: tutup botol 28 mm, cetakan 8 cavity. IM-02: ember 10 liter, 1 cavity.
    contoh = [
        (date(2027, 1, 4), "IM-01", 480, 60, 35, 25, 20, 18, 8, 7450, 260, 40),
        (date(2027, 1, 4), "IM-02", 480, 60, 0, 30, 30, 45, 1, 420, 6, 3),
        (date(2027, 1, 5), "IM-01", 480, 60, 70, 0, 25, 18, 8, 7300, 310, 35),
        (date(2027, 1, 5), "IM-02", 480, 60, 15, 25, 40, 45, 1, 400, 5, 2),
        (date(2027, 1, 6), "IM-01", 480, 60, 20, 30, 15, 18, 8, 8100, 180, 45),
        (date(2027, 1, 6), "IM-02", 480, 60, 45, 25, 35, 45, 1, 370, 8, 4),
        (date(2027, 1, 7), "IM-01", 480, 60, 0, 20, 20, 18, 8, 9050, 120, 30),
        (date(2027, 1, 7), "IM-02", 480, 60, 30, 30, 25, 45, 1, 400, 6, 2),
    ]
    first, last = 5, 24
    for i in range(first, last + 1):
        if i - first < len(contoh):
            for j, v in enumerate(contoh[i - first]):
                ws.cell(row=i, column=1 + j, value=v)
        ws.cell(row=i, column=1).number_format = "dd/mm/yyyy"
        ws[f"M{i}"] = f'=IF(C{i}="","",C{i}-D{i})'
        ws[f"N{i}"] = f'=IF(C{i}="","",M{i}-E{i}-F{i}-G{i})'
        ws[f"O{i}"] = f'=IF(C{i}="","",N{i}/M{i})'
        ws[f"P{i}"] = f'=IF(OR(C{i}="",N{i}<=0,I{i}=0),"",H{i}*J{i}/I{i}/60/N{i})'
        ws[f"Q{i}"] = f'=IF(OR(C{i}="",J{i}=0),"",(J{i}-K{i}-L{i})/J{i})'
        ws[f"R{i}"] = f'=IF(OR(O{i}="",P{i}="",Q{i}=""),"",O{i}*P{i}*Q{i})'
        ws[f"S{i}"] = f'=IF(OR(C{i}="",I{i}=0),"",N{i}-H{i}*J{i}/I{i}/60)'
        ws[f"T{i}"] = f'=IF(OR(C{i}="",I{i}=0),"",H{i}*K{i}/I{i}/60)'
        ws[f"U{i}"] = f'=IF(OR(C{i}="",I{i}=0),"",H{i}*L{i}/I{i}/60)'
        ws[f"V{i}"] = f'=IF(OR(C{i}="",I{i}=0),"",H{i}*(J{i}-K{i}-L{i})/I{i}/60)'
    box(ws, f"A{first}:L{last}", INPUT_FILL)
    box(ws, f"M{first}:V{last}", CALC_FILL)
    for col in "OPQR":
        for i in range(first, last + 1):
            ws[f"{col}{i}"].number_format = "0.0%"
    for col in "MNSTUV":
        for i in range(first, last + 1):
            ws[f"{col}{i}"].number_format = "0.0"
    for i in range(first, last + 1):
        ws[f"J{i}"].number_format = "#,##0"
    widths(ws, {c: 12 for c in "ABCDEFGHIJKLMNOPQRSTUV"})
    ws.freeze_panes = "C5"

    ls = wb.create_sheet("Loss")
    title(ls, "Ringkasan OEE dan enam big losses", "Dihitung dari semua baris di lembar OEE.")
    ls["A4"] = "OEE gabungan"
    ls["B4"] = f'=IFERROR(SUM(OEE!V{first}:V{last})/SUM(OEE!M{first}:M{last}),"")'
    ls["A5"] = "Availability gabungan"
    ls["B5"] = f'=IFERROR(SUM(OEE!N{first}:N{last})/SUM(OEE!M{first}:M{last}),"")'
    ls["A6"] = "Total waktu produksi terencana (menit)"
    ls["B6"] = f"=SUM(OEE!M{first}:M{last})"
    for r in (4, 5, 6):
        ls[f"A{r}"].font = BOLD
        ls[f"B{r}"].fill = CALC_FILL
        ls[f"B{r}"].border = BORDER
    ls["B4"].number_format = "0.0%"
    ls["B5"].number_format = "0.0%"
    ls["B6"].number_format = "#,##0"
    head(ls, 8, ["Enam big losses", "Total (menit)", "Persen dari waktu terencana", "Ranking"], height=40)
    loss_rows = [
        ("Kerusakan", f"=SUM(OEE!E{first}:E{last})"),
        ("Setup dan penyesuaian", f"=SUM(OEE!F{first}:F{last})"),
        ("Henti kecil", f"=SUM(OEE!G{first}:G{last})"),
        ("Kecepatan turun", f"=SUM(OEE!S{first}:S{last})"),
        ("Reject proses", f"=SUM(OEE!T{first}:T{last})"),
        ("Reject start-up", f"=SUM(OEE!U{first}:U{last})"),
    ]
    for k, (nama, f) in enumerate(loss_rows):
        r = 9 + k
        ls[f"A{r}"] = nama
        ls[f"B{r}"] = f
        ls[f"C{r}"] = f'=IF($B$6=0,"",B{r}/$B$6)'
        ls[f"D{r}"] = f"=RANK(B{r},$B$9:$B$14)"
        ls[f"B{r}"].number_format = "0.0"
        ls[f"C{r}"].number_format = "0.0%"
    box(ls, "A9:D14", CALC_FILL)
    ls["A16"] = "Loss terbesar"
    ls["A16"].font = BOLD
    ls["B16"] = '=INDEX(A9:A14,MATCH(MAX(B9:B14),B9:B14,0))'
    ls["B16"].fill = CALC_FILL
    ls["B16"].border = BORDER
    ls["A18"] = "Catatan: loss kecepatan bernilai negatif bila mesin berjalan lebih cepat dari waktu siklus ideal yang diisi. Periksa standarnya."
    ls["A18"].font = Font(italic=True, color="666666")
    widths(ls, {"A": 38, "B": 18, "C": 18, "D": 12})
    ch = BarChart()
    ch.type = "bar"
    ch.title = "Enam big losses (menit)"
    ch.add_data(Reference(ls, min_col=2, min_row=8, max_row=14), titles_from_data=True)
    ch.set_categories(Reference(ls, min_col=1, min_row=9, max_row=14))
    ch.legend = None
    ch.height, ch.width = 8, 16
    ls.add_chart(ch, "F4")
    return wb


# ---------------------------------------------------------------- 2. Pareto dan CAPA
def kalkulator_pareto_capa():
    wb = Workbook()
    panduan(wb, "Pareto, 5 Why, dan CAPA", [
        ("Untuk apa", [
            "Tiga lembar kerja untuk Sesi 1 (Problem Solving dan RCA). Lembar Pareto memilih jenis cacat yang paling banyak. "
            "Lembar 5 Why menelusuri satu masalah sampai akar penyebab. Lembar CAPA mencatat tindakan perbaikan dan pencegahan.",
        ]),
        ("Cara memakai", [
            "1. Lembar Pareto: isi jenis cacat dan jumlahnya selama satu periode. Tabel urut dan grafik tersusun sendiri.",
            "2. Pilih jenis cacat teratas, lalu pindah ke lembar 5 Why. Tulis masalah, lalu jawab mengapa sampai lima kali. Berhenti bila jawabannya sudah berupa sebab yang bisa ditindak.",
            "3. Pindah ke lembar CAPA. Tulis tindakan korektif (memperbaiki penyebab yang ada), tindakan pencegahan (mencegah muncul lagi), penanggung jawab, tenggat, dan cara membuktikan hasilnya.",
            "4. Perbarui status CAPA sampai Selesai terverifikasi. Tindakan tanpa bukti efektivitas belum dianggap selesai.",
        ]),
        ("Arti istilah", [
            "Pareto: urutan penyebab dari yang paling banyak. Biasanya sekitar 80 persen masalah datang dari beberapa jenis saja. Kolom Kelas menandai jenis yang masuk 80 persen pertama sebagai Prioritas.",
            "5 Why: bertanya mengapa berulang sampai penyebab yang bisa ditindak. Fishbone: peta penyebab dalam enam kelompok (manusia, mesin, bahan, metode, pengukuran, lingkungan). Fishbone digambar di kertas plano pada sesi, hasilnya diringkas di kolom Akar penyebab.",
            "CAPA: corrective and preventive action. Korektif memperbaiki yang sudah terjadi. Pencegahan menutup peluang terulang.",
        ]),
        ("Batas kalkulator", [
            "Pareto hanya menunjukkan mana yang paling sering, bukan mana yang paling merugikan. Bila cacat berbeda biayanya, kalikan jumlah dengan biaya per pcs lebih dulu.",
        ]),
    ])
    ws = wb.create_sheet("Pareto")
    title(ws, "Pareto jenis cacat", CONTOH)
    head(ws, 4, ["Jenis cacat", "Jumlah (pcs)", "Persen", "Urutan"], height=32)
    contoh = [("Short shot", 412), ("Flashing", 268), ("Bintik hitam", 131), ("Warna belang", 96),
              ("Retak", 58), ("Sink mark", 44), ("Dimensi tidak sesuai", 27), ("Lain-lain", 19)]
    f, l = 5, 16
    for i in range(f, l + 1):
        if i - f < len(contoh):
            ws[f"A{i}"], ws[f"B{i}"] = contoh[i - f]
        ws[f"C{i}"] = f'=IF(B{i}="","",B{i}/SUM($B${f}:$B${l}))'
        ws[f"D{i}"] = f'=IF(B{i}="","",RANK(B{i},$B${f}:$B${l})+COUNTIF($B${f}:B{i},B{i})-1)'
        ws[f"C{i}"].number_format = "0.0%"
    box(ws, f"A{f}:B{l}", INPUT_FILL)
    box(ws, f"C{f}:D{l}", CALC_FILL)
    ws["F3"] = "Urut dari terbanyak"
    ws["F3"].font = BOLD
    head(ws, 4, ["Urutan", "Jenis cacat", "Jumlah (pcs)", "Persen kumulatif", "Kelas"], col=6, height=32)
    for k in range(1, 13):
        r = 4 + k
        ws[f"F{r}"] = k
        ws[f"G{r}"] = f'=IFERROR(INDEX($A${f}:$A${l},MATCH(F{r},$D${f}:$D${l},0)),"")'
        ws[f"H{r}"] = f'=IFERROR(INDEX($B${f}:$B${l},MATCH(F{r},$D${f}:$D${l},0)),"")'
        ws[f"I{r}"] = f'=IF(H{r}="","",SUM($H$5:H{r})/SUM($B${f}:$B${l}))'
        ws[f"J{r}"] = f'=IF(H{r}="","",IF(OR(F{r}=1,I{r-1}<0.8),"Prioritas","Lainnya"))' if k > 1 else f'=IF(H{r}="","","Prioritas")'
        ws[f"I{r}"].number_format = "0.0%"
    box(ws, "F5:J16", CALC_FILL)
    widths(ws, {"A": 26, "B": 14, "C": 10, "D": 9, "E": 3, "F": 9, "G": 26, "H": 14, "I": 16, "J": 12})
    bar = BarChart()
    bar.title = "Pareto jenis cacat"
    bar.add_data(Reference(ws, min_col=8, min_row=4, max_row=16), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=7, min_row=5, max_row=16))
    bar.y_axis.title = "Pcs"
    line = LineChart()
    line.add_data(Reference(ws, min_col=9, min_row=4, max_row=16), titles_from_data=True)
    line.y_axis.axId = 200
    line.y_axis.title = "Kumulatif"
    line.y_axis.crosses = "max"
    line.y_axis.number_format = "0%"
    bar += line
    bar.height, bar.width = 9, 18
    ws.add_chart(bar, "L4")

    w5 = wb.create_sheet("5 Why")
    title(w5, "5 Why", CONTOH)
    w5["A4"], w5["A5"] = "Masalah (apa, di mana, kapan, berapa)", "Tanggal analisis"
    w5["B4"] = "Short shot pada tutup botol 28 mm di mesin IM-01, 412 pcs dalam satu minggu (data contoh)"
    w5["B5"] = date(2027, 1, 11)
    w5["B5"].number_format = "dd/mm/yyyy"
    head(w5, 7, ["Tahap", "Pertanyaan", "Jawaban (berdasarkan fakta atau data)", "Bukti"], height=30)
    isi = [
        ("Why 1", "Mengapa short shot terjadi?", "Cetakan tidak terisi penuh pada cavity 3 dan 4.", "Foto sampel dan catatan operator"),
        ("Why 2", "Mengapa cetakan tidak terisi penuh?", "Tekanan injeksi turun saat shot kedua dan seterusnya.", "Grafik tekanan di panel mesin"),
        ("Why 3", "Mengapa tekanan turun?", "Viskositas resin berubah karena resin lembap.", "Hasil cek kadar air"),
        ("Why 4", "Mengapa resin lembap?", "Hopper dryer tidak dinyalakan pada shift malam.", "Log dryer"),
        ("Why 5", "Mengapa dryer tidak dinyalakan?", "Langkah menyalakan dryer tidak ada di checklist awal shift.", "Checklist awal shift"),
    ]
    for k, row in enumerate(isi):
        for j, v in enumerate(row):
            w5.cell(row=8 + k, column=1 + j, value=v)
    box(w5, "A8:D12", INPUT_FILL, wrap=True)
    w5["A14"] = "Akar penyebab"
    w5["A14"].font = BOLD
    w5["B14"] = "Checklist awal shift tidak memuat langkah menyalakan dryer dan memeriksa kadar air resin."
    w5["B14"].fill = INPUT_FILL
    w5["B14"].border = BORDER
    w5["B14"].alignment = Alignment(wrap_text=True)
    w5["A16"] = ("Uji akar penyebab: bila akar penyebab ini diperbaiki, apakah masalah awal hilang? "
                 "Bila jawabannya belum pasti, lanjutkan dengan Why berikutnya atau kumpulkan data.")
    w5["A16"].font = Font(italic=True, color="666666")
    widths(w5, {"A": 34, "B": 42, "C": 50, "D": 34})
    for r in range(4, 6):
        w5[f"B{r}"].fill = INPUT_FILL
        w5[f"B{r}"].border = BORDER
        w5[f"B{r}"].alignment = Alignment(wrap_text=True)
    w5.row_dimensions[4].height = 34

    cp = wb.create_sheet("CAPA")
    title(cp, "Daftar CAPA", CONTOH)
    head(cp, 4, ["No", "Masalah", "Akar penyebab", "Tindakan korektif", "Tindakan pencegahan",
                 "PIC", "Tenggat", "Status", "Bukti efektivitas", "Tanggal verifikasi",
                 "Terlambat?"], height=40)
    cp["A5"], cp["B5"] = 1, "Short shot IM-01"
    cp["C5"] = "Checklist awal shift tidak memuat langkah dryer"
    cp["D5"] = "Keringkan resin di hopper selama 2 jam sebelum produksi"
    cp["E5"] = "Tambahkan langkah dryer dan cek kadar air ke checklist awal shift"
    cp["F5"], cp["G5"], cp["H5"] = "Supervisor shift", date(2027, 1, 18), "Berjalan"
    cp["I5"] = "Cacat short shot turun di bawah 100 pcs per minggu selama 2 minggu"
    cp["G5"].number_format = "dd/mm/yyyy"
    for i in range(5, 16):
        cp[f"G{i}"].number_format = "dd/mm/yyyy"
        cp[f"J{i}"].number_format = "dd/mm/yyyy"
        cp[f"K{i}"] = f'=IF(OR(G{i}="",H{i}="Selesai terverifikasi"),"",IF(TODAY()>G{i},"Terlambat","Sesuai jadwal"))'
    box(cp, "A5:J15", INPUT_FILL, wrap=True)
    box(cp, "K5:K15", CALC_FILL)
    dropdown(cp, "H5:H15", ["Rencana", "Berjalan", "Selesai tanpa verifikasi", "Selesai terverifikasi"])
    widths(cp, {"A": 5, "B": 22, "C": 30, "D": 34, "E": 34, "F": 16, "G": 12, "H": 22, "I": 34, "J": 14, "K": 14})
    return wb


# ---------------------------------------------------------------- 3. Anggaran dan varians
def kalkulator_anggaran():
    wb = Workbook()
    panduan(wb, "Kalkulator Anggaran dan Analisis Varians", [
        ("Untuk apa", [
            "Menyusun anggaran departemen satu tahun dari volume produksi, lalu membandingkannya dengan realisasi. Dipakai di Sesi 5 (Budgeting, Cost Control dan Cost Efficiency).",
        ]),
        ("Cara memakai", [
            "1. Lembar Anggaran: isi volume produksi tahun anggaran. Tiap akun biaya diberi perilaku Variabel (naik bila produksi naik, diisi sebagai Rp per unit) atau Tetap (diisi sebagai Rp per tahun).",
            "2. Hasilnya total anggaran, biaya per unit, dan komposisi biaya tetap dan variabel.",
            "3. Lembar Varians: isi anggaran periode, volume anggaran, volume realisasi, dan realisasi tiap akun. Perilaku diambil dari pilihan Anda.",
            "4. Kalkulator membuat anggaran fleksibel, yaitu anggaran akun variabel disesuaikan dengan volume produksi yang benar-benar terjadi. Selisih dihitung terhadap anggaran fleksibel supaya adil.",
            "5. Akun yang selisihnya melewati batas toleransi ditandai Perlu tindakan. Tulis penyebab dan tindakan di kolom yang disediakan.",
            "6. Lembar Dampak Perbaikan: isi scrap dan lembur sebelum dan sesudah perbaikan. Kalkulator menghitung perkiraan penghematan per tahun dan persennya dari total anggaran.",
        ]),
        ("Arti istilah", [
            "Varians: selisih antara realisasi dan anggaran. Untuk biaya, realisasi di atas anggaran berarti biaya lebih besar dari rencana.",
            "Anggaran fleksibel: anggaran yang disesuaikan dengan volume produksi aktual. Tanpa penyesuaian ini, produksi yang naik akan terbaca sebagai pemborosan.",
            "Biaya tetap: besarnya tidak ikut volume dalam jangka pendek, misalnya gaji staf tetap dan penyusutan. Biaya variabel: ikut volume, misalnya resin dan kemasan.",
        ]),
        ("Batas kalkulator", [
            "Kalkulator menunjukkan di mana selisihnya. Penyebabnya tetap harus ditelusuri di lapangan, misalnya dengan Pareto dan 5 Why.",
            "Penghematan hanya dihitung bila mutu dan keselamatan tidak turun. Cek dulu sebelum mengajukan efisiensi.",
        ]),
    ])
    ws = wb.create_sheet("Anggaran")
    title(ws, "Anggaran lini tutup botol tahun 2027", CONTOH)
    ws["A4"], ws["B4"] = "Volume produksi tahun anggaran (pcs)", 18000000
    ws["A4"].font = BOLD
    ws["B4"].fill = INPUT_FILL
    ws["B4"].border = BORDER
    ws["B4"].number_format = "#,##0"
    head(ws, 6, ["Kelompok biaya", "Akun", "Perilaku", "Variabel: Rp per unit", "Tetap: Rp per tahun",
                 "Total anggaran (Rp)", "Rp per unit"], height=40)
    akun = [
        ("Bahan baku", "Resin polipropilen", "Variabel", 67.0, None),
        ("Bahan baku", "Masterbatch warna", "Variabel", 3.2, None),
        ("Bahan pelengkap", "Kemasan dan label", "Variabel", 6.5, None),
        ("Tenaga kerja langsung", "Operator produksi", "Tetap", None, 1_450_000_000),
        ("Tenaga kerja langsung", "Lembur produksi", "Variabel", 2.1, None),
        ("Overhead", "Energi listrik mesin", "Variabel", 9.4, None),
        ("Overhead", "Perawatan mesin", "Tetap", None, 520_000_000),
        ("Overhead", "Bahan pembantu (pelumas, pembersih)", "Variabel", 0.8, None),
        ("Overhead", "Penyusutan mesin dan cetakan", "Tetap", None, 960_000_000),
    ]
    f, l = 7, 22
    for i in range(f, l + 1):
        k = i - f
        if k < len(akun):
            a = akun[k]
            ws[f"A{i}"], ws[f"B{i}"], ws[f"C{i}"], ws[f"D{i}"], ws[f"E{i}"] = a
        ws[f"F{i}"] = f'=IF(B{i}="","",IF(C{i}="Variabel",D{i}*$B$4,E{i}))'
        ws[f"G{i}"] = f'=IF(B{i}="","",F{i}/$B$4)'
        for col in "DEF":
            ws[f"{col}{i}"].number_format = "#,##0.00" if col == "D" else "#,##0"
        ws[f"G{i}"].number_format = "#,##0.00"
    box(ws, f"A{f}:E{l}", INPUT_FILL)
    box(ws, f"F{f}:G{l}", CALC_FILL)
    dropdown(ws, f"C{f}:C{l}", ["Variabel", "Tetap"])
    r = l + 2
    ws[f"A{r}"] = "Total anggaran"
    ws[f"F{r}"] = f"=SUM(F{f}:F{l})"
    ws[f"G{r}"] = f"=F{r}/B4"
    ws[f"A{r+1}"] = "Biaya variabel"
    ws[f"F{r+1}"] = f'=SUMIF(C{f}:C{l},"Variabel",F{f}:F{l})'
    ws[f"G{r+1}"] = f"=F{r+1}/B4"
    ws[f"A{r+2}"] = "Biaya tetap"
    ws[f"F{r+2}"] = f'=SUMIF(C{f}:C{l},"Tetap",F{f}:F{l})'
    ws[f"G{r+2}"] = f"=F{r+2}/B4"
    ws[f"A{r+3}"] = "Persen biaya tetap dari total"
    ws[f"F{r+3}"] = f"=IF(F{r}=0,\"\",F{r+2}/F{r})"
    for rr in range(r, r + 4):
        ws[f"A{rr}"].font = BOLD
        ws[f"F{rr}"].fill = CALC_FILL
        ws[f"F{rr}"].border = BORDER
        ws[f"F{rr}"].number_format = "#,##0"
        ws[f"G{rr}"].number_format = "#,##0.00"
    ws[f"F{r+3}"].number_format = "0.0%"
    widths(ws, {"A": 34, "B": 36, "C": 12, "D": 18, "E": 20, "F": 22, "G": 14})

    v = wb.create_sheet("Varians")
    title(v, "Analisis varians dengan anggaran fleksibel", CONTOH)
    v["A4"], v["B4"] = "Volume anggaran periode (pcs)", 9000000
    v["A5"], v["B5"] = "Volume realisasi periode (pcs)", 9650000
    v["A6"], v["B6"] = "Batas toleransi selisih (persen)", 0.05
    for rr in (4, 5, 6):
        v[f"A{rr}"].font = BOLD
        v[f"B{rr}"].fill = INPUT_FILL
        v[f"B{rr}"].border = BORDER
    v["B4"].number_format = v["B5"].number_format = "#,##0"
    v["B6"].number_format = "0.0%"
    head(v, 8, ["Akun", "Perilaku", "Anggaran periode (Rp)", "Anggaran fleksibel (Rp)",
                "Realisasi (Rp)", "Selisih (Rp)", "Selisih (persen)", "Status", "Penyebab", "Tindakan"],
         height=40)
    real = [
        ("Resin polipropilen", "Variabel", 603_000_000, 690_000_000),
        ("Masterbatch warna", "Variabel", 28_800_000, 31_400_000),
        ("Kemasan dan label", "Variabel", 58_500_000, 62_300_000),
        ("Operator produksi", "Tetap", 725_000_000, 731_000_000),
        ("Lembur produksi", "Variabel", 18_900_000, 41_200_000),
        ("Energi listrik mesin", "Variabel", 84_600_000, 92_800_000),
        ("Perawatan mesin", "Tetap", 260_000_000, 318_000_000),
        ("Bahan pembantu (pelumas, pembersih)", "Variabel", 7_200_000, 7_500_000),
        ("Penyusutan mesin dan cetakan", "Tetap", 480_000_000, 480_000_000),
    ]
    f2, l2 = 9, 24
    for i in range(f2, l2 + 1):
        k = i - f2
        if k < len(real):
            a = real[k]
            v[f"A{i}"], v[f"B{i}"], v[f"C{i}"], v[f"E{i}"] = a
        v[f"D{i}"] = f'=IF(A{i}="","",IF(B{i}="Variabel",C{i}/$B$4*$B$5,C{i}))'
        v[f"F{i}"] = f'=IF(A{i}="","",E{i}-D{i})'
        v[f"G{i}"] = f'=IF(OR(A{i}="",D{i}=0),"",F{i}/D{i})'
        v[f"H{i}"] = f'=IF(G{i}="","",IF(ABS(G{i})<=$B$6,"Wajar",IF(G{i}>0,"Perlu tindakan: biaya melebihi","Perlu dicek: jauh di bawah anggaran")))'
        for col in "CDEF":
            v[f"{col}{i}"].number_format = "#,##0"
        v[f"G{i}"].number_format = "0.0%"
    v["I9"] = "Pemakaian resin lebih besar dari standar, diduga karena scrap start-up"
    v["J9"] = "Cek rekonsiliasi sisa bahan dan reject start-up"
    box(v, f"A{f2}:C{l2}", INPUT_FILL)
    box(v, f"E{f2}:E{l2}", INPUT_FILL)
    box(v, f"I{f2}:J{l2}", INPUT_FILL, wrap=True)
    box(v, f"D{f2}:D{l2}", CALC_FILL)
    box(v, f"F{f2}:H{l2}", CALC_FILL)
    dropdown(v, f"B{f2}:B{l2}", ["Variabel", "Tetap"])
    t = l2 + 2
    v[f"A{t}"] = "Total"
    v[f"A{t}"].font = BOLD
    for col in "CDEF":
        v[f"{col}{t}"] = f"=SUM({col}{f2}:{col}{l2})"
        v[f"{col}{t}"].number_format = "#,##0"
        v[f"{col}{t}"].fill = CALC_FILL
        v[f"{col}{t}"].border = BORDER
    v[f"G{t}"] = f'=IF(D{t}=0,"",F{t}/D{t})'
    v[f"G{t}"].number_format = "0.0%"
    v[f"G{t}"].fill = CALC_FILL
    widths(v, {"A": 34, "B": 12, "C": 20, "D": 20, "E": 18, "F": 16, "G": 14, "H": 34, "I": 40, "J": 34})

    d = wb.create_sheet("Dampak Perbaikan")
    title(d, "Perkiraan dampak perbaikan ke biaya", CONTOH)
    isian = [
        (4, "Volume produksi per tahun (pcs)", "=Anggaran!B4", "#,##0", False),
        (5, "Berat resin per pcs (gram)", 2.6, "0.0", True),
        (6, "Harga resin per kg (Rp)", 24500, "#,##0", True),
        (7, "Scrap sebelum perbaikan (persen)", 0.04, "0.0%", True),
        (8, "Scrap sesudah perbaikan (persen)", 0.015, "0.0%", True),
        (9, "Lembur per bulan sebelum perbaikan (Rp)", 6_900_000, "#,##0", True),
        (10, "Lembur per bulan sesudah perbaikan (Rp)", 3_400_000, "#,##0", True),
    ]
    for r, lab, val, fmt, is_input in isian:
        d[f"A{r}"] = lab
        d[f"B{r}"] = val
        d[f"B{r}"].number_format = fmt
        d[f"B{r}"].fill = INPUT_FILL if is_input else CALC_FILL
        d[f"B{r}"].border = BORDER
    hasil = [
        (12, "Resin yang dihemat per tahun (kg)", "=B4*(B7-B8)*B5/1000", "#,##0"),
        (13, "Penghematan resin per tahun (Rp)", "=B12*B6", "#,##0"),
        (14, "Penghematan lembur per tahun (Rp)", "=(B9-B10)*12", "#,##0"),
        (15, "Total penghematan per tahun (Rp)", "=B13+B14", "#,##0"),
        (16, "Persen dari total anggaran lini", '=IFERROR(B15/Anggaran!F24,"")', "0.0%"),
    ]
    for r, lab, f, fmt in hasil:
        d[f"A{r}"] = lab
        d[f"A{r}"].font = BOLD
        d[f"B{r}"] = f
        d[f"B{r}"].number_format = fmt
        d[f"B{r}"].fill = CALC_FILL
        d[f"B{r}"].border = BORDER
    d["A18"] = ("Hitungan ini perkiraan untuk memilih prioritas. Penghematan nyata dibuktikan dengan data "
                "scrap dan lembur sesudah CAPA berjalan.")
    d["A18"].font = Font(italic=True, color="666666")
    widths(d, {"A": 44, "B": 20})
    return wb


# ---------------------------------------------------------------- 4. Inventori dan gudang
def kalkulator_inventori():
    wb = Workbook()
    panduan(wb, "Kalkulator Inventori dan Gudang", [
        ("Untuk apa", [
            "Empat lembar kerja untuk Sesi 7 (Warehouse Management) dan Sesi 8 (Pengendalian Inventori): klasifikasi ABC, titik pemesanan ulang dan stok pengaman, akurasi stok hasil cycle count, dan pelacakan sisa bahan baku.",
        ]),
        ("Cara memakai", [
            "1. ABC: isi kode, nama, jenis bahan, pemakaian setahun, dan harga satuan. Kalkulator menghitung nilai pemakaian lalu memberi kelas A, B, atau C.",
            "2. Pesan Ulang: untuk item penting (biasanya kelas A), isi permintaan setahun, simpangan baku permintaan harian, lead time, biaya pesan, biaya simpan, dan stok sekarang. Pilih tingkat layanan di sel yang tersedia. Hasilnya stok pengaman, titik pemesanan ulang, jumlah pesan ekonomis, dan peringatan pesan sekarang.",
            "3. Cycle Count: isi stok menurut sistem dan hasil hitung fisik. Kalkulator menunjukkan selisih dan akurasi stok.",
            "4. Sisa Bahan: untuk tiap surat perintah produksi, isi bahan yang dikeluarkan dari gudang, output baik, reject, berat per pcs, bahan yang dikembalikan, dan sisa di area mesin. Kalkulator menghitung bahan yang tidak terlacak.",
        ]),
        ("Arti istilah", [
            "Analisis ABC: kelas A adalah item yang mengisi 80 persen pertama nilai pemakaian (termasuk item yang melewati batas 80 persen), B mengisi sampai 95 persen, C sisanya. Perhatian dan kontrol paling ketat untuk kelas A.",
            "Stok pengaman: cadangan untuk menahan variasi permintaan selama lead time. Rumus: faktor z dikali simpangan baku harian dikali akar lead time.",
            "Titik pemesanan ulang: stok yang memicu pesanan baru. Rumus: rata-rata permintaan harian dikali lead time, ditambah stok pengaman.",
            "EOQ (economic order quantity): jumlah pesan yang menyeimbangkan biaya pesan dan biaya simpan. Rumus: akar dari (2 x permintaan setahun x biaya pesan) dibagi biaya simpan per unit per tahun.",
            "Cycle count: penghitungan stok bergilir tanpa menghentikan gudang. Akurasi stok: persen item yang selisihnya masih dalam toleransi.",
        ]),
        ("Batas kalkulator", [
            "Rumus stok pengaman dan EOQ memakai asumsi permintaan stabil dan berdistribusi normal. Untuk item dengan permintaan tidak teratur, hasilnya perlu dinilai ulang oleh perencana.",
            "Pembagian bahan baku, bahan pembantu, dan bahan pelengkap mengikuti definisi perusahaan. Sesuaikan pilihan di kolom Jenis bahan.",
        ]),
    ])
    abc = wb.create_sheet("ABC")
    title(abc, "Klasifikasi ABC berdasarkan nilai pemakaian", CONTOH)
    head(abc, 4, ["Kode", "Nama bahan", "Jenis bahan", "Pemakaian per tahun", "Satuan", "Harga satuan (Rp)",
                  "Nilai pemakaian (Rp)", "Persen nilai", "Persen kumulatif", "Kelas"], height=40)
    contoh = [
        ("RB-001", "Resin PP homopolimer", "Baku", 420000, "kg", 24500),
        ("RB-002", "Resin HDPE blow", "Baku", 150000, "kg", 26800),
        ("RB-003", "Masterbatch putih", "Baku", 18000, "kg", 52000),
        ("RB-004", "Masterbatch biru", "Baku", 6200, "kg", 61000),
        ("PL-001", "Kardus karton luar", "Pelengkap", 95000, "lembar", 7800),
        ("PL-002", "Plastik pembungkus", "Pelengkap", 4800, "kg", 31000),
        ("PL-003", "Label cetak", "Pelengkap", 1900000, "lembar", 95),
        ("PB-001", "Pelumas cetakan", "Pembantu", 360, "kaleng", 185000),
        ("PB-002", "Cairan pembersih cetakan", "Pembantu", 520, "liter", 62000),
        ("PB-003", "Sarung tangan kerja", "Pembantu", 1800, "pasang", 9500),
        ("PB-004", "Lakban dan tali pengikat", "Pembantu", 2400, "roll", 14000),
        ("PB-005", "Kain lap industri", "Pembantu", 900, "kg", 12500),
    ]
    f, l = 5, 34
    for i in range(f, l + 1):
        k = i - f
        if k < len(contoh):
            for j, val in enumerate(contoh[k]):
                abc.cell(row=i, column=1 + j, value=val)
        abc[f"G{i}"] = f'=IF(B{i}="","",D{i}*F{i})'
        abc[f"H{i}"] = f'=IF(B{i}="","",G{i}/SUM($G${f}:$G${l}))'
        abc[f"I{i}"] = f'=IF(B{i}="","",SUMIF($G${f}:$G${l},">="&G{i})/SUM($G${f}:$G${l}))'
        abc[f"J{i}"] = f'=IF(B{i}="","",IF(I{i}-H{i}<0.8,"A",IF(I{i}-H{i}<0.95,"B","C")))'
        for col in "DFG":
            abc[f"{col}{i}"].number_format = "#,##0"
        abc[f"H{i}"].number_format = abc[f"I{i}"].number_format = "0.0%"
    box(abc, f"A{f}:F{l}", INPUT_FILL)
    box(abc, f"G{f}:J{l}", CALC_FILL)
    dropdown(abc, f"C{f}:C{l}", ["Baku", "Pembantu", "Pelengkap"])
    abc["L3"] = "Ringkasan kelas"
    abc["L3"].font = BOLD
    head(abc, 4, ["Kelas", "Jumlah item", "Persen nilai"], col=12, height=40)
    for k, kelas in enumerate(("A", "B", "C")):
        r = 5 + k
        abc[f"L{r}"] = kelas
        abc[f"M{r}"] = f'=COUNTIF($J${f}:$J${l},L{r})'
        abc[f"N{r}"] = f'=SUMIF($J${f}:$J${l},L{r},$H${f}:$H${l})'
        abc[f"N{r}"].number_format = "0.0%"
    box(abc, "L5:N7", CALC_FILL)
    abc["L9"] = ("Aturan: item masuk kelas A bila persen kumulatif sebelum item itu masih di bawah 80 persen, "
                  "kelas B bila di bawah 95 persen, selebihnya C. Item bernilai sama mendapat kelas yang sama.")
    abc["L9"].alignment = Alignment(wrap_text=True, vertical="top")
    abc.merge_cells("L9:N13")
    widths(abc, {"A": 10, "B": 30, "C": 12, "D": 14, "E": 9, "F": 14, "G": 18, "H": 10, "I": 12, "J": 8, "K": 3,
                 "L": 10, "M": 12, "N": 12})

    pr = wb.create_sheet("Pesan Ulang")
    title(pr, "Stok pengaman, titik pemesanan ulang, dan EOQ", CONTOH)
    pr["A4"], pr["B4"] = "Hari kerja per tahun", 300
    pr["A5"], pr["B5"] = "Tingkat layanan yang dikehendaki", 0.95
    pr["A6"], pr["B6"] = "Faktor z (otomatis)", None
    pr["B6"] = '=VLOOKUP(B5,$R$5:$S$8,2,FALSE)'
    for rr in (4, 5, 6):
        pr[f"A{rr}"].font = BOLD
        pr[f"B{rr}"].border = BORDER
    pr["B4"].fill = INPUT_FILL
    pr["B5"].fill = INPUT_FILL
    pr["B6"].fill = CALC_FILL
    pr["B5"].number_format = "0.0%"
    pr["B6"].number_format = "0.00"
    head(pr, 4, ["Tingkat layanan", "Faktor z"], col=18, height=30)
    for k, (lv, z) in enumerate([(0.90, 1.28), (0.95, 1.65), (0.975, 1.96), (0.99, 2.33)]):
        pr[f"R{5+k}"], pr[f"S{5+k}"] = lv, z
        pr[f"R{5+k}"].number_format = "0.0%"
    box(pr, "R5:S8", CALC_FILL)
    dv = DataValidation(type="list", formula1="=$R$5:$R$8", allow_blank=False)
    pr.add_data_validation(dv)
    dv.add("B5")
    head(pr, 8, ["Kode", "Nama bahan", "Permintaan per tahun", "Simpangan baku permintaan harian",
                 "Lead time (hari)", "Biaya per pesanan (Rp)", "Biaya simpan per unit per tahun (Rp)",
                 "Stok sekarang", "Permintaan rata-rata harian", "Stok pengaman", "Titik pemesanan ulang",
                 "EOQ", "Frekuensi pesan per tahun", "Keputusan"], height=62)
    items = [
        ("RB-001", "Resin PP homopolimer", 420000, 380, 7, 3_500_000, 2450, 41000),
        ("RB-002", "Resin HDPE blow", 150000, 160, 10, 3_500_000, 2680, 21000),
        ("RB-003", "Masterbatch putih", 18000, 22, 14, 1_800_000, 5200, 900),
        ("PL-001", "Kardus karton luar", 95000, 150, 5, 900_000, 780, 2300),
        ("PB-001", "Pelumas cetakan", 360, 0.6, 21, 250_000, 18500, 52),
    ]
    f3, l3 = 9, 18
    for i in range(f3, l3 + 1):
        k = i - f3
        if k < len(items):
            kode, nama, d, sd, lt, s, h, stok = items[k]
            for col, val in zip("ABCDEFGH", (kode, nama, d, sd, lt, s, h, stok)):
                pr[f"{col}{i}"] = val
        pr[f"I{i}"] = f'=IF(B{i}="","",C{i}/$B$4)'
        pr[f"J{i}"] = f'=IF(B{i}="","",$B$6*D{i}*SQRT(E{i}))'
        pr[f"K{i}"] = f'=IF(B{i}="","",I{i}*E{i}+J{i})'
        pr[f"L{i}"] = f'=IF(B{i}="","",SQRT(2*C{i}*F{i}/G{i}))'
        pr[f"M{i}"] = f'=IF(B{i}="","",C{i}/L{i})'
        pr[f"N{i}"] = f'=IF(B{i}="","",IF(H{i}<=K{i},"Pesan sekarang sebanyak EOQ","Aman, pantau terus"))'
        for col in "CFGH":
            pr[f"{col}{i}"].number_format = "#,##0"
        for col in "IJKLM":
            pr[f"{col}{i}"].number_format = "#,##0.0"
    # kolom keputusan dipindah ke kolom N agar tidak menimpa tabel z di N4:O8
    for i in range(f3, l3 + 1):
        pass
    box(pr, f"A{f3}:H{l3}", INPUT_FILL)
    box(pr, f"I{f3}:N{l3}", CALC_FILL)
    widths(pr, {"A": 36, "B": 30, "C": 14, "D": 16, "E": 11, "F": 16, "G": 18, "H": 12, "I": 14, "J": 12,
                "K": 14, "L": 12, "M": 14, "N": 30, "R": 16, "S": 10})
    return wb, abc, pr


def lengkapi_inventori(wb, pr):
    """Menambah lembar Cycle Count dan Sisa Bahan."""
    cc = wb.create_sheet("Cycle Count")
    title(cc, "Cycle count dan akurasi stok", CONTOH)
    cc["A4"], cc["B4"] = "Toleransi selisih (persen)", 0.02
    cc["A4"].font = BOLD
    cc["B4"].fill = INPUT_FILL
    cc["B4"].border = BORDER
    cc["B4"].number_format = "0.0%"
    head(cc, 6, ["Kode", "Nama bahan", "Lokasi", "Stok sistem", "Stok fisik", "Selisih", "Selisih (persen)",
                 "Status", "Dugaan penyebab"], height=40)
    contoh = [
        ("RB-001", "Resin PP homopolimer", "A-01-02", 41250, 40100, "Pengembalian sisa dari mesin IM-01 belum dicatat"),
        ("RB-002", "Resin HDPE blow", "A-01-03", 21000, 20950, "Pembulatan timbang"),
        ("RB-003", "Masterbatch putih", "A-02-01", 2300, 2300, ""),
        ("RB-004", "Masterbatch biru", "A-02-02", 880, 910, "Salah input penerimaan"),
        ("PL-001", "Kardus karton luar", "B-03-01", 2300, 2290, ""),
        ("PL-002", "Plastik pembungkus", "B-03-02", 640, 610, "Terpakai belum dicatat"),
        ("PB-001", "Pelumas cetakan", "C-01-01", 52, 52, ""),
        ("PB-002", "Cairan pembersih cetakan", "C-01-02", 95, 88, "Dipakai bengkel tanpa catatan"),
    ]
    f4, l4 = 7, 36
    for i in range(f4, l4 + 1):
        k = i - f4
        if k < len(contoh):
            kode, nama, lok, sis, fis, dugaan = contoh[k]
            cc[f"A{i}"], cc[f"B{i}"], cc[f"C{i}"], cc[f"D{i}"], cc[f"E{i}"], cc[f"I{i}"] = kode, nama, lok, sis, fis, dugaan
        cc[f"F{i}"] = f'=IF(B{i}="","",E{i}-D{i})'
        cc[f"G{i}"] = f'=IF(OR(B{i}="",D{i}=0),"",F{i}/D{i})'
        cc[f"H{i}"] = f'=IF(G{i}="","",IF(ABS(G{i})<=$B$4,"Cocok","Selidiki"))'
        cc[f"D{i}"].number_format = cc[f"E{i}"].number_format = cc[f"F{i}"].number_format = "#,##0"
        cc[f"G{i}"].number_format = "0.0%"
    box(cc, f"A{f4}:E{l4}", INPUT_FILL)
    box(cc, f"I{f4}:I{l4}", INPUT_FILL, wrap=True)
    box(cc, f"F{f4}:H{l4}", CALC_FILL)
    cc["K6"] = "Akurasi stok"
    cc["K6"].font = BOLD
    cc["K7"] = f'=IFERROR(COUNTIF(H{f4}:H{l4},"Cocok")/(COUNTIF(H{f4}:H{l4},"Cocok")+COUNTIF(H{f4}:H{l4},"Selidiki")),"")'
    cc["K7"].number_format = "0.0%"
    cc["K7"].fill = CALC_FILL
    cc["K7"].border = BORDER
    cc["K8"] = "Item perlu diselidiki"
    cc["K8"].font = BOLD
    cc["K9"] = f'=COUNTIF(H{f4}:H{l4},"Selidiki")'
    cc["K9"].fill = CALC_FILL
    cc["K9"].border = BORDER
    widths(cc, {"A": 10, "B": 28, "C": 11, "D": 12, "E": 12, "F": 10, "G": 12, "H": 11, "I": 38, "J": 3, "K": 22})

    sb = wb.create_sheet("Sisa Bahan")
    title(sb, "Pelacakan sisa bahan baku per surat perintah produksi (tutup botol 28 mm, IM-01)", CONTOH)
    sb["A4"], sb["B4"] = "Batas bahan tidak terlacak (persen dari bahan keluar)", 0.01
    sb["A4"].font = BOLD
    sb["B4"].fill = INPUT_FILL
    sb["B4"].border = BORDER
    sb["B4"].number_format = "0.0%"
    head(sb, 6, ["Tanggal", "No. SPK", "Bahan", "Bahan keluar gudang (kg)", "Output baik (pcs)",
                 "Reject (pcs)", "Berat per pcs (gram)", "Bahan terpakai di output baik (kg)",
                 "Bahan di reject (kg)", "Dikembalikan ke gudang (kg)", "Sisa di area mesin (kg)",
                 "Giling ulang (kg)", "Bahan tidak terlacak (kg)", "Persen tidak terlacak", "Status"], height=70)
    contoh = [
        (date(2027, 1, 4), "SPK-0104-01", "Resin PP", 230, 80000, 2400, 2.6, 10, 4, 5),
        (date(2027, 1, 5), "SPK-0105-01", "Resin PP", 180, 60000, 2100, 2.6, 12, 3, 4),
        (date(2027, 1, 6), "SPK-0106-01", "Resin PP", 120, 41000, 1200, 2.6, 6, 3.5, 0),
        (date(2027, 1, 7), "SPK-0107-01", "Resin PP", 200, 68000, 2600, 2.6, 8, 4, 5),
    ]
    f5, l5 = 7, 26
    for i in range(f5, l5 + 1):
        k = i - f5
        if k < len(contoh):
            tgl, spk, bhn, keluar, baik, rej, berat, kembali, sisa, giling = contoh[k]
            for col, val in zip("ABCDEFGJKL", (tgl, spk, bhn, keluar, baik, rej, berat, kembali, sisa, giling)):
                sb[f"{col}{i}"] = val
        sb[f"A{i}"].number_format = "dd/mm/yyyy"
        sb[f"H{i}"] = f'=IF(B{i}="","",E{i}*G{i}/1000)'
        sb[f"I{i}"] = f'=IF(B{i}="","",F{i}*G{i}/1000)'
        sb[f"M{i}"] = f'=IF(B{i}="","",D{i}-H{i}-I{i}-J{i}-K{i})'
        sb[f"N{i}"] = f'=IF(OR(B{i}="",D{i}=0),"",M{i}/D{i})'
        sb[f"O{i}"] = f'=IF(N{i}="","",IF(ABS(N{i})<=$B$4,"Wajar","Selidiki"))'
        for col in "DHIJKLM":
            sb[f"{col}{i}"].number_format = "#,##0.0"
        sb[f"N{i}"].number_format = "0.0%"
    box(sb, f"A{f5}:G{l5}", INPUT_FILL)
    box(sb, f"J{f5}:L{l5}", INPUT_FILL)
    box(sb, f"H{f5}:I{l5}", CALC_FILL)
    box(sb, f"M{f5}:O{l5}", CALC_FILL)
    sb["A28"] = ("Catatan: giling ulang (regrind) dicatat sebagai informasi. Bahan giling ulang berasal dari reject, jadi sudah terhitung di kolom Bahan di reject. "
                 "Kolom Giling ulang tidak mengurangi bahan tidak terlacak.")
    sb["A28"].font = Font(italic=True, color="666666")
    widths(sb, {"A": 11, "B": 14, "C": 12, "D": 14, "E": 12, "F": 10, "G": 12, "H": 16, "I": 12, "J": 14,
                "K": 12, "L": 11, "M": 14, "N": 12, "O": 10})
    return wb


# ---------------------------------------------------------------- 5. Kapasitas dan jadwal
def kalkulator_jadwal():
    wb = Workbook()
    panduan(wb, "Kalkulator Kapasitas dan Jadwal Produksi", [
        ("Untuk apa", [
            "Menghitung beban jam mesin dari daftar order, membandingkannya dengan kapasitas mingguan, dan memperkirakan order mana yang terlambat menurut urutan pengerjaan. Dipakai di Sesi 6 (Perencanaan dan Penjadwalan Produksi).",
        ]),
        ("Cara memakai", [
            "1. Lembar Mesin: isi daftar mesin, jumlah shift per hari, jam per shift, hari kerja per minggu, dan faktor efisiensi. Faktor efisiensi adalah bagian jam terjadwal yang benar-benar menghasilkan, di luar setup. Ambil dari OEE tanpa kerugian setup.",
            "2. Lembar Order: isi tiap order dengan mesin, jumlah, cavity, waktu siklus, waktu setup, persen scrap, urutan pengerjaan di mesin itu, dan tenggat (hari kerja ke berapa sejak awal minggu).",
            "3. Kalkulator menghitung jam mesin tiap order, jam selesai kumulatif sesuai urutan, hari selesai, dan status Tepat waktu atau Terlambat.",
            "4. Ubah kolom Urutan untuk mencoba aturan prioritas. FIFO: urut menurut kedatangan order. Tenggat terdekat: urutkan dari tenggat paling awal. Waktu proses terpendek: urutkan dari jam mesin paling sedikit. Bandingkan jumlah order yang terlambat.",
            "5. Lembar Mesin menunjukkan beban dibandingkan kapasitas. Bila di atas 100 persen, pilih: tambah shift, pindahkan order ke mesin lain, atau negosiasi tenggat.",
            "6. Lembar Kebutuhan Bahan: isi jenis resin, berat per pcs, persen masterbatch, dan isi karton tiap order. Kalkulator menghitung kebutuhan resin, masterbatch, dan karton, lalu membandingkan kebutuhan resin dengan stok bebas di gudang.",
        ]),
        ("Arti istilah", [
            "Cavity: jumlah produk yang tercetak dalam satu siklus. Waktu siklus: lama satu siklus cetak dalam detik. Jam mesin = (jumlah x (1 + scrap) / cavity x waktu siklus) / 3600, ditambah waktu setup.",
            "Beban: total jam mesin untuk semua order di satu mesin. Kapasitas efektif: jam terjadwal dikali faktor efisiensi.",
        ]),
        ("Batas kalkulator", [
            "Kalkulator tidak mengatur urutan sendiri dan tidak menghitung kekurangan bahan atau ketersediaan cetakan. Perencana tetap memeriksa dua hal itu.",
            "Kalkulator menganggap tiap mesin menjalankan order secara berurutan tanpa jeda antar order selain waktu setup.",
        ]),
    ])
    ms = wb.create_sheet("Mesin")
    title(ms, "Kapasitas mesin mingguan", CONTOH)
    head(ms, 4, ["Mesin", "Shift per hari", "Jam per shift", "Hari kerja per minggu", "Faktor efisiensi",
                 "Jam efektif per hari", "Kapasitas efektif per minggu (jam)", "Beban (jam)", "Beban dibanding kapasitas",
                 "Status"], height=55)
    mesin = [("IM-01", 2, 8, 6, 0.80), ("IM-02", 2, 8, 6, 0.78), ("IM-03", 1, 8, 6, 0.82)]
    f, l = 5, 12
    for i in range(f, l + 1):
        k = i - f
        if k < len(mesin):
            for col, val in zip("ABCDE", mesin[k]):
                ms[f"{col}{i}"] = val
        ms[f"F{i}"] = f'=IF(A{i}="","",B{i}*C{i}*E{i})'
        ms[f"G{i}"] = f'=IF(A{i}="","",F{i}*D{i})'
        ms[f"H{i}"] = f'=IF(A{i}="","",SUMIF(Order!$C$5:$C$24,A{i},Order!$J$5:$J$24))'
        ms[f"I{i}"] = f'=IF(OR(A{i}="",G{i}=0),"",H{i}/G{i})'
        ms[f"J{i}"] = f'=IF(I{i}="","",IF(I{i}>1,"Melebihi kapasitas",IF(I{i}>0.9,"Padat","Cukup")))'
        ms[f"E{i}"].number_format = "0%"
        ms[f"I{i}"].number_format = "0%"
        for col in "FGH":
            ms[f"{col}{i}"].number_format = "0.0"
    box(ms, f"A{f}:E{l}", INPUT_FILL)
    box(ms, f"F{f}:J{l}", CALC_FILL)
    widths(ms, {c: 15 for c in "ABCDEFGHIJ"})
    ms.column_dimensions["J"].width = 22

    od = wb.create_sheet("Order")
    title(od, "Daftar order minggu ini", CONTOH)
    head(od, 4, ["No. order", "Produk", "Mesin", "Jumlah (pcs)", "Cavity", "Waktu siklus (detik)",
                 "Waktu setup (menit)", "Scrap (persen)", "Tenggat (hari kerja ke-)", "Jam mesin",
                 "Urutan di mesin", "Jam selesai kumulatif", "Hari selesai", "Status"], height=55)
    orders = [
        ("PO-2701", "Tutup botol 28 mm putih", "IM-01", 60000, 8, 18, 75, 0.02, 4, 1),
        ("PO-2702", "Tutup botol 28 mm biru", "IM-01", 40000, 8, 18, 60, 0.02, 6, 2),
        ("PO-2703", "Wadah makanan 500 ml", "IM-01", 12000, 4, 32, 90, 0.03, 6, 3),
        ("PO-2704", "Ember 10 liter", "IM-02", 5000, 1, 45, 120, 0.02, 7, 1),
        ("PO-2705", "Botol 600 ml", "IM-02", 5000, 2, 28, 100, 0.025, 3, 2),
        ("PO-2706", "Tutup galon", "IM-03", 12000, 4, 26, 60, 0.02, 4, 1),
        ("PO-2707", "Gelas 220 ml", "IM-03", 10000, 4, 22, 70, 0.02, 6, 2),
    ]
    f2, l2 = 5, 24
    for i in range(f2, l2 + 1):
        k = i - f2
        if k < len(orders):
            for col, val in zip("ABCDEFGHIK", orders[k]):
                od[f"{col}{i}"] = val
        od[f"J{i}"] = f'=IF(A{i}="","",D{i}*(1+H{i})/E{i}*F{i}/3600+G{i}/60)'
        od[f"L{i}"] = f'=IF(A{i}="","",SUMIFS($J${f2}:$J${l2},$C${f2}:$C${l2},C{i},$K${f2}:$K${l2},"<="&K{i}))'
        od[f"M{i}"] = (f'=IF(A{i}="","",ROUNDUP(L{i}/VLOOKUP(C{i},Mesin!$A$5:$F$12,6,FALSE),0))')
        od[f"N{i}"] = f'=IF(A{i}="","",IF(M{i}>I{i},"Terlambat","Tepat waktu"))'
        od[f"D{i}"].number_format = "#,##0"
        od[f"H{i}"].number_format = "0.0%"
        od[f"J{i}"].number_format = od[f"L{i}"].number_format = "0.0"
    box(od, f"A{f2}:I{l2}", INPUT_FILL)
    box(od, f"K{f2}:K{l2}", INPUT_FILL)
    box(od, f"J{f2}:J{l2}", CALC_FILL)
    box(od, f"L{f2}:N{l2}", CALC_FILL)
    od["A26"] = "Jumlah order terlambat"
    od["A26"].font = BOLD
    od["D26"] = f'=COUNTIF(N{f2}:N{l2},"Terlambat")'
    od["D26"].fill = CALC_FILL
    od["D26"].border = BORDER
    widths(od, {"A": 11, "B": 28, "C": 8, "D": 13, "E": 8, "F": 11, "G": 11, "H": 9, "I": 13, "J": 11,
                "K": 11, "L": 13, "M": 10, "N": 14})

    kb = wb.create_sheet("Kebutuhan Bahan")
    title(kb, "Kebutuhan bahan dari jadwal minggu ini", CONTOH)
    head(kb, 4, ["No. order", "Produk", "Jumlah (pcs)", "Scrap (persen)", "Jenis resin", "Berat per pcs (gram)",
                 "Masterbatch (persen dari resin)", "Pcs per karton", "Resin (kg)", "Masterbatch (kg)", "Karton"],
         height=55)
    bahan = [("Resin PP", 2.6, 0.02, 2000), ("Resin PP", 2.6, 0.02, 2000), ("Resin PP", 22, 0.015, 200),
             ("Resin HDPE", 480, 0.02, 20), ("Resin HDPE", 28, 0.02, 100), ("Resin PP", 14, 0.02, 500),
             ("Resin PP", 6, 0.01, 1000)]
    for i in range(f2, l2 + 1):
        k = i - f2
        kb[f"A{i}"] = f'=IF(Order!A{i}="","",Order!A{i})'
        kb[f"B{i}"] = f'=IF(Order!A{i}="","",Order!B{i})'
        kb[f"C{i}"] = f'=IF(Order!A{i}="","",Order!D{i})'
        kb[f"D{i}"] = f'=IF(Order!A{i}="","",Order!H{i})'
        if k < len(bahan):
            kb[f"E{i}"], kb[f"F{i}"], kb[f"G{i}"], kb[f"H{i}"] = bahan[k]
        kb[f"I{i}"] = f'=IF(OR(A{i}="",F{i}=""),"",C{i}*(1+D{i})*F{i}/1000)'
        kb[f"J{i}"] = f'=IF(I{i}="","",I{i}*G{i})'
        kb[f"K{i}"] = f'=IF(OR(A{i}="",H{i}=""),"",ROUNDUP(C{i}/H{i},0))'
        kb[f"C{i}"].number_format = "#,##0"
        kb[f"D{i}"].number_format = kb[f"G{i}"].number_format = "0.0%"
        kb[f"I{i}"].number_format = kb[f"J{i}"].number_format = "#,##0.0"
        kb[f"K{i}"].number_format = "#,##0"
    box(kb, f"A{f2}:D{l2}", CALC_FILL)
    box(kb, f"E{f2}:H{l2}", INPUT_FILL)
    box(kb, f"I{f2}:K{l2}", CALC_FILL)
    dropdown(kb, f"E{f2}:E{l2}", ["Resin PP", "Resin HDPE"])
    kb["M3"] = "Cek stok resin"
    kb["M3"].font = BOLD
    head(kb, 4, ["Jenis resin", "Kebutuhan (kg)", "Stok bebas di gudang (kg)", "Status"], col=13, height=55)
    for k, (jenis, stok) in enumerate((("Resin PP", 2500), ("Resin HDPE", 2400))):
        r = 5 + k
        kb[f"M{r}"] = jenis
        kb[f"N{r}"] = f'=SUMIF($E${f2}:$E${l2},M{r},$I${f2}:$I${l2})'
        kb[f"O{r}"] = stok
        kb[f"P{r}"] = f'=IF(N{r}<=O{r},"Cukup","Kurang, pesan atau geser order")'
        kb[f"N{r}"].number_format = kb[f"O{r}"].number_format = "#,##0.0"
        for col in "MNP":
            kb[f"{col}{r}"].fill = CALC_FILL
            kb[f"{col}{r}"].border = BORDER
        kb[f"O{r}"].fill = INPUT_FILL
        kb[f"O{r}"].border = BORDER
    kb["M8"] = "Stok bebas: stok fisik yang belum dialokasikan untuk order lain. Ambil dari hasil cycle count, bukan dari angka sistem."
    kb["M8"].alignment = Alignment(wrap_text=True, vertical="top")
    kb.merge_cells("M8:P10")
    widths(kb, {"A": 11, "B": 26, "C": 12, "D": 10, "E": 13, "F": 12, "G": 14, "H": 11, "I": 11, "J": 12,
                "K": 9, "L": 3, "M": 14, "N": 14, "O": 16, "P": 30})
    return wb


def atur_cetak(wb):
    """Landscape A4, lebar muat satu halaman, supaya rapi saat dicetak atau diekspor ke PDF."""
    for ws in wb.worksheets:
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.page_setup.fitToWidth = 1
        ws.page_setup.fitToHeight = 0
    return wb


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    atur_cetak(kalkulator_oee()).save(f"{OUT}/1-Kalkulator-OEE.xlsx")
    atur_cetak(kalkulator_pareto_capa()).save(f"{OUT}/2-Pareto-5Why-CAPA.xlsx")
    atur_cetak(kalkulator_anggaran()).save(f"{OUT}/3-Anggaran-dan-Varians.xlsx")
    wb, abc, pr = kalkulator_inventori()
    wb = lengkapi_inventori(wb, pr)
    atur_cetak(wb).save(f"{OUT}/4-Inventori-dan-Gudang.xlsx")
    atur_cetak(kalkulator_jadwal()).save(f"{OUT}/5-Kapasitas-dan-Jadwal.xlsx")
    print("selesai")


main()
