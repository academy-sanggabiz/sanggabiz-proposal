"""Templat prompt Standar Prompt MFA, dua bahasa. Dipakai pustaka prompt dan lembar kerja."""

GLOSARIUM = [
    ("Program Palestina", "Palestine programme", "Program Palestin"),
    ("Pembangunan masjid", "Mosque construction", "Pembinaan masjid"),
    ("Air bersih (sumur, sarana air)", "Clean water (wells, water facilities)", "Air bersih (telaga, kemudahan air)"),
    ("Donatur", "Donor", "Penderma"),
    ("Relawan", "Volunteer", "Sukarelawan"),
    ("Penerima manfaat", "Beneficiary", "Penerima manfaat"),
    ("Sedekah", "Sadaqah", "Sedekah"),
    ("Wakaf", "Waqf", "Wakaf"),
    ("Laporan penyaluran", "Distribution report", "Laporan penyaluran"),
    ("Donasi rutin bulanan", "Monthly regular giving", "Sumbangan bulanan tetap"),
]

ETIKA = [
    "Tidak menulis angka dampak, jumlah penerima manfaat, atau progres pembangunan yang tidak ada di bahan.",
    "Tidak membuat desakan palsu, misalnya 'tinggal 2 jam lagi' bila tidak benar.",
    "Menyebut penerima manfaat dengan hormat. Tidak memakai kalimat yang mengeksploitasi penderitaan.",
    "Tidak memasukkan nama, nomor telepon, alamat, atau surel donatur asli ke AI sebelum ada kebijakan MFA.",
    "Hasil AI adalah draf. Pesan untuk donatur dan publik diperiksa orang sebelum dikirim.",
]

