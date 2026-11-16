"""Panduan Setup Hermes Agent untuk peserta non-programmer (Modul 6)."""
import os

from docx_lib import butir, dokumen, h, kode, para, pindah_halaman, tabel

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "aset", "v1 Panduan Setup Hermes untuk Non-Programmer.docx")

doc = dokumen(
    "Panduan Setup Hermes Agent",
    "Untuk peserta non-programmer, dipakai di Modul 6 dan klinik pendampingan. Versi 1, 16 November 2026.",
)
para(doc, "Hasil akhir panduan ini: satu agen Hermes milik Anda yang menjawab lewat Telegram, dengan pengaturan aman. Ikuti langkah sesuai urutan. Bila tertahan lebih dari 5 menit di satu langkah, angkat tangan atau tulis di grup klinik.")
para(doc, "Catatan untuk trainer: Hermes Agent merilis versi baru hampir tiap minggu. Perintah di panduan ini diambil dari dokumentasi resmi dan panduan publik per November 2026. Cocokkan dengan hermes-agent.nousresearch.com sehari sebelum pelatihan. [ISI TIM: tanggal dan versi Hermes saat dicocokkan]", size=9.5, italic=True)

h(doc, "1. Istilah yang dipakai")
tabel(doc, ["Istilah", "Artinya"], [
    ["Terminal", "Jendela tempat mengetik perintah. Di macOS namanya Terminal. Di Windows kita memakai Ubuntu (WSL2)"],
    ["Perintah", "Satu baris teks yang ditempel ke terminal lalu dijalankan dengan Enter. Di panduan ini ditulis dengan huruf seperti `hermes setup`"],
    ["Model", "Otak AI yang dipakai agen, misalnya Claude. Hermes bisa memakai banyak model"],
    ["Kunci API", "Kata sandi panjang untuk memakai model dan membayar pemakaiannya. Dibagikan trainer, punya batas belanja, dan tidak boleh dibagikan ke orang lain"],
    ["SOUL.md", "Berkas berisi identitas dan aturan agen: siapa dia, untuk siapa dia bekerja, apa yang dilarang"],
    ["Profil", "Satu profil satu agen. Agen CRM, Agen Iklan, dan Agen Analis masing-masing satu profil"],
    ["Gateway", "Penghubung agen dengan aplikasi chat seperti Telegram"],
], lebar=[3.5, 13])

h(doc, "2. Cek perangkat (dikerjakan H-2 bersama tim IT)")
tabel(doc, ["Yang dicek", "Cara cek", "Harus"], [
    ["Sistem operasi", "macOS: menu Apple, About This Mac. Windows: Settings, System, About", "macOS versi terbaru yang masih didukung, atau Windows 10 versi 2004 ke atas atau Windows 11"],
    ["Hak admin", "Coba pasang aplikasi. Bila diminta kata sandi admin yang tidak Anda punya, minta bantuan IT", "Punya hak admin, atau IT hadir saat instalasi"],
    ["Ruang disk", "macOS: About This Mac, Storage. Windows: File Explorer, This PC", "Kosong minimal 5 GB"],
    ["Virtualisasi (Windows)", "Task Manager, tab Performance, CPU, baris Virtualization", "Enabled. Bila Disabled, IT menyalakannya di BIOS"],
    ["Telegram", "Aplikasi Telegram di ponsel sudah masuk dengan nomor Anda", "Bisa mengirim pesan"],
    ["Jaringan", "Buka github.com dan openrouter.ai di peramban", "Keduanya terbuka. Bila diblokir jaringan kantor, IT membuka akses atau peserta memakai hotspot"],
], lebar=[3.2, 7.3, 6])

h(doc, "3. Instalasi di macOS")
butir(doc, [
    "Buka Terminal: tekan Command dan Spasi, ketik Terminal, tekan Enter.",
    "Cek Git dengan perintah di bawah. Bila muncul nomor versi, lanjut ke langkah 3. Bila muncul jendela untuk memasang Command Line Tools, klik Install dan tunggu selesai.",
], nomor=True)
kode(doc, "git --version")
butir(doc, ["Tempel perintah pemasang Hermes, lalu tekan Enter. Tunggu sampai selesai, biasanya beberapa menit."], nomor=True)
kode(doc, "curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash")
butir(doc, ["Tutup Terminal, buka lagi, lalu cek dengan perintah di bawah. Bila muncul daftar perintah Hermes, instalasi berhasil."], nomor=True)
kode(doc, "hermes --help")

