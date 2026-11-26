"""Membuat dua contoh modul (M3 dan M4) sebagai standar minimal modul Sanggabiz.

Pemakaian (dari akar repo):
  python3 mmpp-empathy-leadership/_build/build_visual.py      # visual dulu
  python3 mmpp-empathy-leadership/_build/build_modul_contoh.py
Hasil: mmpp-empathy-leadership/modul-contoh/*.docx dan *.pdf, serta gambar halaman di _build/visual/hal-*.png
"""
import subprocess
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent
VIS = ROOT / "visual"
OUT = ROOT.parent / "modul-contoh"
OUT.mkdir(exist_ok=True)

TEAL = RGBColor(0x0E, 0x8A, 0x8A)
TEAL_D = RGBColor(0x0D, 0x5C, 0x5B)
INK = RGBColor(0x1D, 0x1D, 0x1F)
GREY_T = RGBColor(0x55, 0x55, 0x55)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
STATUS = "CONTOH MODUL. Kasus dan kalimat latihan masih rekaan dan akan diganti dengan hasil asesmen awal PT MMPP."


# ---------------- alat bantu ----------------
def shade(cell, hex_):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_)
    tcPr.append(sh)


def fix_widths(t, widths):
    t.autofit = False
    grid = t._tbl.tblGrid
    for j, gc in enumerate(grid.findall(qn("w:gridCol"))):
        gc.set(qn("w:w"), str(int(widths[j] * 567)))
    for row in t.rows:
        for j, c in enumerate(row.cells):
            c.width = Cm(widths[j])


def borders(table, color="BFBFBF"):
    tblPr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for e in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{e}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:color"), color)
        b.append(el)
    tblPr.append(b)


def run(p, t, size=10.5, bold=False, color=INK, italic=False):
    r = p.add_run(t)
    r.font.name = "Arial"
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "Arial")
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.font.color.rgb = color
    return r


def para(doc_or_cell, parts, align=None, after=4, before=0):
    p = doc_or_cell.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.space_before = Pt(before)
    if isinstance(parts, str):
        parts = [(parts, {})]
    for t, o in parts:
        run(p, t, **o)
    return p


def h1(doc, t, kicker=None):
    if kicker:
        para(doc, [(kicker.upper(), {"size": 9, "bold": True, "color": TEAL})], after=0)
    para(doc, [(t, {"size": 17, "bold": True, "color": TEAL_D})], after=6)


def h2(doc, t):
    para(doc, [(t, {"size": 12.5, "bold": True, "color": TEAL})], after=3, before=6)


def bullets(doc, items, size=10.5):
    for it in items:
        p = para(doc, [("•  ", {"size": size, "color": TEAL, "bold": True})] +
                 (it if isinstance(it, list) else [(it, {"size": size})]), after=2)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)


def table(doc, rows, widths, head=True, size=9.5, head_fill="15908F", zebra="F2F8F9", first_bold=False,
          heights=None):
    t = doc.add_table(rows=len(rows), cols=len(widths))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    borders(t)
    for i, r in enumerate(rows):
        for j, val in enumerate(r):
            c = t.cell(i, j)
            c.width = Cm(widths[j])
            c.paragraphs[0].text = ""
            parts = val if isinstance(val, list) else [(val, {})]
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            for tt, o in parts:
                o = dict(o)
                o.setdefault("size", size)
                if head and i == 0:
                    o.update(bold=True, color=WHITE)
                elif first_bold and j == 0:
                    o.setdefault("bold", True)
                run(p, tt, **o)
            if head and i == 0:
                shade(c, head_fill)
            elif zebra and i % 2 == 0:
                shade(c, zebra)
        if heights and (i > 0 or not head):
            tr = t.rows[i]._tr
            trPr = tr.get_or_add_trPr()
            hgt = OxmlElement("w:trHeight")
            hgt.set(qn("w:val"), str(int(heights * 567)))
            trPr.append(hgt)
    fix_widths(t, widths)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def callout(doc, title, body, fill="D7ECEC"):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = t.cell(0, 0)
    c.width = Cm(17)
    shade(c, fill)
    p = c.paragraphs[0]
    run(p, title, 10.5, True, TEAL_D)
    for b in body:
        q = c.add_paragraph()
        q.paragraph_format.space_after = Pt(1)
        for tt, o in (b if isinstance(b, list) else [(b, {})]):
            o = dict(o)
            o.setdefault("size", 10)
            run(q, tt, **o)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def image(doc, name, width_cm=17, caption=None):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(VIS / f"{name}.png"), width=Cm(width_cm))
    if caption:
        para(doc, [(caption, {"size": 9, "color": GREY_T})], WD_ALIGN_PARAGRAPH.CENTER, after=8)


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def new_doc(code, title):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.left_margin = sec.right_margin = Cm(2)
    sec.top_margin, sec.bottom_margin = Cm(2), Cm(1.8)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10.5)
    hp = sec.header.paragraphs[0]
    run(hp, f"Modul {code[1]}  {title}", 8.5, True, TEAL)
    run(hp, "     Communication & Teamwork Leadership Based on Empathy  |  CONTOH", 8.5, False, GREY_T)
    fp = sec.footer.paragraphs[0]
    run(fp, "WhatsApp 0877-7413-4288   www.sanggabiz.com   partnership@sanggabiz.com", 8, False, GREY_T)
    return doc


