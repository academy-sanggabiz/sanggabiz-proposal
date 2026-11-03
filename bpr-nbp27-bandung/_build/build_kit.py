"""Membuat isi kit pelatihan (HTML) untuk IHT Layanan Inklusif PT BPR NBP 27.

Pemakaian (dari folder _build):
  python3 build_kit.py            # menulis html/ dan jobs_kit.json
  node render.js jobs_kit.json    # membuat PDF di ../kit/
Nama, nomor rekening, dan nominal di kit adalah data rekaan untuk latihan.
"""
import json
from gaya import BUILD, ROOT, kit_html, tabel
from silabus import KIT, MODUL

HTML = BUILD / "html"
HTML.mkdir(exist_ok=True)
REKAAN = '<span class="rekaan">Data rekaan untuk latihan.</span>'
ISI = lambda t: f'<span class="isi">[ISI TIM: {t}]</span>'
CEK = '<span class="cek"></span>'

docs = {}

# 00 Panduan Fasilitator ---------------------------------------------------
peta = "".join(
    f"<tr><td class='b'>{m['no']}</td><td>{m['judul']}</td><td>{m['alat']}</td><td>{m['output']}</td></tr>" for m in MODUL
)
docs["00 Panduan Fasilitator"] = ("Panduan Fasilitator", "Isi kit, peran tim, peta aset per modul, perlengkapan, dan kunci jawaban. Untuk tim pelaksana, tidak dibagikan ke peserta.", "Untuk tim", f"""
<h2>Peran tim</h2>
{tabel(["Peran", "Sebelum kelas", "Di kelas", "Sesudah kelas"], [
 ["<b>Trainer utama</b>", "Meminta SOP layanan dan contoh slip kosong dari BPR. Menyesuaikan slide Modul 1 dan aset 07 dengan SOP itu", "Memandu semua modul, menerjemahkan co-trainer Tuli, menjaga waktu", "Menyusun laporan evaluasi (aset 10)"],
 ["<b>Co-trainer Tuli</b>", "Memeriksa 20 kosakata di aset 02 dan mengisi foto peragaan dengan isyarat BISINDO yang dipakai di Bandung", "Memimpin drill Modul 3, berperan sebagai nasabah Tuli di Modul 6", "Memberi catatan untuk rekomendasi komunikasi"],
 ["<b>Peraga netra</b>", "Mencoba rute dan formulir aset 07 bersama trainer", "Memperagakan dan menilai pemanduan di Modul 2, berperan sebagai nasabah netra di Modul 5 dan 6", "Memberi catatan untuk rekomendasi fasilitas"],
], ["16%", "30%", "30%", "24%"])}
<p class="kecil">Nama dan profil tim: {ISI("nama trainer utama, co-trainer Tuli, dan peraga netra dari komunitas di Bandung")}</p>

<h2>Peta aset per modul</h2>
{tabel(["Modul", "Topik", "Alat dan aset", "Output"], [], ["11%", "29%", "32%", "28%"]).replace("<tbody></tbody>", "<tbody>" + peta + "</tbody>")}

<h2>Perlengkapan</h2>
{tabel(["Dibawa tim Sanggabiz", "Disediakan BPR (TOR bagian VII)", "Diminta dari BPR sebelum kelas"], [[
 "Kit cetak 10 set, penutup mata 10, tongkat putih 1, kursi roda 1, papan tulis genggam dan spidol 5 set, bantalan tinta 3, kartu Boleh dan Tidak 10 pasang, kartu transaksi, lakban warna, meteran, kamera",
 "Ruang rapat ber-AC, proyektor, sound system, makan siang dan dua kali rehat kopi untuk peserta dan tim",
 "SOP layanan nasabah disabilitas bila sudah ada, contoh slip setoran dan penarikan kosong 20 lembar, izin memakai ruang layanan dan ramp kantor untuk Modul 4, daftar nama dan jabatan 10 peserta"]], ["36%", "30%", "34%"])}

<h2>Pembagian peran peserta</h2>
<p>6 frontliner dibagi menjadi tiga pasang yang tetap sepanjang hari. 2 Kasie Operasional berperan sebagai penyelia di Modul 5 dan 6 dan mengisi rubrik. 2 peserta yang menyusul ikut pasangan sesuai jabatannya. {ISI("jabatan 2 peserta tambahan")}</p>

<h2>Jadwal persiapan</h2>
{tabel(["Waktu", "Pekerjaan"], [
 ["H-10", "Kirim formulir data peserta dan permintaan SOP serta slip kosong ke BPR"],
 ["H-7", "Sesuaikan slide Modul 1 dan aset 07 dengan SOP BPR. Co-trainer mengisi foto aset 02"],
 ["H-3", "Cetak kit 10 set. Uji rute Modul 2 dan ramp lewat foto atau kunjungan singkat"],
 ["H-1", "Cek proyektor, susun zona ruang: zona loket simulasi, zona rute pemanduan, zona meja CS"],
 ["Hari H", "Datang 07.45 WIB. Tandai rute dengan lakban, siapkan absen dan pre-test"],
 ["H+7 hari kerja", "Kirim laporan evaluasi dan sertifikat"],
], ["18%", "82%"])}

<h2 class="pecah">Kunci jawaban pre-test dan post-test</h2>
<p>Soal yang sama dipakai di awal dan akhir hari. Tiap soal bernilai 100/15, dibulatkan ke satu desimal di rekap (aset 11).</p>
{tabel(["No", "Kunci", "No", "Kunci", "No", "Kunci"], [
 ["1", "B", "6", "C", "11", "Benar"],
 ["2", "A", "7", "B", "12", "Salah"],
 ["3", "C", "8", "A", "13", "Benar"],
 ["4", "B", "9", "C", "14", "Salah"],
 ["5", "A", "10", "B", "15", "Benar"],
])}
""")

