"""Membuat visual SVG untuk deck v3 dan contoh modul, lalu merender PNG lewat Chromium.

Pemakaian (dari akar repo): python3 mmpp-empathy-leadership/_build/build_visual.py
Hasil: mmpp-empathy-leadership/_build/visual/*.svg dan *.png
"""
import json
import subprocess
from pathlib import Path

from svgkit import (BLUE, BLUE_L, CYAN, GREY, GREY_F, GREY_T, INK, MOD, PINK, PINK_L, ROW_ALT,
                    TEAL, TEAL_D, TEAL_H, TEAL_L, WHITE, arrow, chip, circle, curve, glyph, icon,
                    line, lines_needed, rect, svg, text)

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "visual"
OUT.mkdir(exist_ok=True)
FILES = {}


def save(name, w, h, body):
    p = OUT / f"{name}.svg"
    p.write_text(svg(w, h, body), encoding="utf-8")
    FILES[name] = (w, h)


# ======================================================================
# V1 kebutuhan ke hasil
# ======================================================================
def v_kebutuhan():
    W, H = 1223, 550
    b = []
    b.append(text(0, 0, "KEBUTUHAN PT MMPP", 13, True, TEAL))
    b.append(text(445, 0, "MODUL PELATIHAN", 13, True, TEAL))
    b.append(text(890, 0, "YANG BISA DIKERJAKAN PESERTA", 13, True, BLUE))
    needs = [("chat", "Komunikasi pemimpin", "Memperkuat keterampilan komunikasi para pemimpin"),
             ("people", "Pola pikir kolaboratif", "Kerja sama di dalam dan antartim"),
             ("heart", "Kepemimpinan berbasis empati", "Memimpin dengan memahami orang lain")]
    ny = [40, 170, 300]
    mods = [("M1", "Empati dalam Kepemimpinan", "heart"), ("M2", "Mendengar untuk Memahami", "listen"),
            ("M3", "Umpan Balik yang Menjaga Martabat", "chat"), ("M4", "Percakapan Sulit dengan Empati", "chat2"),
            ("M5", "Tim yang Aman untuk Bicara", "shield"), ("M6", "Rencana Aksi 30 Hari", "flag")]
    my = [34 + i * 66 for i in range(6)]
    mh = 52
    links = {0: [1, 2, 3], 1: [4, 3], 2: [0, 3, 5]}
    for ni, targets in links.items():
        for t in targets:
            b.append(curve(335, ny[ni] + 55, 445, my[t] + mh / 2, TEAL_L, 4))
    for i, (ic, t, d) in enumerate(needs):
        y = ny[i]
        b.append(rect(0, y, 335, 110, ROW_ALT, 12, GREY))
        b.append(icon(ic, 48, y + 55, 30, TEAL_H))
        b.append(text(92, y + 22, t, 18, True, INK, width=230))
        b.append(text(92, y + 22 + 23 * lines_needed(t, 230, 18, True), d, 12.5, False, GREY_T, width=230))
    for i, (code, name, ic) in enumerate(mods):
        y = my[i]
        c = MOD[code]
        b.append(rect(445, y, 335, mh, WHITE, mh / 2, c, 2))
        b.append(icon(ic, 445 + mh / 2, y + mh / 2, mh / 2 - 4, c))
        b.append(text(445 + mh + 8, y + mh / 2, f"{code}  {name}", 13.5, True, INK, valign="middle"))
    outs = [None, "Mendengar sampai paham isi dan perasaan anggota tim",
            "Memberi umpan balik SBI tanpa menjatuhkan martabat",
            "Memimpin percakapan sulit, skor minimal 6 dari 8",
            "Membaca rasa aman tim dan menyusun norma tim",
            "Menjalankan rencana aksi 30 hari yang dipantau tim"]
    for i, o in enumerate(outs):
        y = my[i]
        if o is None:
            b.append(text(890, y + mh / 2, "Dasar cara pandang untuk semua modul", 12.5, False, GREY_T,
                          valign="middle", italic=True))
            continue
        b.append(arrow(782, y + mh / 2, 884, y + mh / 2, MOD[mods[i][0]], 2.5, 9))
        b.append(rect(890, y, 333, mh, BLUE_L, 10))
        b.append(icon("check", 890 + 24, y + mh / 2, 14, BLUE))
        b.append(text(948, y + mh / 2, o, 13, False, INK, width=268, valign="middle"))
    # pita ketentuan
    y = 462
    b.append(line(0, y - 14, W, y - 14, GREY, 1.2))
    b.append(text(0, y - 4, "KETENTUAN DARI BRIEF", 12, True, GREY_T))
    chips = [("pin", "Luring"), ("lock", "Privat, khusus PT MMPP"), ("calendar", "Januari - Maret 2027"),
             ("pin", "Makassar atau Jakarta"), ("build", "Satu paket dengan tempat")]
    cw = (W - 4 * 14) / 5
    for i, (ic, lab) in enumerate(chips):
        x = i * (cw + 14)
        b.append(rect(x, y + 22, cw, 54, TEAL_L, 27))
        b.append(icon(ic, x + 27, y + 49, 19, TEAL_D))
        b.append(text(x + 54, y + 49, lab, 13.5, True, INK, valign="middle", width=cw - 60))
    save("01-kebutuhan-ke-hasil", W, H, "\n".join(b))