def cover(doc, code, title, focus, minutes):
    t = doc.add_table(rows=1, cols=1)
    c = t.cell(0, 0)
    c.width = Cm(17)
    shade(c, "0D5C5B")
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(60)
    run(p, "sanggabiz", 20, True, WHITE)
    for txt, o, sb in [("MODUL PESERTA DAN CATATAN FASILITATOR", {"size": 10, "bold": True, "color": RGBColor(0x33, 0xBC, 0xCF)}, 80),
                       (f"Modul {code[1]}", {"size": 16, "bold": True, "color": WHITE}, 4),
                       (title, {"size": 28, "bold": True, "color": WHITE}, 2),
                       (focus, {"size": 12, "color": WHITE}, 10),
                       (f"Bagian dari pelatihan satu hari Communication & Teamwork Leadership Based on Empathy. Durasi modul {minutes} menit.",
                        {"size": 10.5, "color": WHITE}, 70),
                       ("Disiapkan untuk PT Makassar Mega Putra Prima", {"size": 10.5, "bold": True, "color": WHITE}, 2),
                       ("Versi contoh, November 2026", {"size": 10.5, "color": WHITE}, 2)]:
        q = c.add_paragraph()
        q.paragraph_format.space_before = Pt(sb)
        q.paragraph_format.space_after = Pt(2)
        q.paragraph_format.left_indent = Cm(0.6)
        run(q, txt, **o)
    p.paragraph_format.left_indent = Cm(0.6)
    q = c.add_paragraph()
    q.paragraph_format.space_after = Pt(60)
    para(doc, "")
    callout(doc, "Status dokumen", [STATUS], "F6E5FB")
    page_break(doc)


def peta(doc, rows, why):
    h1(doc, "Peta modul", "Bagian 1")
    table(doc, [["Butir", "Isi"]] + rows, [4.2, 12.8], first_bold=True)
    h2(doc, "Mengapa modul ini penting")
    for w in why:
        para(doc, [(w, {})], after=4)


def save(doc, name):
    p = OUT / f"{name}.docx"
    doc.save(p)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(p)],
                   check=True, capture_output=True)
    return OUT / f"{name}.pdf"


