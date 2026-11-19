#!/usr/bin/env python3
"""Slide Sesi 1. Jalankan: python3 build_slide.py"""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

NAVY, GOLD, INK, MUTED, LIGHT = RGBColor(0x0B,0x39,0x6D), RGBColor(0xFF,0xC0,0x0C), RGBColor(0x1D,0x1D,0x1F), RGBColor(0x5C,0x5F,0x66), RGBColor(0xEE,0xF3,0xF9)
OUT = Path(__file__).resolve().parent.parent / "assets" / "7 Slide Sesi 1 Pendapatan Hotel dan Income Audit.pptx"
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]

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
def slide(title, n):
    s = prs.slides.add_slide(blank)
    box(s, 0, 0, 13.333, 1.1, NAVY); box(s, 0, 1.1, 13.333, 0.06, GOLD)
    text(s, 0.6, 0.2, 12, 0.8, title, 28, RGBColor(255,255,255), True, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 0.6, 7.05, 9, 0.3, "Sanggabiz  |  AR dan Income Audit Hotel  |  Sesi 1", 10, MUTED)
    text(s, 11.8, 7.05, 1, 0.3, str(n), 10, MUTED, align=PP_ALIGN.RIGHT)
    return s

# 1 sampul
s = prs.slides.add_slide(blank); box(s, 0, 0, 13.333, 7.5, NAVY); box(s, 0.8, 4.35, 3, 0.08, GOLD)
text(s, 0.8, 1.5, 11.5, 0.5, "SESI 1 DARI 3", 16, GOLD, True)
text(s, 0.8, 2.1, 11.5, 2.2, ["Pendapatan Hotel dan Income Audit"], 44, RGBColor(255,255,255), True)
text(s, 0.8, 4.7, 11.5, 1.2, ["Pelatihan Online Account Receivable dan Income Audit Hotel", "Untuk Departemen Accounting, Hotel Vila Lumbung"], 18, RGBColor(0xDC,0xE6,0xF2))
text(s, 0.8, 6.6, 8, 0.4, "Sanggabiz  |  Desember 2026", 14, RGBColor(255,255,255))
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
OUT.parent.mkdir(exist_ok=True); prs.save(OUT); print("ditulis", OUT)
