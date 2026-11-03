"""Membuat halaman proposal 16:9: silabus dan aset pelatihan. IHT Layanan Inklusif PT BPR NBP 27.

Urutan (dari folder _build):
  python3 build_kit.py && node render.js jobs_kit.json
  python3 build_rekap.py
  python3 build_proposal.py && node render.js jobs_proposal.json
  python3 build_proposal.py --gabung
"""
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image
from gaya import BUILD, ROOT, FONT_FACE, LOGO, TEAL, TEAL_MUDA, CYAN, UNGU
from silabus import KIT, RINGKAS, MODUL, HASIL
from build_rekap import PESERTA

HTML = BUILD / "html"
HTML.mkdir(exist_ok=True)
SLIDE = ROOT / "proposal" / "aset-slide"
HAL = BUILD / "halaman"
HAL.mkdir(exist_ok=True)
NAMA_PDF = "v1 Silabus dan Aset Pelatihan - IHT Layanan Inklusif PT BPR NBP 27.pdf"

IKON = {
    "wa": '<svg viewBox="0 0 24 24" width="15" height="15"><path fill="#fff" d="M12 3a9 9 0 0 0-7.8 13.5L3 21l4.6-1.2A9 9 0 1 0 12 3zm4.4 12.6c-.2.5-1.1 1-1.6 1-.4.1-.9.1-1.5-.1-3-1.1-4.8-4-5-4.2-.1-.2-1-1.4-1-2.7 0-1.3.7-1.9.9-2.2.3-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.3 0 .5l-.4.6c-.1.2-.3.3-.1.6.6 1 1.4 1.9 2.5 2.4.3.2.5.1.6 0l.7-.9c.2-.2.4-.2.6-.1l1.8.9c.2.1.4.2.4.3.1.2.1.8-.1 1.3z"/></svg>',
    "web": '<svg viewBox="0 0 24 24" width="15" height="15"><circle cx="12" cy="12" r="8" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M4 12h16M12 4c2.5 2.5 2.5 13.5 0 16M12 4c-2.5 2.5-2.5 13.5 0 16" fill="none" stroke="#fff" stroke-width="1.5"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" width="15" height="15"><rect x="4" y="6" width="16" height="12" rx="1.5" fill="none" stroke="#fff" stroke-width="1.8"/><path d="M4.5 7l7.5 6 7.5-6" fill="none" stroke="#fff" stroke-width="1.8"/></svg>',
}

