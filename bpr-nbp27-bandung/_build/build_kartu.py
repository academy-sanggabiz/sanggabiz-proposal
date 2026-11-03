"""Kartu Saku Isyarat Perbankan v2 (desain ulang), dua sisi A5 landscape.

Sisi depan: 20 isyarat loket. Kotak foto diisi foto peragaan BISINDO dari co-trainer Tuli Bandung,
karena isyarat punya variasi daerah dan tidak kami gambar sendiri.
Sisi belakang: kartu tunjuk untuk nasabah, papan angka, dan tips untuk petugas.
Pemakaian: python3 build_kartu.py && node render.js jobs_kartu.json
"""
import json
from gaya import BUILD, ROOT, FONT_FACE

HTML = BUILD / "html"
HTML.mkdir(exist_ok=True)
LOGO_PUTIH = (BUILD / "assets" / "logo_putih.png").as_uri()
SLIDE = ROOT / "proposal" / "aset-slide"

NAVY, TEAL, CYAN = "#13314F", "#15908F", "#34BDCF"
KAT = {
    "Salam": ("#2BA9C4", "#E3F5F9"),
    "Transaksi": ("#15908F", "#DFF1EF"),
    "Nominal": ("#E39B1B", "#FDF1DC"),
    "Dokumen": ("#7357C9", "#ECE7FA"),
    "Konfirmasi": ("#D94F72", "#FBE6EC"),
}


def ikon(nama, warna="currentColor", ukuran=22, tebal=1.8):
    p = {
        "tangan": '<path d="M8 13V5.6a1.4 1.4 0 0 1 2.8 0V11M10.8 10V4.2a1.4 1.4 0 0 1 2.8 0V10M13.6 10V5a1.4 1.4 0 0 1 2.8 0v6M16.4 11V8.2a1.4 1.4 0 0 1 2.8 0V13c0 4.4-3 8-7.4 8-3 0-4.9-1.6-6.4-4l-1.6-2.6a1.4 1.4 0 0 1 2.4-1.5L8 14.6"/>',
        "lambai": '<path d="M7 11V6a1.3 1.3 0 0 1 2.6 0v4.5M9.6 10V4.5a1.3 1.3 0 0 1 2.6 0V10M12.2 10V5.2a1.3 1.3 0 0 1 2.6 0V11M14.8 11V8a1.3 1.3 0 0 1 2.6 0v5c0 4-2.8 7.5-6.8 7.5-2.8 0-4.5-1.5-5.9-3.7L3.2 14.5a1.3 1.3 0 0 1 2.2-1.4L7 14.8"/><path d="M19 3.5c1.2.8 2 2.1 2 3.6M3.5 4.5C2.6 5.4 2 6.6 2 8"/>',
        "matahari": '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/>',
        "mulut": '<circle cx="12" cy="12" r="9"/><path d="M8 14.5c2.2 2 5.8 2 8 0M9 9.5h.01M15 9.5h.01"/>',
        "pena": '<path d="M4 20l1-4L16.5 4.5a2.1 2.1 0 0 1 3 3L8 19z"/><path d="M14.5 6.5l3 3"/>',
        "mata": '<path d="M2 12s3.6-6.5 10-6.5S22 12 22 12s-3.6 6.5-10 6.5S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        "orang": '<circle cx="9" cy="7.5" r="3.2"/><path d="M3 20c.4-3.6 2.8-5.8 6-5.8s5.6 2.2 6 5.8"/><path d="M16 4.6a3 3 0 0 1 0 5.8M18 14.6c1.8.8 2.8 2.7 3 5.4"/>',
        "setor": '<rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M12 3v8M8.5 7.5L12 11l3.5-3.5"/>',
        "tarik": '<rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M12 11V3M8.5 6.5L12 3l3.5 3.5"/>',
        "saldo": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21M8 10.5h5M10.5 8v5"/>',
        "rekening": '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.4-3.8 3-6 6.5-6s6.1 2.2 6.5 6M18 8v6M15 11h6"/>',
        "buku": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M4 5.5v16M9 8h7M9 11.5h7"/>',
        "kartu": '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 9.5h19M6 15h4"/>',
        "ya": '<circle cx="12" cy="12" r="9"/><path d="M7.5 12.5l3 3 6-6.5"/>',
        "tidak": '<circle cx="12" cy="12" r="9"/><path d="M8.5 8.5l7 7M15.5 8.5l-7 7"/>',
        "ulang": '<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 4v5h-5"/>',
        "tunggu": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
        "selesai": '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
        "papan": '<rect x="3" y="4" width="18" height="13" rx="1.5"/><path d="M8 21l4-4 4 4M7 9h10M7 12.5h6"/>',
        "telinga": '<path d="M8 9a5 5 0 0 1 10 0c0 3-2.5 4-3 6.5-.4 2-1.8 3.5-4 3.5a3.5 3.5 0 0 1-3.3-2.3"/><path d="M11 9.5a2 2 0 0 1 4 0c0 1.2-1 1.6-1.5 2.4"/>',
    }[nama]
    return (f'<svg viewBox="0 0 24 24" width="{ukuran}" height="{ukuran}" fill="none" stroke="{warna}" '
            f'stroke-width="{tebal}" stroke-linecap="round" stroke-linejoin="round">{p}</svg>')


