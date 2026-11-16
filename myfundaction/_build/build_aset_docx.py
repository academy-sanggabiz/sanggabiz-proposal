"""Aset peserta dan trainer: pustaka prompt, lembar kerja, pre-test dan post-test, kunci jawaban."""
import os

import build_data
import prompt_data as P
import silabus_data as d
from docx_lib import butir, dokumen, h, kode, kotak_isian, para, pindah_halaman, tabel

HERE = os.path.dirname(os.path.abspath(__file__))
ASET = os.path.join(HERE, "..", "aset")
os.makedirs(ASET, exist_ok=True)

KUNCI = build_data.jalankan()

# =====================================================================
# 1. Pustaka Prompt dan Standar Prompt MFA
# =====================================================================
doc = dokumen(
    "Pustaka Prompt dan Standar Prompt MFA",
    "Satu cara menulis prompt untuk tim Indonesia, Malaysia, dan Australia. Dipakai di Modul 3 dan Modul 7. Versi 1, 16 November 2026.",
)
para(doc, "Dokumen ini adalah draf awal standar. Peserta melengkapinya di Topik 3.3, lalu MFA menetapkan versi resminya. Simpan di satu Claude Project bersama atau satu folder bersama yang dipakai ketiga tim, supaya semua orang memakai templat yang sama.")

h(doc, "1. Enam unsur prompt")
para(doc, "Prompt yang baik memuat enam unsur. Tiap unsur dinilai 0, 1, atau 2, jadi skor prompt 0 sampai 12. Skor ini dipakai di pre-test, post-test, dan saat tim saling memeriksa prompt.")
tabel(doc, ["Unsur", "Artinya", "Skor 0", "Skor 1", "Skor 2"],
      [[f"{u} ({en})", arti, s0, s1, s2] for u, en, arti, s0, s1, s2 in d.RUBRIK],
      lebar=[2.8, 3.8, 2.9, 3.4, 4.1], size=9, kepala_teal=True)
para(doc, "Cara membaca skor: 0 sampai 5 perlu ditulis ulang, 6 sampai 8 cukup untuk tugas ringan, 9 sampai 12 siap dipakai sebagai templat bersama.")

h(doc, "2. Teknik yang dipakai di templat")
butir(doc, [
    "**Tag pemisah.** Bahan, contoh, dan aturan ditaruh di dalam tag seperti <data> dan </data>. AI jadi bisa membedakan perintah dari bahan. Nama tag bebas asal jelas.",
    "**Contoh.** Satu sampai tiga contoh hasil yang baik membuat gaya keluaran konsisten antarorang dan antarnegara.",
    "**Berpikir dulu.** Untuk analisis, minta AI menuliskan langkah atau rumus sebelum jawaban. Kesalahan hitung lebih mudah terlihat.",
    "**Tempat isian.** Bagian yang berubah ditulis dalam kurung kurawal, misalnya {negara} dan {nama_program}. Orang lain cukup mengganti isian tanpa menulis ulang prompt.",
    "**Perbaiki prompt, bukan mengulang pertanyaan.** Bila hasil belum tepat, tambahkan unsur yang kurang lalu jalankan ulang.",
])

h(doc, "3. Contoh: sebelum dan sesudah")
para(doc, "Sebelum (skor 1 dari 12, hanya ada tugas yang kabur):", bold=True)
kode(doc, P.CONTOH_SEBELUM)
para(doc, "Sesudah (skor 12 dari 12):", bold=True)
kode(doc, P.CONTOH_SESUDAH)

h(doc, "4. Aturan etika penggalangan dana")
para(doc, "Aturan ini disalin ke bagian <aturan> di setiap prompt yang hasilnya dibaca donatur atau publik.")
butir(doc, P.ETIKA, nomor=True)