h(doc, "4. Instalasi di Windows lewat WSL2")
para(doc, "Kita memakai WSL2 (Linux di dalam Windows) karena jalur ini paling teruji. Pemasang khusus Windows sudah ada tetapi masih tahap awal, jadi tidak dipakai di pelatihan.")
butir(doc, [
    "Klik Start, ketik PowerShell, klik kanan, pilih Run as administrator.",
    "Tempel perintah di bawah, tekan Enter, lalu restart laptop bila diminta.",
], nomor=True)
kode(doc, "wsl --install -d Ubuntu")
butir(doc, [
    "Setelah restart, jendela Ubuntu terbuka sendiri. Bila tidak, klik Start dan ketik Ubuntu. Buat nama pengguna (tanpa huruf kapital dan tanpa spasi) dan kata sandi. Saat mengetik kata sandi, layar tidak menampilkan apa pun. Itu normal.",
    "Pasang Git dan curl. Masukkan kata sandi Ubuntu bila diminta.",
], nomor=True)
kode(doc, "sudo apt update && sudo apt install -y git curl")
butir(doc, ["Tempel perintah pemasang Hermes. Di Ubuntu, tempel dengan klik kanan atau Ctrl+Shift+V."], nomor=True)
kode(doc, "curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash")
butir(doc, ["Tutup jendela Ubuntu, buka lagi, lalu cek instalasi."], nomor=True)
kode(doc, "hermes --help")

h(doc, "5. Setup pertama dan percakapan pertama")
butir(doc, [
    "Jalankan wizard setup.",
], nomor=True)
kode(doc, "hermes setup")
butir(doc, [
    "Pilih penyedia model yang diumumkan trainer: OpenRouter atau Anthropic. [ISI TIM: penyedia yang dipakai saat pelatihan]",
    "Tempel kunci API latihan dari trainer. Kunci ini punya batas belanja. Jangan memotret atau mengirimnya ke grup.",
    "Pilih model yang diumumkan trainer. Hermes hanya menerima model dengan konteks minimal 64.000 token, jadi model dengan konteks di bawah itu akan ditolak. [ISI TIM: nama model]",
    "Mulai percakapan dengan mengetik hermes, lalu tulis: Halo, siapa kamu dan apa yang bisa kamu kerjakan?",
], nomor=True)
kode(doc, "hermes")
para(doc, "Di dalam percakapan, ketik `/help` untuk melihat perintah yang tersedia. Untuk keluar, tekan Ctrl+C.")
butir(doc, ["Keluar dari percakapan, lalu jalankan pemeriksaan. Semua baris yang ditandai bermasalah dicatat dan ditunjukkan ke trainer."], nomor=True)
kode(doc, "hermes doctor")

h(doc, "6. Mengisi identitas agen (SOUL.md)")
butir(doc, [
    "Pilih templat sesuai calon agen Anda di Modul 4: SOUL-agen-crm.md, SOUL-agen-iklan.md, atau SOUL-agen-analis.md (folder aset/hermes-templat).",
    "Isi bagian bertanda kurung siku [ ] di templat. Jangan menghapus bagian Aturan.",
    "Buka berkas SOUL.md milik agen Anda dengan perintah di bawah, hapus isinya, tempel templat yang sudah diisi, lalu simpan.",
], nomor=True)
tabel(doc, ["Laptop", "Perintah membuka SOUL.md", "Cara menyimpan"], [
    ["macOS", "`open -e ~/.hermes/SOUL.md`", "Command+S, lalu tutup jendela"],
    ["Windows (Ubuntu)", "`nano ~/.hermes/SOUL.md`", "Ctrl+O, Enter, lalu Ctrl+X untuk keluar"],
], lebar=[3.5, 7.5, 5.5])
butir(doc, ["Mulai percakapan baru dengan hermes dan tanyakan: Apa peranmu, dan apa yang tidak boleh kamu lakukan? Jawaban harus sesuai isi SOUL.md."], nomor=True)

h(doc, "7. Menghubungkan agen ke Telegram")
butir(doc, [
    "Di Telegram, cari @BotFather, kirim /newbot. Beri nama, misalnya MFA Latihan Rina. Nama pengguna bot harus berakhiran bot, misalnya mfa_latihan_rina_bot.",
    "BotFather mengirim token. Salin token itu. Token sama rahasianya dengan kunci API.",
    "Cari @userinfobot di Telegram dan kirim pesan apa saja. Catat angka ID Anda. ID ini dipakai agar hanya Anda yang bisa memerintah agen.",
    "Jalankan setup gateway, pilih Telegram, tempel token, dan isi ID Anda saat ditanya pengguna yang diizinkan.",
], nomor=True)
kode(doc, "hermes gateway setup")
butir(doc, ["Nyalakan gateway, lalu kirim pesan ke bot Anda di Telegram. Agen menjawab di Telegram."], nomor=True)
kode(doc, "hermes gateway start")
para(doc, "Gateway berhenti bila terminal ditutup atau laptop dimatikan. Untuk agen yang menyala terus, Hermes dipasang di server. Itu dibahas di klinik pendampingan.", size=9.5, italic=True)