KATA = [
    ("Selamat pagi", "Salam"), ("Terima kasih", "Salam"), ("Silakan duduk", "Salam"), ("Tunggu sebentar", "Salam"),
    ("Setor", "Transaksi"), ("Tarik", "Transaksi"), ("Rekening", "Transaksi"), ("Kartu ATM", "Transaksi"),
    ("Uang", "Nominal"), ("Ribu", "Nominal"), ("Juta", "Nominal"), ("Nomor", "Nominal"),
    ("Formulir", "Dokumen"), ("Tanda tangan", "Dokumen"), ("Cap jempol", "Dokumen"), ("KTP", "Dokumen"),
    ("Nama", "Konfirmasi"), ("Benar?", "Konfirmasi"), ("Ulangi", "Konfirmasi"), ("Selesai", "Konfirmasi"),
]

CSS = FONT_FACE + f"""
@page {{ size: 210mm 148mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; background: transparent; }}
body {{ font-family: 'Inter', sans-serif; color: {NAVY}; }}
.sisi {{ width: 794px; height: 559px; position: relative; overflow: hidden; background: #fff; border-radius: 22px; break-after: page; }}
.kepala {{ height: 84px; padding: 0 28px; display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(115deg, {NAVY} 0%, #145b78 55%, {TEAL} 100%); color: #fff; position: relative; }}
.kepala:after {{ content: ''; position: absolute; right: -40px; top: -60px; width: 220px; height: 220px; border-radius: 50%;
  background: radial-gradient(circle, rgba(52,189,207,.45), rgba(52,189,207,0) 70%); }}
.kepala h1 {{ font-family: 'Montserrat'; font-weight: 800; font-size: 23px; margin: 0; letter-spacing: .2px; }}
.kepala p {{ margin: 3px 0 0; font-size: 11.5px; opacity: .9; }}
.kepala .kanan {{ text-align: right; font-size: 10px; position: relative; z-index: 1; line-height: 1.5; }}
.kepala .kanan img {{ height: 20px; display: block; margin-left: auto; margin-bottom: 3px; }}
.pita {{ display: flex; gap: 6px; padding: 12px 28px 4px; }}
.pita span {{ font-size: 9.5px; font-weight: 700; padding: 3px 10px; border-radius: 20px; letter-spacing: .3px; }}
.grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 9px; padding: 8px 28px 0; }}
.ubin {{ border-radius: 12px; overflow: hidden; background: #fff; border: 1.4px solid; height: 88px; display: flex; flex-direction: column; }}
.foto {{ flex: 1; display: flex; align-items: center; justify-content: center; position: relative; }}
.foto .no {{ position: absolute; left: 6px; top: 5px; font-family: 'Montserrat'; font-weight: 800; font-size: 10px; opacity: .85; }}
.foto .tag {{ position: absolute; right: 6px; bottom: 4px; font-size: 7px; opacity: .65; letter-spacing: .3px; text-transform: uppercase; }}
.kata {{ font-family: 'Montserrat'; font-weight: 700; font-size: 12px; padding: 5px 8px 6px; text-align: center; color: {NAVY}; background: #fff; }}
.kaki {{ position: absolute; left: 28px; right: 28px; bottom: 14px; display: flex; justify-content: space-between; align-items: center;
  font-size: 9.5px; color: #4b6070; }}
.kaki b {{ color: {TEAL}; }}
/* sisi belakang */
.tiga {{ display: grid; grid-template-columns: 1.08fr 0.92fr 1fr; gap: 16px; padding: 16px 28px 0; }}
.judul-k {{ font-family: 'Montserrat'; font-weight: 800; font-size: 12.5px; margin: 0 0 8px; display: flex; align-items: center; gap: 7px; }}
.judul-k i {{ width: 20px; height: 20px; border-radius: 50%; color: #fff; font-style: normal; font-size: 10.5px; display: flex; align-items: center; justify-content: center; }}
.tombol {{ display: grid; grid-template-columns: 1fr 1fr; gap: 7px; }}
.tombol div {{ border-radius: 11px; padding: 9px 8px; display: flex; align-items: center; gap: 8px; font-family: 'Montserrat'; font-weight: 700; font-size: 11.5px; }}
.konf {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; }}
.konf div {{ border-radius: 20px; padding: 6px 10px 6px 7px; display: flex; align-items: center; gap: 5px; font-family: 'Montserrat'; font-weight: 700; font-size: 10.5px; }}
.pad {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }}
.pad div {{ height: 37px; border-radius: 10px; background: #FDF1DC; border: 1.3px solid #F1C879; display: flex; align-items: center; justify-content: center;
  font-family: 'Montserrat'; font-weight: 800; font-size: 17px; color: #8a5a00; }}
.pad div.lebar {{ font-size: 12px; }}
.tulis {{ margin-top: 10px; border: 1.6px dashed #9fb3bf; border-radius: 11px; height: 62px; padding: 6px 9px; font-size: 9px; color: #7b8d98; }}
.contoh {{ position: absolute; left: 28px; right: 28px; bottom: 44px; background: #F6FAFB; border: 1.3px solid #DCE8EC; border-radius: 14px;
  padding: 11px 16px; display: flex; align-items: center; gap: 12px; }}
.contoh .lab {{ font-family: 'Montserrat'; font-weight: 800; font-size: 11px; color: {NAVY}; width: 150px; line-height: 1.3; }}
.contoh .lab span {{ display:block; font-family:'Inter'; font-weight:400; font-size:9.5px; color:#5b6f7c; }}
.contoh .c {{ height: 34px; min-width: 34px; padding: 0 9px; border-radius: 9px; background: #FDF1DC; border: 1.3px solid #F1C879; display: flex; align-items: center; justify-content: center;
  font-family: 'Montserrat'; font-weight: 800; font-size: 15px; color: #8a5a00; }}
.contoh .c.k {{ font-size: 11px; }}
.contoh .sama {{ font-family: 'Montserrat'; font-weight: 800; font-size: 18px; color: #9fb3bf; }}
.contoh .hasil {{ margin-left: auto; font-family: 'Montserrat'; font-weight: 800; font-size: 20px; color: {TEAL}; }}
.tips div {{ display: flex; gap: 9px; align-items: flex-start; margin-bottom: 8px; font-size: 10.3px; line-height: 1.35; color: #24394a; }}
.tips .ik {{ flex: none; width: 30px; height: 30px; border-radius: 9px; background: #E3F5F9; color: {TEAL}; display: flex; align-items: center; justify-content: center; }}
.tips b {{ font-family: 'Montserrat'; color: {NAVY}; display: block; font-size: 10.6px; }}
"""