h(doc, "5. Glosarium tiga bahasa")
para(doc, "Istilah yang dipakai sama di semua prompt dan hasil. [ISI TIM: cocokkan istilah Melayu dan Inggris dengan tim MFA Malaysia dan Australia]")
tabel(doc, ["Bahasa Indonesia", "English", "Bahasa Melayu"], [list(g) for g in P.GLOSARIUM], lebar=[5.6, 5.6, 5.6])

h(doc, "6. Templat")
para(doc, "Sepuluh templat untuk tugas CRM, iklan, marketing, dan analisis. Versi bahasa Indonesia untuk tim Jakarta, versi bahasa Inggris untuk tim Malaysia dan Australia. Ganti semua isian dalam kurung kurawal.")
tabel(doc, ["Kode", "Templat", "Dipakai untuk"], [[t["kode"], t["judul"], t["untuk"]] for t in P.TEMPLAT], lebar=[1.6, 10, 5.2])
for t in P.TEMPLAT:
    h(doc, f"{t['kode']} {t['judul']}", 2)
    para(doc, f"Dipakai untuk: {t['untuk']}", size=9.5, italic=True)
    para(doc, "Bahasa Indonesia", bold=True, size=10)
    kode(doc, t["id"])
    para(doc, "English", bold=True, size=10)
    kode(doc, t["en"])

h(doc, "7. Cara merawat standar")
butir(doc, [
    "Satu orang di tiap negara menjadi penanggung jawab templat. [ISI TIM: nama penanggung jawab Indonesia, Malaysia, Australia]",
    "Templat baru masuk standar bila skornya minimal 10 dari 12 dan sudah dipakai dua orang dengan hasil yang sama baiknya.",
    "Setiap tiga bulan ketiga tim memeriksa ulang templat yang paling sering dipakai.",
], nomor=True)

doc.save(os.path.join(ASET, "v1 Pustaka Prompt dan Standar Prompt MFA.docx"))

# =====================================================================
# 2. Lembar Kerja Peserta
# =====================================================================
doc = dokumen("Lembar Kerja Peserta", "Pelatihan AI Agent untuk Tim CRM dan Marketing MyFundAction. Isi selama pelatihan dan bawa pulang.")
tabel(doc, ["Nama", "Tim", "Negara"], [["", "", ""]], lebar=[6.5, 5, 5])

h(doc, "Halaman 1. Modul 1: Pengenalan AI")
para(doc, "Topik 1.1. Lengkapi kalimat ini dengan kata-kata Anda sendiri.", bold=True)
kotak_isian(doc, "AI bisa salah dengan yakin karena ...", 3)
para(doc, "Topik 1.2. Tulis 5 tugas yang paling menyita waktu minggu lalu, lalu beri warna.", bold=True)
tabel(doc, ["No", "Tugas", "Hijau (AI) / Kuning (AI dan diperiksa) / Merah (bukan untuk AI)", "Alasan"],
      [[str(i), "", "", ""] for i in range(1, 6)], lebar=[1, 6, 5.3, 4.5], tinggi=1.3)
para(doc, "Ingat: data pribadi donatur, angka dampak program, dan keputusan soal uang tidak masuk kolom hijau.", size=9.5, italic=True)
pindah_halaman(doc)

h(doc, "Halaman 2. Topik 2.1: Mengenal Claude")
tabel(doc, ["No", "Langkah", "Selesai"], [
    ["1", "Masuk ke claude.ai atau aplikasi desktop", ""],
    ["2", "Mulai percakapan baru dan minta Claude memperkenalkan diri dalam 3 kalimat", ""],
    ["3", "Unggah PDF profil program air bersih (bahan latihan) dan minta 3 poin utamanya", ""],
    ["4", "Buat Project bernama Latihan MFA", ""],
    ["5", "Isi instruksi Project: Kamu membantu tim CRM dan marketing MyFundAction. Jawab dalam bahasa Indonesia kecuali diminta lain. Jangan mengarang angka.", ""],
    ["6", "Unggah satu berkas ke pengetahuan Project, lalu tanyakan isinya dari percakapan di dalam Project", ""],
], lebar=[1, 13.5, 2.3])
para(doc, "Yang tidak diunggah ke Claude akun pribadi: data donatur asli, dokumen internal yang belum boleh dibagikan, kata sandi, dan kunci API.", size=9.5, italic=True)
pindah_halaman(doc)

