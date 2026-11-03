# ATURAN PROPOSAL SANGGABIZ

Berlaku untuk semua proposal Sanggabiz. Dipakai bersama `ATURAN-PENULISAN.md` (cara menulis) dan `FORMAT-STANDAR-PROPOSAL.md` (bentuk halaman). Aturan di sini ditambah setiap ada arahan baru dari tim.

## 0. Tujuan proposal: mudah dipahami dan meyakinkan
Arahan tim, 3 November 2026, saat merevisi proposal pelatihan CS Aqiqah Al Kautsar. Kutipan chat, tidak diubah:

> aku rasa proposalnya terlalu detail hal teknis, aku pengen proposal tu lebih enak di baca dan meyaknkan pembaca, gak usah semuanya dibaut assets ya kayak pre port test, untuk porosal contoh aja satu kayak kartu saku isyraat seperti apa. udah gitu aja. karena itu sebagai contoh, tap kartu isyaratnya buat yang bagus banget ya. nah bagian lain kalau bagan alat dan media gak usah di gabungkan dengan slde dan asset sebutkan aja general ya, alatnya apa dan media apa. kalau kayak penutup mata dll tu mash masuk. terus hal teknis academic gak usah di sebutin. masukkan hal ini ke pengetahuan mu ya nanti. masukkan ke gihtub juga. jadi proposal tu objektifnya bukan nulis secara teknis semua hal. tapi nulis mudah di pahami dan meyaknkan orang ketika baca proposalnya. dan ketika orang awam baca silabus juga paham akan sepert apa dan apa kegiatannay

Aturan yang diturunkan (tafsiran Claude, koreksi bila keliru). Bagian ini mendahului bagian lain di berkas ini. Bila ada yang bertentangan, ikuti bagian ini.
1. **Tujuan proposal adalah dipahami dan meyakinkan pembaca**, bukan mencatat semua hal teknis. Tulis untuk pemilik usaha atau pejabat yang memutuskan, bukan untuk sesama penyusun pelatihan.
2. **Silabus harus bisa dibayangkan orang awam.** Setiap sesi cukup memuat: yang dipelajari, kegiatannya (urutan nyata di ruang pelatihan, siapa melakukan apa), alat dan media, dan hasil. Tulis kegiatan seperti menceritakan apa yang terjadi di ruangan.
3. **Istilah akademik tidak disebut di dokumen klien.** Nama kerangka seperti ADDIE, Andragogi, Taksonomi Bloom, Kirkpatrick, backward design, dan istilah seperti "tujuan pembelajaran", "level 1 sampai 4", atau "indikator capaian" tidak dipakai. Kerangka tetap dipakai saat menyusun program, tetapi hasilnya ditulis dengan bahasa sehari-hari. Contoh: evaluasi empat level ditulis sebagai tabel "Kapan, Yang kami lihat, Tanda berhasil".
4. **Istilah kerja diganti kata sehari-hari** bila ada padanannya. Contoh: huddle menjadi rapat harian 10 menit, lead tracker menjadi catatan calon pelanggan, scorecard menjadi rekap mingguan, role play menjadi bermain peran, coach menjadi pendamping. Istilah yang dipakai klien sendiri tetap boleh (closing, follow-up, CS).
5. **Cukup satu aset contoh di proposal, dan dibuat bagus.** Pilih satu alat yang paling mewakili program (contoh: kartu saku untuk peserta) dan tampilkan dalam desain jadi. Aset lain (pre-test, post-test, lembar kerja, templat, rubrik, lembar cek) tidak dibuat dan tidak dilampirkan. Cukup disebut dalam kalimat bila perlu, misalnya "kuis singkat di awal dan akhir sesi".
6. **Alat dan media ditulis umum.** Sebut benda yang dipakai di ruangan: penutup mata, kartu, kertas plano, spidol, stiker, pengatur waktu, ponsel peserta. Jangan mencampur dengan slide atau nama berkas aset, dan jangan merujuk ke lampiran.
7. **Meyakinkan lewat gambaran perubahan.** Tunjukkan kondisi sekarang dan kondisi yang dituju, cara mengukur hasil dengan bahasa sederhana, dan batas yang jujur. Hindari tabel teknis yang panjang.
8. Panjang yang wajar untuk pelatihan satu hari dengan pendampingan: sekitar 10 sampai 12 halaman termasuk sampul.

