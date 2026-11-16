"""Deck materi pelatihan AI Agent MyFundAction untuk dipresentasikan trainer di kelas.

Isi modul, topik, aktivitas, dan rubrik diambil dari silabus_data.py dan prompt_data.py
supaya sama dengan silabus. Catatan trainer ada di speaker notes tiap slide.
"""
import os

from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

import build_data
import prompt_data as P
import silabus_data as d
from deck_lib import (BLUE, CYAN, GREY, GREY_L, INK, LILAC, LOGO, ML, MUTED, SH, SW, TEAL, TEAL_M, TEAL_T, ZEBRA,
                      garis, isi_kotak, kerangka, kotak, new_prs, rgb, tabel, teks)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "aset", "v2 Materi Pelatihan AI Agent - MyFundAction.pptx")
LABEL = "Materi Pelatihan AI Agent | MyFundAction | v2"
GELAP = "0D5C5B"
MONO = "Courier New"
CW = SW - 2 * ML

prs = new_prs()
MOD = {m["kode"]: m for m in d.MODUL}
TOP = {t["kode"]: t for m in d.MODUL for t in m["topik"]}
KUNCI = build_data.jalankan()


def catatan(s, teks_):
    s.notes_slide.notes_text_frame.text = "Catatan trainer: " + teks_


def slide(judul_h, judul_t=None, sub=None):
    return kerangka(prs, judul_h, judul_t, sub, label=LABEL)