CSS = FONT_FACE + f"""
@page {{ size: 1280px 720px; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin:0; background:#fff; }}
body {{ font-family:'Inter', sans-serif; color:#1d1d1d; }}
.hal {{ width:1280px; height:720px; position:relative; padding:0 64px; overflow:hidden; }}
.kepala {{ height:84px; display:flex; align-items:center; justify-content:space-between; border-bottom:2px solid; border-image: linear-gradient(90deg,#8b5cf6,#a78bfa,#c4b5fd) 1; }}
.kepala img {{ height:30px; }}
.kepala .th {{ font-family:'Montserrat'; font-weight:700; font-size:17px; }}
h1 {{ font-family:'Montserrat'; font-weight:800; font-size:30px; text-align:center; margin:18px 0 2px; letter-spacing:.3px; color:#111; }}
.sub {{ text-align:center; font-size:13.5px; color:#333; margin:0 0 14px; }}
.kaki {{ position:absolute; left:64px; right:64px; bottom:0; height:62px; border-top:1.5px solid #222; display:flex; justify-content:space-between; align-items:center; font-family:'Montserrat'; font-weight:600; font-size:14px; }}
.kaki span {{ display:flex; align-items:center; gap:9px; }}
.kaki i {{ width:26px; height:26px; border-radius:50%; background:{CYAN}; display:flex; align-items:center; justify-content:center; }}
.isi {{ position:absolute; left:64px; right:64px; top:{84+0}px; bottom:62px; }}
/* aset */
.dua {{ display:grid; grid-template-columns:1fr 1fr; gap:40px; padding:0 6px; }}
.kol h2 {{ display:flex; align-items:center; gap:12px; font-family:'Montserrat'; font-weight:700; font-size:20px; color:#13314f; margin:0 0 10px; }}
.kol h2 b {{ width:34px; height:34px; border-radius:50%; background:{CYAN}; color:#fff; display:flex; align-items:center; justify-content:center; font-size:15px; flex:none; }}
.bingkai {{ background:{TEAL_MUDA}; padding:9px; height:262px; display:flex; align-items:center; justify-content:center; }}
.bingkai img {{ max-width:100%; max-height:100%; box-shadow:0 1px 4px rgba(0,0,0,.18); background:#fff; }}
.berkas {{ background:#fbf3fe; border:1px solid {UNGU}; border-radius:6px; padding:6px 10px; margin:9px 0 8px; font-size:12.5px; line-height:1.45; }}
.desk {{ font-size:12.8px; line-height:1.42; }}
.desk p {{ margin:0 0 1px; }}
.desk b {{ color:{TEAL}; }}
/* tabel */
table {{ width:100%; border-collapse:collapse; font-size:11.2px; line-height:1.33; }}
th {{ background:{TEAL}; color:#fff; font-weight:600; text-align:left; padding:6px 7px; font-size:11.5px; }}
td {{ border:1px solid #c9d6da; padding:5px 7px; vertical-align:top; }}
tr:nth-child(even) td {{ background:#F2F8F9; }}
td.mod {{ background:{TEAL_MUDA} !important; width:17%; }}
td.mod .n {{ font-family:'Montserrat'; font-weight:700; color:{TEAL}; font-size:12.5px; }}
td.mod .j {{ font-family:'Montserrat'; font-weight:700; font-size:12px; color:#13314f; margin:2px 0 4px; }}
td.mod .w {{ font-size:10.3px; color:#355; margin-bottom:4px; }}
td.mod .t {{ font-style:italic; font-size:10.5px; }}
td ol {{ margin:0; padding-left:15px; }}
td li {{ margin-bottom:1px; }}
.pita {{ display:flex; gap:10px; margin:0 0 12px; }}
.pita div {{ flex:1; background:#f4fafb; border-left:4px solid {CYAN}; padding:7px 10px; font-size:12px; line-height:1.4; }}
.pita b {{ font-family:'Montserrat'; color:#13314f; }}
.angka {{ font-family:'Montserrat'; font-weight:800; font-size:22px; color:{TEAL}; }}
.grid {{ display:grid; grid-template-columns:repeat(6,1fr); gap:10px; }}
.grid .k {{ border:1px solid #d6e4e7; border-radius:6px; overflow:hidden; background:#fff; }}
.grid .k .im {{ height:92px; background:{TEAL_MUDA}; display:flex; align-items:flex-start; justify-content:center; overflow:hidden; padding:5px 5px 0; }}
.grid .k img {{ width:100%; }}
.grid .k .tx {{ padding:5px 7px 7px; font-size:10.5px; line-height:1.3; }}
.grid .k .tx b {{ font-family:'Montserrat'; color:{TEAL}; }}
.isi-tim {{ background:#FFF200; font-weight:600; padding:0 3px; }}
"""


def halaman(judul, sub, isi):
    return f"""<div class="hal"><div class="kepala"><img src="{LOGO}"><div class="th">2026</div></div>
<h1>{judul}</h1><p class="sub">{sub}</p>{isi}
<div class="kaki"><span><i>{IKON['wa']}</i>0877-7413-4288</span><span><i>{IKON['web']}</i>www.sanggabiz.com</span><span><i>{IKON['mail']}</i>partnership@sanggabiz.com</span></div></div>"""


def dokumen(nama, badan):
    return f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>{nama}</title><style>{CSS}</style></head><body>{badan}</body></html>'


SLUG = {"00": "panduan", "01": "regulasi-sop", "02": "kartu-isyarat", "03": "lembar-praktik", "04": "skenario",
        "05": "rubrik", "06": "tes", "07": "formulir-slip", "08": "audit-akses", "09": "sertifikat",
        "10": "laporan", "11": "rekap-nilai"}
SINGKAT = {"01": "Ringkasan Regulasi dan SOP", "07": "Formulir Slip dan Cap Jempol", "10": "Draf Laporan Evaluasi",
           "11": "Rekap Nilai dan Rubrik"}