# ======================================================================
# M3
# ======================================================================
def modul_m3():
    doc = new_doc("M3", "Umpan Balik yang Menjaga Martabat")
    cover(doc, "M3", "Umpan Balik yang Menjaga Martabat",
          "Memberi umpan balik yang jelas tanpa menjatuhkan harga diri orang lain", 60)
    peta(doc, [
        ["Tujuan", [("C3 ", {"bold": True}), ("Mengubah kalimat teguran yang menyerang pribadi menjadi kalimat yang menyebut perilaku dan dampaknya.", {})]],
        ["", [("C3 ", {"bold": True}), ("Menyusun dan menyampaikan umpan balik SBI dengan pertanyaan niat untuk satu kasus nyata.", {})]],
        ["Durasi", "60 menit: topik 3.1 (15 menit) dan topik 3.2 (45 menit)"],
        ["Posisi di program", "Setelah M2 Mendengar untuk Memahami, sebelum M4 Percakapan Sulit. Keterampilan mendengar dari M2 dipakai saat lawan bicara menjawab pertanyaan niat."],
        ["Yang dibawa pulang", "5 kalimat teguran yang sudah diperbaiki (lembar kerja 3.1) dan satu naskah umpan balik SBI untuk kasus sendiri (lembar kerja 3.2)"],
        ["Ukuran keberhasilan", "Minimal 4 dari 5 kalimat menyebut perilaku dan dampak. Naskah memuat situasi, perilaku, dampak, dan satu pertanyaan niat."],
    ], [
        "Pemimpin yang menegur dengan menyerang pribadi biasanya mendapat dua tanggapan: anggota tim membela diri atau diam. Keduanya membuat masalah kerja tidak selesai. "
        "Dalam nilai siri' na pacce, harga diri (siri') orang yang ditegur ikut dijaga. Modul ini memberi cara menegur yang tegas soal pekerjaan dan tetap menjaga martabat orang.",
        "Model yang dipakai adalah Situation-Behavior-Impact (SBI) dari Center for Creative Leadership, ditambah satu pertanyaan tentang niat agar umpan balik menjadi percakapan dua arah.",
    ])
    page_break(doc)

    h1(doc, "Pisahkan orang dari perilakunya", "Bagian 2. Konsep inti")
    para(doc, "Kalimat yang menilai orang (\"tidak bisa diandalkan\", \"asal-asalan\") membuat lawan bicara membela harga dirinya. Kalimat yang menyebut perilaku dan dampaknya membuat lawan bicara membahas pekerjaannya.")
    image(doc, "m3-orang-perilaku", 16.5, "Gambar 1. Kalimat yang menyerang orang dan kalimat yang menyebut perilaku serta dampak. Contoh rekaan.")
    h2(doc, "Tiga pegangan")
    bullets(doc, [
        [("Sebut yang terlihat atau terdengar. ", {"bold": True}), ("Jam datang, jumlah salah input, kalimat yang diucapkan. Bukan sifat orang.", {})],
        [("Sebut dampaknya. ", {"bold": True}), ("Apa akibatnya pada pekerjaan, pelanggan, atau rekan kerja.", {})],
        [("Pilih tempatnya. ", {"bold": True}), ("Teguran disampaikan empat mata. Pujian boleh di depan tim.", {})],
    ])
    page_break(doc)

    h1(doc, "Umpan balik dengan SBI dan niat", "Bagian 3. Konsep inti dan contoh")
    image(doc, "m3-sbi", 16.5, "Gambar 2. Empat bagian umpan balik. Sumber model SBI: Center for Creative Leadership.")
    h2(doc, "Contoh lengkap (rekaan)")
    table(doc, [
        ["Bagian", "Yang diucapkan supervisor kepada Andi, staf penjualan"],
        ["Situasi", "\"Andi, saya mau bicara soal rapat mingguan Senin kemarin.\""],
        ["Perilaku", "\"Waktu Rina menjelaskan angka penjualan wilayah timur, kamu memotongnya dua kali.\""],
        ["Dampak", "\"Rina berhenti bicara, dan kita tidak sempat mendengar usulnya soal diskon.\""],
        ["Niat", "\"Apa yang sedang kamu pikirkan waktu itu?\""],
        ["Langkah", "Setelah Andi menjawab: \"Minggu depan, catat dulu tanggapanmu dan sampaikan setelah Rina selesai. Bisa?\""],
    ], [3, 14], first_bold=True)
    h2(doc, "Yang sering keliru")
    table(doc, [
        ["Bagian", "Keliru", "Lebih tepat"],
        ["Situasi", "\"Akhir-akhir ini...\"", "\"Di rapat Senin kemarin...\""],
        ["Perilaku", "\"Kamu tidak sopan.\"", "\"Kamu memotong Rina dua kali.\""],
        ["Dampak", "\"Semua orang kecewa sama kamu.\"", "\"Rina berhenti bicara.\""],
        ["Niat", "\"Kenapa sih kamu begitu?\"", "\"Apa yang sedang kamu pikirkan waktu itu?\""],
    ], [3, 6.5, 7.5], first_bold=True)
    page_break(doc)

    h1(doc, "Lembar kerja 3.1: tulis ulang kalimat teguran", "Bagian 4. Lembar kerja")
    para(doc, "Waktu: 10 menit, berpasangan. Ubah tiap kalimat agar menyebut perilaku yang terlihat dan dampaknya. Kalimat di bawah rekaan dan akan diganti dengan kalimat dari asesmen awal.")
    table(doc, [
        ["No", "Kalimat awal", "Tulis ulang: perilaku dan dampak"],
        ["1", "\"Kamu ini memang tidak bisa diandalkan.\"", ""],
        ["2", "\"Laporanmu selalu berantakan.\"", ""],
        ["3", "\"Kamu tidak peduli sama tim.\"", ""],
        ["4", "\"Malas sekali kamu bulan ini.\"", ""],
        ["5", "\"Kerja begini saja tidak becus.\"", ""],
    ], [1, 6.5, 9.5], heights=1.6)
    callout(doc, "Ukuran keberhasilan", ["Minimal 4 dari 5 kalimat menyebut perilaku yang terlihat dan dampaknya. Pasangan Anda memeriksa dengan tanda centang."])
    page_break(doc)

    h1(doc, "Lembar kerja 3.2: naskah umpan balik untuk kasus Anda", "Bagian 4. Lembar kerja")
    para(doc, "Waktu: 10 menit menulis, 20 menit praktik berpasangan. Pilih satu kejadian nyata dalam dua minggu terakhir.")
    table(doc, [
        ["Bagian", "Tulis kalimat Anda"],
        ["Situasi", ""], ["Perilaku", ""], ["Dampak", ""], ["Pertanyaan niat", ""], ["Langkah yang diharapkan", ""],
    ], [4, 13], first_bold=True, heights=1.5)
    h2(doc, "Lembar cek untuk pasangan")
    table(doc, [
        ["No", "Yang diperiksa", "Ya", "Belum"],
        ["1", "Situasi menyebut waktu dan tempat yang jelas", "", ""],
        ["2", "Perilaku bisa dilihat atau didengar, tanpa kata sifat tentang orang", "", ""],
        ["3", "Dampak menyebut akibat nyata pada pekerjaan atau orang", "", ""],
        ["4", "Pertanyaan niat terbuka dan tidak menuduh", "", ""],
        ["5", "Nada suara tenang, penyampai mendengar jawaban sampai selesai", "", ""],
    ], [1, 12, 2, 2])
    page_break(doc)

    h1(doc, "Refleksi dan tindak lanjut", "Bagian 5")
    for q in ["Kalimat teguran apa yang paling sering Anda ucapkan, dan bagaimana bunyinya bila ditulis ulang?",
              "Kepada siapa Anda akan memberi umpan balik SBI minggu ini?",
              "Apa yang akan Anda lakukan bila orang itu membela diri?"]:
        para(doc, [(q, {"bold": True})], after=2)
        table(doc, [[""]], [17], head=False, zebra=None, heights=1.4)
    callout(doc, "Coba minggu ini", ["Berikan satu umpan balik SBI untuk perilaku yang perlu diperbaiki dan satu untuk perilaku yang perlu dipertahankan. Catat tanggapan orangnya di rencana aksi 30 hari (M6)."])
    h2(doc, "Rujukan")
    bullets(doc, ["Center for Creative Leadership. Situation-Behavior-Impact (SBI) Feedback Tool. ccl.org",
                  "Center for Creative Leadership. Closing the Gap Between Intent and Impact (SBII). ccl.org",
                  "Siri' na pacce: Good News From Indonesia, 21 Mei 2025"], 9.5)
    page_break(doc)

    h1(doc, "Catatan fasilitator", "Bagian 6. Untuk trainer dan co-fasilitator")
    table(doc, [
        ["Menit", "Kegiatan", "Bahan"],
        ["0 - 5", "Penjelasan memisahkan orang dan perilaku, Gambar 1", "Slide"],
        ["5 - 15", "Lembar kerja 3.1 berpasangan, pasangan saling memeriksa", "Lembar kerja 3.1"],
        ["15 - 23", "Trainer memperagakan umpan balik tanpa struktur, lalu dengan SBI dan niat, bersama co-fasilitator", "Naskah peragaan"],
        ["23 - 33", "Peserta menulis naskah di lembar kerja 3.2", "Lembar kerja 3.2"],
        ["33 - 53", "Praktik berpasangan, 2 putaran x 10 menit, memakai lembar cek", "Lembar cek, pengatur waktu"],
        ["53 - 60", "Dua pasangan tampil, kelas memberi masukan", ""],
    ], [2.2, 11, 3.8])
    h2(doc, "Kesalahan umum peserta dan cara meluruskan")
    table(doc, [
        ["Yang terjadi", "Yang dilakukan fasilitator"],
        ["Peserta menulis perilaku berupa kata sifat (\"kurang inisiatif\")", "Tanya: \"Kalau saya rekam dengan kamera, apa yang terlihat?\""],
        ["Pertanyaan niat terdengar seperti tuduhan", "Minta peserta mengucapkannya ulang dengan awalan \"apa\" atau \"bagaimana\""],
        ["Penerima umpan balik langsung membela diri", "Ingatkan teknik refleksi perasaan dari M2 sebelum melanjutkan ke langkah"],
    ], [7.5, 9.5])
    h2(doc, "Penyesuaian setelah asesmen awal")
    bullets(doc, ["Lima kalimat di lembar kerja 3.1 diganti dengan kalimat teguran yang paling sering muncul di formulir peserta.",
                  "Contoh lengkap disesuaikan dengan jenis pekerjaan peserta (penjualan, gudang, administrasi, atau lainnya)."])
    return save(doc, "Contoh Modul M3 - Umpan Balik yang Menjaga Martabat - PT MMPP")