h(doc, "Halaman 3. Topik 2.2: Praktik Claude")
para(doc, "Kerjakan berpasangan. Bahan ada di bagian Lampiran di akhir lembar kerja dan di folder data-latihan.")
tabel(doc, ["Tugas", "Yang diminta", "Prompt yang Anda pakai (ringkas)"], [
    ["A", "Ringkas laporan program Palestina (Lampiran 1) menjadi 5 poin untuk donatur", ""],
    ["B", "Draf pesan terima kasih donatur program masjid dalam bahasa Indonesia dan Inggris", ""],
    ["C", "Unggah kampanye-iklan-rekaan.csv, minta tabel total biaya dan jumlah donasi per negara", ""],
], lebar=[1.5, 7.5, 7.8], tinggi=2.2)
para(doc, "Daftar periksa hasil AI. Centang bila sudah benar.", bold=True)
tabel(doc, ["Butir", "Tugas A", "Tugas B", "Tugas C"], [
    ["Fakta sesuai bahan", "", "", ""],
    ["Semua angka ada di bahan, tidak ada angka karangan", "", "", ""],
    ["Nada sesuai pembaca", "", "", ""],
    ["Bahasa benar untuk negara tujuan", "", "", ""],
    ["Tidak ada data pribadi", "", "", ""],
], lebar=[8, 2.9, 2.9, 2.9])
kotak_isian(doc, "Satu kesalahan AI yang kami temukan:", 2)
pindah_halaman(doc)

h(doc, "Halaman 4. Topik 3.1: Enam unsur prompt")
para(doc, "Tulis ulang prompt tugas B dari Modul 2 memakai enam unsur.", bold=True)
for u, en, arti, *_ in d.RUBRIK:
    kotak_isian(doc, f"{u}: {arti}", 2)
kotak_isian(doc, "Apa yang berubah pada hasilnya dibanding prompt pertama?", 2)
pindah_halaman(doc)

h(doc, "Halaman 5. Topik 3.2: Bedah dan perbaiki prompt")
para(doc, "Beri skor tiap prompt dari trainer dengan rubrik (0, 1, atau 2 per unsur), lalu tulis versi perbaikan.")
tabel(doc, ["Unsur", "Prompt 1", "Prompt 2", "Prompt 3"], [[u, "", "", ""] for u, *_ in d.RUBRIK] + [["Total (maks 12)", "", "", ""], ["Skor versi perbaikan", "", "", ""]],
      lebar=[5, 3.9, 3.9, 3.9], tinggi=0.9)
kotak_isian(doc, "Versi perbaikan prompt nomor ...", 6)
pindah_halaman(doc)

h(doc, "Halaman 6. Topik 3.3: Templat bersama")
para(doc, "Pilih satu tugas dari peta tugas di halaman 1. Susun templatnya dalam dua bahasa dengan tempat isian {seperti_ini}.")
tabel(doc, ["Bagian", "Isi"], [["Nama templat", ""], ["Dipakai oleh tim", ""], ["Isian yang berubah", ""]], lebar=[4.5, 12.3], tinggi=0.9)
kotak_isian(doc, "Versi bahasa Indonesia", 7)
kotak_isian(doc, "English version", 7)
pindah_halaman(doc)