def poin(judul_h, judul_t, sub, items, kanan=None, size=16, lebar_kiri=None, notes=None, y0=1.5):
    s = slide(judul_h, judul_t, sub)
    wl = lebar_kiri or (CW if not kanan else CW * 0.58)
    for i, it in enumerate(items):
        y = y0 + i * (5.2 / max(len(items), 4))
        o = kotak(s, ML, y + 0.06, 0.36, 0.36, TEAL, shape=MSO_SHAPE.OVAL)
        isi_kotak(o, str(i + 1), size=11, bold=True, color="FFFFFF")
        runs = it if isinstance(it, list) else [(it, False, INK)]
        teks(s, ML + 0.5, y, wl - 0.5, 1.2, [runs], size=size)
    if kanan:
        jdl, baris, warna = kanan
        x = ML + wl + 0.3
        w = CW - wl - 0.3
        k = kotak(s, x, y0, w, 0.55, warna)
        isi_kotak(k, jdl, size=13, bold=True, color="FFFFFF")
        b = kotak(s, x, y0 + 0.55, w, 5.0 - 0.55, TEAL_M if warna == TEAL else "EAF3FC")
        isi_kotak(b, [[(t, False, INK)] for t in baris], size=14, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
        b.text_frame.margin_top = Inches(0.15)
        for p in b.text_frame.paragraphs:
            p.space_after = Pt(8)
    if notes:
        catatan(s, notes)
    return s


def kode_slide(judul_h, judul_t, sub, kode, samping=None, size=12, notes=None, h=5.0):
    s = slide(judul_h, judul_t, sub)
    w = CW if not samping else CW * 0.62
    k = kotak(s, ML, 1.45, w, h, "F2F8F9", line=GREY)
    tf = k.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.15)
    for i, baris in enumerate(kode.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = baris if baris else " "
        r.font.name = MONO
        r.font.size = Pt(size)
        r.font.color.rgb = rgb("0E5E5D" if baris.strip().startswith("<") else INK)
    if samping:
        x = ML + w + 0.3
        jdl, baris = samping
        teks(s, x, 1.45, CW - w - 0.3, 0.4, jdl, size=14, bold=True, color=TEAL_T)
        teks(s, x, 1.95, CW - w - 0.3, h - 0.5, baris, size=14)
        for p in s.shapes[-1].text_frame.paragraphs:
            p.space_after = Pt(8)
    if notes:
        catatan(s, notes)
    return s


def grid(judul_h, judul_t, sub, items, cols=3, notes=None, y0=1.5, tinggi=None, size=15):
    s = slide(judul_h, judul_t, sub)
    rows = (len(items) + cols - 1) // cols
    gap = 0.25
    w = (CW - gap * (cols - 1)) / cols
    hgt = tinggi or (3.4 if rows == 1 else (5.1 - gap * (rows - 1)) / rows)
    for i, (jdl, isi, warna) in enumerate(items):
        x = ML + (i % cols) * (w + gap)
        y = y0 + (i // cols) * (hgt + gap)
        top = kotak(s, x, y, w, 0.55, warna, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
        isi_kotak(top, jdl, size=13, bold=True, color="FFFFFF")
        b = kotak(s, x, y + 0.6, w, hgt - 0.6, GREY_L, line=GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
        isi_kotak(b, isi if isinstance(isi, list) else [isi], size=size, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
        b.text_frame.margin_top = Inches(0.12)
        for p in b.text_frame.paragraphs:
            p.space_after = Pt(6)
    if notes:
        catatan(s, notes)
    return s


def pembatas(kode_m, sesi):
    m = MOD[kode_m]
    s = prs.slides.add_slide(prs.slide_layouts[6])
    kotak(s, 0, 0, SW, SH, GELAP)
    kotak(s, 0, 0, 0.35, SH, CYAN)
    s.shapes.add_picture(LOGO, Inches(SW - 2.4), Inches(0.5), height=Inches(0.36))
    teks(s, 0.9, 0.9, 8, 0.5, f"MODUL {kode_m[1:]}  |  {sesi}", size=14, bold=True, color=CYAN)
    teks(s, 0.9, 1.4, 11.5, 1.0, m["judul"], size=40, bold=True, color="FFFFFF")
    teks(s, 0.9, 2.35, 11.5, 0.5, f"{m['judul_id']}  |  {sum(t['menit'] for t in m['topik'])} menit", size=18, color="CDE9E9")
    teks(s, 0.9, 3.1, 11.3, 0.8, m["fokus"], size=16, color="FFFFFF", italic=True)
    teks(s, 0.9, 4.0, 11.3, 0.4, "Setelah modul ini, peserta mampu:", size=13, bold=True, color=CYAN)
    teks(s, 0.9, 4.45, 11.3, 2.6, [f"{t['kode']}  {t['tujuan']}" for t in m["topik"]], size=13, color="FFFFFF")
    for p in s.shapes[-1].text_frame.paragraphs:
        p.space_after = Pt(6)
    catatan(s, f"Sampaikan fokus modul dan tujuan dengan kata sendiri. Prasyarat: {m['prasyarat']}.")
    return s


def aktivitas(kode_t, judul_akt=None, notes=None):
    t = TOP[kode_t]
    s = slide("Aktivitas", f"Topik {kode_t}", f"{judul_akt or t['judul']}  |  {t['menit']} menit  |  {t['format']}")
    n = len(t["aktivitas"])
    gap = 0.25
    w = (CW - gap * (n - 1)) / n
    mulai = 0
    for i, (menit, langkah) in enumerate(t["aktivitas"]):
        x = ML + i * (w + gap)
        top = kotak(s, x, 1.5, w, 0.6, TEAL if i % 2 == 0 else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
        isi_kotak(top, f"Langkah {i + 1}  |  menit {mulai}-{mulai + menit}", size=13, bold=True, color="FFFFFF")
        b = kotak(s, x, 2.15, w, 2.6, GREY_L, line=GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
        isi_kotak(b, langkah, size=16 if n <= 3 else 14, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
        b.text_frame.margin_top = Inches(0.12)
        if i < n - 1:
            garis(s, x + w + 0.02, 3.45, x + w + gap - 0.02, 3.45, TEAL, 1.5, panah=True)
        mulai += menit
    for i, (jdl, isi) in enumerate([("Bahan", t["alat"]), ("Output", t["output"]), ("Berhasil bila", t["ukuran"])]):
        x = ML + i * (CW / 3)
        k = kotak(s, x, 5.0, CW / 3 - 0.15, 1.75, LILAC if i == 2 else TEAL_M, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        isi_kotak(k, [[(jdl, True, TEAL_T if i < 2 else INK)], [(isi, False, INK)]], size=12, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
        k.text_frame.margin_top = Inches(0.1)
    catatan(s, notes or "Pasang pengatur waktu sesuai menit tiap langkah. Asisten berkeliling, peserta daring dibantu di ruang breakout.")
    return s


# =====================================================================
# Pembuka
# =====================================================================
s = prs.slides.add_slide(prs.slide_layouts[6])
kotak(s, 0, 0, SW, SH, GELAP)
kotak(s, 0, 0, 0.35, SH, CYAN)
s.shapes.add_picture(LOGO, Inches(0.9), Inches(0.8), height=Inches(0.55))
teks(s, 0.9, 2.2, 11, 0.5, "MATERI PELATIHAN", size=16, bold=True, color=CYAN)
teks(s, 0.9, 2.7, 11.5, 1.6, d.PROGRAM["judul"], size=40, bold=True, color="FFFFFF")
teks(s, 0.9, 4.25, 11, 0.5, "Claude, prompt engineering, dan AI Agent dengan Hermes", size=18, color="E6F4F4")
teks(s, 0.9, 5.6, 11, 0.9, ["MyFundAction  |  November 2026", "[ISI TIM: nama trainer]"], size=14, color="FFFFFF")
catatan(s, "Sambutan MFA lebih dulu. Perkenalkan trainer dan asisten. Pastikan peserta daring bisa mendengar dan melihat layar.")

poin("Hari Ini Kita", "Akan Bisa", "Hasil yang dibawa pulang setiap peserta", [
    "Memakai Claude untuk tugas kerja nyata dan memeriksa hasilnya",
    "Menulis prompt dengan 6 unsur yang sama di Indonesia, Malaysia, dan Australia",
    "Memasang Hermes Agent dan menjalankan agen pertama lewat Telegram dengan aman",
    "Menjalankan agen untuk segmentasi donatur, brief iklan, dan laporan kampanye",
    "Membawa pulang draf Standar Prompt MFA dan rencana agen 30 hari",
], kanan=("Yang kita pakai", ["Laptop dan Claude", "Telegram di ponsel", "Lembar kerja", "Pustaka prompt", "Data latihan rekaan"], TEAL),
    notes="Tanyakan satu harapan dari tiap peserta dalam satu kalimat. Catat di papan dan kembali ke daftar ini di penutup.")

s = slide("Alur", "Pelatihan", d.SKEMA_B["ringkas"])
for i, ses in enumerate(d.SKEMA_B["sesi"]):
    x = ML + i * (CW / 4)
    w = CW / 4 - 0.2
    top = kotak(s, x, 1.5, w, 0.9, TEAL if i % 2 == 0 else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    nama = ses["nama"].split(": ")
    isi_kotak(top, [[(nama[0] + "  |  " + ses["bentuk"], True, "FFFFFF")], [(nama[1], False, "FFFFFF")]], size=12)
    isi = [r[2] for r in ses["rundown"]]
    b = kotak(s, x, 2.5, w, 2.9, GREY_L, line=GREY)
    isi_kotak(b, isi, size=11, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    b.text_frame.margin_top = Inches(0.1)
teks(s, ML, 5.6, CW, 0.4, "Aturan main kelas", size=13, bold=True, color=TEAL_T)
teks(s, ML, 6.0, CW, 0.9, "Laptop terbuka, ponsel untuk Telegram. Semua latihan memakai data rekaan. Bertanya kapan saja, peserta daring lewat kolom chat. Bila tertahan lebih dari 5 menit, angkat tangan.", size=12)
catatan(s, "Untuk Skema A satu hari, urutan modulnya sama. Lihat tab Rundown Skema A di silabus.")

s = poin("Pre-test", "10 Menit", "Soal yang sama diulang di akhir untuk mengukur kemajuan", [
    "Bagian A: 10 soal pilihan ganda tentang AI, Claude, prompt, agen, dan Hermes",
    "Bagian B: tulis satu prompt untuk pesan terima kasih donatur program air bersih di Malaysia",
    "Tidak ada nilai lulus. Skor hanya dipakai untuk melihat kemajuan dan menyesuaikan tempo kelas",
], notes="Bagikan lembar pre-test. Bagian B dinilai dengan rubrik 6 unsur setelah sesi. Jangan bahas jawaban sekarang.")

# =====================================================================
# M1
# =====================================================================
pembatas("M1", "Sesi 1")
s = slide("Apa Itu", "AI Generatif", "Topik 1.1")
for i, (r, jdl, ket, warna) in enumerate([(5.0, "Kecerdasan artifisial (AI)", "Mesin mengerjakan tugas yang biasanya butuh kecerdasan manusia", "CDE9E9"),
                                           (3.6, "Machine learning", "Mesin belajar pola dari data, bukan dari aturan yang ditulis satu per satu", "8FD0CF"),
                                           (2.2, "AI generatif dan LLM", "Membuat teks, gambar, dan kode baru. Contoh: Claude", TEAL)]):
    cx, cy = ML + 2.7, 4.2
    o = kotak(s, cx - r / 2 * 1.05, cy - r / 2 + (5.0 - r) * 0.18, r * 1.05, r, warna, shape=MSO_SHAPE.OVAL)
teks(s, ML + 0.6, 1.85, 4.2, 0.4, "Kecerdasan artifisial", size=12, bold=True, align=PP_ALIGN.CENTER)
teks(s, ML + 1.2, 2.75, 3.0, 0.4, "Machine learning", size=12, bold=True, align=PP_ALIGN.CENTER)
teks(s, ML + 1.6, 4.25, 2.2, 0.8, ["AI generatif", "(LLM)"], size=13, bold=True, color="FFFFFF", align=PP_ALIGN.CENTER)
teks(s, ML + 6.2, 1.6, CW - 6.2, 5, [
    [("AI: ", True, TEAL_T), ("payung besar untuk mesin yang mengerjakan tugas yang biasanya butuh kecerdasan manusia.", False, INK)],
    [("Machine learning: ", True, TEAL_T), ("mesin belajar pola dari banyak contoh, bukan dari aturan yang ditulis programmer satu per satu.", False, INK)],
    [("AI generatif: ", True, TEAL_T), ("membuat konten baru. LLM (large language model) seperti Claude membuat teks.", False, INK)],
    [("Yang kita pakai hari ini ", True, INK), ("ada di lingkaran paling dalam.", False, INK)],
], size=15)
for p in s.shapes[-1].text_frame.paragraphs:
    p.space_after = Pt(14)
catatan(s, "Cukup 2 menit. Tujuannya peserta tahu Claude adalah LLM, dan LLM adalah satu jenis AI.")

s = slide("Cara Kerja LLM:", "Menebak Kata Berikutnya", "Ilustrasi, bukan angka sebenarnya")
teks(s, ML, 1.6, CW, 0.6, [[("Kalimat: ", True, INK), ("Program air bersih membantu warga desa mendapatkan ...", False, INK)]], size=18)
for i, (kata, pct) in enumerate([("air", 0.62), ("akses", 0.21), ("sumur", 0.09), ("bantuan", 0.05), ("listrik", 0.03)]):
    y = 2.5 + i * 0.62
    teks(s, ML, y, 1.6, 0.5, kata, size=16, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    kotak(s, ML + 1.7, y + 0.08, 6.0 * pct / 0.62, 0.38, TEAL if i == 0 else "8FD0CF")
    teks(s, ML + 1.8 + 6.0 * pct / 0.62, y, 1, 0.5, f"{int(pct * 100)}%", size=13, anchor=MSO_ANCHOR.MIDDLE)
k = kotak(s, ML + 8.6, 2.4, CW - 8.6, 3.2, LILAC, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
isi_kotak(k, [[("Akibatnya", True, INK)], [("LLM memilih kata yang paling mungkin, bukan mencari fakta di basis data.", False, INK)],
              [("Jawaban yang lancar belum tentu benar.", True, INK)], [("Seperti pelengkap otomatis di ponsel, dengan skala yang sangat besar.", False, INK)]],
          size=13, align=PP_ALIGN.LEFT)
catatan(s, "Pakai analogi pelengkap otomatis keyboard ponsel. Tekankan: lancar tidak sama dengan benar.")

s = slide("Halusinasi:", "Salah dengan Yakin", "Pertanyaan: berapa sumur yang dibangun MFA di program air bersih tahun ini?")
for i, (jdl, isi, warna) in enumerate([
    ("Jawaban A", "Tahun ini MyFundAction telah membangun 47 sumur yang melayani lebih dari 12.000 warga di 9 provinsi.", "C0504D"),
    ("Jawaban B", "Saya tidak punya data jumlah sumur MyFundAction tahun ini. Bila Anda mengunggah laporan program, saya bisa merangkumnya.", TEAL),
]):
    x = ML + i * (CW / 2)
    top = kotak(s, x, 1.6, CW / 2 - 0.25, 0.6, warna)
    isi_kotak(top, jdl, size=14, bold=True, color="FFFFFF")
    b = kotak(s, x, 2.2, CW / 2 - 0.25, 2.0, GREY_L, line=GREY)
    isi_kotak(b, isi, size=15, align=PP_ALIGN.LEFT)
teks(s, ML, 4.5, CW, 2.2, [
    [("Jawaban A terdengar meyakinkan, tetapi semua angkanya dikarang. ", True, INK), ("Ini disebut halusinasi.", False, INK)],
    [("Cara mengurangi: ", True, TEAL_T), ("beri AI bahan resmi, larang angka di luar bahan, dan periksa setiap angka sebelum dipakai.", False, INK)],
], size=15)
catatan(s, "Tanyakan dulu ke peserta mana yang dikarang sebelum membuka penjelasan. Contoh ini ilustrasi, angkanya rekaan.")

grid("Dari Chatbot", "ke Agen", "Perkembangan yang relevan untuk pekerjaan kita", [
    ("Chatbot", ["Tanya jawab teks", "Pengetahuan terbatas pada yang dipelajari model"], "8FD0CF"),
    ("Asisten kerja", ["Membaca berkas, tabel, dan gambar", "Ruang kerja dengan instruksi tetap, misalnya Claude Projects"], TEAL),
    ("Agen", ["Merencanakan langkah dan memakai alat", "Bekerja terjadwal dan lewat aplikasi chat", "Beberapa agen bisa bekerja sama, misalnya Hermes"], BLUE),
], cols=3, size=16, notes="Ini jembatan ke Modul 4. Cukup 2 menit.")

aktivitas("1.1")
grid("Peta Tugas:", "Hijau, Kuning, Merah", "Topik 1.2  |  Contoh dari pekerjaan CRM dan marketing", [
    ("Hijau: AI", ["Ide judul dan caption", "Ringkasan laporan publik", "Draf brief iklan", "Terjemahan awal"], "4E9A52"),
    ("Kuning: AI lalu diperiksa", ["Pesan untuk donatur", "Analisis kinerja kampanye", "Jawaban pertanyaan donatur", "Teks iklan yang akan tayang"], "D9A400"),
    ("Merah: bukan untuk AI", ["Data pribadi donatur sebelum ada kebijakan", "Angka dampak tanpa sumber", "Keputusan soal uang", "Persetujuan akhir publikasi"], "C0504D"),
], cols=3, size=16, notes="Contoh ini pancingan. Peserta menempatkan tugas mereka sendiri di aktivitas berikutnya.")

poin("Batas dan", "Aturan Dasar", "Topik 1.2", [
    [("Data pribadi donatur ", True, INK), ("dilindungi UU 27 Tahun 2022 tentang Pelindungan Data Pribadi. Malaysia dan Australia punya aturannya sendiri.", False, INK)],
    [("Angka dampak program ", True, INK), ("hanya dari laporan resmi. AI tidak boleh mengarang jumlah penerima manfaat atau progres.", False, INK)],
    [("Keputusan soal uang dan publikasi ", True, INK), ("tetap di tangan orang.", False, INK)],
    [("Aturan dasar: AI membuat draf, manusia memeriksa dan memutuskan.", True, TEAL_T)],
], notes="Aturan dasar ini diulang di setiap modul, termasuk saat menyusun SOUL.md agen.")
aktivitas("1.2", notes="Siapkan papan tiga kolom dan kartu tempel tiga warna. Peserta daring memakai papan daring. Tandai 3 tugas untuk latihan Modul 7.")

# =====================================================================
# M2
# =====================================================================
pembatas("M2", "Sesi 1")
grid("Mengenal", "Claude", "Topik 2.1", [
    ("Di mana", ["claude.ai di peramban", "Aplikasi desktop", "Aplikasi ponsel"], TEAL),
    ("Model", ["Pilih model di kotak percakapan", "Model lebih kuat untuk analisis dan tulisan panjang"], BLUE),
    ("Unggah berkas", ["PDF, gambar, tabel", "Claude membaca isinya sebelum menjawab"], TEAL),
    ("Projects", ["Instruksi tetap untuk semua percakapan", "Berkas pengetahuan yang dipakai berulang"], BLUE),
    ("Riwayat", ["Percakapan tersimpan", "Bisa dicari dan dilanjutkan"], TEAL),
    ("Privasi", ["Jangan unggah data donatur asli, kata sandi, atau kunci API ke akun pribadi"], "C0504D"),
], cols=3, notes="Demonstrasikan langsung di layar. Fitur per paket berbeda, cek paket akun MFA sebelum kelas.")

kode_slide("Claude Projects:", "Instruksi Tetap", "Contoh instruksi untuk Project Latihan MFA",
           "Kamu membantu tim CRM dan marketing MyFundAction.\n\nProgram kami: Palestina, pembangunan masjid, dan air bersih.\nAudiens kami: donatur di Indonesia, Malaysia, dan Australia.\n\nJawab dalam bahasa Indonesia kecuali diminta lain.\nJangan mengarang angka. Bila datanya tidak ada, katakan tidak ada.\nTandai setiap teks untuk donatur sebagai DRAF.",
           samping=("Mengapa Projects", ["Instruksi tidak perlu diketik ulang setiap percakapan.", "Satu Project bersama bisa dipakai tim tiga negara, sehingga konteksnya sama.", "Berkas pengetahuan: laporan program, glosarium, contoh pesan yang baik."]),
           size=14, notes="Peserta menyalin instruksi ini ke Project mereka di aktivitas 2.1.")
aktivitas("2.1")

grid("Praktik:", "Tiga Tugas Nyata", "Topik 2.2  |  Berpasangan, 25 menit", [
    ("Tugas A", ["Ringkas laporan program Palestina (Lampiran 1 lembar kerja) menjadi 5 poin untuk donatur"], TEAL),
    ("Tugas B", ["Draf pesan terima kasih donatur program masjid", "Bahasa Indonesia dan Inggris"], BLUE),
    ("Tugas C", ["Unggah kampanye-iklan-rekaan.csv", "Minta tabel total biaya dan jumlah donasi per negara"], TEAL),
], cols=3, size=17, notes="Tidak perlu prompt yang bagus dulu. Prompt diperbaiki di Modul 3 dari hasil tugas B.")
grid("Daftar Periksa", "Hasil AI", "Dipakai setiap kali hasil AI akan dipakai", [
    ("Fakta", "Sesuai bahan yang diberikan", TEAL),
    ("Angka", "Semua angka ada di bahan, tidak ada yang dikarang", BLUE),
    ("Nada", "Sesuai pembaca: donatur, pimpinan, publik", TEAL),
    ("Bahasa", "Benar untuk negara tujuan", BLUE),
    ("Data pribadi", "Tidak ada nama, nomor, atau alamat asli", "C0504D"),
], cols=5, tinggi=3.0, size=15, notes="Daftar ini juga ada di lembar kerja halaman 3.")
aktivitas("2.2")

# =====================================================================
# M3
# =====================================================================
pembatas("M3", "Sesi 2")
s = slide("Satu Tugas,", "Dua Prompt", "Topik 3.1")
k = kotak(s, ML, 1.5, 4.2, 0.55, "C0504D")
isi_kotak(k, "Sebelum: skor 1 dari 12", size=13, bold=True, color="FFFFFF")
b = kotak(s, ML, 2.05, 4.2, 1.2, "F2F8F9", line=GREY)
isi_kotak(b, P.CONTOH_SEBELUM, size=14, align=PP_ALIGN.LEFT)
teks(s, ML, 3.5, 4.2, 3.2, ["Hasilnya umum, tanpa negara, tanpa fakta program, dan bisa berisi angka karangan.", "Tiap orang menulis prompt berbeda, jadi hasil antarnegara juga berbeda."], size=13, color=MUTED)
k = kotak(s, ML + 4.5, 1.5, CW - 4.5, 0.55, TEAL)
isi_kotak(k, "Sesudah: skor 12 dari 12", size=13, bold=True, color="FFFFFF")
b = kotak(s, ML + 4.5, 2.05, CW - 4.5, 4.75, "F2F8F9", line=GREY)
tf = b.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.TOP
for i, baris in enumerate(P.CONTOH_SESUDAH.split("\n")):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = baris
    r.font.name = MONO
    r.font.size = Pt(10)
    r.font.color.rgb = rgb("0E5E5D" if baris.startswith("<") else INK)
catatan(s, "Jalankan kedua prompt di Claude secara langsung dan bandingkan hasilnya di layar.")

s = slide("Enam Unsur", "Prompt", "Standar yang sama untuk tim Indonesia, Malaysia, dan Australia")
w6 = (CW - 5 * 0.15) / 6
for i, (u, en, arti, s0, s1, s2) in enumerate(d.RUBRIK):
    x = ML + i * (w6 + 0.15)
    top = kotak(s, x, 1.5, w6, 1.0, TEAL if i % 2 == 0 else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    isi_kotak(top, [[(f"{i + 1}. {u}", True, "FFFFFF")], [(en, False, "E6F4F4")]], size=14)
    b = kotak(s, x, 2.6, w6, 3.0, GREY_L, line=GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    isi_kotak(b, arti, size=13, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    b.text_frame.margin_top = Inches(0.12)
teks(s, ML, 5.85, CW, 0.9, "Hafalan singkat: Konteks, Tugas, Bahan, Aturan, Contoh, Format. Tiap unsur bernilai 0 sampai 2, total 12.", size=15, bold=True, color=TEAL_T)
catatan(s, "Pakai contoh program air bersih untuk menjelaskan tiap unsur.")

grid("Teknik", "Dasar", "Topik 3.1", [
    ("Tag pemisah", ["Bahan ditaruh di <data> ... </data>", "AI bisa membedakan perintah dari bahan"], TEAL),
    ("Contoh", ["1 sampai 3 contoh hasil yang baik", "Gaya hasil jadi konsisten antarorang"], BLUE),
    ("Berpikir dulu", ["Untuk analisis, minta langkah atau rumus sebelum jawaban", "Kesalahan hitung lebih mudah terlihat"], TEAL),
    ("Tempat isian", ["Bagian yang berubah ditulis {negara}, {nama_program}", "Orang lain cukup mengganti isian"], BLUE),
    ("Iterasi", ["Hasil belum tepat? Tambah unsur yang kurang", "Jangan mengulang pertanyaan yang sama"], TEAL),
    ("Sumber teknik", ["Panduan prompting resmi Anthropic", "platform.claude.com, Prompting best practices"], "8FD0CF"),
], cols=3, notes="Teknik ini sudah terpasang di 10 templat pustaka prompt.")

s = slide("Rubrik", "Skor Prompt", "Dipakai di pre-test, post-test, dan saat saling memeriksa")
tabel(s, ML, 1.45, CW, ["Unsur", "Skor 0", "Skor 1", "Skor 2"], [2.2, 3.0, 3.6, CW - 8.8],
      [[{"t": f"{u} ({en})", "bold": True}, s0, s1, s2] for u, en, arti, s0, s1, s2 in d.RUBRIK], size=11, tinggi_baris=[0.75] * 6)
teks(s, ML, 6.5, CW, 0.4, "0 sampai 5: tulis ulang.   6 sampai 8: cukup untuk tugas ringan.   9 sampai 12: siap jadi templat bersama.", size=12, bold=True, color=TEAL_T)
catatan(s, "Bagikan rubrik cetak. Rubrik juga ada di pustaka prompt bagian 1.")
aktivitas("3.1")

poin("Kesalahan yang", "Sering Muncul", "Topik 3.2", [
    "Tidak menyebut negara dan audiens, sehingga nada iklan Australia sama dengan Indonesia",
    "Tidak melarang angka di luar bahan, sehingga muncul angka dampak karangan",
    "Bahan bercampur dengan perintah, sehingga AI meringkas instruksi, bukan laporan",
    "Format tidak disebut, sehingga hasil terlalu panjang untuk WhatsApp atau iklan",
    "Mengulang pertanyaan yang sama berkali-kali alih-alih memperbaiki prompt",
], notes="Ambil contoh nyata dari prompt formulir asesmen bila ada.")
aktivitas("3.2", notes="Pakai 3 prompt nyata dari formulir asesmen, nama penulis dihapus.")

poin("Mengapa Hasil AI", "Berbeda Antarnegara", "Topik 3.3", [
    "Prompt berbeda: tiap orang menulis dengan caranya sendiri",
    "Konteks audiens berbeda: program masjid paling banyak direspons di Australia, nadanya pun berbeda",
    "Contoh berbeda: tiap tim punya contoh pesan baik sendiri, atau tidak memakai contoh sama sekali",
    "Istilah berbeda: penderma, donatur, donor untuk orang yang sama",
], kanan=("Isi Standar Prompt MFA", ["Templat 6 unsur dua bahasa", "Glosarium tiga bahasa", "Aturan etika penggalangan dana", "Contoh hasil yang baik per negara", "Satu tempat simpan: Claude Project atau folder bersama", "Satu penanggung jawab per negara"], BLUE),
    notes="Ini inti kebutuhan penyelarasan yang disampaikan klien. Beri waktu diskusi bila peserta lintas negara hadir.")

s = slide("Glosarium dan", "Aturan Etika", "Disalin ke setiap prompt yang hasilnya dibaca donatur atau publik")
tabel(s, ML, 1.45, 6.4, ["Indonesia", "English", "Melayu"], [2.2, 2.2, 2.0], [list(g) for g in P.GLOSARIUM], size=10, tinggi_baris=[0.42] * len(P.GLOSARIUM))
teks(s, ML + 6.8, 1.45, CW - 6.8, 0.4, "Aturan etika", size=14, bold=True, color=TEAL_T)
teks(s, ML + 6.8, 1.95, CW - 6.8, 4.8, [f"{i}. {e}" for i, e in enumerate(P.ETIKA, 1)], size=13)
for p in s.shapes[-1].text_frame.paragraphs:
    p.space_after = Pt(10)
catatan(s, "Istilah Melayu dan Inggris perlu dicocokkan dengan tim MFA Malaysia dan Australia.")

s = slide("Sepuluh", "Templat Siap Pakai", "Lengkap dua bahasa di Pustaka Prompt dan Standar Prompt MFA")
half = 5
for col in range(2):
    rows = [[{"t": t["kode"], "bold": True, "color": TEAL_T, "align": PP_ALIGN.CENTER}, t["judul"], t["untuk"]] for t in P.TEMPLAT[col * half:(col + 1) * half]]
    tabel(s, ML + col * (CW / 2 + 0.1), 1.5, CW / 2 - 0.1, ["Kode", "Templat", "Untuk"], [0.8, 3.3, CW / 2 - 0.1 - 4.1], rows, size=12, tinggi_baris=[0.8] * 5)
catatan(s, "Peserta memilih satu templat untuk dipakai di pekerjaan sebelum sesi berikutnya.")
aktivitas("3.3")

# =====================================================================
# M4
# =====================================================================
pembatas("M4", "Sesi 3")
s = slide("Chatbot dan", "AI Agent", "Topik 4.1")
for i, (jdl, items, warna) in enumerate([
    ("Chatbot", ["Menjawab satu permintaan", "Menunggu diperintah", "Hasil berupa teks di layar", "Tidak mengingat antarpercakapan, kecuali fitur memori", "Contoh: tanya Claude untuk caption"], "8FD0CF"),
    ("AI Agent", ["Bekerja menuju tujuan dalam beberapa langkah", "Bisa bekerja terjadwal tanpa diperintah ulang", "Memakai alat: membaca berkas, menghitung, mengirim pesan", "Mengingat preferensi dan cara kerja", "Contoh: laporan kampanye tiap Senin ke Telegram"], TEAL),
]):
    x = ML + i * (CW / 2)
    top = kotak(s, x, 1.5, CW / 2 - 0.25, 0.65, warna)
    isi_kotak(top, jdl, size=18, bold=True, color="FFFFFF" if i else INK)
    b = kotak(s, x, 2.15, CW / 2 - 0.25, 4.6, GREY_L, line=GREY)
    isi_kotak(b, [f"• {t}" for t in items], size=15, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP)
    b.text_frame.margin_top = Inches(0.2)
    for p in b.text_frame.paragraphs:
        p.space_after = Pt(10)
catatan(s, "Demonstrasikan tugas yang sama lewat chat Claude dan lewat agen di server latihan.")

s = slide("Putaran", "Kerja Agen", "Agen mengulang putaran ini sampai tujuan tercapai")
langkah = [("1. Tujuan", "Laporan biaya per donasi minggu ini"), ("2. Rencana", "Baca berkas, hitung, tulis ringkasan"),
           ("3. Pakai alat", "Membaca CSV, menghitung"), ("4. Periksa", "Angka masuk akal? Ada yang kosong?"),
           ("5. Ingat dan kirim", "Simpan cara kerja, kirim ke Telegram")]
import math
cx, cy, R = ML + 3.3, 4.1, 2.1
pos = []
for i, (jdl, ket) in enumerate(langkah):
    a = -math.pi / 2 + i * 2 * math.pi / 5
    x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    pos.append((x, y))
for i in range(5):
    x1, y1 = pos[i]
    x2, y2 = pos[(i + 1) % 5]
    garis(s, x1 + (x2 - x1) * 0.3, y1 + (y2 - y1) * 0.3, x1 + (x2 - x1) * 0.7, y1 + (y2 - y1) * 0.7, TEAL, 2, panah=True)
for i, ((jdl, ket), (x, y)) in enumerate(zip(langkah, pos)):
    o = kotak(s, x - 0.95, y - 0.45, 1.9, 0.9, TEAL if i % 2 == 0 else BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3)
    isi_kotak(o, jdl, size=12, bold=True, color="FFFFFF")
teks(s, ML + 7.0, 1.6, CW - 7.0, 5, [[(jdl + ": ", True, TEAL_T), (ket, False, INK)] for jdl, ket in langkah] +
     [[("Komponen agen: ", True, INK), ("model, instruksi, alat, memori, jadwal, dan saluran komunikasi.", False, INK)],
      [("Multi-agen: ", True, INK), ("beberapa agen dengan peran berbeda saling mengirim hasil.", False, INK)]], size=14)
for p in s.shapes[-1].text_frame.paragraphs:
    p.space_after = Pt(10)
catatan(s, "Jelaskan dengan contoh laporan kampanye mingguan, yang dipraktikkan di Topik 7.3.")

poin("Empat Pertanyaan", "Sebelum Membuat Agen", "Jawab ya untuk keempatnya", [
    [("Berulang? ", True, INK), ("Tugas muncul setiap hari atau minggu.", False, INK)],
    [("Aturannya jelas? ", True, INK), ("Langkahnya bisa ditulis untuk orang baru.", False, INK)],
    [("Datanya boleh dipakai? ", True, INK), ("Tidak ada data pribadi tanpa kebijakan.", False, INK)],
    [("Ada pemeriksa? ", True, INK), ("Ada orang yang memeriksa sebelum hasil dipakai.", False, INK)],
], kanan=("Risiko agen", ["Bertindak tanpa diperiksa", "Biaya API tanpa batas", "Data bocor lewat berkas atau chat", "Perintah berbahaya di komputer", "Semua dijawab dengan pengaturan aman di Modul 6"], "C0504D"),
    notes="Peserta memakai empat pertanyaan ini di lembar kerja halaman 7.")
aktivitas("4.1")

# =====================================================================
# M5
# =====================================================================
pembatas("M5", "Sesi 3")
poin("Mengenal", "Hermes Agent", "Topik 5.1", [
    "Dibuat Nous Research, sumber terbuka dengan lisensi MIT, rilis awal 2026",
    "Berjalan di laptop atau server sendiri, memakai model pilihan, termasuk Claude",
    "Bisa dihubungi lewat terminal, Telegram, WhatsApp, Slack, dan aplikasi chat lain",
    "Belajar dari pemakaian: menyimpan cara kerja sebagai skill dan mengingat preferensi",
    "Versi baru rilis hampir tiap minggu. Kita memakai versi yang dicocokkan trainer sebelum kelas",
], kanan=("Yang dibayar", ["Hermes gratis", "Yang dibayar adalah pemakaian model lewat kunci API", "Panduan publik: sekitar USD 5 sampai 8 per bulan untuk pemakaian ringan", "Pasang batas belanja sejak awal"], TEAL),
    notes="[ISI TIM: versi Hermes yang dipakai]. Tanyakan apa yang peserta lihat di workshop Hermes sebelumnya.")
grid("Bagian-bagian", "Hermes", "Topik 5.1", [
    ("SOUL.md", ["Identitas dan aturan agen", "Siapa dia, untuk siapa, apa yang dilarang"], TEAL),
    ("Memori", ["MEMORY.md dan USER.md", "Hal yang diingat antarpercakapan"], BLUE),
    ("Skill", ["Cara kerja yang disimpan dan dipakai ulang", "Diperbaiki saat dipakai"], TEAL),
    ("Profil", ["Satu profil satu agen", "Agen CRM, Iklan, Analis"], BLUE),
    ("Gateway", ["Penghubung ke Telegram, WhatsApp, Slack", "Satu bot untuk satu profil"], TEAL),
    ("Jadwal", ["Agen bekerja otomatis", "Contoh: laporan tiap Senin 09.00"], BLUE),
], cols=3, notes="Bot Mode di versi 0.21 memungkinkan beberapa agen bernama di satu grup dan saling mengirim pesan. Ini yang dilihat tim di workshop.")

s = slide("Demo:", "Tiga Agen dalam Satu Grup", "Semua pesan ke donatur melewati pemeriksaan manusia")
tm = kotak(s, ML, 2.9, 2.0, 1.2, BLUE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
isi_kotak(tm, [[("Tim MFA", True, "FFFFFF")], [("meminta laporan", False, "FFFFFF")]], size=13)
tg = kotak(s, ML + 2.6, 2.9, 2.1, 1.2, CYAN, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.15)
isi_kotak(tg, [[("Grup Telegram", True, "FFFFFF")], [("anggota terdaftar", False, "FFFFFF")]], size=13)
garis(s, ML + 2.0, 3.5, ML + 2.6, 3.5, INK, 1.5, panah=True)
for i, (n, ket) in enumerate([("1. Agen Analis", "Menghitung biaya per donasi per negara dan program"),
                              ("2. Agen Iklan", "Mengusulkan perbaikan teks iklan dari temuan Analis"),
                              ("3. Agen CRM", "Menyusun draf pesan untuk donatur segmen terkait")]):
    y = 1.5 + i * 1.6
    a = kotak(s, ML + 5.4, y, 3.6, 1.3, GREY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    isi_kotak(a, [[(n, True, TEAL_T)], [(ket, False, INK)]], size=12)
    garis(s, ML + 4.7, 3.5, ML + 5.4, y + 0.65, INK, 1.0, panah=True)
    garis(s, ML + 9.0, y + 0.65, ML + 9.6, 3.5, INK, 1.0, panah=True)
cek = kotak(s, ML + 9.6, 2.5, CW - 9.6, 2.0, LILAC, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
isi_kotak(cek, [[("Pemeriksaan manusia", True, INK)], [("Draf diperiksa, baru dikirim oleh orang", False, INK)]], size=13)
catatan(s, "Jalankan demo nyata di server latihan. Siapkan rekaman layar sebagai cadangan bila jaringan bermasalah.")
aktivitas("5.1")

# =====================================================================
# M6
# =====================================================================
pembatas("M6", "Sesi 3")
grid("Terminal dalam", "Tiga Langkah", "Topik 6.1  |  Tidak perlu bisa memprogram", [
    ("1. Tempel", ["Salin perintah dari panduan", "Tempel ke terminal", "macOS: Command+V. Ubuntu: Ctrl+Shift+V atau klik kanan"], TEAL),
    ("2. Enter", ["Tekan Enter sekali", "Tunggu sampai muncul baris baru untuk mengetik"], BLUE),
    ("3. Baca baris terakhir", ["Ada kata error atau galat? Tunjukkan ke asisten", "Kata sandi tidak tampil saat diketik, itu normal"], TEAL),
], cols=3, size=16, notes="Peragakan dengan perintah git --version sebelum instalasi.")
kode_slide("Instalasi", "macOS", "Panduan Setup Hermes bagian 3",
           "# 1. Cek Git\ngit --version\n\n# 2. Pasang Hermes\ncurl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash\n\n# 3. Tutup dan buka lagi Terminal, lalu cek\nhermes --help",
           samping=("Catatan", ["Bila muncul jendela Command Line Tools, klik Install.", "Instalasi butuh beberapa menit.", "Baris yang diawali # adalah keterangan, tidak perlu diketik."]),
           size=15, notes="Cocokkan perintah dengan dokumentasi resmi H-1.")
kode_slide("Instalasi", "Windows lewat WSL2", "Panduan Setup Hermes bagian 4",
           "# Di PowerShell (Run as administrator)\nwsl --install -d Ubuntu\n\n# Restart, buka Ubuntu, buat nama pengguna dan kata sandi\n\n# Di Ubuntu\nsudo apt update && sudo apt install -y git curl\ncurl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash\n\n# Tutup dan buka lagi Ubuntu\nhermes --help",
           samping=("Catatan", ["WSL2 adalah Linux di dalam Windows, jalur yang paling teruji.", "Virtualisasi harus menyala. Dicek H-2 bersama IT.", "Pemasang khusus Windows masih tahap awal, tidak dipakai di kelas."]),
           size=14, notes="Peserta Windows yang belum menyelesaikan WSL2 saat cek perangkat langsung memakai akun di server latihan.")
kode_slide("Setup", "Pertama", "Panduan Setup Hermes bagian 5",
           "hermes setup\n#  pilih penyedia model\n#  tempel kunci API latihan\n#  pilih model\n\nhermes\n#  ketik: Halo, siapa kamu dan apa yang bisa kamu kerjakan?\n#  ketik /help untuk perintah, Ctrl+C untuk keluar\n\nhermes doctor",
           samping=("Ingat", ["Kunci API latihan punya batas belanja.", "Jangan memotret atau mengirim kunci ke grup.", "Model harus punya konteks minimal 64.000 token.", "[ISI TIM: penyedia dan model]"]),
           size=15, notes="Tulis nama penyedia dan model di papan.")
kode_slide("Identitas Agen:", "SOUL.md", "Panduan Setup Hermes bagian 6  |  Templat di aset/hermes-templat",
           "# Agen CRM MyFundAction\n\n## Siapa kamu\nKamu Agen CRM milik tim [nama tim] MyFundAction [negara].\n\n## Tugasmu\n1. Mengelompokkan donatur dari tabel ...\n2. Menyusun draf pesan per segmen ...\n\n## Aturan yang tidak boleh dilanggar\n1. Kamu tidak pernah mengirim pesan ke donatur. Hanya draf.\n2. Jangan menulis angka yang tidak ada di bahan.\n3. Selama latihan hanya membaca folder data-latihan.\n4. Tanyakan dulu sebelum mengubah berkas atau sistem.",
           samping=("Cara membuka", ["macOS: open -e ~/.hermes/SOUL.md", "Ubuntu: nano ~/.hermes/SOUL.md", "Uji: tanyakan ke agen apa perannya dan apa yang dilarang."]),
           size=12, notes="SOUL.md memakai enam unsur prompt yang sama dengan Modul 3.")
kode_slide("Menghubungkan ke", "Telegram", "Panduan Setup Hermes bagian 7",
           "# Di Telegram\n@BotFather  kirim /newbot, beri nama, salin token\n@userinfobot  kirim pesan apa saja, catat ID Anda\n\n# Di terminal\nhermes gateway setup\n#  pilih Telegram, tempel token, isi ID Anda\n\nhermes gateway start\n#  kirim pesan ke bot Anda di Telegram",
           samping=("Ingat", ["Token bot sama rahasianya dengan kunci API.", "Satu token untuk satu profil agen.", "Gateway berhenti bila terminal ditutup. Agen yang menyala terus dipasang di server."]),
           size=14, notes="Cocokkan perintah gateway dengan dokumentasi resmi H-1.")
grid("Lima Pengaturan", "Aman", "Diperiksa bersama trainer di akhir Modul 6", [
    ("1. Persetujuan aktif", "Agen bertanya sebelum perintah berisiko. Tidak memakai --yolo atau /yolo", TEAL),
    ("2. Hanya Anda", "Bot hanya menjalankan perintah dari ID Telegram terdaftar", BLUE),
    ("3. Batas belanja", "Kunci API berbatas belanja dan tidak tersebar", TEAL),
    ("4. Data rekaan", "Hanya folder data-latihan sampai ada kebijakan MFA", BLUE),
    ("5. Manusia memeriksa", "Agen hanya membuat draf untuk donatur dan publik", "C0504D"),
], cols=5, tinggi=3.4, size=15, notes="Uji butir 2 dengan meminta rekan mengirim pesan ke bot. Bot tidak boleh menjalankannya.")
s = slide("Agen Kedua dan", "Masalah Umum", "Panduan Setup Hermes bagian 9 dan 11")
k = kotak(s, ML, 1.5, 5.2, 2.6, "F2F8F9", line=GREY)
tf = k.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.TOP
for i, baris in enumerate(["hermes profile create iklan", "hermes -p iklan setup", "hermes -p iklan gateway setup", "hermes -p iklan gateway start"]):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = baris
    r.font.name = MONO
    r.font.size = Pt(15)
    r.font.color.rgb = rgb(INK)
teks(s, ML, 4.3, 5.2, 2, "Satu profil satu agen, dengan SOUL.md, memori, dan bot Telegram sendiri.", size=13)
tabel(s, ML + 5.5, 1.5, CW - 5.5, ["Gejala", "Yang dilakukan"], [2.6, CW - 5.5 - 2.6], [
    ["command not found: hermes", "Tutup dan buka lagi terminal"],
    ["WSL2 gagal", "IT menyalakan virtualisasi di BIOS"],
    ["Model ditolak", "Pilih model lain dengan hermes model"],
    ["Galat 401", "Salin ulang kunci API, jalankan hermes model"],
    ["Galat 402", "Batas belanja tercapai, lapor trainer"],
    ["Bot diam", "Jalankan hermes gateway start, cek token dan ID"],
], size=11, tinggi_baris=[0.6] * 6)
catatan(s, "Masalah yang belum selesai dicatat untuk klinik pendampingan.")
aktivitas("6.1")
aktivitas("6.2")

# =====================================================================
# M7
# =====================================================================
pembatas("M7", "Sesi 4")
s = slide("Agen CRM:", "Segmentasi Donatur", "Topik 7.1  |  Data: donatur-rekaan.csv, 120 donatur rekaan")
tabel(s, ML, 1.5, 6.2, ["Urutan", "Segmen", "Aturan (acuan 16 November 2026)"], [0.9, 1.5, 3.8], [
    [{"t": "1", "align": PP_ALIGN.CENTER}, {"t": "Baru", "bold": True}, "Donasi pertama paling lama 90 hari"],
    [{"t": "2", "align": PP_ALIGN.CENTER}, {"t": "Tidak aktif", "bold": True}, "Donasi terakhir lebih dari 180 hari"],
    [{"t": "3", "align": PP_ALIGN.CENTER}, {"t": "Rutin", "bold": True}, "Donasi 12 bulan 3 kali atau lebih"],
    [{"t": "4", "align": PP_ALIGN.CENTER}, {"t": "Lainnya", "bold": True}, "Sisanya"],
], size=13, tinggi_baris=[0.6] * 4)
teks(s, ML, 4.6, 6.2, 2.2, ["Draf pesan hanya untuk donatur dengan setuju_dihubungi = Ya.", "Agen menunjukkan cara menghitung sebelum hasil.", "Pakai templat T4 (segmentasi) dan T2 (pesan terima kasih)."], size=13)
k = kotak(s, ML + 6.6, 1.5, CW - 6.6, 5.2, "F2F8F9", line=GREY)
tf = k.text_frame
tf.word_wrap = True
tf.vertical_anchor = MSO_ANCHOR.TOP
for i, baris in enumerate(P.TEMPLAT[3]["id"].split("\n")):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = baris
    r.font.name = MONO
    r.font.size = Pt(9.5)
    r.font.color.rgb = rgb("0E5E5D" if baris.startswith("<") else INK)
catatan(s, f"Kunci jawaban: Baru {KUNCI['segmen'].get('Baru')}, Rutin {KUNCI['segmen'].get('Rutin')}, Tidak aktif {KUNCI['segmen'].get('Tidak aktif')}, Lainnya {KUNCI['segmen'].get('Lainnya')}. Jangan tampilkan sebelum peserta selesai.")
aktivitas("7.1")

poin("Agen Iklan:", "Brief dan Variasi", "Topik 7.2  |  Templat T5 dan T6", [
    [("Brief: ", True, INK), ("tujuan, audiens, pesan utama, bukti, ajakan, larangan klaim, ukuran berhasil.", False, INK)],
    [("Australia: ", True, INK), ("program masjid paling banyak direspons. Bahasa Inggris Australia, nada hangat dan langsung.", False, INK)],
    [("Indonesia: ", True, INK), ("bahasa Indonesia sehari-hari yang sopan, istilah dari glosarium.", False, INK)],
    [("Periksa setiap variasi dengan aturan etika ", True, TEAL_T), ("sebelum dipilih.", False, INK)],
], kanan=("Aturan etika singkat", ["Tidak ada angka di luar bahan", "Tidak ada desakan palsu", "Penerima manfaat disebut dengan hormat", "Agen tidak memasang iklan, hanya draf"], "C0504D"),
    notes="Bila waktu cukup, minta satu peserta Australia atau Malaysia menilai variasi untuk negaranya.")
aktivitas("7.2")

s = slide("Agen Analis:", "Ukuran Kampanye", "Topik 7.3  |  Data: kampanye-iklan-rekaan.csv, 8 minggu")
tabel(s, ML, 1.5, 6.4, ["Ukuran", "Rumus"], [2.6, 3.8], [
    [{"t": "CTR", "bold": True}, "klik dibagi tayangan"],
    [{"t": "Biaya per donasi", "bold": True}, "biaya dibagi jumlah donasi"],
    [{"t": "Nilai per 1 USD iklan", "bold": True}, "nilai donasi dibagi biaya"],
], size=14, tinggi_baris=[0.7] * 3)
teks(s, ML + 6.8, 1.5, CW - 6.8, 0.4, "Pertanyaan untuk agen", size=15, bold=True, color=TEAL_T)
teks(s, ML + 6.8, 2.0, CW - 6.8, 3.5, [
    "1. Negara dan program mana yang biaya per donasinya paling rendah?",
    "2. Negara dan program mana yang nilai donasi per 1 USD iklannya paling tinggi?",
    "3. Mengapa dua jawaban itu bisa berbeda?",
    "4. Cek satu angka secara manual di spreadsheet.",
], size=14)
for p in s.shapes[-1].text_frame.paragraphs:
    p.space_after = Pt(10)
teks(s, ML, 4.6, 6.4, 2, "Pakai templat T7. Minta agen menulis rumus dan berpikir dulu sebelum menjawab.", size=13)
catatan(s, "Slide berikutnya berisi pembahasan. Tampilkan setelah peserta menjawab.")

s = slide("Pembahasan:", "Ukuran Menentukan Jawaban", "Data latihan rekaan, total 8 minggu, dalam USD")
terendah = min(KUNCI["kampanye"], key=lambda t: t["cpd"])
tertinggi = max(KUNCI["kampanye"], key=lambda t: t["roas"])
koma = lambda x: f"{x:.2f}".replace(".", ",")
rows = []
for t in KUNCI["kampanye"]:
    sty_c = {"bold": True, "color": "FFFFFF"} if t is terendah else {}
    rows.append([t["negara"], t["program"], str(t["donasi"]),
                 {"t": koma(t["cpd"]), "bold": t is terendah, "color": TEAL_T if t is terendah else INK, "align": PP_ALIGN.CENTER},
                 {"t": koma(t["roas"]), "bold": t is tertinggi, "color": BLUE if t is tertinggi else INK, "align": PP_ALIGN.CENTER}])
tabel(s, ML, 1.45, 7.6, ["Negara", "Program", "Donasi", "Biaya per donasi", "Nilai per 1 USD"], [1.4, 2.2, 1.0, 1.5, 1.5], rows, size=11, tinggi_baris=[0.45] * 9)
teks(s, ML + 8.0, 1.5, CW - 8.0, 5.2, [
    [("Biaya per donasi terendah: ", True, TEAL_T), (f"{terendah['negara']}, {terendah['program']} (USD {koma(terendah['cpd'])}).", False, INK)],
    [("Nilai per 1 USD tertinggi: ", True, BLUE), (f"{tertinggi['negara']}, {tertinggi['program']} (USD {koma(tertinggi['roas'])}).", False, INK)],
    [("Pelajaran: ", True, INK), ("donasi di Australia lebih mahal didapat, tetapi nilainya lebih besar. Agen harus menyebut ukuran yang dipakai, dan manusia memilih ukuran sesuai tujuan kampanye.", False, INK)],
], size=14)
for p in s.shapes[-1].text_frame.paragraphs:
    p.space_after = Pt(14)
catatan(s, "Data rekaan, polanya dibuat searah dengan informasi rapat bahwa program masjid paling banyak direspons di Australia.")

kode_slide("Laporan Terjadwal dan", "Kerja Tiga Agen", "Topik 7.3",
           "Setiap Senin pukul 09.00 WIB, baca berkas kampanye-iklan-rekaan.csv,\nhitung biaya per donasi dan nilai per 1 USD per negara dan program\nuntuk minggu terakhir, lalu kirim ringkasan 5 baris ke Telegram ini.\n\n# cek jadwal\nhermes cron --help",
           samping=("Lalu di grup latihan", ["Analis mengirim laporan.", "Iklan mengusulkan perbaikan untuk program dengan biaya tertinggi.", "CRM menyiapkan draf pesan untuk segmen terkait.", "Orang memutuskan dan mengirim."]),
           size=13, h=3.6, notes="Trainer menjalankan alur tiga agen di grup latihan memakai laporan yang dijadwalkan peserta.")
aktivitas("7.3")

s = slide("Kanvas Agen", "30 Hari", "Topik 7.4  |  Lembar kerja halaman 10")
bagian = [("Tugas", "Apa yang dikerjakan agen"), ("Pemicu", "Jadwal atau permintaan"), ("Data boleh", "Dan data yang tidak boleh"),
          ("Alat", "Telegram, berkas, spreadsheet"), ("Hasil", "Apa yang dikirim dan ke siapa"), ("Pemeriksa", "Nama orang"),
          ("Ukuran berhasil", "Setelah 30 hari"), ("Minggu 1 sampai 4", "Data rekaan, uji terbatas, rutin")]
for i, (jdl, ket) in enumerate(bagian):
    x = ML + (i % 4) * (CW / 4)
    y = 1.5 + (i // 4) * 2.55
    k = kotak(s, x, y, CW / 4 - 0.2, 2.3, TEAL_M if i % 2 == 0 else "EAF3FC", shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    isi_kotak(k, [[(jdl, True, TEAL_T)], [(ket, False, MUTED)]], size=14)
catatan(s, "Pilih tiga kanvas untuk dibacakan. Pertanyaan yang tersisa dibawa ke klinik pendampingan.")
aktivitas("7.4")

# =====================================================================
# Penutup
# =====================================================================
poin("Post-test dan", "Survei", "10 menit post-test, 5 menit survei", [
    "Soal sama dengan pre-test. Bagian B dinilai dengan rubrik 6 unsur",
    "Survei kepuasan 8 butir, skala 1 sampai 5",
    "Hasil per peserta dan per negara dikirim dalam laporan akhir",
], notes="Target: skor prompt rata-rata minimal 9 dari 12, selisih antarnegara tidak lebih dari 2 poin.")
poin("Setelah", "Pelatihan", "Rencana 30 hari", [
    "Pakai minimal satu templat Standar Prompt MFA setiap minggu",
    "Jalankan agen dari kanvas 30 hari dengan data rekaan, lalu uji terbatas",
    "Klinik pendampingan daring 60 menit sekitar 1 sampai 2 minggu lagi. [ISI TIM: tanggal klinik]",
    "MFA menetapkan kebijakan pemakaian AI untuk data donatur sebelum agen memakai data asli",
    "Formulir singkat 30 hari untuk melihat penerapan",
], kanan=("Yang dibawa pulang", [o for o, _ in d.HASIL[:7]] + ["dan seterusnya, lihat silabus"], TEAL), size=15,
    notes="Kembali ke daftar harapan peserta di awal pelatihan.")

s = prs.slides.add_slide(prs.slide_layouts[6])
kotak(s, 0, 0, SW, SH, GELAP)
kotak(s, 0, 0, 0.35, SH, CYAN)
s.shapes.add_picture(LOGO, Inches(0.9), Inches(0.8), height=Inches(0.55))
teks(s, 0.9, 2.6, 11.5, 1.0, "Terima kasih", size=44, bold=True, color="FFFFFF")
teks(s, 0.9, 3.7, 11.5, 0.6, "Pertanyaan setelah pelatihan dibawa ke klinik pendampingan", size=18, color="E6F4F4")
teks(s, 0.9, 5.4, 11.5, 1.0, ["WhatsApp 0877-7413-4288  |  www.sanggabiz.com  |  partnership@sanggabiz.com"], size=14, color="FFFFFF")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print("tersimpan:", os.path.normpath(OUT), "slide:", len(prs.slides))