# ======================================================================
# M4
# ======================================================================
def modul_m4():
    doc = new_doc("M4", "Percakapan Sulit dengan Empati")
    cover(doc, "M4", "Percakapan Sulit dengan Empati",
          "Memimpin percakapan dengan taruhan tinggi dan emosi kuat tanpa merusak hubungan kerja", 90)
    peta(doc, [
        ["Tujuan", [("C3 ", {"bold": True}), ("Menyusun lembar persiapan percakapan sulit dengan 4 langkah untuk satu kasus sendiri.", {})]],
        ["", [("C3 ", {"bold": True}), ("Memimpin percakapan sulit 8 menit dengan Alur Percakapan Empatik.", {})]],
        ["", [("C5 ", {"bold": True}), ("Menilai percakapan rekan dengan rubrik 0 sampai 8.", {})]],
        ["Durasi", "90 menit: topik 4.1 (30 menit) dan topik 4.2 role play (60 menit)"],
        ["Posisi di program", "Setelah M2 dan M3. Memakai keterampilan mendengar (M2) dan bahasa yang menjaga martabat (M3) dalam satu percakapan utuh."],
        ["Yang dibawa pulang", "Lembar persiapan untuk kasus sendiri, kartu Alur 4 langkah, skor rubrik dari pengamat"],
        ["Ukuran keberhasilan", "Skor rata-rata putaran ketiga role play minimal 6 dari 8"],
    ], [
        "Percakapan sulit adalah percakapan dengan taruhan tinggi, pendapat berbeda, dan emosi kuat. Contohnya membahas target yang tidak tercapai, konflik antaranggota tim, atau keputusan yang tidak populer. "
        "Banyak pemimpin menundanya sampai masalah membesar, atau menjalankannya dengan nada menekan.",
        "Alur Percakapan Empatik memberi urutan yang sederhana: siapkan, dengarkan, akui, sepakati. Urutan ini menjaga hubungan kerja tanpa mengendurkan standar.",
    ])
    page_break(doc)

    h1(doc, "Mengenali percakapan sulit", "Bagian 2. Konsep inti")
    table(doc, [
        ["Ciri", "Contoh di tempat kerja"],
        ["Taruhan tinggi", "Target bulanan, penilaian kinerja, keselamatan kerja"],
        ["Pendapat berbeda", "Supervisor dan staf punya penjelasan berbeda soal penyebab keterlambatan"],
        ["Emosi kuat", "Kesal, malu, takut disalahkan, merasa tidak dihargai"],
    ], [4.5, 12.5], first_bold=True)
    para(doc, "Saat emosi naik, orang cenderung bergerak ke salah satu ujung: diam atau menyerang. Tugas pemimpin adalah membawa percakapan kembali ke tengah, yaitu dialog.")
    image(doc, "m4-spektrum", 16.5, "Gambar 1. Spektrum percakapan. Pemimpin memperhatikan tanda di kedua ujung.")
    page_break(doc)

    h1(doc, "Alur Percakapan Empatik 4 langkah", "Bagian 3. Konsep inti")
    image(doc, "m4-alur-ringkas", 16.5, "Gambar 2. Empat langkah, masing-masing dinilai 0, 1, atau 2.")
    table(doc, [
        ["Langkah", "Yang dilakukan", "Kalimat pembuka yang bisa dipakai"],
        ["1 Siapkan", "Tulis fakta dan tafsiran secara terpisah. Tetapkan tujuan yang diinginkan kedua pihak.", "(Ditulis sebelum bertemu, tidak diucapkan)"],
        ["2 Dengarkan", "Buka dengan fakta, lalu satu pertanyaan terbuka. Refleksikan perasaan, beri jeda.", "\"Saya lihat... Bagaimana keadaannya dari sisi kamu?\"\n\"Sepertinya kamu kecewa karena...\""],
        ["3 Akui", "Sebut kepentingan dan kekhawatiran kedua pihak tanpa menyalahkan.", "\"Kamu perlu..., dan saya juga perlu...\""],
        ["4 Sepakati", "Tutup dengan langkah, penanggung jawab, waktu, dan cara memantau.", "\"Jadi kita sepakat... Kita cek lagi hari...\""],
    ], [2.8, 6.7, 7.5], first_bold=True)
    page_break(doc)

    h1(doc, "Contoh lengkap dengan skor", "Bagian 4. Contoh (rekaan)")
    para(doc, "Supervisor gudang berbicara dengan Dewi, staf administrasi, tentang laporan stok yang terlambat tiga kali bulan ini.")
    table(doc, [
        ["Langkah", "Percakapan", "Skor"],
        ["Siapkan", "Catatan supervisor. Fakta: laporan terlambat 3 kali bulan ini. Tafsiran saya: dia kurang peduli. Tujuan bersama: laporan tepat waktu tanpa lembur berlebihan.", "2"],
        ["Dengarkan", "Supervisor: \"Laporan stok tiga kali terlambat bulan ini. Bagaimana keadaannya dari sisi kamu?\"\nDewi: \"Data dari gudang baru masuk jam empat sore, Pak. Saya sudah bilang berkali-kali.\"\nSupervisor: \"Jadi kamu menunggu data yang datangnya sore, dan kesal karena sudah sering menyampaikan itu.\"", "2"],
        ["Akui", "Supervisor: \"Kamu perlu data masuk lebih awal supaya tidak lembur. Saya perlu laporan itu untuk rapat pagi. Dua-duanya penting.\"", "2"],
        ["Sepakati", "Supervisor: \"Besok saya bicara dengan kepala gudang supaya data masuk jam 14.00. Jumat kamu kabari saya apakah berjalan.\"", "1"],
    ], [2.8, 12.4, 1.8], first_bold=True)
    callout(doc, "Mengapa langkah Sepakati diberi skor 1", ["Langkah, penanggung jawab, dan waktu sudah disebut. Cara memantau setelah hari Jumat belum disepakati, misalnya apa yang dilakukan bila data tetap datang sore. Skor total contoh ini 7 dari 8."])
    page_break(doc)

    h1(doc, "Lembar persiapan percakapan sulit", "Bagian 5. Lembar kerja")
    para(doc, "Waktu: 8 menit. Isi untuk kasus yang Anda tulis di awal modul.")
    table(doc, [
        ["Butir", "Isi"],
        ["Dengan siapa", ""], ["Masalahnya", ""], ["Fakta (yang bisa dibuktikan)", ""], ["Tafsiran saya (yang belum tentu benar)", ""],
        ["Tujuan yang diinginkan kedua pihak", ""], ["Kalimat pembuka saya", ""], ["Perasaan yang mungkin muncul pada lawan bicara", ""],
        ["Usulan kesepakatan dan cara memantau", ""],
    ], [5.5, 11.5], first_bold=True, heights=1.25)
    page_break(doc)

    h1(doc, "Kartu peran untuk role play", "Bagian 5. Lembar kerja (contoh kasus rekaan)")
    t = doc.add_table(rows=1, cols=2)
    borders(t)
    fix_widths(t, [8.5, 8.5])
    for j, (ttl, fill, lines) in enumerate([
        ("KARTU PEMIMPIN", "D7ECEC", ["Anda kepala regu pengiriman. Target pengiriman tepat waktu bulan ini 95 persen, regu Anda baru mencapai 82 persen.",
                                     "Budi, anggota regu yang paling senior, dua kali menolak lembur minggu ini.",
                                     "Tujuan Anda: memahami alasannya dan menyepakati langkah agar target bulan depan tercapai.",
                                     "Pakai Alur 4 langkah. Waktu: 8 menit."]),
        ("KARTU ANGGOTA TIM (BUDI)", "F6E5FB", ["Anda sudah 9 tahun di regu ini. Minggu ini anak Anda sakit dan Anda harus menjemput istri dari kerja.",
                                                "Anda merasa rekan yang lebih muda sering pulang cepat tanpa ditegur.",
                                                "Bila pemimpin bertanya dengan tulus, ceritakan keadaan Anda. Bila pemimpin langsung menyalahkan, jawab singkat dan diam.",
                                                "Jangan tunjukkan kartu ini kepada pemimpin."])]):
        c = t.cell(0, j)
        c.width = Cm(8.5)
        shade(c, fill)
        run(c.paragraphs[0], ttl, 10.5, True, TEAL_D)
        for ln in lines:
            q = c.add_paragraph()
            q.paragraph_format.space_after = Pt(4)
            run(q, ln, 10)
    para(doc, "")
    para(doc, [("Kartu pengamat: ", {"bold": True}), ("isi rubrik di halaman berikutnya selama percakapan. Catat satu kalimat pemimpin yang paling membantu dan satu yang perlu diperbaiki.", {})])
    page_break(doc)

    h1(doc, "Rubrik pengamat", "Bagian 6. Alat ukur")
    table(doc, [
        ["Langkah", "0", "1", "2"],
        ["Siapkan", "Langsung menilai orang, tanpa fakta", "Fakta ada, tafsiran masih tercampur", "Fakta terpisah dari tafsiran, tujuan bersama jelas"],
        ["Dengarkan", "Tidak bertanya, langsung memberi solusi atau menegur", "Bertanya, tetapi tertutup atau memotong jawaban", "Pertanyaan terbuka dan minimal satu refleksi perasaan"],
        ["Akui", "Menyalahkan atau mengabaikan kepentingan lawan bicara", "Menyebut kepentingan satu pihak saja", "Kepentingan kedua pihak disebut, martabat terjaga"],
        ["Sepakati", "Tidak ada kesepakatan", "Ada langkah, tetapi tanpa waktu atau penanggung jawab", "Langkah, penanggung jawab, waktu, dan cara memantau disebut"],
    ], [2.8, 4.7, 4.7, 4.8], first_bold=True)
    table(doc, [
        ["Putaran", "Nama pemimpin", "Siapkan", "Dengarkan", "Akui", "Sepakati", "Total"],
        ["1", "", "", "", "", "", ""], ["2", "", "", "", "", "", ""], ["3", "", "", "", "", "", ""],
    ], [1.8, 5, 2, 2.2, 1.8, 2.2, 2], heights=0.9)
    callout(doc, "Target", ["Skor rata-rata putaran ketiga minimal 6 dari 8."])
    page_break(doc)

    h1(doc, "Refleksi dan tindak lanjut", "Bagian 7")
    for q in ["Langkah mana yang paling sulit bagi Anda, dan mengapa?",
              "Percakapan sulit apa yang akan Anda jalankan dalam dua minggu ke depan, dan kapan?"]:
        para(doc, [(q, {"bold": True})], after=2)
        table(doc, [[""]], [17], head=False, zebra=None, heights=1.6)
    callout(doc, "Coba minggu ini", ["Jalankan satu percakapan sulit dengan lembar persiapan ini. Catat skor diri Anda dengan rubrik dan bawa ke sesi tindak lanjut hari ke-30."])
    h2(doc, "Rujukan")
    bullets(doc, ["Edmondson, A. (1999). Psychological Safety and Learning Behavior in Work Teams. Administrative Science Quarterly, 44(2)",
                  "DDI. Key Principles: listen and respond with empathy, maintain self-esteem. ddi.com",
                  "Alur Percakapan Empatik 4 langkah disusun Sanggabiz untuk program ini"], 9.5)
    page_break(doc)

    h1(doc, "Catatan fasilitator", "Bagian 8. Untuk trainer dan co-fasilitator")
    table(doc, [
        ["Menit", "Kegiatan", "Bahan"],
        ["0 - 5", "Peserta menulis satu percakapan sulit yang sedang atau akan dihadapi", "Kertas kasus"],
        ["5 - 15", "Penjelasan ciri, spektrum, alur 4 langkah, dan rubrik", "Slide, Gambar 1 dan 2"],
        ["15 - 22", "Trainer memperagakan alur dengan relawan, kelas menilai dengan rubrik", "Rubrik"],
        ["22 - 30", "Peserta mengisi lembar persiapan", "Lembar persiapan"],
        ["30 - 84", "Role play bertiga, 3 putaran x 18 menit: 8 menit percakapan, 3 menit skor, 7 menit umpan balik", "Kartu peran, rubrik, pengatur waktu"],
        ["84 - 90", "Pembahasan bagian yang paling sering sulit dari lembar skor", "Rekap skor"],
    ], [2.2, 10.8, 4])
    h2(doc, "Kesalahan umum peserta dan cara meluruskan")
    table(doc, [
        ["Yang terjadi", "Yang dilakukan fasilitator"],
        ["Pemimpin langsung ke solusi di menit pertama", "Hentikan sebentar, minta pemimpin mengulang dengan pertanyaan terbuka"],
        ["Pemeran anggota tim terlalu mudah setuju", "Ingatkan isi kartu peran: diam bila disalahkan"],
        ["Kesepakatan tanpa waktu", "Tanya: \"Kapan Anda berdua akan tahu bahwa langkah ini berhasil?\""],
    ], [7.5, 9.5])
    h2(doc, "Penyesuaian setelah asesmen awal")
    bullets(doc, ["Tiga kasus role play diganti dengan tiga percakapan sulit yang paling sering ditulis peserta di formulir.",
                  "Kartu peran ditulis ulang bersama HR PT MMPP agar tidak mengarah ke orang tertentu."])
    return save(doc, "Contoh Modul M4 - Percakapan Sulit dengan Empati - PT MMPP")


def pages_png(pdf, prefix, pages):
    for pg in pages:
        subprocess.run(["pdftoppm", "-r", "70", "-png", "-f", str(pg), "-l", str(pg), "-singlefile", str(pdf),
                        str(VIS / f"hal-{prefix}-{pg:02d}")], check=True)


if __name__ == "__main__":
    p3 = modul_m3()
    p4 = modul_m4()
    pages_png(p3, "m3", range(1, 9))
    pages_png(p4, "m4", range(1, 11))
    print("Selesai:", p3.name, p4.name)