h(doc, "Halaman 7. Topik 4.1: Memilih calon agen")
para(doc, "Uji 3 tugas dari halaman 1 dengan empat pertanyaan. Tugas yang menjawab ya pada keempatnya layak dijadikan agen.")
tabel(doc, ["Pertanyaan", "Tugas 1", "Tugas 2", "Tugas 3"], [
    ["Nama tugas", "", "", ""],
    ["Berulang setiap hari atau minggu?", "", "", ""],
    ["Ada aturan yang jelas untuk mengerjakannya?", "", "", ""],
    ["Ada data yang boleh dipakai agen?", "", "", ""],
    ["Ada orang yang memeriksa hasilnya?", "", "", ""],
], lebar=[7, 3.3, 3.3, 3.3], tinggi=1.2)
kotak_isian(doc, "Calon agen saya:", 2)
pindah_halaman(doc)

h(doc, "Halaman 8. Topik 5.1: Alur tiga agen")
para(doc, "Gambar alur pesan saat trainer meminta laporan kampanye di grup Telegram latihan. Tandai dengan bintang titik di mana manusia memeriksa sebelum pesan keluar.")
kotak_isian(doc, "Tim MFA, Agen Analis, Agen Iklan, Agen CRM, donatur", 11)
tabel(doc, ["Bagian Hermes", "Fungsinya (tulis sendiri)"], [["SOUL.md", ""], ["Memori", ""], ["Skill", ""], ["Profil", ""], ["Gateway", ""], ["Jadwal", ""]], lebar=[4, 12.8], tinggi=0.85)
pindah_halaman(doc)

h(doc, "Halaman 9. Catatan praktik Modul 6 dan Modul 7")
tabel(doc, ["Langkah", "Hasil", "Catatan masalah"], [
    ["6.1 Hermes terpasang (laptop atau server latihan)", "", ""],
    ["6.1 hermes doctor tanpa masalah", "", ""],
    ["6.2 SOUL.md terisi dari templat", "", ""],
    ["6.2 Agen menjawab di Telegram", "", ""],
    ["6.2 Lima butir keamanan terpenuhi", "", ""],
], lebar=[7.5, 3, 6.3])
para(doc, "Topik 7.1. Aturan segmen: Baru bila donasi pertama paling lama 90 hari sebelum 16 November 2026. Tidak aktif bila donasi terakhir lebih dari 180 hari. Rutin bila donasi 12 bulan 3 kali atau lebih. Sisanya Lainnya. Periksa dengan urutan itu.", size=10)
tabel(doc, ["Segmen", "Jumlah donatur", "Yang setuju dihubungi"], [["Baru", "", ""], ["Rutin", "", ""], ["Tidak aktif", "", ""], ["Lainnya", "", ""]], lebar=[5.6, 5.6, 5.6])
para(doc, "Topik 7.2. Variasi iklan terpilih", size=10, bold=True)
tabel(doc, ["Negara", "Judul", "Teks utama", "Lolos aturan etika?"], [["Australia", "", "", ""], ["Indonesia", "", "", ""]], lebar=[2.6, 4, 7.4, 2.8])
para(doc, "Topik 7.3. Analisis kampanye", size=10, bold=True)
tabel(doc, ["Pertanyaan", "Jawaban agen", "Cek manual"], [
    ["Negara dan program dengan biaya per donasi terendah", "", ""],
    ["Negara dan program dengan nilai donasi per 1 USD iklan tertinggi", "", ""],
    ["Mengapa dua jawaban di atas bisa berbeda?", "", ""],
    ["Jadwal laporan mingguan yang dibuat", "", ""],
], lebar=[7, 5, 4.8])
pindah_halaman(doc)

h(doc, "Halaman 10. Topik 7.4: Kanvas agen 30 hari")
tabel(doc, ["Bagian", "Isi"], [
    ["Nama agen", ""],
    ["Tugas yang dikerjakan", ""],
    ["Pemicu: kapan agen bekerja (jadwal atau permintaan)", ""],
    ["Data yang boleh dipakai", ""],
    ["Data yang tidak boleh dipakai", ""],
    ["Alat: Telegram, berkas, situs, spreadsheet", ""],
    ["Hasil yang dikirim dan ke siapa", ""],
    ["Pemeriksa sebelum hasil dipakai", ""],
    ["Ukuran berhasil setelah 30 hari", ""],
    ["Minggu 1: uji dengan data rekaan", ""],
    ["Minggu 2: uji terbatas", ""],
    ["Minggu 3 dan 4: dipakai rutin", ""],
    ["Pertanyaan untuk klinik pendampingan", ""],
], lebar=[6.5, 10.3], tinggi=1.45)
pindah_halaman(doc)

