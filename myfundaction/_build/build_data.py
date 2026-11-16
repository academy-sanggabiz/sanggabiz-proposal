"""Membuat data latihan REKAAN untuk Modul 2 dan Modul 7.

Semua nama, angka, dan transaksi dibuat acak dengan seed tetap. Bukan data MyFundAction.
Kunci jawaban dihitung di sini dan dipakai build_aset_docx.py.
"""
import csv
import os
import random
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "aset", "data-latihan")
ACUAN = date(2026, 11, 16)

NAMA_ID = ["Rina", "Budi", "Siti", "Agus", "Dewi", "Fajar", "Lestari", "Hendra", "Nur", "Yusuf", "Putri", "Rizki", "Maya", "Dimas", "Ayu", "Bayu"]
NAMA_MY = ["Aisyah", "Hafiz", "Nurul", "Faiz", "Siti Aminah", "Amir", "Farah", "Iskandar", "Zulaikha", "Haziq", "Liyana", "Syafiq"]
NAMA_AU = ["Sarah", "Omar", "Fatima", "James", "Aisha", "Daniel", "Mariam", "Adam", "Hannah", "Bilal", "Zainab", "Ryan"]
BELAKANG = ["A.", "B.", "H.", "K.", "M.", "N.", "R.", "S.", "T.", "W."]
KOTA = {"Indonesia": ["Jakarta", "Bandung", "Surabaya", "Depok", "Bekasi"], "Malaysia": ["Kuala Lumpur", "Shah Alam", "Johor Bahru", "Penang"], "Australia": ["Sydney", "Melbourne", "Perth", "Brisbane"]}
BAHASA = {"Indonesia": "Indonesia", "Malaysia": "Melayu", "Australia": "Inggris"}
PROGRAM = ["Palestina", "Pembangunan masjid", "Air bersih"]
KANAL = ["Iklan Meta", "Instagram organik", "WhatsApp", "Situs web", "Acara"]


def segmen(r):
    pertama = date.fromisoformat(r["tanggal_donasi_pertama"])
    terakhir = date.fromisoformat(r["tanggal_donasi_terakhir"])
    if (ACUAN - pertama).days <= 90:
        return "Baru"
    if (ACUAN - terakhir).days > 180:
        return "Tidak aktif"
    if int(r["jumlah_donasi_12_bulan"]) >= 3:
        return "Rutin"
    return "Lainnya"


def buat_donatur(rng):
    rows = []
    for i in range(1, 121):
        negara = rng.choices(["Indonesia", "Malaysia", "Australia"], [5, 3, 3])[0]
        nama = rng.choice({"Indonesia": NAMA_ID, "Malaysia": NAMA_MY, "Australia": NAMA_AU}[negara]) + " " + rng.choice(BELAKANG)
        prog = rng.choices(PROGRAM, [4, 5, 3] if negara == "Australia" else [5, 3, 3])[0]
        pertama = ACUAN - timedelta(days=rng.randint(10, 900))
        terakhir = pertama + timedelta(days=rng.randint(0, max(0, (ACUAN - pertama).days - 1)))
        dalam_12 = (ACUAN - terakhir).days <= 365
        n12 = rng.choice([1, 1, 2, 3, 4, 6, 12]) if dalam_12 else 0
        if (ACUAN - pertama).days <= 90:
            n12 = rng.choice([1, 1, 2])
        rata = {"Indonesia": rng.choice([10, 15, 20, 30, 50]), "Malaysia": rng.choice([10, 20, 30, 50]), "Australia": rng.choice([25, 50, 75, 100, 150])}[negara]
        rows.append({
            "id_donatur": f"D{i:04d}",
            "nama_rekaan": nama,
            "negara": negara,
            "kota": rng.choice(KOTA[negara]),
            "bahasa_pilihan": BAHASA[negara],
            "program_terakhir": prog,
            "kanal_pertama": rng.choice(KANAL),
            "tanggal_donasi_pertama": pertama.isoformat(),
            "tanggal_donasi_terakhir": terakhir.isoformat(),
            "jumlah_donasi_12_bulan": n12,
            "total_donasi_12_bulan_usd": n12 * rata,
            "setuju_dihubungi": rng.choices(["Ya", "Tidak"], [4, 1])[0],
        })
    return rows