Contoh penerapan: `aqiqah-alkautsar/proposal/v1 Proposal Training CS Closing - Aqiqah Al Kautsar.docx` dan kartu saku di `aqiqah-alkautsar/aset/`.

## 1. Kerangka kerja dan metode
1. Pilih metode yang umum dipakai di dunia pelatihan dan sesuai dengan masalah yang mau diselesaikan. Jelaskan alasan pemilihannya dalam satu atau dua kalimat.
2. Jangan memakai kerangka `Define, Design, Deliver, Discuss` (4D) di proposal mana pun. Proposal lama yang masih memakainya diganti saat disentuh berikutnya.
3. Daftar metode yang sudah dikaji dan boleh dipilih:

| Metode | Dipakai untuk | Cocok bila |
|---|---|---|
| ADDIE (Analysis, Design, Development, Implementation, Evaluation) | Alur penyelenggaraan program dari analisis sampai evaluasi | Hampir semua pelatihan, terutama yang punya modul dan evaluasi |
| Andragogi (Knowles) | Cara belajar peserta dewasa: dari pengalaman sendiri, berorientasi masalah, pengajar sebagai fasilitator | Peserta guru, pegawai, pelaku usaha |
| Taksonomi Bloom revisi (Anderson dan Krathwohl) | Merumuskan tujuan dan ukuran capaian dengan kata kerja: mengingat, memahami, menerapkan, menganalisis, mengevaluasi, mencipta | Tujuan pembelajaran perlu terukur |
| Kirkpatrick (4 level: reaksi, pembelajaran, perilaku, dampak) | Evaluasi pelatihan | Klien meminta bukti hasil |
| Backward design (lihat bagian 2) | Menyusun materi dari kebutuhan peserta | Ada waktu untuk pemetaan awal |
| Siklus PDCA atau CQI | Pendampingan berulang selama beberapa bulan | Program pendampingan panjang |

4. Setiap proposal menyebut metode yang dipakai dan di bagian mana metode itu muncul (misalnya ADDIE pada alur program, Bloom pada rumusan tujuan, Kirkpatrick pada evaluasi).
   (Direvisi 3 November 2026, lihat bagian 0: nama metode tidak lagi ditulis di dokumen klien. Metode cukup dicatat di catatan tim proyek.)

## 2. Backward design (preferensi Nauval dan rekan kantor)
Nauval dan beberapa rekan kantor menyukai pendekatan ini. Alurnya:
1. Petakan kondisi awal peserta: apa yang sudah bisa dan apa yang masih perlu diperkuat (asesmen awal, formulir, wawancara singkat, pre-test).
2. Tetapkan hasil akhir yang diharapkan dari peserta.
3. Tentukan bukti keberhasilan (tes, produk, observasi).
4. Rancang materi dan aktivitas yang menjembatani kondisi awal ke hasil akhir. Materi mengikuti temuan pemetaan, bukan sebaliknya.
5. Laksanakan, lalu evaluasi dan perbaiki.

Cara memakainya: sediakan alurnya di proposal bila waktu program memungkinkan pemetaan awal terpisah. Pada proposal SLB Kaltim alur ini tidak dipakai karena acara setengah hari dan pemetaan cukup lewat formulir pendaftaran dan pre-test.