# ---------- Gambar aset dari PDF kit ----------
def gambar_aset():
    """Mengambil halaman pertama tiap PDF kit, memotong bagian atas, menyimpan ke proposal/aset-slide."""
    SLIDE.mkdir(parents=True, exist_ok=True)
    tmp = BUILD / "tmp"
    tmp.mkdir(exist_ok=True)
    hasil = {}
    for no, nama, *_ in KIT:
        if no == "11":
            continue
        pdf = ROOT / "kit" / f"{nama}.pdf"
        if not pdf.exists():
            pdf = next((ROOT / "kit").glob(f"{no} *.pdf"))
        out = tmp / f"k{no}"
        subprocess.run(["pdftoppm", "-r", "110", "-f", "1", "-l", "1", "-png", "-singlefile", str(pdf), str(out)], check=True)
        im = Image.open(f"{out}.png").convert("RGB")
        w, h = im.size
        if no != "09":
            mx = int(w * 0.045)
            top = int(h * 0.025)
            im = im.crop((mx, top, w - mx, top + int((w - 2 * mx) / 1.85)))
        p = SLIDE / f"{no}-{SLUG[no]}.png"
        im.save(p, optimize=True)
        hasil[no] = p
    hasil["11"] = SLIDE / f"11-{SLUG['11']}.png"
    return hasil


def html_rekap():
    """Tampilan lembar Nilai dari berkas Excel aset 11, dihitung dengan rumus yang sama."""
    fmt = lambda x: f"{x:.1f}"
    rows = ""
    for i, (nama, jab, pre, post) in enumerate(PESERTA, 2):
        a, b = round(pre * 100 / 15, 1), round(post * 100 / 15, 1)
        g = "" if a == 100 else f"{(b - a) / (100 - a):.2f}"
        st = "Ya" if b >= 80 else "Belum"
        warna = "" if st == "Ya" else "background:#F8C8D0"
        rows += f"<tr><td class='rn'>{i}</td><td>{i-1}</td><td>{nama}</td><td>{jab}</td><td class='r'>{fmt(a)}</td><td class='r'>{fmt(b)}</td><td class='r'>{fmt(b-a)}</td><td class='r'>{g}</td><td style='{warna}'>{st}</td></tr>"
    css = f"""{FONT_FACE} body{{margin:0;font-family:'Inter';font-size:12px;background:#fff}}
.bar{{background:#217346;color:#fff;padding:6px 10px;font-weight:600}} .fx{{border-bottom:1px solid #ccc;padding:5px 8px;font-family:monospace;color:#333}}
.fx b{{display:inline-block;width:44px;color:#555}} table{{border-collapse:collapse;width:100%}} td,th{{border:1px solid #d4d4d4;padding:3px 6px;white-space:nowrap}}
th{{background:{TEAL};color:#fff;font-weight:600}} th.c,td.rn{{background:#f0f0f0;color:#555;text-align:center;font-weight:400}} td.r{{text-align:right}}
.tabs{{display:flex;gap:2px;padding:4px 6px;background:#f0f0f0;border-top:1px solid #ccc}} .tabs span{{padding:3px 10px;background:#fff;border:1px solid #ccc}} .tabs .on{{border-bottom:2px solid #217346;font-weight:700}}"""
    body = f"""<div class="bar">11 Rekap Nilai dan Rubrik.xlsx</div><div class="fx"><b>G2</b>=IF(D2=100,"",ROUND((E2-D2)/(100-D2),2))</div>
<table><tr><th class="c"></th><th class="c">A</th><th class="c">B</th><th class="c">C</th><th class="c">D</th><th class="c">E</th><th class="c">F</th><th class="c">G</th><th class="c">H</th></tr>
<tr><td class="rn">1</td><th>No</th><th>Nama</th><th>Jabatan</th><th>Pre</th><th>Post</th><th>Naik</th><th>N-gain</th><th>Post 80 atau lebih</th></tr>{rows}</table>
<div class="tabs"><span>Petunjuk</span><span>Jawaban</span><span class="on">Nilai</span><span>Rubrik</span><span>Grafik</span></div>"""
    p = HTML / "rekap.html"
    p.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>", encoding="utf8")
    return p