# 01 Ringkasan Regulasi dan SOP ------------------------------------------
docs["01 Ringkasan Regulasi dan SOP Layanan Disabilitas"] = ("Ringkasan Regulasi dan SOP Layanan Nasabah Disabilitas", "Pegangan peserta untuk Modul 1 dan untuk dipakai di loket. Disesuaikan dengan SOP internal PT BPR NBP 27 sebelum dicetak.", "Modul cetak", f"""
<h2>Dasar aturan</h2>
{tabel(["Aturan", "Yang perlu diingat petugas loket"], [
 ["<b>POJK No. 22 Tahun 2023</b> tentang Pelindungan Konsumen dan Masyarakat di Sektor Jasa Keuangan. Berlaku sejak 22 Desember 2023", "BPR sebagai PUJK wajib memberi layanan yang setara dan tidak diskriminatif kepada konsumen penyandang disabilitas"],
 ["<b>Pedoman SETARA</b> (Pedoman Akses Pelayanan Keuangan untuk Disabilitas Berdaya), OJK, Desember 2024", "Panduan praktis untuk menjalankan amanat POJK 22/2023: aksesibilitas fisik dan digital, serta sensitivitas layanan"],
 ["<b>UU No. 8 Tahun 2016</b> tentang Penyandang Disabilitas", "Ragam disabilitas: fisik, intelektual, mental, dan sensorik. Seseorang bisa memiliki lebih dari satu ragam"],
], ["40%", "60%"])}
<p class="kecil">Pasal yang dirujuk di slide Modul 1 diambil dari naskah resmi dan diperiksa tim sebelum kelas. {ISI("nomor pasal POJK 22/2023 yang dikutip")}</p>

<h2>Enam prinsip di ruang layanan</h2>
<ol>
<li><b>Tanya dulu sebelum membantu.</b> "Boleh saya bantu? Bagaimana cara yang Bapak atau Ibu inginkan?"</li>
<li><b>Bicara kepada nasabah</b>, bukan kepada pendamping atau juru bahasa isyarat.</li>
<li><b>Nasabah yang memutuskan.</b> Pendamping membantu, tidak menentukan transaksi.</li>
<li><b>Tidak menolak dan tidak menunda</b> layanan karena disabilitas. Bila ragu, eskalasi ke Kasie, bukan meminta nasabah datang lagi.</li>
<li><b>Rahasia tetap rahasia.</b> Membacakan data dengan suara pelan dan di posisi yang tidak terdengar antrean.</li>
<li><b>Catat.</b> Pembacaan slip, saksi, dan keluhan dicatat di formulir supaya bisa ditunjukkan saat pemeriksaan.</li>
</ol>

<h2>Langkah ringkas per ragam disabilitas</h2>
{tabel(["Nasabah", "Saat menyambut", "Saat transaksi"], [
 ["<b>Netra dan low vision</b>", "Sebut nama dan jabatan. Tawarkan lengan, nasabah memegang di atas siku. Jelaskan arah dengan arah jarum jam", "Bacakan slip: nama, nomor rekening, nominal angka dan terbilang. Tanya apakah nasabah ingin tanda tangan atau cap jempol. Hitung uang di depan nasabah per pecahan"],
 ["<b>Tuli dan wicara</b>", "Tarik perhatian dengan melambai pelan atau menepuk meja. Berhadapan, wajah terkena cahaya, mulut tidak tertutup", "Pakai isyarat dasar, papan tulis, dan kalimat pendek. Tunjukkan nominal di kalkulator atau layar. Bila ada juru bahasa, tetap menatap nasabah"],
 ["<b>Fisik dan pengguna kursi roda</b>", "Tanya sebelum mendorong kursi roda. Bicara sejajar mata, duduk bila perlu", "Layani di meja yang terjangkau. Dekatkan pena, mesin EDC, dan dokumen. Beri antrean prioritas"],
 ["<b>Intelektual</b>", "Sapa seperti nasabah lain. Pakai kalimat pendek dan satu informasi per kalimat", "Beri waktu lebih. Minta nasabah mengulang dengan kata-katanya sendiri. Pendamping boleh membantu menjelaskan, keputusan tetap pada nasabah"],
], ["18%", "38%", "44%"])}

<h2>Istilah yang dipakai</h2>
{tabel(["Dipakai", "Tidak dipakai"], [
 ["penyandang disabilitas, nasabah disabilitas", "cacat, penderita, orang tidak normal"],
 ["Tuli, nasabah Tuli", "bisu, tuna rungu (sebagian komunitas Tuli tidak memakai istilah ini)"],
 ["netra, nasabah netra", "buta (sebagai panggilan)"],
 ["pengguna kursi roda", "terikat kursi roda"],
], ["50%", "50%"])}

<h2>Bukti yang disimpan untuk pemeriksaan</h2>
<p>Tandai yang sudah ada di kantor Anda.</p>
{tabel(["", "Bukti", "Siapa menyimpan"], [
 [CEK, "Sertifikat dan daftar hadir pelatihan layanan disabilitas", "SDM"],
 [CEK, "SOP layanan nasabah disabilitas yang berlaku", "Kepatuhan"],
 [CEK, "Formulir pembacaan slip dan kesaksian cap jempol", "Kasie Operasional"],
 [CEK, "Log keluhan nasabah disabilitas dan tindak lanjutnya", "Kasie Operasional"],
 [CEK, "Hasil audit aksesibilitas kantor dan rencana perbaikan", "Umum atau Kepatuhan"],
], ["6%", "64%", "30%"])}
""")