def sisi_depan():
    ubin = ""
    for i, (k, kat) in enumerate(KATA, 1):
        tua, muda = KAT[kat]
        ubin += (f'<div class="ubin" style="border-color:{muda}"><div class="foto" style="background:{muda};color:{tua}">'
                 f'<span class="no">{i:02d}</span>{ikon("tangan", tua, 30, 1.5)}<span class="tag">foto isyarat</span></div>'
                 f'<div class="kata">{k}</div></div>')
    pita = "".join(f'<span style="background:{m};color:{t}">{n.upper()}</span>' for n, (t, m) in KAT.items())
    return f"""<div class="sisi">
<div class="kepala"><div><h1>Kartu Saku Isyarat Perbankan</h1><p>20 isyarat BISINDO yang paling sering dipakai di loket</p></div>
<div class="kanan"><img src="{LOGO_PUTIH}">PT BPR NBP 27, Bandung</div></div>
<div class="pita">{pita}</div>
<div class="grid">{ubin}</div>
<div class="kaki"><span>Foto isyarat diperagakan oleh <b>co-trainer Tuli dari Bandung</b>, sesuai isyarat yang dipakai nasabah setempat.</span><span>Balik kartu untuk kartu tunjuk</span></div>
</div>"""


def sisi_belakang():
    tr, tm = KAT["Transaksi"]
    kr, km = KAT["Konfirmasi"]
    nr, _ = KAT["Nominal"]
    layanan = [("setor", "Setor"), ("tarik", "Tarik"), ("saldo", "Cek saldo"), ("rekening", "Buka rekening"), ("buku", "Cetak buku"), ("kartu", "Kartu ATM")]
    tombol = "".join(f'<div style="background:{tm};color:{tr}">{ikon(i, tr, 20)}<span style="color:{NAVY}">{t}</span></div>' for i, t in layanan)
    konf = "".join(f'<div style="background:{km};color:{kr}">{ikon(i, kr, 15, 2)}<span style="color:{NAVY}">{t}</span></div>'
                   for i, t in [("ya", "Ya"), ("tidak", "Tidak"), ("ulang", "Ulangi"), ("tunggu", "Tunggu"), ("selesai", "Selesai")])
    pad = "".join(f"<div>{n}</div>" for n in "123456789") + '<div>0</div><div class="lebar">RIBU</div><div class="lebar">JUTA</div>'
    tips = [
        ("lambai", "Tarik perhatian", "Lambaikan tangan pelan di depan nasabah atau ketuk meja."),
        ("matahari", "Wajah terlihat jelas", "Berhadapan, wajah terkena cahaya, mulut tidak tertutup."),
        ("pena", "Tulis angkanya", "Nominal dan nomor rekening selalu ditulis atau ditunjuk."),
        ("mata", "Tatap nasabah", "Bila ada juru bahasa isyarat, tetap bicara kepada nasabah."),
        ("papan", "Kalimat pendek", "Satu informasi per kalimat. Tanyakan cara yang diinginkan nasabah."),
    ]
    tp = "".join(f'<div><span class="ik">{ikon(i, TEAL, 17)}</span><span><b>{j}</b>{t}</span></div>' for i, j, t in tips)
    return f"""<div class="sisi">
<div class="kepala"><div><h1>Kartu Tunjuk untuk Nasabah</h1><p>Nasabah menunjuk, petugas mengonfirmasi dengan isyarat atau tulisan</p></div>
<div class="kanan"><img src="{LOGO_PUTIH}">PT BPR NBP 27, Bandung</div></div>
<div class="tiga">
 <div><div class="judul-k"><i style="background:{tr}">1</i>Saya ingin</div><div class="tombol">{tombol}</div>
  <div class="judul-k" style="margin-top:14px"><i style="background:{kr}">3</i>Jawaban</div><div class="konf">{konf}</div></div>
 <div><div class="judul-k"><i style="background:{nr}">2</i>Jumlahnya</div><div class="pad">{pad}</div>
  <div class="tulis">Tulis di sini dengan spidol. Kartu dilaminasi, bisa dihapus.</div></div>
 <div><div class="judul-k"><i style="background:{TEAL}">{ikon("orang", "#fff", 13, 2.2)}</i>Untuk petugas</div><div class="tips">{tp}</div></div>
</div>
<div class="contoh"><div class="lab">Contoh menunjuk nominal<span>Tunjuk berurutan dari kiri ke kanan</span></div>
<div class="c">2</div><div class="c k">JUTA</div><div class="c">7</div><div class="c">5</div><div class="c">0</div><div class="c k">RIBU</div>
<div class="sama">=</div><div class="hasil">Rp 2.750.000</div></div>
<div class="kaki"><span>Disiapkan Sanggabiz untuk In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas.</span><span><b>sanggabiz.com</b></span></div>
</div>"""


def main():
    full = f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Kartu Saku Isyarat</title><style>{CSS}</style></head><body>{sisi_depan()}{sisi_belakang()}</body></html>'
    p = HTML / "kartu-v2.html"
    p.write_text(full, encoding="utf8")
    jobs = [{"html": str(p), "pdf": str(ROOT / "kit" / "02 Kartu Saku Isyarat Perbankan v2.pdf"), "width": 794, "height": 559}]
    for nama, isi in (("depan", sisi_depan()), ("belakang", sisi_belakang())):
        h = HTML / f"kartu-v2-{nama}.html"
        h.write_text(f'<!doctype html><html lang="id"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{isi}</body></html>', encoding="utf8")
        jobs.append({"html": str(h), "png": str(SLIDE / f"v2-kartu-isyarat-{nama}.png"), "width": 794, "height": 559, "scale": 3, "transparent": True})
    (BUILD / "jobs_kartu.json").write_text(json.dumps(jobs, indent=1))
    print("kartu siap")


if __name__ == "__main__":
    main()