def buat_kampanye(rng):
    rows = []
    awal = date(2026, 9, 14)
    # biaya per donasi dasar (USD) per negara dan program, masjid paling efisien di Australia
    dasar = {
        ("Indonesia", "Palestina"): 6, ("Indonesia", "Pembangunan masjid"): 8, ("Indonesia", "Air bersih"): 9,
        ("Malaysia", "Palestina"): 9, ("Malaysia", "Pembangunan masjid"): 10, ("Malaysia", "Air bersih"): 12,
        ("Australia", "Palestina"): 24, ("Australia", "Pembangunan masjid"): 15, ("Australia", "Air bersih"): 30,
    }
    nilai_rata = {"Indonesia": 12, "Malaysia": 22, "Australia": 85}
    for w in range(8):
        minggu = awal + timedelta(weeks=w)
        for (negara, prog), cpa in dasar.items():
            for platform in ["Meta", "Google"]:
                biaya = round(rng.uniform(120, 260) * (2.2 if negara == "Australia" else 1.0), 2)
                cpm = rng.uniform(2.0, 4.0) * (3 if negara == "Australia" else 1)
                tayang = int(biaya / cpm * 1000)
                ctr = rng.uniform(0.008, 0.02)
                klik = int(tayang * ctr)
                f = rng.uniform(0.8, 1.25) * (1.1 if platform == "Google" else 1.0)
                donasi = max(1, int(biaya / (cpa * f)))
                nilai = round(donasi * nilai_rata[negara] * rng.uniform(0.8, 1.3), 2)
                rows.append({
                    "minggu_mulai": minggu.isoformat(),
                    "negara": negara,
                    "program": prog,
                    "platform": platform,
                    "biaya_usd": biaya,
                    "tayangan": tayang,
                    "klik": klik,
                    "jumlah_donasi": donasi,
                    "nilai_donasi_usd": nilai,
                })
    return rows


def simpan(path, rows):
    with open(path, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def kunci(donatur, kampanye):
    seg = {}
    for r in donatur:
        s = segmen(r)
        seg[s] = seg.get(s, 0) + 1
    seg_kontak = {}
    for r in donatur:
        if r["setuju_dihubungi"] == "Ya":
            s = segmen(r)
            seg_kontak[s] = seg_kontak.get(s, 0) + 1
    agg = {}
    for r in kampanye:
        k = (r["negara"], r["program"])
        a = agg.setdefault(k, {"biaya": 0.0, "donasi": 0, "klik": 0, "tayang": 0, "nilai": 0.0})
        a["biaya"] += r["biaya_usd"]
        a["donasi"] += r["jumlah_donasi"]
        a["klik"] += r["klik"]
        a["tayang"] += r["tayangan"]
        a["nilai"] += r["nilai_donasi_usd"]
    tabel = []
    for (n, p), a in sorted(agg.items()):
        tabel.append({
            "negara": n, "program": p, "biaya": round(a["biaya"], 2), "donasi": a["donasi"],
            "cpd": round(a["biaya"] / a["donasi"], 2), "ctr": round(100 * a["klik"] / a["tayang"], 2),
            "roas": round(a["nilai"] / a["biaya"], 2),
        })
    return {"segmen": seg, "segmen_setuju": seg_kontak, "kampanye": tabel}


def jalankan():
    rng = random.Random(20261116)
    donatur = buat_donatur(rng)
    kampanye = buat_kampanye(rng)
    os.makedirs(OUT, exist_ok=True)
    simpan(os.path.join(OUT, "donatur-rekaan.csv"), donatur)
    simpan(os.path.join(OUT, "kampanye-iklan-rekaan.csv"), kampanye)
    return kunci(donatur, kampanye)


if __name__ == "__main__":
    k = jalankan()
    print(k["segmen"], k["segmen_setuju"])
    for t in k["kampanye"]:
        print(t)