# 02 Kartu Saku Isyarat -----------------------------------------------------
kosakata = [
    ("Selamat pagi atau siang", "Menyambut"), ("Terima kasih", "Penutup"), ("Silakan duduk", "Mempersilakan"),
    ("Tunggu sebentar", "Saat memproses"), ("Nama", "Konfirmasi nama"), ("Rekening", "Nomor rekening"),
    ("Nomor", "Rekening, antrean"), ("Setor", "Setoran tunai"), ("Tarik", "Penarikan"),
    ("Uang", "Tunai"), ("Ribu", "Nominal"), ("Juta", "Nominal"),
    ("Formulir atau slip", "Mengisi slip"), ("Tanda tangan", "Pengesahan"), ("Cap jempol", "Pengganti tanda tangan"),
    ("KTP", "Verifikasi"), ("Kartu ATM", "Layanan kartu"), ("Buku tabungan", "Cetak buku"),
    ("Benar? Ya atau tidak", "Konfirmasi"), ("Selesai", "Transaksi beres"),
]
sel = "".join(
    f"<tr><td class='b'>{i}</td><td class='b'>{k}</td><td>{d}</td><td><div class='foto'>Foto peragaan<br>co-trainer Tuli</div></td><td></td></tr>"
    for i, (k, d) in enumerate(kosakata, 1)
)
docs["02 Kartu Saku Isyarat Perbankan"] = ("Kartu Saku Isyarat Perbankan", "20 kosakata loket dan cara berkomunikasi dengan nasabah Tuli. Disimpan di meja teller dan CS.", "Modul 3", f"""
<div class="kotak"><b>Isyarat yang dipakai: BISINDO.</b> Bahasa Isyarat Indonesia dipakai sehari-hari oleh komunitas Tuli dan punya variasi daerah. Foto peragaan diisi oleh co-trainer Tuli dari Bandung supaya sesuai dengan isyarat yang dipakai nasabah setempat. {ISI("foto 20 peragaan dan abjad jari dari co-trainer, sebelum dicetak")}</div>
<h2>Cara berkomunikasi dengan nasabah Tuli</h2>
<div class="dua"><ol>
<li>Tarik perhatian dengan melambai pelan di bidang pandang atau menepuk meja.</li>
<li>Berhadapan, wajah terkena cahaya. Jangan berdiri membelakangi jendela.</li>
<li>Mulut terlihat. Lepas masker bila aman, atau pakai masker transparan.</li>
</ol><ol start="4">
<li>Kalimat pendek dan satu informasi per kalimat. Tulis angka, jangan hanya diucapkan.</li>
<li>Tanya cara yang diinginkan nasabah: isyarat, tulisan, atau gerak bibir.</li>
<li>Bila ada juru bahasa isyarat, tetap menatap nasabah saat berbicara.</li>
</ol></div>
<h2>Kosakata loket</h2>
<table><colgroup><col style="width:5%"><col style="width:22%"><col style="width:20%"><col style="width:23%"><col style="width:30%"></colgroup>
<thead><tr><th>No</th><th>Kata</th><th>Dipakai saat</th><th>Peragaan</th><th>Catatan saya di kelas</th></tr></thead><tbody>{sel}</tbody></table>
<h2>Kalimat tertulis siap pakai</h2>
{tabel(["Untuk papan tulis atau layar", "Untuk papan tulis atau layar"], [
 ["Mau setor atau tarik?", "Berapa jumlahnya? Tulis di sini."],
 ["Boleh lihat KTP?", "Tanda tangan atau cap jempol?"],
 ["Mohon tunggu 5 menit.", "Sudah selesai. Ada lagi?"],
])}
""")

# 03 Lembar Praktik Pemanduan dan Kursi Roda -------------------------------
def daftar_cek(butir):
    return tabel(["No", "Langkah", "Wajib", "Putaran 1", "Putaran 2"],
                 [[str(i), b, "Ya" if w else "", CEK, CEK] for i, (b, w) in enumerate(butir, 1)],
                 ["5%", "65%", "10%", "10%", "10%"])