# Tiap templat: kode, judul, dipakai_untuk, id, en
TEMPLAT = [
    {
        "kode": "T1",
        "judul": "Ringkasan laporan program untuk donatur",
        "untuk": "CRM, marketing",
        "id": """<konteks>
Kami tim {tim} MyFundAction {negara}. Pembaca ringkasan ini adalah donatur program {nama_program} yang ingin tahu ke mana dana mereka disalurkan.
</konteks>
<tugas>
Ringkas laporan di <laporan> menjadi 5 poin untuk donatur.
</tugas>
<laporan>
{tempel isi laporan di sini}
</laporan>
<aturan>
Pakai hanya fakta dan angka yang ada di <laporan>. Bila suatu hal tidak ada, jangan ditulis.
Nada hangat dan sopan. Bahasa {bahasa}.
</aturan>
<format>
5 poin, masing-masing paling banyak 25 kata. Tutup dengan satu kalimat terima kasih.
</format>""",
        "en": """<context>
We are the MyFundAction {country} {team} team. The readers are donors of the {programme} programme who want to know where their money went.
</context>
<task>
Summarise the report in <report> into 5 points for donors.
</task>
<report>
{paste the report here}
</report>
<rules>
Use only facts and figures that appear in <report>. If something is not there, leave it out.
Warm and respectful tone. Language: {language}.
</rules>
<format>
5 points, each no longer than 25 words. End with one thank-you sentence.
</format>""",
    },
    {
        "kode": "T2",
        "judul": "Pesan terima kasih per segmen donatur",
        "untuk": "CRM",
        "id": """<konteks>
Kami tim CRM MyFundAction {negara}. Segmen donatur: {segmen}, misalnya donatur baru dalam 90 hari terakhir.
</konteks>
<tugas>
Tulis pesan WhatsApp terima kasih untuk segmen ini setelah mereka berdonasi ke program {nama_program}.
</tugas>
<bahan>
{fakta program yang boleh disebut, dari laporan resmi}
</bahan>
<aturan>
Sapa dengan {nama_donatur}, jangan menulis nama asli di prompt.
Jangan menyebut angka yang tidak ada di <bahan>. Tidak meminta donasi lagi di pesan ini.
</aturan>
<contoh>
{1 sampai 2 pesan terima kasih yang pernah dinilai baik}
</contoh>
<format>
Paling banyak 60 kata. Bahasa {bahasa}. Buat 2 versi.
</format>""",
        "en": """<context>
We are the MyFundAction {country} CRM team. Donor segment: {segment}, for example new donors in the last 90 days.
</context>
<task>
Write a WhatsApp thank-you message for this segment after they gave to the {programme} programme.
</task>
<input>
{programme facts we may mention, from the official report}
</input>
<rules>
Address the donor as {donor_name}. Do not put real names in the prompt.
Do not mention any figure that is not in <input>. Do not ask for another donation in this message.
</rules>
<examples>
{1 to 2 thank-you messages that worked well}
</examples>
<format>
Up to 60 words. Language: {language}. Give 2 versions.
</format>""",
    },
    {
        "kode": "T3",
        "judul": "Jawaban pertanyaan donatur dari sumber resmi",
        "untuk": "CRM",
        "id": """<konteks>
Kami tim CRM MyFundAction {negara}. Donatur bertanya lewat {kanal}.
</konteks>
<tugas>
Susun jawaban untuk pertanyaan di <pertanyaan> memakai hanya <sumber>.
</tugas>
<pertanyaan>
{pertanyaan donatur, tanpa nama dan nomor}
</pertanyaan>
<sumber>
{FAQ resmi, laporan, atau kebijakan MFA}
</sumber>
<aturan>
Bila jawabannya tidak ada di <sumber>, tulis: "Kami cek dulu dan kabari Anda paling lambat {waktu}." Jangan menebak.
</aturan>
<format>
Paling banyak 80 kata. Bahasa {bahasa}.
</format>""",
        "en": """<context>
We are the MyFundAction {country} CRM team. A donor asked through {channel}.
</context>
<task>
Draft a reply to the question in <question> using only <source>.
</task>
<question>
{donor question, without name or number}
</question>
<source>
{official FAQ, report, or MFA policy}
</source>
<rules>
If the answer is not in <source>, write: "We will check and get back to you by {time}." Do not guess.
</rules>
<format>
Up to 80 words. Language: {language}.
</format>""",
    },
    {
        "kode": "T4",
        "judul": "Segmentasi donatur dari tabel",
        "untuk": "CRM, analisis",
        "id": """<konteks>
Kami tim CRM MyFundAction. Tanggal acuan {tanggal}. Data di <data> adalah data rekaan atau data tanpa nama.
</konteks>
<tugas>
Kelompokkan donatur ke segmen di <aturan_segmen>, lalu hitung jumlah per segmen dan per negara.
</tugas>
<aturan_segmen>
Urutan pemeriksaan: Baru bila donasi pertama paling lama 90 hari sebelum tanggal acuan. Tidak aktif bila donasi terakhir lebih dari 180 hari. Rutin bila jumlah donasi 12 bulan 3 kali atau lebih. Sisanya Lainnya.
</aturan_segmen>
<data>
{tempel atau unggah tabel}
</data>
<aturan>
Tunjukkan cara menghitung sebelum hasil. Pisahkan donatur yang setuju dihubungi.
</aturan>
<format>
Tabel: segmen, negara, jumlah, jumlah yang setuju dihubungi.
</format>""",
        "en": """<context>
We are the MyFundAction CRM team. Reference date {date}. The data in <data> is synthetic or anonymised.
</context>
<task>
Group donors into the segments in <segment_rules>, then count them by segment and country.
</task>
<segment_rules>
Check in this order: New if the first gift is at most 90 days before the reference date. Lapsed if the last gift is more than 180 days ago. Regular if they gave 3 or more times in 12 months. Everyone else is Other.
</segment_rules>
<data>
{paste or upload the table}
</data>
<rules>
Show how you counted before the result. Separate donors who agreed to be contacted.
</rules>
<format>
Table: segment, country, count, count who agreed to be contacted.
</format>""",
    },
    {
        "kode": "T5",
        "judul": "Brief iklan",
        "untuk": "Iklan, marketing",
        "id": """<konteks>
Kami tim marketing MyFundAction {negara}. Program {nama_program}. Kampanye berjalan {periode} di {platform}.
</konteks>
<tugas>
Susun brief iklan satu halaman.
</tugas>
<bahan>
{fakta program, target dana, hasil kampanye sebelumnya}
</bahan>
<aturan>
Klaim hanya dari <bahan>. Ikuti aturan etika penggalangan dana MFA.
</aturan>
<format>
Judul bagian: Tujuan, Audiens, Pesan utama, Bukti pendukung, Ajakan, Larangan klaim, Ukuran keberhasilan.
</format>""",
        "en": """<context>
We are the MyFundAction {country} marketing team. Programme: {programme}. The campaign runs {period} on {platform}.
</context>
<task>
Write a one-page ad brief.
</task>
<input>
{programme facts, fundraising target, previous campaign results}
</input>
<rules>
Claims only from <input>. Follow the MFA fundraising ethics rules.
</rules>
<format>
Sections: Objective, Audience, Key message, Supporting proof, Call to action, Claims to avoid, Success measure.
</format>""",
    },
    {
        "kode": "T6",
        "judul": "Variasi teks iklan per negara",
        "untuk": "Iklan",
        "id": """<konteks>
Kami tim marketing MyFundAction. Program {nama_program}. Audiens {negara}. Program masjid paling banyak direspons donatur Australia.
</konteks>
<tugas>
Tulis 3 variasi teks iklan {platform} dari brief di <brief>.
</tugas>
<brief>
{tempel brief dari T5}
</brief>
<aturan>
Sesuaikan nada dengan audiens {negara}. Tidak ada angka di luar <brief>. Tidak ada desakan palsu.
</aturan>
<contoh>
{1 sampai 2 iklan yang pernah berhasil di negara ini}
</contoh>
<format>
Tabel: judul (maks 40 karakter), teks utama (maks 125 karakter), ajakan, alasan pemilihan sudut pesan.
</format>""",
        "en": """<context>
We are the MyFundAction marketing team. Programme: {programme}. Audience: {country}. The mosque programme gets the strongest response from Australian donors.
</context>
<task>
Write 3 {platform} ad variations from the brief in <brief>.
</task>
<brief>
{paste the brief from T5}
</brief>
<rules>
Match the tone to the {country} audience. No figures outside <brief>. No false urgency.
</rules>
<examples>
{1 to 2 ads that performed well in this country}
</examples>
<format>
Table: headline (max 40 characters), primary text (max 125 characters), call to action, why this angle.
</format>""",
    },
    {
        "kode": "T7",
        "judul": "Analisis kinerja kampanye",
        "untuk": "Analisis",
        "id": """<konteks>
Kami tim marketing MyFundAction. Data kampanye {periode} di <data>, dalam USD.
</konteks>
<tugas>
Hitung per negara dan program: total biaya, jumlah donasi, CTR, biaya per donasi, dan nilai donasi per 1 USD biaya iklan. Lalu jawab: program dan negara mana yang paling efisien, dan mengapa jawabannya bisa berbeda tergantung ukuran yang dipakai.
</tugas>
<data>
{unggah berkas}
</data>
<aturan>
Tulis rumus yang dipakai. Pikirkan dulu langkahnya sebelum menulis jawaban. Tandai angka yang perlu dicek manual.
</aturan>
<format>
Tabel ringkas, lalu 3 temuan dan 2 usulan tindakan.
</format>""",
        "en": """<context>
We are the MyFundAction marketing team. Campaign data for {period} is in <data>, in USD.
</context>
<task>
For each country and programme, calculate total spend, number of donations, CTR, cost per donation, and donation value per 1 USD of ad spend. Then answer: which programme and country is most efficient, and why the answer can change depending on the measure used.
</task>
<data>
{upload the file}
</data>
<rules>
Write the formulas you used. Think through the steps before answering. Flag any figure that should be checked by hand.
</rules>
<format>
A short table, then 3 findings and 2 suggested actions.
</format>""",
    },
    {
        "kode": "T8",
        "judul": "Laporan mingguan untuk pimpinan",
        "untuk": "Analisis, marketing",
        "id": """<konteks>
Laporan untuk {pembaca}, dibaca di ponsel dalam 1 menit.
</konteks>
<tugas>
Susun laporan mingguan dari hasil analisis di <hasil>.
</tugas>
<hasil>
{tempel hasil T7}
</hasil>
<aturan>
Mulai dari hal terpenting. Sebutkan angka dengan satuannya. Tidak memakai istilah teknis tanpa penjelasan.
</aturan>
<format>
Paling banyak 6 baris: 1 kalimat ringkasan, 3 angka utama, 1 risiko, 1 keputusan yang diminta.
</format>""",
        "en": """<context>
Report for {reader}, read on a phone in 1 minute.
</context>
<task>
Write a weekly report from the analysis in <results>.
</task>
<results>
{paste the T7 output}
</results>
<rules>
Lead with the most important point. State every figure with its unit. No jargon without a short explanation.
</rules>
<format>
Up to 6 lines: 1 summary sentence, 3 key figures, 1 risk, 1 decision requested.
</format>""",
    },
    {
        "kode": "T9",
        "judul": "Lokalisasi pesan antarnegara",
        "untuk": "Marketing, CRM",
        "id": """<konteks>
Pesan asli ditulis untuk audiens {negara_asal}. Akan dipakai untuk audiens {negara_tujuan}.
</konteks>
<tugas>
Sesuaikan pesan di <pesan> untuk audiens {negara_tujuan}, bukan diterjemahkan kata per kata.
</tugas>
<pesan>
{pesan asli}
</pesan>
<aturan>
Pakai istilah dari glosarium MFA. Fakta dan angka tidak berubah. Jelaskan perubahan nada yang Anda buat.
</aturan>
<format>
Pesan hasil, lalu daftar perubahan paling banyak 3 butir.
</format>""",
        "en": """<context>
The original message was written for a {source_country} audience. It will be used for a {target_country} audience.
</context>
<task>
Adapt the message in <message> for the {target_country} audience rather than translating word for word.
</task>
<message>
{original message}
</message>
<rules>
Use terms from the MFA glossary. Facts and figures stay the same. Explain the tone changes you made.
</rules>
<format>
The adapted message, then up to 3 bullet points listing the changes.
</format>""",
    },
    {
        "kode": "T10",
        "judul": "Cek klaim sebelum terbit",
        "untuk": "Semua tim",
        "id": """<konteks>
Draf di bawah akan diterbitkan atas nama MyFundAction.
</konteks>
<tugas>
Periksa setiap klaim, angka, dan nama di <draf> terhadap <sumber>.
</tugas>
<draf>
{draf}
</draf>
<sumber>
{laporan resmi atau data}
</sumber>
<aturan>
Jangan memperbaiki gaya tulisan. Fokus pada kebenaran klaim.
</aturan>
<format>
Tabel: klaim, ada di sumber (ya atau tidak), kutipan sumber, usulan perbaikan.
</format>""",
        "en": """<context>
The draft below will be published under the MyFundAction name.
</context>
<task>
Check every claim, figure, and name in <draft> against <source>.
</task>
<draft>
{draft}
</draft>
<source>
{official report or data}
</source>
<rules>
Do not edit the writing style. Focus on whether each claim is true.
</rules>
<format>
Table: claim, found in source (yes or no), source quote, suggested fix.
</format>""",
    },
]

# Contoh prompt lemah dan perbaikannya, untuk Modul 3.1
CONTOH_SEBELUM = "Buatkan caption donasi masjid yang menarik."
CONTOH_SESUDAH = """<konteks>
Kami tim marketing MyFundAction Australia. Program pembangunan masjid paling banyak direspons donatur Australia. Caption untuk Instagram, pembaca Muslim Australia usia 25 sampai 45.
</konteks>
<tugas>
Tulis 3 caption Instagram untuk mengajak donasi program pembangunan masjid.
</tugas>
<bahan>
{lokasi masjid, kebutuhan dana, progres pembangunan dari laporan terakhir}
</bahan>
<aturan>
Bahasa Inggris Australia. Nada hangat, tidak menggurui. Tidak ada angka di luar <bahan>. Tidak ada desakan palsu.
</aturan>
<contoh>
{1 caption yang pernah berhasil}
</contoh>
<format>
Tiap caption paling banyak 60 kata, 1 ajakan di akhir, paling banyak 3 tagar.
</format>"""