# ======================================================================
# V2 riset
# ======================================================================
def v_riset():
    W, H = 1223, 565
    b = []
    pw, ph, gap = 290, 340, 21
    xs = [i * (pw + gap) for i in range(4)]
    for x in xs:
        b.append(rect(x, 0, pw, ph, ROW_ALT, 14, GREY))

    def src(x, label):
        b.append(chip(x + 14, ph - 50, pw - 28, 36, label, PINK, INK, 11.5))

    # CCL
    x = xs[0]
    b.append(icon("globe", x + 40, 42, 24, TEAL_H))
    b.append(text(x + 74, 22, "Empati dan kinerja manajer", 13.5, True, TEAL, width=200))
    b.append(text(x + 20, 82, "6.731", 52, True, TEAL_D))
    b.append(text(x + 20, 146, "manajer dari 38 negara", 17, True, INK))
    b.append(text(x + 20, 182, "Manajer yang dinilai bawahannya lebih empatik dinilai atasannya "
                               "berkinerja lebih baik. Pengaruhnya lebih besar di budaya dengan jarak "
                               "kekuasaan tinggi.", 12.5, False, GREY_T, width=pw - 40, lh=1.3))
    src(x, "Center for Creative Leadership, 2016")
    # Catalyst
    x = xs[1]
    b.append(icon("chart", x + 40, 42, 24, BLUE))
    b.append(text(x + 74, 22, "Pemimpin senior yang empatik", 13.5, True, BLUE, width=200))
    groups = [("Merasa terlibat", 76, 32), ("Sering inovatif", 61, 13)]
    y = 88
    for lab, a, c in groups:
        b.append(text(x + 20, y, lab, 13, True, INK))
        bw = pw - 90
        b.append(rect(x + 20, y + 22, bw * a / 100, 22, TEAL_H, 4))
        b.append(text(x + 26 + bw * a / 100, y + 26, f"{a}%", 13, True, TEAL_D))
        b.append(rect(x + 20, y + 48, bw * c / 100, 22, GREY, 4))
        b.append(text(x + 26 + bw * c / 100, y + 52, f"{c}%", 13, True, GREY_T))
        y += 92
    b.append(rect(x + 20, 268, 14, 14, TEAL_H, 3))
    b.append(text(x + 40, 267, "sangat empatik", 11.5, False, INK))
    b.append(rect(x + 150, 268, 14, 14, GREY, 3))
    b.append(text(x + 170, 267, "kurang empatik", 11.5, False, INK))
    src(x, "Catalyst 2021, survei 889 karyawan")
    # Edmondson
    x = xs[2]
    b.append(icon("people", x + 40, 42, 24, TEAL_H))
    b.append(text(x + 74, 22, "Studi 51 tim kerja manufaktur", 13.5, True, TEAL, width=200))
    chain = [("Rasa aman psikologis", TEAL_H, WHITE), ("Perilaku belajar tim", TEAL_L, INK),
             ("Kinerja tim", BLUE_L, INK)]
    y = 92
    for i, (lab, f, c) in enumerate(chain):
        b.append(rect(x + 30, y, pw - 60, 46, f, 23))
        b.append(text(x + pw / 2, y + 23, lab, 14, True, c, "middle", valign="middle"))
        if i < 2:
            b.append(arrow(x + pw / 2, y + 48, x + pw / 2, y + 70, TEAL_D, 3, 9))
        y += 72
    src(x, "Edmondson, ASQ, 1999")
    # Google
    x = xs[3]
    b.append(icon("star", x + 40, 42, 24, BLUE))
    b.append(text(x + 74, 22, "Lima ciri tim yang efektif", 13.5, True, BLUE, width=200))
    pyr = ["Dampak", "Makna", "Struktur dan kejelasan", "Dapat diandalkan", "Rasa aman psikologis"]
    y = 76
    for i, lab in enumerate(pyr):
        w = 130 + i * 30
        base = i == 4
        b.append(rect(x + (pw - w) / 2, y, w, 34, TEAL_H if base else TEAL_L, 6))
        b.append(text(x + pw / 2, y + 17, lab, 12.5 if not base else 13, base, WHITE if base else INK,
                      "middle", valign="middle"))
        y += 38
    b.append(text(x + pw / 2, y + 6, "Fondasi: faktor paling mendasar", 12, True, TEAL_D, "middle"))
    src(x, "Google, Project Aristotle, 2016")

    # pembeda
    y0 = 362
    b.append(text(0, y0, "YANG MEMBUAT PROGRAM INI BERBEDA", 13, True, TEAL))
    cards = [("search", "Kasus nyata PT MMPP",
              "Asesmen awal mengumpulkan percakapan sulit yang benar-benar dihadapi peserta. Tiga kasus terbanyak menjadi bahan role play."),
             ("heart", "Nilai lokal siri' na pacce",
              "Pacce: ikut merasakan kesusahan orang lain. Siri': harga diri. Dipakai sebagai bahasa bersama untuk empati dan menjaga martabat."),
             ("chart", "Terukur sebelum dan sesudah",
              "Rubrik percakapan 0 sampai 8 di role play. Survei anggota tim sebelum pelatihan dan 30 hari sesudahnya.")]
    cw = (W - 2 * 18) / 3
    for i, (ic, t, d) in enumerate(cards):
        x = i * (cw + 18)
        b.append(rect(x, y0 + 26, cw, 150, WHITE, 14, GREY))
        b.append(icon(ic, x + 42, y0 + 70, 26, [TEAL_H, BLUE, TEAL_D][i]))
        b.append(text(x + 82, y0 + 46, t, 16, True, INK, width=cw - 95))
        b.append(text(x + 82, y0 + 74, d, 12.5, False, GREY_T, width=cw - 95, lh=1.3))
    save("02-riset", W, H, "\n".join(b))