h(doc, "Lampiran 1. Laporan rekaan program Palestina (untuk Tugas A)")
para(doc, "Teks ini rekaan untuk latihan. Angkanya bukan data MyFundAction.", italic=True, size=9.5)
para(doc, "Laporan penyaluran Oktober 2026. Pada bulan Oktober tim lapangan menyalurkan 1.200 paket makanan di dua titik pengungsian. Setiap paket berisi beras, minyak, kacang-kacangan, dan susu bubuk untuk satu keluarga selama satu minggu. Penyaluran dilakukan bersama dua mitra lokal. Selain paket makanan, 300 keluarga menerima selimut menjelang musim dingin. Kendala utama adalah antrean pemeriksaan di perbatasan yang membuat pengiriman tertunda lima hari. Rencana November adalah 1.500 paket makanan dan pengadaan tangki air untuk satu titik pengungsian. Dana yang terkumpul untuk rencana November baru mencapai 60 persen dari kebutuhan.")
h(doc, "Lampiran 2. Isi folder data-latihan")
tabel(doc, ["Berkas", "Isi"], [
    ["donatur-rekaan.csv", "120 donatur rekaan di Indonesia, Malaysia, dan Australia: tanggal donasi pertama dan terakhir, jumlah donasi 12 bulan, total USD, program terakhir, persetujuan dihubungi. Nama rekaan, tanpa kontak"],
    ["kampanye-iklan-rekaan.csv", "Kinerja iklan rekaan 8 minggu (14 September sampai 8 November 2026) per negara, program, dan platform: biaya, tayangan, klik, jumlah donasi, nilai donasi dalam USD"],
], lebar=[5, 11.8])

doc.save(os.path.join(ASET, "v1 Lembar Kerja Peserta.docx"))