docs["03 Lembar Praktik Pemanduan dan Kursi Roda"] = ("Lembar Praktik Pemanduan dan Kursi Roda", "Diisi oleh pasangan pengamat. Butir wajib harus tercentang sebelum peraga memaraf.", "Modul 2 dan 4", f"""
<p>Nama pemandu: <span class="garis"></span> &nbsp; Nama pengamat: <span class="garis"></span></p>
<h2>A. Pemanduan nasabah netra (Modul 2)</h2>
<p class="kecil">Rute empat titik: pintu masuk, undakan, lorong antrean, kursi di depan meja CS.</p>
{daftar_cek([
 ("Menyapa, menyebut nama dan jabatan sebelum menyentuh", True),
 ("Bertanya apakah nasabah ingin dipandu", True),
 ("Menyentuhkan punggung tangan ke tangan nasabah, nasabah memegang lengan di atas siku", True),
 ("Berjalan setengah langkah di depan, kecepatan mengikuti nasabah", True),
 ("Lorong selebar satu orang: memindahkan lengan ke belakang punggung, nasabah berjalan di belakang", False),
 ("Pintu: menyebut arah buka pintu, nasabah memegang pintu dengan tangan bebas", False),
 ("Undakan: berhenti sebelum undakan, menyebut naik atau turun dan jumlahnya", True),
 ("Kursi: meletakkan tangan nasabah di sandaran kursi, menyebut arah meja", True),
 ("Menjelaskan posisi benda di meja dengan arah jarum jam", False),
 ("Berpamitan sebelum meninggalkan nasabah", True),
])}
<h2>B. Kursi roda dan ramp (Modul 4)</h2>
{daftar_cek([
 ("Bertanya sebelum menyentuh atau mendorong kursi roda", True),
 ("Mengunci kedua rem sebelum nasabah naik, turun, atau pindah duduk", True),
 ("Memberi tahu sebelum mulai bergerak, berbelok, atau berhenti", True),
 ("Naik ramp: mendorong maju dengan badan condong ke depan, langkah pendek", True),
 ("Turun ramp curam: kursi roda mundur, pendorong di bawah dan melihat ke belakang", True),
 ("Undakan: memberi tahu, menginjak batang pengungkit, mengangkat roda depan pelan", False),
 ("Membantu pindah duduk hanya bila diminta, mengikuti cara yang ditunjukkan nasabah", True),
 ("Berbicara sejajar mata saat melayani di meja", False),
])}
<p>Paraf peraga netra: <span class="garis"></span> &nbsp; Paraf trainer: <span class="garis"></span></p>
""")

# 04 Kartu Skenario ---------------------------------------------------------
skenario = [
    ("Skenario 1. Pintu masuk", "Security, nasabah netra (peraga)", "Ibu Ratna, netra total, datang sendiri dengan tongkat untuk menyetor uang arisan. Pintu kaca berat, ada dua undakan.", ["Menyapa dan menyebut nama", "Menawarkan pemanduan, tidak langsung menarik tangan", "Menyebut undakan dan arah pintu", "Mengantar ke antrean prioritas dan memberi tahu CS"]),
    ("Skenario 2. Pembukaan rekening", "CS, nasabah Tuli (co-trainer)", "Pak Dimas, Tuli, ingin membuka tabungan untuk usaha laundry. Datang tanpa juru bahasa isyarat. Membawa e-KTP dan setoran awal Rp 500.000.", ["Menarik perhatian dan berhadapan", "Bertanya cara komunikasi yang diinginkan", "Menjelaskan produk dengan isyarat dasar dan tulisan", "Memastikan nasabah paham biaya bulanan dengan meminta ia menuliskannya kembali"]),
    ("Skenario 3. Setoran di teller", "Teller, nasabah netra (peraga)", "Ibu Ratna dari skenario 1 menyetor Rp 2.750.000 ke rekening 0271 0455 18. Uang terdiri dari pecahan Rp 100.000 dan Rp 50.000.", ["Membacakan slip: nama, nomor rekening, nominal angka dan terbilang", "Menghitung uang per pecahan dengan suara pelan", "Bertanya tanda tangan atau cap jempol", "Membacakan bukti setor sebelum diserahkan"]),
    ("Skenario 4. Penarikan dengan cap jempol", "Teller, Kasie, nasabah dan pendamping", "Pak Hasan, 68 tahun, tangan gemetar karena stroke dan tidak bisa tanda tangan. Datang dengan anaknya yang ingin menandatangani untuk ayahnya. Menarik Rp 1.200.000.", ["Bicara kepada Pak Hasan, bukan kepada anaknya", "Menjelaskan bahwa anak tidak bisa tanda tangan atas nama ayah tanpa surat kuasa", "Kasie hadir sebagai saksi internal", "Formulir aset 07 diisi lengkap"]),
    ("Skenario 5. Keluhan di ruang layanan", "Kasie, nasabah pengguna kursi roda", "Ibu Sari, pengguna kursi roda, sudah menunggu 40 menit karena nomor antreannya dipanggil saat ia di toilet. Ia menyampaikan keluhan dengan suara keras di ruang tunggu.", ["Mendekat dan bicara sejajar mata", "Mendengarkan tanpa memotong, mengakui keterlambatan", "Memberi layanan saat itu juga di meja yang terjangkau", "Mencatat keluhan di log dan menjelaskan tindak lanjut"]),
]
kartu = [
    f"""<div class="kartu"><div class="judul">{j}</div><p><b>Peran:</b> {p}</p><p><b>Situasi:</b> {s}</p>
<p><b>Yang harus muncul:</b></p><ol>{''.join(f'<li>{x}</li>' for x in h)}</ol></div>""" for j, p, s, h in skenario]
docs["04 Kartu Skenario Role-Play"] = ("Kartu Skenario Role-Play", "Lima skenario untuk Modul 6. Tiap skenario 8 menit main dan 1 menit umpan balik. Kartu dipotong dan dibagikan per peran.", "Modul 6", f"""
<p>{REKAAN} Nama, nomor rekening, dan nominal tidak terkait dengan nasabah PT BPR NBP 27.</p>
<div class="dua"><div>{"".join(kartu[:3])}</div><div>{"".join(kartu[3:])}</div></div>
<div class="kotak"><b>Untuk peraga.</b> Di skenario 3 dan 4, peraga sengaja tidak mengoreksi bila petugas lupa membacakan nominal terbilang. Kesalahan itu dibahas saat umpan balik.</div>
""")