## 3. Silabus
Silabus ditulis per sesi dan per topik, cukup rinci supaya semua pembaca memahaminya dengan cara yang sama.
1. Ringkasan di awal: sesi, topik, durasi, hasil.
2. Tiap sesi memuat empat baris: **yang dipelajari**, **kegiatannya** (urutan nyata, siapa melakukan apa), **alat dan media** (benda yang dipakai, ditulis umum), dan **hasil**. Pecahan per topik dengan menit, kata kerja Bloom, dan ukuran keberhasilan per topik disimpan di catatan tim bila diperlukan, tidak di dokumen klien.
   (Direvisi 3 November 2026, lihat bagian 0. Versi sebelumnya meminta tujuan pembelajaran, outline, aktivitas per menit, output, dan ukuran keberhasilan untuk setiap topik.)
3. Aktivitas menggambarkan keadaan nyata di ruang pelatihan, bukan istilah umum.
4. Output tiap topik ditulis jelas. Semua output dikumpulkan di bagian "Hasil yang dibawa pulang" dengan keterangan dihasilkan di topik mana.
5. Tidak ada istilah yang bisa dibaca dua arti. Bila memakai istilah teknis, jelaskan sekali di tempat pertama muncul.

## 4. Anggaran untuk klien
0. Semua angka mengikuti `STANDAR-HARGA.md` (rentang harga, rumus keuntungan dan pajak, harga yang tidak diambil). Butir di bawah mengatur cara menampilkannya ke klien.
1. Tampilkan satu opsi, yaitu paket paling ekonomis yang tetap memenuhi tujuan dan hasil program. Opsi lain hanya bila klien memintanya.
2. Dokumen klien memuat satu baris Fee sebesar 10 persen dari biaya langsung (arahan Pak Priyo, 17 Oktober 2026, lihat `ARAHAN-PRIYO.md`). Tidak ada baris cadangan atau margin lain. Keuntungan tidak disembunyikan di harga perabot atau barang lain.
3. Setiap komponen ditulis per baris dengan volume dan harga satuan, tidak digabung ke satu item besar. Biaya kecil yang belum sempat dirinci ditutup dengan pembulatan harga satuan dan kelebihan porsi konsumsi, dengan harga tetap di dalam rentang `STANDAR-HARGA.md`.
4. Pajak: tulis "sudah termasuk pajak" atau tampilkan baris PPN bila klien meminta. Rincian hitungan internal disimpan di catatan tim, bukan di dokumen klien.
(Butir 2 sampai 4 direvisi pada 17 Oktober 2026. Versi sebelumnya melarang baris biaya manajemen dan menyerap fee ke komponen produk.)
5. Honor pemateri dan harga tempat memakai acuan pasar atau standar biaya pemerintah yang dapat ditunjukkan. Pemateri lokal bila ada, untuk meniadakan biaya mobilisasi.
6. Jumlah pengajar sesuai kebutuhan nyata. Tidak menambah orang agar terlihat besar.

## 4a. Menyusun proposal dari proses bisnis
Usul Pak Priyo Pamungkas (Sanggabiz), diteruskan Muchson pada 17 Oktober 2026 saat membahas anggaran SLB Kaltim. Berlaku untuk proposal berikutnya. Kutipan chat, tidak diubah:

> trus untuk teknisnya :
> cb kamu break down dulu bisnis prosesnya. nah penganggaran mengikuti itu proses bisnisnya
>
> kalo gw break down :
> 1. Scrapping data SLB/Pengajar
> 2. Komunikasi dan Proses mengundang SLB/Pengajar
> 3. Pembuatan Modul
> 4. Teknis Acara
> 5. Monev (bisa bentuk survey atau monitoring implementasi)
> 6. Laporan