# ---------- Isi halaman ----------
DESK = {
    "00": ("Isi kit, peran tim, peta aset per modul, perlengkapan, jadwal persiapan, dan kunci jawaban. Untuk tim pelaksana, bukan peserta.", "Sebelum dan selama pelatihan.", "Tim cukup 1 trainer, 1 co-trainer Tuli, dan 1 peraga netra dengan langkah persiapan yang jelas."),
    "01": ("Ringkasan POJK 22/2023, Pedoman SETARA, dan UU 8/2016, enam prinsip layanan, langkah per ragam disabilitas, dan daftar bukti audit.", "Modul 1, lalu disimpan di loket.", "Pegangan satu lembar bolak-balik untuk melayani dan menyiapkan bukti pemeriksaan."),
    "02": ("20 kosakata isyarat loket dengan foto peragaan BISINDO dari co-trainer Tuli, enam cara berkomunikasi, dan kalimat tertulis siap pakai.", "Modul 3 dan simulasi Modul 6.", "Kartu yang disimpan di meja teller dan CS."),
    "03": ("Daftar langkah pemanduan nasabah netra dan pengoperasian kursi roda di ramp, dengan butir wajib dan dua putaran centang.", "Modul 2 dan Modul 4.", "Bukti praktik per peserta yang diparaf peraga netra."),
    "04": ("Lima skenario layanan dari pintu masuk sampai keluhan: peran, situasi, dan hal yang harus muncul. Data nasabah rekaan.", "Modul 6.", "Bahan latihan ulang di kantor, misalnya saat briefing pagi."),
    "05": ("Delapan aspek layanan dengan skor 1 sampai 3 per skenario dan target rata-rata 2,5.", "Modul 6, diisi Kasie Operasional.", "Alat Kasie untuk memantau tiga layanan nasabah disabilitas pertama setelah pelatihan."),
    "06": ("15 soal yang sama untuk awal dan akhir hari, ditambah empat butir survei kepuasan. Bisa dipindah ke Google Form.", "08.45 dan 16.10 WIB.", "Nilai awal dan akhir per peserta untuk laporan dan bukti audit."),
    "07": ("Contoh formulir pembacaan slip, pilihan tanda tangan atau cap jempol, saksi internal, dan daftar periksa Kasie.", "Modul 5.", "Contoh berkas lengkap yang bisa disesuaikan bagian kepatuhan BPR."),
    "08": ("19 butir pemeriksaan ruang layanan dari parkir sampai ATM, dengan kolom ukuran dan foto.", "Modul 4, di ruang layanan BPR.", "Daftar temuan yang menjadi rekomendasi perbaikan fasilitas di laporan."),
    "09": ("Sertifikat perorangan bernomor dengan judul pelatihan, rujukan POJK 22/2023 dan Pedoman SETARA, nilai post-test, dan skor rubrik.", "Dikirim bersama laporan.", "Bukti pemenuhan pelatihan untuk berkas SDM dan pemeriksaan OJK."),
    "10": ("Bentuk laporan evaluasi: rekap pre-test dan post-test, rubrik, survei, rekomendasi fasilitas, dan tindak lanjut. Angka di draf adalah contoh.", "Paling lambat 7 hari kerja setelah pelatihan.", "Laporan untuk manajemen dan bukti pemenuhan TOR bagian VI."),
    "11": ("Excel dengan rumus: jawaban diketik, nilai, kenaikan, N-gain, status lulus, rata-rata rubrik, dan grafik terhitung sendiri.", "Sesudah kelas, oleh tim Sanggabiz.", "Rekap rapi yang bisa dicek ulang BPR, angka laporan bisa ditelusuri ke jawaban peserta."),
}


def kol_aset(no, gambar):
    nama = SINGKAT.get(no, next(k[1] for k in KIT if k[0] == no))
    berkas = next((ROOT / "kit").glob(f"{no} *")).name
    apa, dipakai, bawa = DESK[no]
    rel = gambar.relative_to(ROOT).as_posix()
    return f"""<div class="kol"><h2><b>{int(no)}</b>{nama}</h2>
<div class="bingkai"><img src="{gambar.as_uri()}"></div>
<div class="berkas"><b>Berkas di kit:</b> kit/{berkas}<br><b>Gambar:</b> {rel}</div>
<div class="desk"><p><b>Apa ini.</b> {apa}</p><p><b>Dipakai di.</b> {dipakai}</p><p><b>Dibawa pulang.</b> {bawa}</p></div></div>"""