# 05 Rubrik Observasi -------------------------------------------------------
docs["05 Rubrik Observasi Layanan"] = ("Rubrik Observasi Layanan Nasabah Disabilitas", "Diisi Kasie Operasional saat Modul 6, lalu dipakai untuk memantau layanan di kantor.", "Modul 6", f"""
<p>Skor 1: belum dilakukan atau keliru. Skor 2: dilakukan dengan bantuan atau tidak lengkap. Skor 3: dilakukan sendiri dan lengkap.</p>
{tabel(["Aspek", "Skor 3 bila", "S1", "S2", "S3", "S4", "S5"], [
 ["<b>Menyambut</b>", "Menyapa, menyebut nama dan jabatan, bertanya sebelum membantu", "", "", "", "", ""],
 ["<b>Bicara kepada nasabah</b>", "Menatap dan bertanya kepada nasabah, bukan pendamping", "", "", "", "", ""],
 ["<b>Cara komunikasi</b>", "Memakai cara yang dipilih nasabah: isyarat, tulisan, lisan deskriptif", "", "", "", "", ""],
 ["<b>Mobilitas</b>", "Teknik pemanduan atau kursi roda sesuai lembar praktik", "", "", "", "", ""],
 ["<b>Pembacaan dokumen</b>", "Nama, nomor rekening, nominal angka dan terbilang dibacakan", "", "", "", "", ""],
 ["<b>Legalitas</b>", "Identitas dicek, saksi hadir, formulir lengkap", "", "", "", "", ""],
 ["<b>Kerahasiaan</b>", "Data tidak terdengar antrean", "", "", "", "", ""],
 ["<b>Penanganan keluhan</b>", "Mendengar, mengakui, menyelesaikan, mencatat", "", "", "", "", ""],
 ["<b>Rata-rata</b>", "Target minimal 2,5", "", "", "", "", ""],
], ["20%", "45%", "7%", "7%", "7%", "7%", "7%"])}
<p class="kecil">S1 sampai S5 adalah skenario di aset 04. Aspek yang tidak muncul di satu skenario dikosongkan dan tidak dihitung.</p>
<h2>Catatan pengamat</h2>
<p>Hal yang sudah baik: <span class="garis" style="min-width:420px"></span></p>
<p>Hal yang perlu diulang: <span class="garis" style="min-width:410px"></span></p>
<h2>Memakai rubrik di kantor</h2>
<p>Kasie mengamati tiga layanan nasabah disabilitas pertama setelah pelatihan dengan rubrik yang sama, lalu menyimpan lembarnya bersama log keluhan sebagai bukti pemantauan.</p>
""")

# 06 Pre-Test dan Post-Test --------------------------------------------------
soal = [
    ("Nasabah netra masuk ke kantor sendirian. Langkah pertama security adalah", ["Langsung menggandeng tangannya ke kursi", "Menyapa, menyebut nama dan jabatan, lalu bertanya apakah ia ingin dipandu", "Meminta ia menunggu keluarganya"]),
    ("Saat memandu nasabah netra, nasabah sebaiknya memegang", ["Lengan petugas sedikit di atas siku", "Telapak tangan petugas", "Bahu petugas dari belakang"]),
    ("Nasabah Tuli datang dengan juru bahasa isyarat. Petugas berbicara sambil menatap", ["Juru bahasa", "Layar komputer", "Nasabah"]),
    ("Pendamping ingin memutuskan jumlah penarikan untuk nasabah disabilitas intelektual. Sikap petugas", ["Mengikuti pendamping karena lebih paham", "Bertanya kepada nasabah dengan kalimat pendek dan memastikan keputusannya", "Menolak transaksi"]),
    ("Sebelum pengguna kursi roda pindah duduk, petugas", ["Mengunci kedua rem kursi roda", "Memegang sandaran saja", "Melepas sandaran kaki tanpa bertanya"]),
    ("Untuk ramp yang curam, cara aman menurunkan kursi roda adalah", ["Maju dengan cepat", "Maju sambil menahan pegangan", "Mundur, pendorong berada di bawah dan melihat ke belakang"]),
    ("Saat membacakan slip setoran kepada nasabah netra, yang dibacakan adalah", ["Nominal saja", "Nama, nomor rekening, nominal angka dan terbilang", "Nomor rekening saja"]),
    ("Nasabah netra yang bisa tanda tangan", ["Tetap berhak tanda tangan bila ia memilih", "Wajib memakai cap jempol", "Harus diwakili pendamping"]),
    ("Data nasabah dibacakan", ["Dengan suara keras supaya jelas", "Oleh pendamping", "Dengan suara pelan agar tidak terdengar antrean"]),
    ("Pedoman SETARA diterbitkan oleh", ["Bank Indonesia", "Otoritas Jasa Keuangan", "Kementerian Sosial"]),
]
bs = [
    "POJK 22/2023 mengatur pelindungan konsumen dan masyarakat di sektor jasa keuangan.",
    "Anak nasabah boleh tanda tangan atas nama orang tuanya tanpa surat kuasa bila orang tuanya hadir.",
    "Tongkat dan anjing pemandu tidak disentuh tanpa izin pemiliknya.",
    "Istilah cacat masih tepat dipakai di ruang layanan.",
    "Log keluhan nasabah disabilitas dapat menjadi bukti saat pemeriksaan.",
]
s_html = "".join(
    f"<li>{q}<br>" + " &nbsp; ".join(f"{CEK}{'ABC'[i]}. {o}" for i, o in enumerate(op)) + "</li>" for q, op in soal
)
b_html = "".join(f"<li>{q} &nbsp; {CEK}Benar {CEK}Salah</li>" for q in bs)
docs["06 Pre-Test dan Post-Test"] = ("Pre-Test dan Post-Test", "15 soal, 15 menit. Soal yang sama dipakai di awal dan akhir hari supaya peningkatan dapat dibandingkan.", "Awal dan akhir hari", f"""
<p>Nama: <span class="garis"></span> &nbsp; Jabatan: <span class="garis"></span> &nbsp; {CEK}Pre-test {CEK}Post-test</p>
<h2>A. Pilih satu jawaban</h2><ol>{s_html}</ol>
<h2>B. Benar atau salah</h2><ol start="11">{b_html}</ol>
<h2>C. Survei kepuasan (hanya saat post-test)</h2>
{tabel(["Pernyataan", "1", "2", "3", "4", "5"], [[p, CEK, CEK, CEK, CEK, CEK] for p in [
 "Praktik hari ini bisa saya pakai di loket besok",
 "Porsi praktik cukup untuk saya mencoba sendiri",
 "Peraga dan co-trainer membantu saya memahami kebutuhan nasabah",
 "Kit yang dibagikan mudah dipakai",
]], ["70%", "6%", "6%", "6%", "6%", "6%"])}
<p class="kecil">1 sangat tidak setuju, 5 sangat setuju. Soal bisa dipindah ke Google Form bila BPR ingin rekap otomatis. Kunci jawaban ada di Panduan Fasilitator.</p>
""")