# =====================================================================
# 3. Pre-test dan Post-test
# =====================================================================
SOAL = [
    ("Bagaimana model bahasa besar (LLM) seperti Claude menghasilkan jawaban?",
     ["Mencari jawaban di internet setiap kali ditanya", "Menebak kata berikutnya berdasarkan pola dari data yang dipelajari", "Menyalin jawaban yang ditulis manusia sebelumnya", "Menjalankan rumus yang ditulis programmer untuk tiap pertanyaan"], "B"),
    ("Apa yang dimaksud halusinasi AI?",
     ["AI menolak menjawab pertanyaan", "AI menjawab terlalu panjang", "AI memberi jawaban yang terdengar yakin tetapi salah atau dikarang", "AI menjawab dalam bahasa yang salah"], "C"),
    ("Mana yang tidak boleh dimasukkan ke AI sebelum ada kebijakan MFA?",
     ["Draf caption Instagram", "Nama dan nomor telepon donatur", "Ringkasan laporan yang sudah dipublikasikan", "Ide judul kampanye"], "B"),
    ("Apa fungsi Projects di Claude?",
     ["Menyimpan instruksi dan berkas pengetahuan yang dipakai berulang dalam satu ruang kerja", "Mengirim pesan otomatis ke donatur", "Membuat laporan keuangan", "Menghubungkan Claude ke Telegram"], "A"),
    ("Kalimat 'Kami tim marketing MyFundAction Australia, pembaca kami donatur Muslim usia 25 sampai 45' termasuk unsur prompt yang mana?",
     ["Tugas", "Format", "Konteks", "Contoh"], "C"),
    ("Mengapa bahan seperti laporan ditaruh di dalam tag seperti <data> ... </data>?",
     ["Agar AI menjawab lebih cepat", "Agar AI bisa membedakan bahan dari perintah", "Agar biaya lebih rendah", "Agar hasil memakai bahasa Inggris"], "B"),
    ("Apa beda utama AI Agent dengan chatbot?",
     ["Agent selalu memakai biaya lebih rendah", "Agent bisa merencanakan langkah, memakai alat, mengingat, dan bekerja terjadwal untuk mencapai tujuan", "Agent tidak membutuhkan model AI", "Agent hanya bisa dipakai programmer"], "B"),
    ("Di Hermes Agent, berkas apa yang berisi identitas dan aturan agen?",
     ["MEMORY.md", "config.yaml", "SOUL.md", "USER.md"], "C"),
    ("Perintah apa yang dipakai untuk menghubungkan Hermes ke Telegram?",
     ["hermes doctor", "hermes gateway setup", "hermes model", "hermes profile create"], "B"),
    ("Pengaturan mana yang paling aman untuk pemula?",
     ["Mode YOLO menyala agar agen tidak terus bertanya", "Bot Telegram bisa dipakai siapa saja agar tim mudah mencoba", "Persetujuan perintah aktif, hanya pengguna terdaftar, dan kunci API berbatas belanja", "Agen langsung mengirim pesan ke donatur tanpa diperiksa"], "C"),
]
TUGAS_PROMPT = "Tulis prompt untuk meminta AI menyusun pesan WhatsApp terima kasih kepada donatur program air bersih di Malaysia yang baru pertama kali berdonasi. Tulis seluruh prompt seperti yang akan Anda ketik ke Claude."

doc = dokumen("Pre-test dan Post-test", "Soal yang sama dipakai di awal dan di akhir pelatihan. Waktu 10 menit. Lingkari satu jawaban.")
tabel(doc, ["Nama", "Negara", "Pre-test atau post-test (lingkari)"], [["", "", "Pre-test   /   Post-test"]], lebar=[6.5, 4, 6.3])
h(doc, "Bagian A. Pilihan ganda (10 soal)")
for i, (q, ops, _) in enumerate(SOAL, 1):
    para(doc, f"{i}. {q}", bold=True, after=1)
    for huruf, o in zip("ABCD", ops):
        para(doc, f"     {huruf}. {o}", after=0)
    para(doc, "", after=2)
h(doc, "Bagian B. Tugas prompt")
para(doc, TUGAS_PROMPT)
kotak_isian(doc, "Prompt Anda:", 12)
para(doc, "Bagian B dinilai dengan rubrik 6 unsur (skor 0 sampai 12). Rubrik ada di Pustaka Prompt dan Standar Prompt MFA.", size=9.5, italic=True)
doc.save(os.path.join(ASET, "v1 Pre-test dan Post-test.docx"))