def baris_modul(m):
    materi = "".join(f"<li>{x}</li>" for x in m["materi"])
    akt = "".join(f"<li>{x}</li>" for x in m["aktivitas"])
    return f"""<tr><td class="mod"><div class="n">{m['no']}</div><div class="j">{m['judul']}</div><div class="w">{m['jam']}</div><div class="t">{m['tujuan']}</div></td>
<td style="width:20%"><ol>{materi}</ol></td><td style="width:30%"><ol style="list-style:none;padding-left:0">{akt}</ol></td>
<td style="width:11%">{m['alat']}</td><td style="width:11%">{m['indikator']}</td><td style="width:11%">{m['output']}</td></tr>"""


def tabel_modul(ms):
    return ("<table><thead><tr><th>Modul, waktu, dan tujuan (Bloom)</th><th>Outline materi</th><th>Aktivitas di ruang pelatihan</th>"
            "<th>Alat dan media</th><th>Indikator capaian</th><th>Output konkret</th></tr></thead><tbody>"
            + "".join(baris_modul(m) for m in ms) + "</tbody></table>")


def susun(gambar):
    hal = []
    # 1. Ringkasan
    total = sum(r[2] for r in RINGKAS[2:])
    rk = "".join(f"<tr><td style='white-space:nowrap'>{j}</td><td><b>{s}</b></td><td style='text-align:center'>{m}</td><td>{mt}</td><td>{h}</td></tr>" for j, s, m, mt, h in RINGKAS)
    rk += "<tr><td></td><td>Rehat kopi 10.15 - 10.30 dan 15.00 - 15.15, ishoma 12.00 - 13.00 (disediakan BPR)</td><td></td><td></td><td></td></tr>"
    hal.append(halaman("SILABUS PELATIHAN: RINGKASAN SATU HARI",
        "In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas, PT BPR NBP 27, Bandung. 10 peserta, luring, 08.30 - 16.30 WIB.",
        f"""<div class="pita">
<div><span class="angka">30</span> menit teori dari <b>{total} menit</b> pembelajaran. Sisanya, {total-30} menit atau {round((total-30)*100/total)} persen, adalah praktik dan simulasi sesuai TOR.</div>
<div><b>Metode.</b> Andragogi: peserta belajar dari kasus loket sendiri. Bloom revisi untuk tujuan tiap modul (C1 sampai C5). Kirkpatrick level 1 dan 2 untuk evaluasi, level 3 lewat rubrik di kantor.</div>
<div><b>Tim di kelas.</b> 1 trainer utama, 1 co-trainer Tuli untuk isyarat BISINDO, 1 peraga netra untuk pemanduan dan pembacaan slip.</div></div>
<table><thead><tr><th>Waktu (WIB)</th><th>Sesi</th><th>Menit</th><th>Metode</th><th>Hasil</th></tr></thead><tbody>{rk}</tbody></table>"""))
    # 2-4. Modul
    for a, b, ket in ((0, 2, "Modul 1 dan 2"), (2, 4, "Modul 3 dan 4"), (4, 6, "Modul 5 dan 6")):
        hal.append(halaman(f"SILABUS PELATIHAN: {ket.upper()}",
            "Tiap modul memuat tujuan berkode Bloom, outline materi, aktivitas per menit, alat, indikator, dan output. Nomor aset merujuk ke isi kit.",
            tabel_modul(MODUL[a:b])))
    # 5. Hasil dan evaluasi
    hs = "".join(f"<tr><td>{h}</td><td>{d}</td><td>{u}</td></tr>" for h, d, u in HASIL)
    hal.append(halaman("HASIL YANG DIBAWA PULANG DAN EVALUASI",
        "Semua output tiap modul dikumpulkan di sini, lalu diukur dengan empat level Kirkpatrick.",
        f"""<div style="display:grid;grid-template-columns:1.25fr 1fr;gap:24px">
<div><table><thead><tr><th>Hasil</th><th>Dari</th><th>Dipakai untuk</th></tr></thead><tbody>{hs}</tbody></table></div>
<div><table><thead><tr><th>Level</th><th>Diukur dengan</th><th>Target</th></tr></thead><tbody>
<tr><td><b>1. Reaksi</b></td><td>Survei 4 butir di lembar post-test</td><td>Rata-rata minimal 4 dari 5</td></tr>
<tr><td><b>2. Pembelajaran</b></td><td>Pre-test dan post-test 15 soal, lembar praktik, rubrik Modul 6</td><td>Post-test minimal 80, rubrik minimal 2,5 dari 3</td></tr>
<tr><td><b>3. Perilaku</b></td><td>Kasie memakai rubrik untuk tiga layanan pertama di kantor</td><td>Diusulkan, dicatat BPR</td></tr>
<tr><td><b>4. Dampak</b></td><td>Log keluhan nasabah disabilitas dan hasil pemeriksaan</td><td>Dipantau BPR, di luar paket</td></tr>
</tbody></table>
<p style="font-size:11.5px;line-height:1.45;margin-top:8px">Laporan evaluasi dikirim paling lambat 7 hari kerja setelah pelatihan, berisi rekap nilai, dokumentasi foto dan video, dan rekomendasi perbaikan fasilitas layanan sesuai TOR bagian VI. Target angka adalah usulan kami dan dapat disesuaikan dengan BPR.</p></div></div>"""))
    # 6. Isi kit
    kartu = "".join(f"""<div class="k"><div class="im"><img src="{gambar[no].as_uri()}"></div><div class="tx"><b>{int(no)}. {nama}</b><br>{siapa}. {pakai}.</div></div>""" for no, nama, siapa, pakai in KIT)
    hal.append(halaman("ASET PELATIHAN: ISI KIT",
        "Disiapkan Sanggabiz untuk 10 peserta dan tim. Data nasabah di kit adalah rekaan dan dibuat khusus untuk layanan BPR.",
        f'<div class="grid">{kartu}</div>'))
    # 7-12. Aset berpasangan
    pasangan = [("01", "02", "RINGKASAN REGULASI DAN KARTU ISYARAT"), ("03", "04", "LEMBAR PRAKTIK DAN SKENARIO"),
                ("05", "06", "RUBRIK DAN TES"), ("07", "08", "FORMULIR SLIP DAN AUDIT AKSESIBILITAS"),
                ("09", "10", "SERTIFIKAT DAN LAPORAN"), ("11", "00", "REKAP NILAI DAN PANDUAN FASILITATOR")]
    for a, b, j in pasangan:
        hal.append(halaman(f"ASET PELATIHAN: {j}",
            "Disiapkan Sanggabiz dan dibagikan ke peserta. Semua data nasabah rekaan, dibuat khusus untuk layanan BPR.",
            f'<div class="dua">{kol_aset(a, gambar[a])}{kol_aset(b, gambar[b])}</div>'))
    return hal


def main():
    if "--gabung" in sys.argv:
        files = sorted(HAL.glob("hal-*.pdf"))
        out = ROOT / "proposal" / NAMA_PDF
        subprocess.run(["pdfunite", *map(str, files), str(out)], check=True)
        prev = ROOT / "preview"
        prev.mkdir(exist_ok=True)
        subprocess.run(["pdftoppm", "-r", "72", "-png", str(out), str(prev / "hal")], check=True)
        print(out)
        return
    gambar = gambar_aset()
    jobs = [{"html": str(html_rekap()), "png": str(gambar["11"]), "width": 760, "height": 372, "scale": 2}]
    hal = susun(gambar)
    jobs2 = []
    for i, h in enumerate(hal, 1):
        p = HTML / f"hal-{i:02d}.html"
        p.write_text(dokumen(f"Halaman {i}", h), encoding="utf8")
        jobs2.append({"html": str(p), "pdf": str(HAL / f"hal-{i:02d}.pdf"), "width": 1280, "height": 720, "scale": 1})
    # rekap harus ada sebelum halaman dirender
    (BUILD / "jobs_proposal.json").write_text(json.dumps(jobs + jobs2, indent=1))
    print(len(hal), "halaman")


if __name__ == "__main__":
    main()