# 07 Formulir Pembacaan Slip dan Cap Jempol ----------------------------------
docs["07 Contoh Formulir Pembacaan Slip dan Kesaksian Cap Jempol"] = ("Formulir Pembacaan Slip dan Kesaksian Cap Jempol", "Contoh formulir untuk simulasi Modul 5. Bentuk akhir mengikuti SOP dan persetujuan bagian kepatuhan PT BPR NBP 27.", "Modul 5", f"""
<div class="kotak">Formulir ini contoh latihan, bukan formulir resmi bank. {ISI("cocokkan dengan formulir dan SOP yang berlaku di BPR NBP 27")}</div>
<h2>Data transaksi</h2>
{tabel(["Butir", "Isi"], [
 ["Tanggal dan jam", "<span class='garis'></span>"],
 ["Jenis transaksi", f"{CEK}Setoran {CEK}Penarikan {CEK}Pembukaan rekening {CEK}Lainnya"],
 ["Nama nasabah sesuai e-KTP", "<span class='garis'></span>"],
 ["NIK dicocokkan dengan e-KTP asli", f"{CEK}Ya, wajah sesuai foto"],
 ["Nomor rekening", "<span class='garis'></span>"],
 ["Nominal angka", "Rp <span class='garis'></span>"],
 ["Nominal terbilang", "<span class='garis' style='min-width:300px'></span>"],
 ["Ragam disabilitas (bila nasabah menyampaikan)", f"{CEK}Netra {CEK}Tuli atau wicara {CEK}Fisik {CEK}Intelektual {CEK}Lainnya"],
], ["38%", "62%"])}
<h2>Pembacaan dan persetujuan</h2>
{tabel(["", "Langkah"], [
 [CEK, "Slip dibacakan lengkap: nama, nomor rekening, nominal angka dan terbilang"],
 [CEK, "Nasabah menyatakan isi slip sesuai kehendaknya"],
 [CEK, "Nasabah ditanya cara pengesahan dan memilih: tanda tangan atau cap jempol"],
 [CEK, "Pendamping (bila ada) hanya membantu, keputusan dari nasabah"],
 [CEK, "Pembacaan dilakukan dengan suara pelan, tidak terdengar antrean"],
], ["6%", "94%"])}
<h2>Pengesahan</h2>
<table><thead><tr><th>Cap jempol atau tanda tangan nasabah</th><th>Petugas yang membacakan</th><th>Saksi internal</th></tr></thead>
<tbody><tr><td style="height:90px"></td><td style="height:90px"></td><td style="height:90px"></td></tr>
<tr><td>Jari yang dipakai: <span class="garis" style="min-width:80px"></span></td><td>Nama dan jabatan</td><td>Nama dan jabatan</td></tr></tbody></table>
<h2>Daftar periksa Kasie</h2>
<p>{CEK}Identitas &nbsp; {CEK}Slip dibacakan &nbsp; {CEK}Pilihan pengesahan dicatat &nbsp; {CEK}Saksi hadir &nbsp; {CEK}Formulir disimpan bersama warkat</p>
""")