h(doc, "8. Daftar periksa keamanan")
para(doc, "Kelima butir harus terpenuhi sebelum agen dipakai. Trainer memeriksa bersama Anda di akhir Modul 6.")
tabel(doc, ["No", "Butir", "Cara memastikan", "Ya"], [
    ["1", "Persetujuan perintah aktif", "Saat agen ingin menjalankan perintah berisiko, ia bertanya dulu. Jangan pernah memakai `hermes --yolo` atau `/yolo`. Trainer memeriksa pengaturan persetujuan di `~/.hermes/config.yaml` tidak bernilai off", ""],
    ["2", "Hanya Anda yang bisa memerintah bot", "Minta rekan mengirim pesan ke bot Anda. Bot tidak boleh menjalankan permintaannya", ""],
    ["3", "Kunci API berbatas belanja dan tidak tersebar", "Kunci dari trainer. Tidak ada di foto, chat, atau dokumen bersama", ""],
    ["4", "Hanya data rekaan", "Berkas yang diberikan ke agen hanya dari folder data-latihan. Data donatur asli menunggu kebijakan MFA", ""],
    ["5", "Manusia memeriksa sebelum pesan keluar", "SOUL.md memuat aturan: agen hanya membuat draf pesan untuk donatur atau publik, tidak mengirimnya", ""],
], lebar=[1, 4.5, 9.5, 1.5])
para(doc, "Saat agen meminta persetujuan: baca perintahnya. Bila Anda tidak paham artinya, atau perintah itu di luar tugas yang Anda minta, tolak dan tanyakan ke trainer.")

h(doc, "9. Agen kedua dan seterusnya (profil)")
para(doc, "Setiap agen dibuat sebagai profil sendiri dengan SOUL.md, memori, dan bot Telegram sendiri. Contoh untuk Agen Iklan:")
kode(doc, "hermes profile create iklan\nhermes -p iklan setup\nhermes -p iklan gateway setup\nhermes -p iklan gateway start")
para(doc, "Satu token bot Telegram hanya untuk satu profil. Untuk tiga agen di satu grup Telegram, buat tiga bot di BotFather.")

h(doc, "10. Laporan terjadwal")
para(doc, "Jadwal dibuat dengan meminta langsung ke agen lewat percakapan, misalnya:")
kode(doc, "Setiap Senin pukul 09.00 WIB, baca berkas kampanye-iklan-rekaan.csv,\nhitung biaya per donasi per negara dan program untuk minggu terakhir,\nlalu kirim ringkasan 5 baris ke Telegram ini.")
para(doc, "Daftar jadwal bisa dilihat dan diatur dengan perintah `hermes cron`. Ketik `hermes cron --help` untuk melihat pilihannya.")

h(doc, "11. Masalah yang sering muncul")
tabel(doc, ["Gejala", "Penyebab yang mungkin", "Yang dilakukan"], [
    ["command not found: hermes", "Terminal belum memuat pengaturan baru", "Tutup dan buka lagi terminal. Bila tetap, jalankan `source ~/.zshrc` (macOS) atau `source ~/.bashrc` (Ubuntu)"],
    ["wsl --install gagal atau Ubuntu tidak mau jalan", "Virtualisasi mati atau Windows belum diperbarui", "IT menyalakan virtualisasi di BIOS dan menjalankan Windows Update"],
    ["Model ditolak saat mulai", "Konteks model di bawah 64.000 token", "Pilih model lain dengan `hermes model`"],
    ["Galat 401 atau kunci tidak valid", "Kunci API tidak lengkap atau ada spasi", "Salin ulang kunci dari trainer, jalankan `hermes model`"],
    ["Galat 402 atau saldo habis", "Batas belanja latihan tercapai", "Lapor trainer"],
    ["Bot Telegram tidak menjawab", "Gateway belum dinyalakan, token salah, atau ID Anda tidak terdaftar", "Jalankan `hermes gateway start`. Bila tetap, ulangi `hermes gateway setup`"],
    ["Kata sandi tidak tampil saat diketik", "Memang tidak ditampilkan", "Ketik seperti biasa, lalu Enter"],
    ["Unduhan sangat lambat atau gagal", "Jaringan kantor membatasi akses", "Pakai hotspot atau minta IT membuka akses"],
], lebar=[4.2, 5.3, 7])

h(doc, "12. Ringkasan perintah")
tabel(doc, ["Perintah", "Gunanya"], [
    ["`hermes setup`", "Wizard pertama: penyedia, kunci API, model"],
    ["`hermes`", "Mulai percakapan dengan agen"],
    ["`hermes model`", "Ganti penyedia atau model, masukkan ulang kunci"],
    ["`hermes doctor`", "Memeriksa masalah instalasi"],
    ["`hermes gateway setup`", "Menghubungkan agen ke Telegram atau aplikasi chat lain"],
    ["`hermes gateway start`", "Menyalakan gateway"],
    ["`hermes profile create <nama>`", "Membuat agen baru"],
    ["`hermes -p <nama> ...`", "Menjalankan perintah untuk profil tertentu"],
    ["`hermes cron --help`", "Melihat cara mengatur jadwal"],
], lebar=[6, 10.5])

h(doc, "13. Biaya setelah pelatihan")
para(doc, "Hermes gratis dan sumber terbuka. Yang dibayar adalah pemakaian model. Panduan publik memperkirakan sekitar USD 5 sampai 8 per bulan untuk satu agen dengan pemakaian ringan lewat OpenRouter, dan USD 25 sampai 40 untuk pemakaian berat. Angka ini dari panduan vendor dan belum kami uji. Pasang batas belanja di akun penyedia model sebelum agen dipakai rutin.")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print("tersimpan:", os.path.normpath(OUT))