# =====================================================================
# 4. Kunci jawaban dan panduan penilaian (trainer)
# =====================================================================
doc = dokumen("Kunci Jawaban dan Panduan Penilaian", "Untuk trainer dan asisten. Jangan dibagikan ke peserta.")
h(doc, "1. Pilihan ganda")
tabel(doc, ["No", "Kunci", "Modul"], [[str(i), k, m] for i, ((_, _, k), m) in enumerate(zip(SOAL, ["M1", "M1", "M1", "M2", "M3", "M3", "M4", "M5", "M6", "M6"]), 1)], lebar=[2, 3, 3])
para(doc, "Skor bagian A: 1 poin per soal benar, maksimal 10.")
h(doc, "2. Tugas prompt (rubrik 6 unsur)")
para(doc, "Nilai tiap unsur 0, 1, atau 2 dengan rubrik. Dua penilai menilai prompt yang sama secara terpisah untuk 3 peserta pertama, lalu menyamakan cara menilai bila selisih lebih dari 2 poin.")
para(doc, "Contoh jawaban skor 12:", bold=True)
kode(doc, """<konteks>
Kami tim CRM MyFundAction Malaysia. Penerima pesan adalah donatur program air bersih
yang baru pertama kali berdonasi bulan ini.
</konteks>
<tugas>
Tulis pesan WhatsApp terima kasih untuk donatur ini.
</tugas>
<bahan>
{fakta program air bersih dari laporan terakhir: lokasi dan progres}
</bahan>
<aturan>
Bahasa Melayu, sapa dengan {nama_penderma}. Jangan menulis angka yang tidak ada di <bahan>.
Jangan meminta donasi lagi. Nada hangat dan sopan.
</aturan>
<contoh>
{satu pesan terima kasih yang pernah dinilai baik}
</contoh>
<format>
Paling banyak 60 kata, 2 versi.
</format>""")
h(doc, "3. Kunci Topik 7.1: segmen donatur")
para(doc, "Dihitung dari donatur-rekaan.csv dengan tanggal acuan 16 November 2026 dan urutan pemeriksaan Baru, Tidak aktif, Rutin, Lainnya.")
urut = ["Baru", "Rutin", "Tidak aktif", "Lainnya"]
tabel(doc, ["Segmen", "Jumlah donatur", "Yang setuju dihubungi"],
      [[s, str(KUNCI["segmen"].get(s, 0)), str(KUNCI["segmen_setuju"].get(s, 0))] for s in urut] +
      [["Total", str(sum(KUNCI["segmen"].values())), str(sum(KUNCI["segmen_setuju"].values()))]], lebar=[5, 5, 5])
para(doc, "Hal yang diperiksa: draf pesan tidak ditujukan ke donatur yang tidak setuju dihubungi, dan tidak memakai angka di luar bahan.")
h(doc, "4. Kunci Topik 7.3: kampanye 8 minggu")
para(doc, "Dihitung dari kampanye-iklan-rekaan.csv. Biaya per donasi = total biaya dibagi jumlah donasi. Nilai per 1 USD = total nilai donasi dibagi total biaya. CTR = klik dibagi tayangan.")
rows = [[t["negara"], t["program"], f"{t['biaya']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), str(t["donasi"]),
         f"{t['cpd']:.2f}".replace(".", ","), f"{t['ctr']:.2f}".replace(".", ",") + "%", f"{t['roas']:.2f}".replace(".", ",")] for t in KUNCI["kampanye"]]
tabel(doc, ["Negara", "Program", "Biaya USD", "Donasi", "Biaya per donasi", "CTR", "Nilai per 1 USD"], rows, lebar=[2.6, 3.6, 2.4, 1.8, 2.3, 1.8, 2.3], size=9)
terendah = min(KUNCI["kampanye"], key=lambda t: t["cpd"])
tertinggi = max(KUNCI["kampanye"], key=lambda t: t["roas"])
koma = lambda x: f"{x:.2f}".replace(".", ",")
para(doc, f"Jawaban: biaya per donasi terendah ada di {terendah['negara']}, program {terendah['program']} (USD {koma(terendah['cpd'])}). Nilai donasi per 1 USD iklan tertinggi ada di {tertinggi['negara']}, program {tertinggi['program']} (USD {koma(tertinggi['roas'])}).")
para(doc, "Poin diskusi: jawaban berbeda karena ukuran berbeda. Donasi di Australia lebih mahal didapat tetapi nilainya jauh lebih besar per transaksi. Inilah alasan agen diminta menuliskan rumus dan ukuran yang dipakai, dan manusia memilih ukuran yang sesuai tujuan kampanye. Data ini rekaan, polanya dibuat searah dengan informasi di rapat bahwa program masjid paling banyak direspons di Australia.")

doc.save(os.path.join(ASET, "v1 Kunci Jawaban dan Panduan Penilaian - untuk Trainer.docx"))
print("aset docx tersimpan di", os.path.normpath(ASET))