# 08 Lembar Audit Aksesibilitas ----------------------------------------------
butir_audit = [
    ("Luar gedung", ["Parkir dekat pintu untuk pengguna kursi roda", "Ramp tersedia di setiap undakan menuju pintu", "Kemiringan ramp diukur (tinggi dibagi panjang)", "Pegangan tangan di ramp", "Permukaan ramp tidak licin"]),
    ("Pintu dan ruang tunggu", ["Lebar pintu cukup untuk kursi roda", "Pintu mudah dibuka atau ada petugas yang siap membantu", "Kursi tunggu prioritas diberi tanda", "Nomor antrean diumumkan lewat suara dan layar", "Jalur dari pintu ke loket bebas halangan"]),
    ("Loket dan meja CS", ["Ada meja layanan yang terjangkau dari kursi roda", "Pena, kalkulator, dan mesin EDC bisa didekatkan", "Papan tulis kecil untuk nasabah Tuli", "Kaca pembesar atau formulir huruf besar", "Posisi meja memungkinkan bicara pelan tanpa terdengar antrean"]),
    ("Fasilitas lain", ["Toilet dapat dipakai pengguna kursi roda", "Informasi biaya dan produk tersedia dalam huruf besar", "ATM dapat dijangkau dari kursi roda", "Kontak layanan pengaduan tertulis, bukan hanya telepon"]),
]
rows = []
for kel, bs_ in butir_audit:
    rows.append([f"<b>{kel}</b>", "", "", "", ""])
    rows += [["", b, CEK, CEK, ""] for b in bs_]
docs["08 Lembar Audit Aksesibilitas Kantor"] = ("Lembar Audit Aksesibilitas Kantor", "Diisi dua kelompok peserta saat Modul 4 di ruang layanan BPR. Hasilnya menjadi rekomendasi perbaikan fasilitas di laporan.", "Modul 4", f"""
<p>Kantor: <span class="garis"></span> &nbsp; Kelompok: <span class="garis" style="min-width:80px"></span> &nbsp; Jam: <span class="garis" style="min-width:80px"></span></p>
{tabel(["Area", "Butir yang diperiksa", "Ada", "Belum", "Ukuran, foto, catatan"], rows, ["15%", "45%", "7%", "7%", "26%"])}
<p class="kecil">Ukuran ramp dan pintu dibandingkan dengan Permen PUPR No. 14/PRT/M/2017 tentang Persyaratan Kemudahan Bangunan Gedung saat laporan disusun. Lembar ini mencatat keadaan, bukan menilai kelayakan bangunan secara teknis.</p>
<h2>Tiga temuan utama kelompok</h2>
<ol><li><span class="garis" style="min-width:480px"></span></li><li><span class="garis" style="min-width:480px"></span></li><li><span class="garis" style="min-width:480px"></span></li></ol>
""")

# 09 Contoh Sertifikat ---------------------------------------------------------
docs["09 Contoh Sertifikat Pelatihan"] = None  # dibuat di bawah dengan halaman landscape

# 10 Draf Contoh Laporan Evaluasi ----------------------------------------------
nilai = [("Peserta 1", "Frontliner", 53.3, 86.7), ("Peserta 2", "Frontliner", 60.0, 93.3), ("Peserta 3", "Frontliner", 46.7, 80.0),
         ("Peserta 4", "Frontliner", 66.7, 93.3), ("Peserta 5", "Frontliner", 40.0, 73.3), ("Peserta 6", "Frontliner", 60.0, 86.7),
         ("Peserta 7", "Kasie Operasional", 73.3, 100.0), ("Peserta 8", "Kasie Operasional", 66.7, 93.3),
         ("Peserta 9", "Lainnya", 46.7, 80.0), ("Peserta 10", "Lainnya", 53.3, 86.7)]
fmt = lambda x: f"{x:.1f}".replace(".", ",")
baris_n = [[n, j, fmt(a), fmt(b), fmt(b - a), "Ya" if b >= 80 else "Belum"] for n, j, a, b in nilai]
ra = sum(a for _, _, a, _ in nilai) / len(nilai)
rb = sum(b for _, _, _, b in nilai) / len(nilai)
baris_n.append(["<b>Rata-rata</b>", "", f"<b>{fmt(ra)}</b>", f"<b>{fmt(rb)}</b>", f"<b>{fmt(rb-ra)}</b>", f"<b>{sum(1 for *_, b in nilai if b >= 80)} dari 10</b>"])
batang = "".join(
    f"<div style='display:flex;align-items:center;gap:6px;margin:2px 0'><div style='width:70px;font-size:7.5pt'>{n}</div>"
    f"<div style='flex:1;position:relative;height:14px;background:#f1f5f5'>"
    f"<div style='position:absolute;left:0;top:0;height:7px;width:{a}%;background:#9fb8c4'></div>"
    f"<div style='position:absolute;left:0;top:7px;height:7px;width:{b}%;background:#15908F'></div></div></div>"
    for n, _, a, b in nilai)
