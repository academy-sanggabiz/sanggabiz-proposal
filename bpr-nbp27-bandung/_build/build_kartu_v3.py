"""Kartu Saku Isyarat v3: kartu belajar mandiri di rumah, dua sisi A5 landscape.

Sisi depan: 20 kata loket, tiap kata punya kotak untuk menempel foto atau menggambar isyarat yang dipelajari
dari pengajar Tuli, garis catatan, centang hafal, dan paraf pengajar. Sisi belakang: kartu tunjuk (sama dengan v2).
Isyarat tidak digambar oleh tim (lihat ../../pengetahuan/BISINDO-LAYANAN-KEUANGAN.md).
Pemakaian: python3 build_kartu_v3.py && node render.js jobs_kartu_v3.json
"""
import json
from gaya import BUILD, ROOT
from build_kartu import CSS, KAT, KATA, NAVY, TEAL, LOGO_PUTIH, ikon, sisi_belakang

HTML = BUILD / "html"
CSS3 = CSS + f"""
.grid3 {{ display:grid; grid-template-columns:repeat(5,1fr); gap:8px; padding:8px 28px 0; }}
.u3 {{ border-radius:11px; border:1.4px solid; overflow:hidden; height:92px; display:flex; flex-direction:column; background:#fff; }}
.u3 .atas {{ display:flex; align-items:center; gap:6px; padding:4px 8px; font-family:'Montserrat'; font-weight:700; font-size:10.5px; color:{NAVY}; white-space:nowrap; letter-spacing:-.1px; }}
.u3 .atas b {{ font-weight:800; font-size:9.5px; color:#fff; border-radius:6px; padding:1px 5px; }}
.u3 .bawah {{ flex:1; display:flex; gap:6px; padding:0 7px 6px; }}
.u3 .tempel {{ width:46px; border:1.3px dashed; border-radius:7px; display:flex; flex-direction:column; gap:1px; align-items:center; justify-content:center; text-align:center; font-size:6.5px; line-height:1.2; flex:none; }}
.u3 .catat {{ flex:1; min-width:0; padding-right:2px; display:flex; flex-direction:column; justify-content:space-between; }}
.u3 .catat i {{ display:block; border-bottom:1px solid #d5dee3; height:10px; }}
.u3 .cek3 {{ display:flex; align-items:center; gap:2px; font-size:6.6px; white-space:nowrap; color:#5b6f7c; }}
.u3 .cek3 span {{ width:8px; height:8px; border:1px solid #9fb3bf; border-radius:2px; display:inline-block; }}
.petunjuk {{ display:flex; gap:14px; padding:10px 28px 0; font-size:9.3px; color:#3b5161; }}
.petunjuk div {{ display:flex; gap:6px; align-items:center; }}
.petunjuk i {{ font-style:normal; width:17px; height:17px; border-radius:50%; background:{TEAL}; color:#fff; font-family:'Montserrat'; font-weight:800; font-size:9px; display:flex; align-items:center; justify-content:center; flex:none; }}
"""


def sisi_depan_v3():
    ubin = ""
    for i, (k, kat) in enumerate(KATA, 1):
        tua, muda = KAT[kat]
        ubin += (f'<div class="u3" style="border-color:{muda}"><div class="atas" style="background:{muda}"><b style="background:{tua}">{i:02d}</b>{k}</div>'
                 f'<div class="bawah"><div class="tempel" style="border-color:{tua};color:{tua}">{ikon("tangan", tua, 15, 1.6)}<span>tempel foto<br>atau gambar</span></div>'
                 f'<div class="catat"><i></i><i></i><div class="cek3">Hafal<span></span><span></span><span></span>&nbsp;Cek<span></span></div></div></div></div>')
    langkah = ["Pelajari isyaratnya dari pengajar Tuli atau kelas BISINDO", "Tempel foto atau gambar sendiri, catat bentuk tangan dan gerak",
               "Centang Hafal setiap kali berhasil tanpa melihat", "Minta pengajar memeriksa, lalu centang Cek"]
    pet = "".join(f"<div><i>{n}</i>{t}</div>" for n, t in enumerate(langkah, 1))
    return f"""<div class="sisi">
<div class="kepala"><div><h1>Kartu Belajar Isyarat Loket</h1><p>20 kata BISINDO untuk melayani nasabah Tuli. Diisi sendiri saat belajar.</p></div>
<div class="kanan"><img src="{LOGO_PUTIH}">Belajar mandiri</div></div>
<div class="petunjuk">{pet}</div>
<div class="grid3">{ubin}</div>
<div class="kaki"><span>Isyarat dipelajari langsung dari pengguna BISINDO. Bila lupa, pakai tulisan atau kartu tunjuk di balik kartu.</span><span>Nama: ____________________</span></div>
</div>"""


def main():
    belakang = (sisi_belakang().replace("PT BPR NBP 27, Bandung", "Belajar mandiri")
                .replace("Disiapkan Sanggabiz untuk In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas.",
                         "Latihan: minta teman menunjuk layanan dan jumlah, lalu jawab dengan isyarat yang sudah Anda pelajari."))
    html = f'<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Kartu Belajar Isyarat Loket</title><style>{CSS3}</style></head><body>{sisi_depan_v3()}{belakang}</body></html>'
    p = HTML / "kartu-v3.html"
    p.write_text(html, encoding="utf8")
    jobs = [{"html": str(p), "pdf": str(ROOT / "kit" / "02 Kartu Saku Isyarat Perbankan v3 - belajar mandiri.pdf"), "width": 794, "height": 559},
            {"html": str(p), "png": str(BUILD / "tmp" / "kartu-v3-depan.png"), "width": 794, "height": 559, "scale": 2}]
    (BUILD / "tmp").mkdir(exist_ok=True)
    (BUILD / "jobs_kartu_v3.json").write_text(json.dumps(jobs, indent=1))
    print("v3 siap")


if __name__ == "__main__":
    main()