# ======================================================================
# V3 alur program
# ======================================================================
def v_alur():
    W, H = 1223, 560
    b = []
    steps = [
        ("search", "H-18 sampai H-10", "Asesmen kebutuhan",
         "Formulir diri, survei 3 anggota tim per peserta, survei rasa aman tim, wawancara 3 sampai 5 peserta",
         "Profil peserta dan 3 kasus utama"),
        ("pencil", "H-10 sampai H-7", "Penyesuaian modul",
         "Kasus role play, kalimat latihan, dan kartu peran dari hasil asesmen. Disetujui HR PT MMPP",
         "Modul, kartu peran, lembar kerja"),
        ("build", "H-3 sampai H-1", "Persiapan tempat",
         "Meja kelompok 5 orang, ruang latihan bertiga, proyektor, flipchart, konsumsi",
         "Ruang dan bahan siap"),
        ("people", "Hari H, 08.30 - 16.30", "Pelatihan 1 hari",
         "Enam modul, 340 menit materi. Pre-test di awal, post-test di akhir",
         "Skor tes, rubrik, norma tim, rencana 30 hari"),
        ("calendar", "H+30", "Tindak lanjut",
         "Survei anggota tim diulang. Sesi daring 90 menit untuk berbagi penerapan dan kendala",
         "Skor survei sebelum dan sesudah"),
        ("doc", "H+40", "Evaluasi dan laporan",
         "Analisis tes, rubrik, survei kepuasan, perubahan skor survei tim, rekomendasi lanjutan",
         "Laporan akhir"),
    ]
    n = len(steps)
    sp = W / n
    cy = 110
    b.append(line(sp / 2, cy, W - sp / 2, cy, TEAL_L, 8))
    for i, (ic, when, t, d, out) in enumerate(steps):
        cx = sp / 2 + i * sp
        hi = i == 3
        b.append(chip(cx - 88, 8, 176, 32, when, BLUE if hi else TEAL_L, WHITE if hi else TEAL_D, 12.5))
        b.append(icon(ic, cx, cy, 44 if hi else 38, BLUE if hi else CYAN))
        b.append(circle(cx + 30, cy - 30, 14, TEAL_D))
        b.append(text(cx + 30, cy - 30, str(i + 1), 13, True, WHITE, "middle", valign="middle"))
        b.append(text(cx, 168, t, 16, True, INK, "middle", width=sp - 16))
        b.append(text(cx, 200, d, 12.5, False, GREY_T, "middle", width=sp - 24, lh=1.3))
        b.append(chip(cx - (sp - 24) / 2, 330, sp - 24, 50, out, PINK, INK, 12))
    # metode
    y = 410
    b.append(text(0, y, "METODE DI SEPANJANG ALUR", 12.5, True, TEAL))
    b.append(rect(0, y + 26, W, 34, TEAL_H, 17))
    b.append(text(W / 2, y + 43, "ADDIE: alur program dari analisis kebutuhan sampai evaluasi (tahap 1 sampai 6)",
                  13, True, WHITE, "middle", valign="middle"))

    def span(i0, i1, label, fill, color=INK):
        x0 = i0 * sp + 8
        x1 = (i1 + 1) * sp - 8
        b.append(chip(x0, y + 72, x1 - x0, 40, label, fill, color, 12))

    span(1, 1, "Bloom: tujuan berkode C2 sampai C6", TEAL_L)
    span(3, 3, "Andragogi: belajar dari kasus sendiri", BLUE_L)
    span(4, 5, "Kirkpatrick: evaluasi level 1 sampai 3", PINK_L)
    span(0, 0, "Backward design: mulai dari kondisi peserta", TEAL_L)
    save("03-alur-program", W, H, "\n".join(b))


# ======================================================================
# V4 ringkasan modul dan peta hari
# ======================================================================
MODS = [
    ("M1", "Empati dalam Kepemimpinan", "heart", 40,
     ["1.1 Empati di tempat kerja", "1.2 Pacce: empati dalam nilai lokal"], "Daftar perilaku siri' dan pacce"),
    ("M2", "Mendengar untuk Memahami", "listen", 60,
     ["2.1 Tingkat mendengar", "2.2 Bertanya dan merefleksikan perasaan"], "Lembar cek praktik mendengar"),
    ("M3", "Umpan Balik yang Menjaga Martabat", "chat", 60,
     ["3.1 Bahasa yang menjaga martabat", "3.2 Umpan balik SBI dan niat"], "Naskah umpan balik kasus nyata"),
    ("M4", "Percakapan Sulit dengan Empati", "chat2", 90,
     ["4.1 Alur Percakapan Empatik", "4.2 Role play kasus nyata"], "Skor rubrik 0 sampai 8"),
    ("M5", "Tim yang Aman untuk Bicara", "shield", 60,
     ["5.1 Rasa aman psikologis", "5.2 Norma tim"], "Draf norma tim"),
    ("M6", "Rencana Aksi 30 Hari", "flag", 30,
     ["6.1 Profil empati dan rencana aksi"], "Rencana aksi 30 hari"),
]
PRAKTIK, JELAS = 257, 83