docs["10 Draf Contoh Laporan Evaluasi Program"] = ("Draf Contoh Laporan Evaluasi Program", "Bentuk laporan yang diserahkan paling lambat 7 hari kerja setelah pelatihan. Angka di draf ini contoh untuk menunjukkan isi laporan, bukan hasil pelatihan.", "Sesudah kelas", f"""
<div class="kotak"><b>Contoh.</b> Semua nilai dan temuan di halaman ini rekaan. Laporan asli memakai data dari aset 06, 05, dan 08.</div>
<h2>Daftar isi laporan</h2>
<ol><li>Ringkasan pelaksanaan: tanggal, tempat, peserta, tim</li><li>Hasil pre-test dan post-test per peserta</li><li>Hasil rubrik observasi per skenario</li><li>Survei kepuasan</li><li>Temuan audit aksesibilitas dan rekomendasi perbaikan fasilitas</li><li>Rekomendasi tindak lanjut layanan</li><li>Lampiran: daftar hadir, dokumentasi foto dan video, salinan sertifikat</li></ol>
<h2>2. Nilai pre-test dan post-test</h2>
{tabel(["Peserta", "Jabatan", "Pre", "Post", "Naik", "Post 80 atau lebih"], baris_n, ["18%", "26%", "12%", "12%", "12%", "20%"])}
<div style="border:1px solid #cfd8dc;padding:8px 10px;margin-bottom:10px"><div class="kecil" style="margin-bottom:4px"><b>Grafik nilai per peserta.</b> Abu: pre-test. Teal: post-test. Skala 0 sampai 100. Sumber: data contoh.</div>{batang}</div>
<h2>5. Rekomendasi fasilitas (contoh)</h2>
{tabel(["Temuan", "Rekomendasi", "Prioritas"], [
 ["Ramp di pintu depan tanpa pegangan tangan", "Pasang pegangan di kedua sisi ramp", "Tinggi"],
 ["Semua meja teller setinggi meja berdiri", "Sediakan satu meja layanan rendah di CS untuk pengguna kursi roda", "Tinggi"],
 ["Nomor antrean hanya dipanggil lewat suara", "Tampilkan nomor di layar atau beri kartu getar untuk nasabah Tuli", "Sedang"],
 ["Belum ada papan tulis di loket", "Simpan papan tulis genggam di tiap loket", "Rendah, biaya ringan"],
], ["38%", "47%", "15%"])}
<h2>6. Rekomendasi tindak lanjut layanan</h2>
<p>Kasie Operasional memakai rubrik (aset 05) untuk tiga layanan nasabah disabilitas pertama setelah pelatihan dan menyimpan lembarnya bersama log keluhan. Hasilnya menjadi bukti pemantauan dan menunjukkan apakah praktik di kelas sudah dipakai di loket.</p>
""")

# Tulis semua HTML ---------------------------------------------------------
jobs = []
for nama, val in docs.items():
    if val is None:
        continue
    judul, sub, label, isi = val
    p = HTML / f"kit-{nama[:2]}.html"
    p.write_text(kit_html(judul, sub, label, isi), encoding="utf8")
    jobs.append({"html": str(p), "pdf": str(ROOT / "kit" / f"{nama}.pdf"), "width": 794, "height": 1123})

# Sertifikat (A4 landscape)
from gaya import FONT_FACE, LOGO, TEAL, CYAN, BIRU
sert = f"""<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Sertifikat</title><style>{FONT_FACE}
@page {{ size: A4 landscape; margin: 0 }} body {{ margin:0; font-family:'Inter'; }}
.s {{ width:297mm; height:210mm; padding:14mm; box-sizing:border-box; }}
.b {{ border:3px solid {TEAL}; height:100%; padding:12mm 16mm; box-sizing:border-box; position:relative; text-align:center; }}
.b:before {{ content:''; position:absolute; inset:5px; border:1px solid {CYAN}; }}
img {{ height:30px; }} h1 {{ font-family:'Montserrat'; font-weight:800; letter-spacing:6px; color:#13314f; font-size:30pt; margin:10mm 0 2mm; }}
.n {{ font-family:'Montserrat'; font-weight:700; font-size:24pt; color:{TEAL}; margin:6mm 0 2mm; }}
.t {{ font-size:11pt; color:#333; line-height:1.55; }} .ttd {{ display:flex; justify-content:space-around; margin-top:12mm; font-size:10pt; }}
.ttd div {{ width:70mm; border-top:1px solid #333; padding-top:4px; }} .isi {{ background:#FFF200; font-weight:600; padding:0 3px; }}
.no {{ position:absolute; top:8mm; right:12mm; font-size:8.5pt; color:#555; }}
</style></head><body><div class="s"><div class="b"><div class="no">Nomor: SGB/IHT-NBP27/2026/001</div>
<img src="{LOGO}"><h1>SERTIFIKAT</h1><div class="t">diberikan kepada</div>
<div class="n">Nama Peserta</div><div class="t">Staf Pelaksana Frontliner, PT BPR NBP 27</div>
<p class="t" style="margin-top:6mm">sebagai peserta <b>In-House Training Pelayanan Inklusif bagi Konsumen Disabilitas Sektor Perbankan</b><br>
yang diselenggarakan di Bandung pada <span class="isi">[ISI TIM: tanggal]</span> selama 1 hari (6 jam pembelajaran),<br>
sesuai amanat POJK No. 22 Tahun 2023 tentang Pelindungan Konsumen dan Masyarakat di Sektor Jasa Keuangan<br>dan Pedoman Akses Pelayanan Keuangan untuk Disabilitas Berdaya (SETARA) OJK.</p>
<p class="t">Nilai post-test: 86,7 &nbsp; | &nbsp; Rubrik praktik: 2,7 dari 3</p>
<div class="ttd"><div>Direktur Sanggabiz<br><span class="isi">[ISI TIM: nama]</span></div><div>Trainer Utama<br><span class="isi">[ISI TIM: nama]</span></div></div>
</div></div></body></html>"""
p = HTML / "kit-09.html"
p.write_text(sert, encoding="utf8")
jobs.append({"html": str(p), "pdf": str(ROOT / "kit" / "09 Contoh Sertifikat Pelatihan.pdf"), "width": 1123, "height": 794})

(BUILD / "jobs_kit.json").write_text(json.dumps(jobs, indent=1))
print(len(jobs), "dokumen kit")
