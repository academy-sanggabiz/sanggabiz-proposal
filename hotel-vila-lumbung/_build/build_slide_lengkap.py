#!/usr/bin/env python3
"""Slide lengkap tiga sesi. Jalankan: python3 build_slide_lengkap.py"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY, GOLD, INK, MUTED, LIGHT = RGBColor(0x0B,0x39,0x6D), RGBColor(0xFF,0xC0,0x0C), RGBColor(0x1D,0x1D,0x1F), RGBColor(0x5C,0x5F,0x66), RGBColor(0xEE,0xF3,0xF9)
OUT = Path(__file__).resolve().parent.parent / "assets" / "7 Slide Pelatihan AR dan Income Audit Hotel (Sesi 1 sampai 3).pptx"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
FOOT = ["Sanggabiz  |  AR dan Income Audit Hotel  |  Sesi 1"]

def box(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None: sh.fill.background()
    else: sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb = line; sh.line.width = Pt(1)
    sh.shadow.inherit = False
    return sh
def text(s, x, y, w, h, lines, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    if isinstance(lines, str): lines = [lines]
    for i, ln in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = align; para.space_after = Pt(6)
        r = para.add_run(); r.text = ln; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = "Montserrat"
    return tb
def slide(title, n=None):
    n = len(prs.slides) + 1
    s = prs.slides.add_slide(blank)
    box(s, 0, 0, 13.333, 1.1, NAVY); box(s, 0, 1.1, 13.333, 0.06, GOLD)
    text(s, 0.6, 0.2, 12, 0.8, title, 28, RGBColor(255,255,255), True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 0.6, 7.05, 9, 0.3, FOOT[0], 10, MUTED)
    text(s, 11.8, 7.05, 1, 0.3, str(n), 10, MUTED, align=PP_ALIGN.RIGHT)
    return s


WHITE = RGBColor(255,255,255)
def divider(sesi, judul, sub, foot):
    FOOT[0] = foot
    s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY); box(s, 0.8, 4.1, 3, 0.08, GOLD)
    text(s, 0.8, 1.6, 11.5, 0.5, sesi, 16, GOLD, True)
    text(s, 0.8, 2.2, 11.5, 1.8, judul, 40, WHITE, True)
    text(s, 0.8, 4.4, 11.5, 1.2, sub, 18, RGBColor(0xDC,0xE6,0xF2))
def cards(s, items, cols=3, y0=1.7, h=4.4, size=15):
    w = (12.1 - 0.25 * (cols - 1)) / cols
    for i, (a, b) in enumerate(items):
        x = 0.6 + i * (w + 0.25); box(s, x, y0, w, h, LIGHT); box(s, x, y0, w, 0.12, GOLD)
        text(s, x + 0.2, y0 + 0.3, w - 0.4, 0.9, a, 20, NAVY, True); text(s, x + 0.2, y0 + 1.3, w - 0.4, h - 1.4, b, size)
def pairs(s, items, y0=1.5, lw=3.4, rh=0.85, gap=0.15, size=15):
    for i, (a, b) in enumerate(items):
        y = y0 + i * (rh + gap); box(s, 0.6, y, lw, rh, NAVY); text(s, 0.7, y, lw - 0.2, rh, a, size, WHITE, True, anchor=MSO_ANCHOR.MIDDLE)
        box(s, 0.6 + lw, y, 12.1 - lw, rh, LIGHT); text(s, 0.8 + lw, y, 11.7 - lw, rh, b, size, anchor=MSO_ANCHOR.MIDDLE)
def listing(s, items, cols=1, y0=1.5, rh=0.8, gap=0.12, size=16, numbered=True):
    per = (len(items) + cols - 1) // cols; w = (12.1 - 0.3 * (cols - 1)) / cols
    for i, t in enumerate(items):
        x = 0.6 + (i // per) * (w + 0.3); y = y0 + (i % per) * (rh + gap)
        box(s, x, y, w, rh, LIGHT); text(s, x + 0.2, y, w - 0.4, rh, (f"{i+1}. " if numbered else "") + t, size, anchor=MSO_ANCHOR.MIDDLE)
def note(s, t, y=6.45): text(s, 0.6, y, 12.1, 0.5, t, 13, MUTED)

# sampul program
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY); box(s, 0.8, 4.35, 3, 0.08, GOLD)
text(s, 0.8, 1.4, 11.5, 0.5, "PELATIHAN ONLINE", 16, GOLD, True)
text(s, 0.8, 2.0, 11.5, 2.3, "Account Receivable dan Income Audit Hotel", 44, WHITE, True)
text(s, 0.8, 4.7, 11.5, 1.2, ["Untuk Departemen Accounting, Hotel Vila Lumbung", "3 sesi, masing-masing 3 jam tatap muka daring"], 18, RGBColor(0xDC,0xE6,0xF2))
text(s, 0.8, 6.6, 8, 0.4, "Sanggabiz  |  Desember 2026", 14, WHITE)
# peta program
FOOT[0] = "Sanggabiz  |  AR dan Income Audit Hotel"
s = slide("Peta tiga sesi")
cards(s, [("Sesi 1", "Pendapatan hotel dan income audit: alur dokumen, night audit, kontrol dan temuan harian."),
          ("Sesi 2", "Piutang, city ledger, dan invoice: kebijakan kredit, jurnal, penyusunan dan pemeriksaan invoice."),
          ("Sesi 3", "Monitoring, rekonsiliasi, dan laporan AR: aging, mencocokkan pembayaran, laporan, kasus terpadu.")], 3, 1.7, 3.6, 16)
note(s, "Target: peserta menjalankan proses AR dan income hotel secara mandiri, dari pencatatan pendapatan sampai laporan AR.", 5.7)
divider("SESI 1 DARI 3", "Pendapatan Hotel dan Income Audit", "Alur dokumen, night audit, kontrol dan temuan harian", "Sanggabiz  |  AR dan Income Audit Hotel  |  Sesi 1")
# 2 agenda
s = slide("Tujuan dan rencana tiga jam", 2)
rows = [("15", "Pembukaan dan hasil pre-test"), ("40", "1.1 Peta pendapatan dan alur dokumen hotel"), ("55", "1.2 Night audit dan laporan harian"), ("10", "Jeda"), ("60", "1.3 Income audit harian: kontrol dan temuan")]
for i, (m, t) in enumerate(rows):
    y = 1.6 + i * 0.85; box(s, 0.6, y, 1.2, 0.65, NAVY if m != "10" else MUTED); text(s, 0.6, y, 1.2, 0.65, m + " mnt", 16, RGBColor(255,255,255), True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, 2.0, y, 6, 0.65, t, 18, anchor=MSO_ANCHOR.MIDDLE)
box(s, 8.6, 1.6, 4.2, 4.1, LIGHT)
text(s, 8.8, 1.7, 3.8, 4, ["Setelah sesi ini Anda bisa:", "Menjelaskan alur dari reservasi sampai laporan pendapatan", "Menghitung okupansi, ARR, dan RevPAR", "Menjalankan night audit dan memeriksa catatan serah terima", "Mengerjakan income audit harian dan menulis temuan"], 14)
# 3 alur
s = slide("Alur satu tagihan di hotel", 3)
steps = ["Reservasi", "Check-in", "Posting selama menginap", "Check-out", "Night audit", "Income audit", "Penagihan AR", "Laporan"]
for i, st in enumerate(steps):
    x = 0.5 + (i % 4) * 3.15; y = 1.7 + (i // 4) * 2.4
    box(s, x, y, 2.7, 1.5, NAVY if i < 4 else GOLD, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, x, y, 2.7, 1.5, [f"{i+1}", st], 17, RGBColor(255,255,255) if i < 4 else INK, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
text(s, 0.6, 6.4, 12, 0.5, "Baris atas: kegiatan tamu. Baris bawah: pemeriksaan dan penagihan. Tiap perpindahan dokumen adalah tempat kesalahan bisa masuk.", 14, MUTED)
# 4 istilah
s = slide("Tiga saldo yang sering tertukar", 4)
cols = [("Guest ledger", "Folio tamu yang masih menginap. Hilang saat tamu check-out dan membayar."), ("City ledger", "Piutang atas tagihan yang dibayar kemudian: perusahaan, agen, OTA, instansi."), ("Advance deposit", "Uang muka dari tamu. Kewajiban hotel, bukan pendapatan, sampai kamar dipakai.")]
for i, (a, b) in enumerate(cols):
    x = 0.6 + i * 4.15; box(s, x, 1.7, 3.9, 4.4, LIGHT); box(s, x, 1.7, 3.9, 0.12, GOLD)
    text(s, x + 0.2, 2.0, 3.5, 0.8, a, 22, NAVY, True); text(s, x + 0.2, 2.9, 3.5, 3, b, 16)
# 5 rasio
s = slide("Okupansi, ARR, dan RevPAR", 5)
data = [("Okupansi", "kamar terjual berbayar ÷ kamar tersedia", "28 ÷ 50 = 56%"), ("ARR", "pendapatan kamar ÷ kamar terjual berbayar", "Rp 15.240.000 ÷ 28 = Rp 544.286"), ("RevPAR", "pendapatan kamar ÷ kamar tersedia", "Rp 15.240.000 ÷ 50 = Rp 304.800")]
for i, (a, b, c) in enumerate(data):
    y = 1.6 + i * 1.5; box(s, 0.6, y, 12.1, 1.3, LIGHT); text(s, 0.8, y, 2.3, 1.3, a, 22, NAVY, True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 3.2, y, 5.2, 1.3, b, 16, anchor=MSO_ANCHOR.MIDDLE); text(s, 8.5, y, 4.1, 1.3, c, 17, INK, True, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 6.2, 12, 0.6, "Data Hotel Sampel (rekaan): 50 kamar tersedia, 28 terjual berbayar, 2 kamar komplimen dan house use dipisah.", 13, MUTED)
# 6 night audit
s = slide("Urutan night audit", 6)
na = ["Tutup shift dan setor laporan kasir", "Cocokkan POS dengan PMS", "Periksa folio terbuka", "Proses no-show dan pembatalan", "Posting kamar, service, dan pajak", "Cetak laporan harian", "Ganti tanggal dan cadangkan data", "Serahkan paket ke income audit"]
for i, st in enumerate(na):
    x = 0.6 + (i % 2) * 6.2; y = 1.5 + (i // 2) * 1.35
    box(s, x, y, 0.7, 0.7, NAVY, shape=MSO_SHAPE.OVAL); text(s, x, y, 0.7, 0.7, str(i + 1), 16, RGBColor(255,255,255), True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, x + 0.9, y, 5, 0.7, st, 17, anchor=MSO_ANCHOR.MIDDLE)
# 7 latihan 2
s = slide("Latihan: catatan serah terima", 7)
text(s, 0.6, 1.5, 12, 1, "Tandai tiap catatan: wajar atau perlu ditindaklanjuti. Tulis alasan dalam satu kalimat. Waktu 20 menit.", 18)
for i, t in enumerate(["Batch EDC shift malam belum ditutup, tiga transaksi terakhir belum masuk.", "Void folio kamar 212 Rp 605.000, kolom pemberi izin kosong.", "Folio kamar 105 dipindah ke city ledger, ada surat jaminan bertanda tangan sales."]):
    box(s, 0.6, 2.8 + i * 1.2, 12.1, 1.0, LIGHT); text(s, 0.8, 2.8 + i * 1.2, 11.7, 1.0, f"{i+1}. {t}", 16, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 6.4, 12, 0.5, "Tiga catatan lain ada di Modul Bab 2.", 13, MUTED)
# 8 kontrol
s = slide("Sepuluh kontrol income audit harian", 8)
k = ["Kelengkapan dokumen", "Tarif kamar sesuai rate code", "Jumlah kamar terjual", "Service dan pajak", "F&B POS ke PMS", "Penyelesaian per metode bayar", "Void, koreksi, diskon", "Deposit", "Transfer ke city ledger", "Komplimen dan house use"]
for i, t in enumerate(k):
    x = 0.6 + (i // 5) * 6.2; y = 1.5 + (i % 5) * 1.05
    box(s, x, y, 5.9, 0.85, LIGHT); text(s, x + 0.15, y, 5.6, 0.85, f"{i+1}. {t}", 16, anchor=MSO_ANCHOR.MIDDLE)
# 9 temuan
s = slide("Menulis temuan: fakta, dampak, tindakan", 9)
tbl = [("Fakta", "Kamar 105, tarif CORP seharusnya Rp 380.000, terposting Rp 450.000"), ("Dampak", "Tagihan lebih Rp 70.000 sebelum service dan pajak"), ("Dugaan penyebab", "Rate code tidak terpilih saat check-in"), ("Tindakan", "Koreksi folio sebelum check-out, cek reservasi lain milik pelanggan"), ("Penanggung jawab dan waktu", "Supervisor front office, hari ini")]
for i, (a, b) in enumerate(tbl):
    y = 1.5 + i * 1.0; box(s, 0.6, y, 3.4, 0.85, NAVY); text(s, 0.7, y, 3.2, 0.85, a, 15, RGBColor(255,255,255), True, anchor=MSO_ANCHOR.MIDDLE)
    box(s, 4.0, y, 8.7, 0.85, LIGHT); text(s, 4.2, y, 8.4, 0.85, b, 15, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.6, 6.6, 12, 0.4, "Tulis fakta tanpa menuduh orang. Bila penyebab belum pasti, tulis dugaan dan minta bukti.", 13, MUTED)
# 10 tugas
s = slide("Latihan utama: income audit hari kasus", 10)
text(s, 0.6, 1.5, 12, 4.5, ["Buka workbook latihan, lembar IA-Tarif kamar dan IA-Rekap.", "1. Cek tarif 30 kamar dan tandai selisih.", "2. Cocokkan F&B POS dengan PMS.", "3. Cocokkan penyelesaian per metode bayar.", "4. Tulis tiga temuan terpenting dengan format fakta, dampak, tindakan.", "Waktu: 45 menit. Bagikan layar, pengajar mendampingi."], 20)
text(s, 0.6, 6.2, 12, 0.5, "Berikutnya: Sesi 2, piutang, city ledger, dan invoice.", 14, MUTED)

divider("SESI 2 DARI 3", "Piutang, City Ledger, dan Invoice", "Kebijakan kredit, jurnal, penyusunan dan pemeriksaan invoice", "Sanggabiz  |  AR dan Income Audit Hotel  |  Sesi 2")
s = slide("Tujuan dan rencana tiga jam")
for i, (m, t) in enumerate([("35", "2.1 Jenis piutang dan kebijakan kredit"), ("50", "2.2 Alur folio ke city ledger dan jurnalnya"), ("10", "Jeda"), ("45", "2.3 Invoice dan dokumen penagihan"), ("40", "2.4 Praktik memeriksa dan memperbaiki invoice")]):
    y = 1.6 + i * 0.85; box(s, 0.6, y, 1.2, 0.65, NAVY if m != "10" else MUTED); text(s, 0.6, y, 1.2, 0.65, m + " mnt", 16, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, 2.0, y, 6.4, 0.65, t, 18, anchor=MSO_ANCHOR.MIDDLE)
box(s, 8.6, 1.6, 4.2, 4.1, LIGHT)
text(s, 8.8, 1.7, 3.8, 4, ["Setelah sesi ini Anda bisa:", "Menetapkan limit dan termin kredit", "Menyusun jurnal dari posting sampai pelunasan", "Menerbitkan invoice yang lengkap dan benar", "Menemukan dan memperbaiki kesalahan invoice"], 14)
s = slide("Jenis piutang hotel")
cards(s, [("Guest ledger", "Saldo tamu yang masih menginap. Selesai saat check-out dan bayar."), ("City ledger", "Tagihan yang dibayar kemudian: perusahaan, agen perjalanan, OTA, instansi, penyelenggara acara."), ("Pola bayar", "Instansi mengikuti proses anggaran, termin 30 sampai 45 hari lazim. OTA membayar bersih setelah komisi, satu pembayaran untuk banyak reservasi.")], 3, 1.7, 4.4, 15)
s = slide("Kebijakan kredit: lima langkah")
listing(s, ["Pelanggan mengisi formulir permohonan kredit dan menyerahkan NPWP, akta, kontak keuangan, referensi", "Pihak berwenang menyetujui limit dan termin", "Perjanjian kerja sama memuat tarif, termin, alamat penagihan, syarat dokumen", "Pelanggan baru tanpa riwayat bisa diminta bayar di muka atau deposit", "Limit dan riwayat bayar ditinjau berkala, kredit ditahan bila melewati limit atau terlambat"], 1, 1.5, 0.85, 0.15, 16)
s = slide("Latihan: tiga permohonan kredit")
pairs(s, [("PT Nusa Teknik", "Korporasi baru. Perkiraan 40 kamar-malam per bulan, tarif kontrak Standard Rp 380.000 nett. Minta termin 45 hari. Belum ada riwayat."), ("CV Cahaya Wisata", "Agen, pelanggan lama. Limit Rp 15.000.000, sisa tagihan Rp 19.745.000, ada faktur lebih dari 90 hari. Minta limit Rp 30.000.000."), ("Dinas Pendidikan Kab. Contoh", "Instansi. 20 kamar-malam per bulan, bayar sekitar 45 hari mengikuti anggaran. Minta surat tugas jadi dasar tagihan.")], 1.5, 3.0, 1.25, 0.2, 15)
note(s, "Putuskan: disetujui atau tidak, limit, termin, syarat dokumen, dan alasan. Waktu 15 menit.", 6.0)
s = slide("Jurnal dari posting sampai pelunasan")
pairs(s, [("1. Posting satu malam", "Debit guest ledger 605.000. Kredit pendapatan kamar 500.000, utang service 50.000, utang pajak hotel 55.000"), ("2. Check-out ke city ledger", "Debit city ledger perusahaan 605.000. Kredit guest ledger 605.000"), ("3. Perusahaan melunasi", "Debit bank 605.000. Kredit city ledger perusahaan 605.000"), ("Advance deposit", "Diterima: debit bank, kredit advance deposit. Check-out: debit advance deposit, kredit guest ledger")], 1.5, 3.6, 0.95, 0.15, 15)
note(s, "Nama akun contoh. Perlakuan service charge mengikuti kebijakan hotel Anda.", 6.35)
s = slide("Latihan: lima jurnal")
listing(s, ["Tamu mengirim deposit Rp 500.000 lewat transfer bank sebelum menginap", "Posting satu malam kamar: tarif nett Rp 500.000, service 10 persen, pajak 10 persen dari tarif plus service", "Saat check-out, deposit Rp 500.000 dipakai mengurangi folio", "Sisa folio dibayar tunai di kasir", "Folio tamu perusahaan Rp 1.210.000 dipindah ke city ledger PT Maju Bersama"], 1, 1.5, 0.85, 0.15, 16)
note(s, "Waktu 25 menit. Bagikan layar, tulis jurnal di Modul Bab 3.", 6.4)
s = slide("Unsur invoice yang lengkap")
listing(s, ["Nomor invoice unik dan berurutan", "Tanggal invoice", "Nama dan alamat pelanggan sesuai perjanjian", "NPWP bila diminta", "Uraian: tanggal, tipe kamar, kamar, malam", "Tarif sama dengan folio dan kontrak", "Service dan pajak, dasar hitung benar", "Termin dan jatuh tempo sesuai perjanjian", "Nomor PO, voucher, nomor folio", "Rekening pembayaran dan lampiran"], 2, 1.5, 0.85, 0.12, 15)
s = slide("Contoh perhitungan invoice")
pairs(s, [("Tarif nett", "3 kamar x 2 malam x Rp 500.000 = Rp 3.000.000"), ("Service 10 persen", "Rp 300.000"), ("Pajak 10 persen", "10 persen dari (3.000.000 + 300.000) = Rp 330.000"), ("Total ditagih", "Rp 3.630.000"), ("Jatuh tempo", "10 Desember 2026 ditambah termin 30 hari = 9 Januari 2027")], 1.5, 3.4, 0.85, 0.15, 16)
note(s, "Dasar pajak adalah tarif ditambah service. Bila dasar hotel Anda berbeda, ikuti dasar hotel Anda.", 6.5)
s = slide("Latihan: isi invoice di workbook")
text(s, 0.6, 1.5, 12, 4.5, ["Buka lembar Invoice di workbook.", "Pelanggan PT Maju Bersama, 3 kamar Deluxe tarif CORP, 8 sampai 10 Desember 2026.", "Termin 30 hari. Referensi PO-2025-118 dan folio 8841.", "Isi invoice, hitung total dan jatuh tempo.", "Pengajar berperan sebagai staf keuangan pelanggan dan memeriksa invoice Anda."], 20)
note(s, "Waktu 15 menit.", 6.4)
s = slide("Latihan: periksa tiga invoice")
pairs(s, [("A. PT Alfa", "2 kamar Standard CORP Rp 380.000, 2 malam, nett Rp 1.520.000. Service Rp 152.000. Pajak Rp 152.000. Total Rp 1.824.000. Kolom PO kosong. Kontrak: pajak 10 persen dari tarif plus service, PO wajib."), ("B. Dinas Pendidikan Kota Contoh", "Invoice 1 Desember 2026. Termin 14 hari. Jatuh tempo 15 Desember 2026. Perjanjian dengan Dinas Pendidikan Kab. Contoh: termin 45 hari."), ("C. CV Cahaya Wisata", "1 kamar Deluxe, 3 malam, Rp 600.000 per malam. Folio: 2 malam, tarif OTA Rp 560.000 per malam.")], 1.5, 3.0, 1.35, 0.2, 14)
note(s, "Temukan dua kesalahan di tiap invoice, tulis versi benar, lalu susun draf credit note untuk satu invoice. Waktu 30 menit.", 6.3)
s = slide("Koreksi: credit note dan rebill")
cards(s, [("Jangan menghapus", "Invoice yang sudah terkirim tidak dihapus. Setiap koreksi meninggalkan jejak dokumen."), ("Credit note", "Menurunkan tagihan pada invoice yang salah. Punya nomor sendiri dan merujuk invoice asal."), ("Rebill", "Invoice baru yang benar, dengan nomor baru, bila tagihan perlu diterbitkan ulang. Catat keduanya di city ledger.")], 3, 1.7, 4.2, 15)
s = slide("Ringkasan sesi 2 dan persiapan sesi 3")
text(s, 0.6, 1.5, 12, 4.5, ["Yang sudah dikerjakan: keputusan kredit, jurnal lima transaksi, satu invoice, tiga invoice terperiksa.", "Persiapan sesi 3: buka workbook, lembar City Ledger dan Rekon Bank.", "Berikutnya: aging, rekonsiliasi pembayaran, dan laporan AR."], 20)

divider("SESI 3 DARI 3", "Monitoring, Rekonsiliasi, dan Laporan AR", "Aging, mencocokkan pembayaran, laporan, kasus terpadu", "Sanggabiz  |  AR dan Income Audit Hotel  |  Sesi 3")
s = slide("Tujuan dan rencana tiga jam")
for i, (m, t) in enumerate([("40", "3.1 Aging dan monitoring outstanding"), ("45", "3.2 Rekonsiliasi pembayaran"), ("10", "Jeda"), ("35", "3.3 Laporan AR"), ("25", "3.4 Kasus terpadu"), ("25", "Penutup: post-test, survei, rencana 30 hari")]):
    y = 1.5 + i * 0.8; box(s, 0.6, y, 1.2, 0.62, NAVY if m != "10" else MUTED); text(s, 0.6, y, 1.2, 0.62, m + " mnt", 16, WHITE, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    text(s, 2.0, y, 6.4, 0.62, t, 17, anchor=MSO_ANCHOR.MIDDLE)
box(s, 8.6, 1.5, 4.2, 4.5, LIGHT)
text(s, 8.8, 1.6, 3.8, 4.3, ["Setelah sesi ini Anda bisa:", "Menyusun umur piutang dan memilih prioritas penagihan", "Mencocokkan pembayaran masuk dengan faktur", "Menyusun laporan AR satu halaman", "Menangani beberapa kejadian sekaligus"], 14)
s = slide("Aging: hari lewat jatuh tempo")
pairs(s, [("Sisa tagihan", "Jumlah faktur dikurangi dibayar"), ("Jatuh tempo", "Tanggal faktur ditambah termin"), ("Hari lewat jatuh tempo", "Tanggal laporan dikurangi jatuh tempo. Nol bila belum jatuh tempo atau lunas"), ("Kelompok umur", "Belum jatuh tempo, 1-30, 31-60, 61-90, lebih dari 90 hari")], 1.5, 3.6, 1.0, 0.2, 16)
note(s, "Pilih satu cara hitung (dari jatuh tempo atau dari tanggal faktur) dan konsisten di semua laporan.", 6.2)
s = slide("Prioritas dan siklus pengingat")
cards(s, [("Urutan prioritas", "Nilai sisa tagihan, umur keterlambatan, dan riwayat pelanggan. Pelanggan yang melewati limit ikut diprioritaskan."), ("Siklus pengingat (usulan)", "H-3 surel pengingat. H+1 surel dan pesan. H+7 telepon. H+14 surat peringatan. H+30 eskalasi ke manajer keuangan dan GM."), ("Catatan penagihan", "Tanggal, siapa dihubungi, hasil, dan janji bayar. Jadi bukti bila perlu eskalasi.")], 3, 1.7, 4.4, 15)
s = slide("Latihan: aging city ledger")
text(s, 0.6, 1.5, 12, 4.5, ["Buka lembar City Ledger di workbook. Tanggal laporan 10 Desember 2026.", "Tulis rumus sisa tagihan, jatuh tempo, hari lewat, dan kelompok umur untuk 19 faktur.", "Pilih lima faktur yang ditagih lebih dulu dan jelaskan alasannya.", "Catatan: lembar ini belum memuat pembayaran yang baru masuk di bank."], 20)
note(s, "Waktu 30 menit.", 6.4)
s = slide("Rekonsiliasi pembayaran: lima langkah")
listing(s, ["Ambil mutasi bank dan daftar faktur terbuka pada tanggal yang sama", "Cocokkan lewat nomor faktur di berita transfer, nama pengirim, dan jumlah", "Tanpa nomor faktur: minta konfirmasi tertulis, aplikasikan ke faktur terlama hanya bila kebijakan mengizinkan", "Hitung selisih tiap mutasi, tentukan jenisnya, catat jurnalnya", "Mutasi tidak dikenali: dana belum teridentifikasi sampai pengirim jelas"], 1, 1.5, 0.85, 0.15, 16)
s = slide("Jenis selisih dan perlakuannya")
pairs(s, [("Beberapa ribu rupiah", "Biaya transfer dipotong pelanggan. Catat biaya bank, lalu lunaskan atau tagih selisih"), ("Bayar kurang atau lebih", "Aplikasikan sebagian bila kurang. Bila lebih, catat kewajiban ke pelanggan"), ("Komisi OTA", "OTA membayar bersih. Debit komisi OTA, kredit city ledger sebesar tagihan penuh"), ("Tanpa nomor faktur", "Konfirmasi alokasi ke pelanggan"), ("Tidak dikenali", "Dana belum teridentifikasi, telusuri lewat bank dan front office")], 1.5, 3.4, 0.85, 0.15, 14)
s = slide("Contoh jurnal komisi OTA")
pairs(s, [("Tagihan", "Rp 21.780.000"), ("Komisi 15 persen", "Rp 3.267.000"), ("Diterima di bank", "Rp 18.513.000"), ("Jurnal", "Debit bank 18.513.000. Debit komisi OTA 3.267.000. Kredit city ledger OTA 21.780.000")], 1.5, 3.4, 1.0, 0.2, 17)
note(s, "Perlakuan bergantung pada jenis perjanjian dengan OTA. Konfirmasi dengan bagian keuangan hotel Anda.", 6.2)
s = slide("Latihan: tujuh mutasi bank")
text(s, 0.6, 1.5, 12, 4.5, ["Buka lembar Rekon Bank di workbook.", "Untuk tiap mutasi tulis: faktur yang dicocokkan, selisih, dan perlakuan.", "Siapkan jurnal untuk selisih yang ada."], 20)
note(s, "Waktu 25 menit.", 6.4)
s = slide("Isi laporan AR bulanan")
listing(s, ["Total piutang dan perubahannya dari bulan lalu", "Umur piutang dalam lima kelompok, dengan persentase", "Piutang per pelanggan terhadap limit kredit", "DSO dan persentase piutang lewat jatuh tempo lebih dari 30 hari", "Tiga temuan dan tiga tindakan, dengan penanggung jawab dan tanggal"], 1, 1.5, 0.85, 0.15, 16)
s = slide("DSO, buku besar, dan penyisihan")
cards(s, [("DSO", "Total piutang dibagi penjualan kredit 90 hari terakhir, dikali 90. Bandingkan dengan termin rata-rata pelanggan."), ("Buku pembantu dan buku besar", "Saldo city ledger harus sama dengan akun di buku besar. Bila beda, telusuri transaksi sebelum membuat jurnal penyesuaian."), ("Penyisihan", "PSAK 71 meminta kerugian kredit diperkirakan lebih awal. Persentase per kelompok umur ditetapkan hotel. Penghapusan butuh persetujuan pihak berwenang.")], 3, 1.7, 4.6, 14)
s = slide("Latihan: laporan AR")
text(s, 0.6, 1.5, 12, 4.5, ["Lengkapi lembar Laporan AR di workbook.", "Tulis tiga rekomendasi tindakan.", "Sampaikan tiga poin utama lisan dalam satu menit, seolah kepada Financial Controller."], 20)
note(s, "Waktu 25 menit.", 6.4)
s = slide("Kasus terpadu: Senin pagi di Hotel Sampel")
listing(s, ["Income audit menemukan transfer folio Rp 505.000 ke city ledger tanpa otorisasi dan dokumen", "Keuangan PT Maju Bersama menelepon: tarif di invoice terbaru lebih tinggi dari kontrak", "Mutasi bank menunjukkan transfer masuk Rp 1.000.000 tanpa keterangan", "Sales meminta persetujuan booking 10 kamar untuk CV Cahaya Wisata dengan termin 14 hari", "Financial Controller meminta laporan aging untuk rapat pukul 14.00"], 1, 1.5, 0.85, 0.15, 16)
note(s, "Tentukan urutan penanganan. Untuk tiap kejadian: tindakan, dokumen, dan penanggung jawab. Waktu 25 menit.", 6.4)
s = slide("Penutup: ukur hasil dan rencana penerapan")
listing(s, ["Post-test 15 butir pilihan ganda dan 2 uraian", "Survei kepuasan, enam butir dan dua pertanyaan terbuka", "Rencana penerapan 30 hari: tiga hal, dengan tanggal dan tanda selesai"], 1, 1.5, 1.0, 0.2, 18)
note(s, "Sertifikat diterbitkan setelah syarat kehadiran dan hasil kerja terpenuhi.", 5.6)
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY); box(s, 0.8, 4.0, 3, 0.08, GOLD)
text(s, 0.8, 2.2, 11.5, 1.5, "Terima kasih", 48, WHITE, True)
text(s, 0.8, 4.4, 11.5, 1.5, ["Sanggabiz", "WhatsApp 0877-7413-4288  |  www.sanggabiz.com  |  partnership@sanggabiz.com"], 18, RGBColor(0xDC,0xE6,0xF2))
OUT.parent.mkdir(exist_ok=True); prs.save(OUT); print('ditulis', OUT, len(prs.slides), 'slide')
