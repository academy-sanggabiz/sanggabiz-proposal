# Gambar isyarat contoh (dari pengguna, 3 November 2026)

20 gambar di folder ini dipotong dari gambar kartu yang dikirim pengguna di chat: `../../sumber/Kartu isyarat dengan gambar dari pengguna - 3 November 2026.webp` (1024 x 707 piksel). Tata letak gambar itu sama persis dengan Kartu Saku Isyarat v2 buatan kami, jadi besar kemungkinan gambarnya dibuat dengan alat AI pembuat gambar. Sumber pastinya belum dikonfirmasi.

Status: **contoh, belum diperiksa pengguna Tuli.** Gerakan di gambar belum tentu isyarat BISINDO yang benar. Beberapa gambar hanya memperagakan benda (Formulir memegang kertas, Tanda tangan memegang pena), dan Ribu serta Juta hampir sama. Karena itu setiap foto di kartu v4 diberi label "contoh" dan kaki kartu menyebut statusnya.

Cara dibuat: `../potong_foto_contoh.py`. Tulisan "FOTO ISYARAT" dan nomor yang menempel di gambar dihapus, lalu gambar diperbesar 3 kali. Gambar asli kecil (sekitar 180 x 77 piksel per kotak), jadi hasil cetak bisa agak lembut.

Dipakai oleh: `../build_kartu_v4.py` (PDF dan PPTX). Tidak dipakai di proposal v2.

Bila foto asli dari co-trainer Tuli sudah ada, simpan di `../foto-isyarat/` (lihat README di sana). Folder ini tidak perlu diubah.