Cara memakainya (tafsiran Claude, koreksi bila keliru):
1. Ini cara menyusun proposal secara umum, bukan aturan pengelompokan tabel anggaran. Mulai dengan memecah proses bisnis program menjadi tahap. Isi proposal (rundown, silabus, tim, anggaran) lalu mengikuti tahap itu.
2. Enam tahap di atas adalah contoh dari program pelatihan guru SLB Kaltim. Proposal lain menulis tahapnya sendiri sesuai programnya, dengan urutan yang mengikuti alur kerja nyata.
3. Anggaran mengikuti proses. Setiap baris biaya bisa ditelusuri ke satu tahap, dan setiap tahap yang punya pekerjaan punya biaya, atau ditulis diserap di baris mana. Bentuk tabel anggaran tidak harus sama dengan tahap. Bila klien punya templat sendiri, ikuti templat klien.
4. Biaya yang melintasi tahap, misalnya manajer proyek, dicatat sebagai biaya lintas tahap atau di tahap yang paling banyak memakainya.
5. Harga tiap baris tetap mengikuti `STANDAR-HARGA.md`.
6. Monev adalah singkatan monitoring dan evaluasi. Monitoring memantau jalannya program, evaluasi menilai hasilnya.

Pekerjaan dan biaya yang lazim per tahap (tafsiran Claude):
| Tahap | Pekerjaan dan biaya |
|---|---|
| 1. Pendataan SLB dan pengajar | Daftar sekolah dan guru, kontak, kuota per sekolah |
| 2. Komunikasi dan undangan | Kunjungan sekolah, surat undangan, formulir pendaftaran, konfirmasi, pengingat |
| 3. Pembuatan modul | Modul, templat, instrumen tes, bahan ajar |
| 4. Teknis acara | Tempat, perabot, konsumsi, perlengkapan, pemateri, MC, fasilitator, dokumentasi, transport peserta |
| 5. Monev | Survei kepuasan, pre-test dan post-test, pemantauan penerapan di kelas |
| 6. Laporan | Laporan akhir |

## 5. Tempat pelaksanaan
1. Tulis nama hotel atau gedung, alamat, nama ruang lengkap, ukuran ruang (panjang kali lebar atau meter persegi), kapasitas per susunan, dan harga acuan.
2. Pilih tempat berdasarkan pencarian terbaru, di lokasi yang mudah dijangkau peserta.
3. Cantumkan foto ruang bila tersedia, atau skema susunan ruang. Foto dari situs pihak lain mencantumkan sumbernya.
4. Satu tempat saja di dokumen klien. Pilihan cadangan disimpan di catatan tim.
5. Tulis akses bagi peserta penyandang disabilitas bila pesertanya guru dan tenaga pendidik.

## 6. Bahasa proposal
1. Formal dan positif. Hindari kata bernada negatif atau meremehkan untuk menyebut program, tempat, atau peserta: sempit, kecil, murah, mepet, lemah, buruk, minim.
2. Gantinya: ringkas, terfokus, efisien, ekonomis, area pengembangan, kebutuhan penguatan.
3. Uraian masalah tetap memakai data dan ditulis faktual, tanpa menilai pihak mana pun.

## 7. Gambar dan keterangan gambar
1. Keterangan gambar diletakkan di tengah di bawah gambar, huruf tegak (tidak miring), ukuran sedikit lebih kecil dari teks isi.
2. Setiap grafik menyebut sumber data dan tahunnya di dalam gambar.
3. Grafik hanya dibuat dari data yang ada. Tidak ada angka rekaan.

## 8. Dokumen kerja
1. Bagian yang harus diisi tim ditandai `[ISI TIM: ...]` dengan stabilo kuning.
2. Setiap proposal punya catatan tim: daftar isian, daftar cek klaim, dan hitungan internal anggaran.
3. Proposal yang direvisi diberi nomor versi pada nama file (misalnya `v2 Proposal ...`).
4. Versi lama tidak pernah dihapus. Saat membuat v2, v3, dan seterusnya, file versi sebelumnya tetap disimpan di folder yang sama sebagai arsip. Penghapusan hanya atas permintaan tim.
5. Bila skrip pembuat dokumen diperbarui, simpan salinan skrip versi lama (misalnya `build_proposal_v1.js`) supaya versi lama tetap bisa dibuat ulang.