def v_ringkasan():
    W, H = 1223, 555
    b = []
    cw, ch, g = 278, 262, 14
    for i, (code, name, ic, mnt, tops, out) in enumerate(MODS):
        x = (i % 3) * (cw + g)
        y = (i // 3) * (ch + g)
        c = MOD[code]
        b.append(rect(x, y, cw, ch, WHITE, 14, GREY))
        b.append(f'<path d="M{x},{y + 14} a14,14 0 0 1 14,-14 h{cw - 28} a14,14 0 0 1 14,14 v48 h-{cw} z" fill="{c}"/>')
        b.append(icon(ic, x + 32, y + 31, 20, "#FFFFFF33"))
        b.append(text(x + 62, y + 31, code, 22, True, WHITE, valign="middle"))
        b.append(text(x + cw - 16, y + 31, f"{mnt} menit", 15, True, WHITE, "end", valign="middle"))
        b.append(text(x + 16, y + 76, name, 15.5, True, INK, width=cw - 32))
        ty = y + 76 + 21 * lines_needed(name, cw - 32, 15.5, True) + 6
        for t in tops:
            b.append(text(x + 16, ty, t, 12.5, False, GREY_T, width=cw - 32))
            ty += 19
        # bar menit (skala 90)
        b.append(rect(x + 16, y + ch - 76, cw - 32, 10, ROW_ALT, 5))
        b.append(rect(x + 16, y + ch - 76, (cw - 32) * mnt / 90, 10, c, 5))
        b.append(rect(x + 12, y + ch - 52, cw - 24, 40, PINK_L, 8))
        b.append(glyph("check", x + 18, y + ch - 44, 20).replace("#fff", TEAL_D))
        b.append(text(x + 44, y + ch - 32, out, 12.5, True, INK, valign="middle", width=cw - 60))
    # donat
    x0 = 3 * (cw + g) + 14
    cx, cy, r = x0 + (W - x0) / 2, 150, 105
    import math
    tot = PRAKTIK + JELAS
    a = 2 * math.pi * PRAKTIK / tot
    sx, sy = cx, cy - r
    ex, ey = cx + r * math.sin(a), cy - r * math.cos(a)
    b.append(circle(cx, cy, r, "none", GREY, 34))
    b.append(f'<path d="M{sx},{sy} A{r},{r} 0 {1 if a > math.pi else 0} 1 {ex:.1f},{ey:.1f}" fill="none" '
             f'stroke="{TEAL_H}" stroke-width="34"/>')
    b.append(text(cx, cy - 10, "340", 40, True, INK, "middle", valign="middle"))
    b.append(text(cx, cy + 24, "menit materi", 14, False, GREY_T, "middle", valign="middle"))
    ly = 285
    b.append(rect(x0, ly, 16, 16, TEAL_H, 3))
    b.append(text(x0 + 24, ly - 1, f"{PRAKTIK} menit praktik, role play, kerja kelompok ({round(PRAKTIK * 100 / tot)}%)",
                  13, True, INK, width=W - x0 - 24))
    b.append(rect(x0, ly + 48, 16, 16, GREY, 3))
    b.append(text(x0 + 24, ly + 47, f"{JELAS} menit penjelasan dan peragaan trainer ({round(JELAS * 100 / tot)}%)",
                  13, False, INK, width=W - x0 - 24))
    b.append(text(x0, ly + 92, "Sumber: hitungan dari rundown aktivitas silabus ini", 11, False, GREY_F,
                  width=W - x0, italic=True))
    facts = [("people", "Paling banyak 24 peserta per kelas"),
             ("handshake", "1 trainer dan 1 co-fasilitator"),
             ("calendar", "Tindak lanjut daring 90 menit di hari ke-30")]
    fy = ly + 128
    for ic, t in facts:
        b.append(icon(ic, x0 + 16, fy + 14, 15, TEAL_D))
        b.append(text(x0 + 40, fy + 14, t, 12.5, True, INK, valign="middle", width=W - x0 - 40))
        fy += 40
    save("04-ringkasan-modul", W, H, "\n".join(b))


def v_peta_hari():
    W, H = 1223, 565
    b = []
    blocks = [("08.30", 15, "Pembukaan", "o"), ("08.45", 10, "Pre-test", "o"), ("08.55", 40, "M1", "M1"),
              ("09.35", 60, "M2", "M2"), ("10.35", 15, "Rehat", "r"), ("10.50", 60, "M3", "M3"),
              ("11.50", 60, "Ishoma", "r"), ("12.50", 90, "M4", "M4"), ("14.20", 15, "Rehat", "r"),
              ("14.35", 60, "M5", "M5"), ("15.35", 30, "M6", "M6"), ("16.05", 10, "Post-test", "o"),
              ("16.15", 15, "Penutupan", "o")]
    k = W / 480
    y, h = 62, 96
    x = 0
    up = 0
    names = {m[0]: m[1] for m in MODS}
    for st, mnt, lab, kind in blocks:
        w = mnt * k
        fill = MOD.get(kind, PINK if kind == "o" else GREY)
        b.append(rect(x + 1, y, w - 2, h, fill, 6))
        if kind in MOD:
            b.append(text(x + w / 2, y + 26, lab, 20, True, WHITE, "middle", valign="middle"))
            b.append(text(x + w / 2, y + 52, f"{mnt} menit", 12, True, WHITE, "middle", valign="middle"))
            if w > 120:
                b.append(text(x + w / 2, y + 76, names[lab], 10.5, False, WHITE, "middle", valign="middle",
                              width=w - 10))
        elif w > 60:
            b.append(text(x + w / 2, y + h / 2, lab, 12.5, True, GREY_T, "middle", valign="middle"))
        else:
            ly = 20 if up % 2 == 0 else 40
            up += 1
            b.append(line(x + w / 2, ly + 14, x + w / 2, y, GREY_F, 1))
            anc = "start" if x < 40 else ("end" if x + w > W - 40 else "middle")
            lx = x if anc == "start" else (x + w if anc == "end" else x + w / 2)
            b.append(text(lx, ly - 2, lab, 11, True, GREY_T, anc))
        x += w
    for hr in range(9, 17):
        tx = (hr * 60 - 510) * k
        b.append(line(tx, y + h, tx, y + h + 8, GREY_T, 1.2))
        b.append(text(tx, y + h + 12, f"{hr:02d}.00", 11.5, False, GREY_T, "middle"))
    b.append(text(0, y + h + 12, "08.30", 11.5, True, INK))
    b.append(text(W, y + h + 12, "16.30", 11.5, True, INK, "end"))
    # perjalanan peserta
    y2 = 250
    b.append(text(0, y2, "PERJALANAN PESERTA", 13, True, TEAL))
    stages = [("search", "H-18 sampai H-10", "Asesmen awal",
               "Formulir diri, survei 3 anggota tim, survei rasa aman tim, wawancara. Kasus role play berasal dari sini."),
              ("people", "Hari H", "Pelatihan 1 hari",
               "6 modul, 340 menit materi, role play dengan rubrik 0 sampai 8, pre-test dan post-test."),
              ("flag", "Hari 1 sampai 30", "Menjalankan rencana",
               "Dua perilaku prioritas dengan tindakan mingguan, dipantau bersama mitra pengingat."),
              ("calendar", "H+30", "Tindak lanjut daring",
               "Sesi 90 menit: berbagi hasil, membahas kendala, membaca skor survei tim kedua.")]
    sw = W / 4
    b.append(line(sw / 2, y2 + 70, W - sw / 2, y2 + 70, TEAL_L, 6))
    for i, (ic, when, t, d) in enumerate(stages):
        cx = sw / 2 + i * sw
        b.append(icon(ic, cx, y2 + 70, 34, BLUE if i == 1 else TEAL_H))
        b.append(chip(cx - 80, y2 + 116, 160, 28, when, TEAL_L, TEAL_D, 12))
        b.append(text(cx, y2 + 156, t, 15.5, True, INK, "middle"))
        b.append(text(cx, y2 + 182, d, 12.5, False, GREY_T, "middle", width=sw - 30, lh=1.3))
    save("05-peta-hari", W, H, "\n".join(b))


# ======================================================================
# V5 alur percakapan empatik
# ======================================================================
STEPS4 = [
    ("Siapkan", "clip", "Pisahkan fakta dan tafsiran. Tetapkan tujuan bersama",
     "Catatan: laporan stok terlambat 3 kali bulan ini (fakta). Dia kurang peduli (tafsiran saya). Tujuan: laporan tepat waktu tanpa lembur.",
     "note"),
    ("Dengarkan", "listen", "Buka dengan fakta dan pertanyaan terbuka. Refleksikan perasaan",
     "\"Laporan stok tiga kali terlambat bulan ini. Bagaimana keadaannya dari sisi kamu?\"", "lead"),
    ("Akui", "heart", "Sebut kepentingan kedua pihak tanpa menyalahkan",
     "\"Jadi data gudang sering baru masuk sore, dan kamu kesal karena kamu yang ditegur. Saya juga perlu laporan itu untuk rapat pagi.\"",
     "lead"),
    ("Sepakati", "handshake", "Langkah, penanggung jawab, waktu, cara memantau",
     "\"Besok saya bicara dengan kepala gudang supaya data masuk jam 14.00. Jumat kamu kabari saya apakah berjalan.\"",
     "lead"),
]


def v_alur4(name="06-alur-percakapan", compact=False):
    W = 1223
    H = 330 if compact else 560
    b = []
    sw = W / 4
    cols = [TEAL_H, BLUE, TEAL_H, BLUE]
    for i, (nm, ic, do, ex, kind) in enumerate(STEPS4):
        cx = sw / 2 + i * sw
        if i < 3:
            b.append(arrow(cx + 52, 58, cx + sw - 56, 58, GREY_F, 3, 12))
        b.append(icon(ic, cx, 58, 46, cols[i]))
        b.append(circle(cx + 36, 22, 15, TEAL_D))
        b.append(text(cx + 36, 22, str(i + 1), 14, True, WHITE, "middle", valign="middle"))
        b.append(text(cx, 118, nm, 20, True, INK, "middle"))
        b.append(text(cx, 148, do, 13, False, GREY_T, "middle", width=sw - 40, lh=1.3))
        if compact:
            b.append(chip(cx - 110, 230, 220, 34, "Skor 0, 1, atau 2", TEAL_L, TEAL_D, 12.5))
            continue
        # gelembung contoh
        by, bh = 222, 168
        bx, bw = cx - sw / 2 + 12, sw - 24
        if kind == "note":
            b.append(rect(bx, by, bw, bh, "#FFF8D6", 6, "#E8D98A"))
            b.append(text(bx + 12, by + 10, "CATATAN PEMIMPIN", 11, True, "#8A7A20"))
            b.append(text(bx + 12, by + 30, ex, 12.5, False, INK, width=bw - 24, lh=1.3))
        else:
            b.append(rect(bx, by, bw, bh, ROW_ALT, 14, cols[i], 1.5))
            b.append(f'<path d="M{cx - 12},{by} l12,-14 l12,14 z" fill="{ROW_ALT}" stroke="{cols[i]}" stroke-width="1.5"/>')
            b.append(rect(cx - 11, by - 1, 22, 4, ROW_ALT, 0))
            b.append(text(bx + 12, by + 10, "SUPERVISOR", 11, True, cols[i]))
            b.append(text(bx + 12, by + 30, ex, 12.5, False, INK, width=bw - 24, lh=1.3, italic=True))
    if compact:
        b.append(text(W / 2, 290, "Total 0 sampai 8. Target: minimal 6 di putaran ketiga role play",
                      14, True, TEAL_D, "middle"))
        save(name, W, H, "\n".join(b))
        return
    # rubrik
    y = 420
    b.append(text(0, y, "RUBRIK PENGAMAT", 12.5, True, TEAL))
    rw = (W - 200 - 4 * 12) / 4
    for i, (nm, *_r) in enumerate(STEPS4):
        x = i * (rw + 12)
        b.append(rect(x, y + 24, rw, 56, WHITE, 10, GREY))
        b.append(text(x + 14, y + 52, nm, 14, True, INK, valign="middle"))
        for j in range(3):
            fill = cols[i] if j == 2 else (TEAL_L if j == 1 else ROW_ALT)
            b.append(circle(x + rw - 96 + j * 32, y + 52, 13, fill, GREY, 1))
            b.append(text(x + rw - 96 + j * 32, y + 52, str(j), 12, True, WHITE if j == 2 else INK, "middle",
                          valign="middle"))
    tx = 4 * (rw + 12)
    b.append(rect(tx, y + 24, W - tx, 56, TEAL_D, 10))
    b.append(text(tx + (W - tx) / 2, y + 42, "Total 8", 15, True, WHITE, "middle", valign="middle"))
    b.append(text(tx + (W - tx) / 2, y + 64, "Target minimal 6", 12, False, WHITE, "middle", valign="middle"))
    b.append(text(0, y + 100, "Contoh rekaan: supervisor dan staf administrasi gudang. Kasus asli diambil dari asesmen awal.",
                  11.5, False, GREY_F, italic=True))
    save(name, W, H, "\n".join(b))


# ======================================================================
# V6 persiapan dan evaluasi
# ======================================================================
def v_persiapan():
    W, H = 1223, 560
    b = []
    who = {"S": (TEAL_H, "Sanggabiz"), "P": (BLUE, "PT MMPP"), "B": (TEAL_D, "Bersama")}
    items = [("H-21", "Rapat awal: jumlah peserta, jadwal, kota, daftar peserta dan atasan", "B"),
             ("H-18", "Asesmen awal dikirim, disebarkan HR PT MMPP", "S"),
             ("H-14", "Wawancara 30 menit dengan 3 sampai 5 peserta dan atasannya", "S"),
             ("H-10", "Rekap asesmen, 3 kasus utama, profil empati per peserta", "S"),
             ("H-7", "Modul, kartu peran, dan lembar kerja disetujui", "P"),
             ("H-3", "Cetak bahan, konfirmasi ruang, konsumsi, daftar hadir", "S"),
             ("H-1", "Penataan ruang: meja kelompok 5 orang, proyektor, flipchart", "S"),
             ("Hari H", "Pelatihan 1 hari, 08.30 - 16.30", "B"),
             ("H+30", "Survei tim kedua dan sesi tindak lanjut daring", "S"),
             ("H+40", "Laporan akhir diserahkan", "S")]
    n = len(items)
    sp = W / n
    cy = 250
    b.append(line(sp / 2, cy, W - sp / 2, cy, TEAL_L, 8))
    for i, (when, t, w) in enumerate(items):
        cx = sp / 2 + i * sp
        c, _ = who[w]
        hi = when == "Hari H"
        b.append(circle(cx, cy, 30 if hi else 22, BLUE if hi else c))
        b.append(text(cx, cy, when, 12 if hi else 11.5, True, WHITE, "middle", valign="middle", width=56))
        top = i % 2 == 0
        ty = cy - 60 if top else cy + 50
        b.append(line(cx, cy + (-24 if top else 24), cx, ty + (0 if top else 0), c, 1.5, "4 3"))
        bw = sp * 1.6
        nl = lines_needed(t, bw - 16, 12.5)
        bh = nl * 16 + 22
        by = ty - bh if top else ty
        bx = min(max(cx - bw / 2, 1), W - bw - 1)
        b.append(rect(bx, by, bw, bh, ROW_ALT, 10, c, 1.5))
        b.append(text(bx + bw / 2, by + 10, t, 12.5, False, INK, "middle", width=bw - 16, lh=1.25))
    ly = 470
    for i, k in enumerate(["S", "P", "B"]):
        c, lab = who[k]
        b.append(circle(20 + i * 200, ly, 10, c))
        b.append(text(38 + i * 200, ly, lab, 13, True, INK, valign="middle"))
    b.append(text(640, ly, "Warna titik menunjukkan penanggung jawab", 12, False, GREY_T, valign="middle", italic=True))
    save("07-persiapan", W, H, "\n".join(b))


def v_evaluasi():
    W, H = 1223, 560
    b = []
    lv = [("Level 1", "Reaksi", "Survei kepuasan 8 butir di akhir pelatihan", "Rata-rata minimal 4 dari 5", TEAL_L, INK),
          ("Level 2", "Pembelajaran", "Pre-test dan post-test 10 soal kasus. Rubrik 0 sampai 8 di role play",
           "Skor tes naik. Rubrik minimal 6 dari 8", CYAN, WHITE),
          ("Level 3", "Perilaku", "Survei 3 anggota tim per peserta sebelum pelatihan dan di hari ke-30",
           "Dua perilaku prioritas naik pada minimal separuh peserta", TEAL_H, WHITE),
          ("Level 4", "Dampak bisnis", "Tidak kami janjikan dalam 30 hari. Bisa dibandingkan dengan data PT MMPP bila tersedia",
           "", WHITE, GREY_T)]
    sw = 290
    for i, (l, nm, tool, tgt, f, c) in enumerate(lv):
        x = i * (sw + 21)
        h = 170 + i * 50
        y = 330 - h
        dashed = i == 3
        b.append(rect(x, y, sw, h, f, 12, GREY_F if dashed else None, 2, "6 5" if dashed else None))
        b.append(text(x + 16, y + 14, l, 13, True, c))
        b.append(text(x + 16, y + 34, nm, 20, True, c))
        b.append(text(x + 16, y + 66, tool, 12.5, False, c, width=sw - 32, lh=1.3))
        if tgt:
            ty = y + 66 + 17 * lines_needed(tool, sw - 32, 12.5) + 10
            b.append(rect(x + 12, ty, sw - 24, 22 + 16 * lines_needed(tgt, sw - 56, 12, True), WHITE, 8, None,
                          opacity=0.92))
            b.append(text(x + 24, ty + 8, "Target: " + tgt, 12, True, TEAL_D, width=sw - 48))
    # titik ukur
    y = 380
    b.append(text(0, y, "KAPAN DIUKUR", 12.5, True, TEAL))
    pts = [("H-18", "Survei tim pertama, profil empati", TEAL_H),
           ("Hari H, 08.45", "Pre-test", CYAN),
           ("Hari H, 12.50", "Rubrik role play 3 putaran", CYAN),
           ("Hari H, 16.05", "Post-test dan survei kepuasan", CYAN),
           ("H+30", "Survei tim kedua", TEAL_H)]
    sp = W / len(pts)
    b.append(line(sp / 2, y + 52, W - sp / 2, y + 52, TEAL_L, 6))
    for i, (w, t, c) in enumerate(pts):
        cx = sp / 2 + i * sp
        b.append(circle(cx, y + 52, 14, c))
        b.append(text(cx, y + 80, w, 13, True, INK, "middle"))
        b.append(text(cx, y + 102, t, 12.5, False, GREY_T, "middle", width=sp - 20))
    save("08-evaluasi", W, H, "\n".join(b))


# ======================================================================
# V7 hasil yang dibawa pulang
# ======================================================================
def v_hasil():
    W, H = 1223, 540
    b = []
    outs = [("1.1", "M1", "doc", "Catatan tiga bentuk empati dengan contoh dari pekerjaan"),
            ("1.2", "M1", "heart", "Daftar perilaku siri' dan pacce di tempat kerja"),
            ("2.2", "M2", "clip", "Lembar cek pengamat praktik mendengar"),
            ("3.1", "M3", "pencil", "5 kalimat teguran yang sudah diperbaiki"),
            ("3.2", "M3", "chat", "Naskah umpan balik SBI untuk kasus nyata"),
            ("4.1", "M4", "doc", "Lembar persiapan dan kartu Alur 4 langkah"),
            ("4.2", "M4", "chart", "Skor rubrik percakapan sulit dari pengamat"),
            ("5.1", "M5", "shield", "Skor rasa aman tim dan butir terendah"),
            ("5.2", "M5", "people", "Draf norma tim untuk rapat tim"),
            ("6.1", "M6", "search", "Profil empati diri dan tim"),
            ("6.1", "M6", "flag", "Rencana aksi 30 hari dengan mitra pengingat"),
            ("H+30", "M6", "calendar", "Skor survei tim sebelum dan sesudah")]
    cw, ch, g = (W - 3 * 16) / 4, 150, 16
    for i, (tp, m, ic, t) in enumerate(outs):
        x = (i % 4) * (cw + g)
        y = (i // 4) * (ch + g) + 10
        c = MOD[m]
        b.append(rect(x, y, cw, ch, WHITE, 14, GREY))
        b.append(rect(x, y, 8, ch, c, 4))
        b.append(icon(ic, x + 44, y + 44, 26, c))
        b.append(chip(x + cw - 84, y + 14, 70, 28, tp, TEAL_L, TEAL_D, 12.5))
        b.append(text(x + 22, y + 82, t, 14, True, INK, width=cw - 36, lh=1.25))
    ly = 3 * (ch + g) + 30
    for i, (m, nm) in enumerate([("M1", "Empati"), ("M2", "Mendengar"), ("M3", "Umpan balik"),
                                 ("M4", "Percakapan sulit"), ("M5", "Tim aman"), ("M6", "Rencana aksi")]):
        b.append(rect(i * 200, ly, 18, 18, MOD[m], 4))
        b.append(text(i * 200 + 26, ly - 1, f"{m} {nm}", 12.5, False, INK))
    save("09-hasil", W, H, "\n".join(b))


# ======================================================================
# V8 standar minimal modul
# ======================================================================
STANDAR = [
    ("book", "Sampul dan status", "Judul modul, program, klien, versi, label DRAF atau CONTOH"),
    ("target", "Peta modul", "Tujuan berkode Bloom, durasi, posisi di program, output"),
    ("search", "Konsep inti bergambar", "Satu halaman per konsep, satu diagram yang mudah dibaca"),
    ("chat", "Contoh lengkap", "Contoh dari konteks klien. Diberi label rekaan bila belum dari asesmen"),
    ("pencil", "Lembar kerja", "Diisi peserta di kelas, langsung dipakai di role play"),
    ("clip", "Alat ukur", "Lembar cek atau rubrik dengan target yang jelas"),
    ("flag", "Refleksi dan tindak lanjut", "Yang dibawa dan dicoba di tempat kerja minggu itu"),
    ("clock", "Catatan fasilitator dan rujukan", "Alur menit, bahan, kesalahan umum peserta, sumber"),
]


def v_standar():
    W, H = 1223, 420
    b = []
    cw, ch, g = (W - 3 * 16) / 4, 190, 16
    for i, (ic, t, d) in enumerate(STANDAR):
        x = (i % 4) * (cw + g)
        y = (i // 4) * (ch + 20)
        b.append(rect(x, y, cw, ch, ROW_ALT, 14, GREY))
        b.append(f'<path d="M{x + cw - 40},{y} h26 a14,14 0 0 1 14,14 v26 z" fill="{TEAL_L}"/>')
        b.append(icon(ic, x + 40, y + 42, 26, TEAL_H if i % 2 == 0 else BLUE))
        b.append(text(x + cw - 18, y + 30, str(i + 1), 22, True, TEAL_D, "end", valign="middle"))
        b.append(text(x + 18, y + 84, t, 16, True, INK, width=cw - 36))
        b.append(text(x + 18, y + 84 + 21 * lines_needed(t, cw - 36, 16, True) + 4, d, 12.5, False, GREY_T,
                      width=cw - 36, lh=1.3))
    save("10-standar-modul", W, H, "\n".join(b))


# ======================================================================
# visual untuk contoh modul (A4)
# ======================================================================
def m_sbi():
    W, H = 1000, 330
    b = []
    parts = [("S", "Situasi", "Kapan dan di mana", "\"Di rapat mingguan Senin kemarin...\"", TEAL_H),
             ("B", "Perilaku", "Yang terlihat atau terdengar, tanpa menilai", "\"...kamu memotong Rina dua kali saat ia menjelaskan angka.\"", BLUE),
             ("I", "Dampak", "Akibatnya pada orang, tim, atau pekerjaan", "\"Rina berhenti bicara, dan kita tidak dengar usulnya.\"", TEAL_D),
             ("N", "Niat", "Pertanyaan agar umpan balik dua arah", "\"Apa yang sedang kamu pikirkan waktu itu?\"", "#7B4C9C")]
    sw = W / 4
    for i, (k, nm, d, ex, c) in enumerate(parts):
        x = i * sw
        if i < 3:
            b.append(arrow(x + sw - 26, 50, x + sw + 6, 50, GREY_F, 3, 10))
        b.append(circle(x + sw / 2 - 10, 50, 40, c))
        b.append(text(x + sw / 2 - 10, 50, k, 30, True, WHITE, "middle", valign="middle"))
        b.append(text(x + sw / 2 - 10, 104, nm, 20, True, INK, "middle"))
        b.append(text(x + sw / 2 - 10, 132, d, 13.5, False, GREY_T, "middle", width=sw - 40))
        b.append(rect(x + 8, 196, sw - 36, 112, ROW_ALT, 12, c, 1.5))
        b.append(text(x + 20, 208, ex, 14, False, INK, width=sw - 60, lh=1.3, italic=True))
    save("m3-sbi", W, H, "\n".join(b))


def m_orang_perilaku():
    W, H = 1000, 300
    b = []
    b.append(rect(0, 0, 470, 300, "#F4F4F4", 14, GREY))
    b.append(rect(530, 0, 470, 300, ROW_ALT, 14, TEAL_H, 1.5))
    b.append(text(24, 20, "MENYERANG ORANG", 15, True, GREY_T))
    b.append(text(554, 20, "MENYEBUT PERILAKU DAN DAMPAK", 15, True, TEAL_D))
    bad = ["\"Kamu tidak bisa diandalkan.\"", "\"Kamu selalu telat.\"", "\"Kerjamu asal-asalan.\""]
    good = ["\"Laporan stok terlambat dua hari minggu ini, rapat pagi jadi tanpa data.\"",
            "\"Kamu datang 08.40 tiga kali minggu ini, briefing jadi diulang.\"",
            "\"Ada 4 salah input di faktur kemarin, tim keuangan harus memeriksa ulang.\""]
    for i in range(3):
        y = 62 + i * 76
        b.append(text(24, y, bad[i], 15, False, INK, width=420, italic=True))
        b.append(text(554, y, good[i], 15, False, INK, width=420, italic=True))
    b.append(arrow(478, 150, 522, 150, TEAL_H, 4, 14))
    save("m3-orang-perilaku", W, H, "\n".join(b))


def m_spektrum():
    W, H = 1000, 250
    b = []
    b.append('<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#9FB7C9"/>'
             f'<stop offset="0.5" stop-color="{TEAL_H}"/><stop offset="1" stop-color="#C98BA8"/></linearGradient></defs>')
    b.append(rect(0, 70, W, 30, "url(#g)", 15))
    b.append(text(0, 10, "DIAM", 17, True, "#4F6F86"))
    b.append(text(W / 2, 10, "DIALOG", 17, True, TEAL_D, "middle"))
    b.append(text(W, 10, "MENYERANG", 17, True, "#8E4468", "end"))
    b.append(text(0, 34, "Menghindar dan menahan pendapat", 13, False, GREY_T))
    b.append(text(W / 2, 34, "Fakta, perasaan, dan usul dibicarakan", 13, False, GREY_T, "middle"))
    b.append(text(W, 34, "Memaksa pendapat dan menekan", 13, False, GREY_T, "end"))
    cols = [("Tanda diam", ["Mengalihkan topik", "Setuju di mulut, tidak dijalankan", "Jawaban singkat, menghindari tatapan"], "#4F6F86"),
            ("Tanda dialog", ["Bertanya untuk memahami", "Mengakui perasaan lawan bicara", "Mencari langkah bersama"], TEAL_D),
            ("Tanda menyerang", ["Nada meninggi, memotong", "Menyindir atau melabeli orang", "Membawa kesalahan lama"], "#8E4468")]
    for i, (t, items, c) in enumerate(cols):
        x = i * 340
        b.append(text(x + (0 if i == 0 else 10), 118, t, 14, True, c))
        for j, it in enumerate(items):
            b.append(text(x + (0 if i == 0 else 10), 142 + j * 24, "• " + it, 13, False, INK))
    save("m4-spektrum", W, H, "\n".join(b))


def render():
    names = list(FILES)
    js = """
const { chromium } = require('playwright');
const fs = require('fs');
const files = %s;
(async () => {
  const b = await chromium.launch();
  for (const [name, w, h] of files) {
    const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    const svg = fs.readFileSync('%s/' + name + '.svg', 'utf8');
    await p.setContent('<html><body style="margin:0;background:transparent">' + svg + '</body></html>');
    await p.screenshot({ path: '%s/' + name + '.png', omitBackground: true, clip: { x: 0, y: 0, width: w, height: h } });
    await p.close();
  }
  await b.close();
})();
""" % (json.dumps([[n, *FILES[n]] for n in names]), OUT, OUT)
    js_path = OUT / "_render.js"
    js_path.write_text(js)
    subprocess.run(["node", str(js_path)], check=True,
                   env={**__import__("os").environ, "NODE_PATH": "/opt/node22/lib/node_modules"})
    js_path.unlink()


if __name__ == "__main__":
    v_kebutuhan()
    v_riset()
    v_alur()
    v_ringkasan()
    v_peta_hari()
    v_alur4()
    v_alur4("m4-alur-ringkas", compact=True)
    v_persiapan()
    v_evaluasi()
    v_hasil()
    v_standar()
    m_sbi()
    m_orang_perilaku()
    m_spektrum()
    render()
    print("Visual:", ", ".join(FILES))
