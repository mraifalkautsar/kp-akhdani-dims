# Catatan peninjauan penulis

Berkas ini untuk peninjauan internal, terpisah dari dokumen akademik dan artefak CI.
Tidak perlu dilampirkan atau diunggah bersama PDF. Referensi asli tidak diubah.

## Keputusan penulisan

- Laporan merupakan satu laporan bersama Muhammad Ra'if Alkautsar (13523011) dan Frederiko Eldad Mugiyono (13523147).
- Nama proyek, identitas klien, nama unit klien, serta produk internal disamarkan. Tidak ada kode internal, alamat layanan, kredensial, atau tangkapan layar aplikasi asli di laporan.
- Contoh penulisan mengikuti `references/previous_year/Laporan Kp - 13522137_13522142_13522147.pdf`: latar belakang, tujuan, pembagian tugas, kebutuhan, rancangan, implementasi, pengujian, hasil, dan kendala. Isi pengalaman tahun sebelumnya tidak dipindahkan menjadi pengalaman tahun ini.
- Periode 22 Juni sampai 31 Agustus 2026 dikonfirmasi surat kerahasiaan. Jangan mengatribusikan perubahan September sampai November sebagai capaian KP.
- Pola WFO Senin sampai Kamis, WFH Jumat, rapat Selasa 09.30, dan penugasan melalui WhatsApp/Microsoft 365 dikonfirmasi penulis dalam percakapan.
- Pembimbing perusahaan/penanda tangan: Gita Marshelina (Project Manager). Pembimbing teknis: Muhammad Usgan (Senior). Dosen pembimbing: Dr. Maya Nabila, S.Si., M.Si. Semua dikonfirmasi penulis; identitas lama pada template tidak dipakai.
- Pemenggalan kata otomatis dengan tanda hubung dinonaktifkan atas permintaan penulis.

## Pemetaan bukti kontribusi Ra'if

Identitas penulis commit dikenali melalui alamat surel milik Ra'if; riwayat diperiksa pada cabang lokal yang tersedia. Penetapan tanggal kegiatan tidak hanya didasarkan pada tanggal commit, karena pekerjaan bisa berlangsung sebelum perubahan dicatat. Hash berikut hanya untuk penelusuran internal, bukan sitasi publik.

| Bagian | Referensi lokal dan contoh perubahan | Implikasi untuk penulisan |
| --- | --- | --- |
| Dasbor awal | `old_repos/dims-fe`: `b89cc3f` (23 Juni), `073ffe5` dan `5b00d8a` (26 Juni), `a20b219` dan `4cc6a50` (29 Juni) | Kerangka halaman, layanan simulasi, dan pemisahan pemanggilan data dari komponen. Tidak diklaim seluruh sumber data operasional sudah terhubung. |
| Pengelolaan peran | `old_repos/dims-fe`: `be4b521`, `b5e5c6c`; `old_repos/dims-be`: `5e5a6bc` (13 Juli), `1c7bf34` (14 Juli) | Halaman peran, formulir bersama, lapisan layanan, repositori, dan data awal. |
| Penamaan dan pesan kesalahan | `476a05d`, `1e2177a`, `301cb97`, `b05d27e` | Penyeragaman penamaan, pemakaian komponen bersama, dan penanganan kesalahan. |
| Riwayat | `old_repos/dims-fe`: `0ce4b2e`, `220b6d9`, `605008e`, `642bb4f`; `old_repos/dims-be`: `17f70e1`, `f379eb3`, `f17643f`, `7f6421c` | Integrasi data, komentar, pelaksana, dan transisi. Diagram dalam laporan adalah konseptual, bukan salinan artefak internal. |
| Data hak akses lama | `old_repos/dims-fe`: `4b2af0c` (28 Juli) | Perbaikan keadaan data detail dan keterkaitannya dengan pemuatan data. |
| Pengujian komponen | `old_repos/dims-fe`: `87121e8` dan `bc14ca7` (31 Juli) | Enam berkas pengujian halaman peran dan riwayat serta pemisahan stub. Tidak tersedia rekaman eksekusi/cakupan untuk diklaim sebagai hasil pengujian. |
| Adaptasi Go | `new_repos/dims-core`: `6fa0e1c` (24 Agustus) | Implementasi pengelolaan peran dan data awal. `go.mod` historis menggunakan Fiber v2 dan sqlx; bukan Fiber v3 pada versi November. |
| Rekonstruksi 25 Agustus | `new_repos/dims-auth`: `04c6166` | Isi perubahan mengonfirmasi penyesuaian kueri pengambilan peran dan penambahan dua kasus uji integrasi. Tidak ada klaim kasus uji telah lulus. Entri ditambahkan setelah sebelumnya tidak ada pada CSV asli. |
| Dependensi 26 Agustus | `new_repos/dims-auth`: `6337bc4` | Penghapusan pengandar yang tidak digunakan. Kegiatan Docker didukung catatan logbook, bukan disimpulkan dari commit ini. |

Semua lokasi repositori di atas berada di bawah `references/`. Bahan yang dibaca tidak disalin ke dokumen akademik. Kode dan konfigurasi contoh di repositori sumber tidak boleh disalin begitu saja karena dapat memuat informasi rahasia.

Pembelajaran Go, eksperimen Gin/GORM, kegiatan internal 18 Agustus, serta rancangan Visily 27–28 Agustus bersumber dari logbook. Materi yang dipelajari tidak selalu sama dengan pustaka implementasi akhir. Kegiatan autentikasi 3 Juli didukung logbook; tidak ditemukan perubahan kode milik Ra'if pada tanggal yang sama untuk menyatakan hasil eksekusi tertentu.

Repositori baru memuat pekerjaan setelah akhir KP. Tidak ada kontribusi Ra'if pada antarmuka baru yang teridentifikasi dalam rentang KP pada riwayat yang diperiksa. Karena itu, laporan menyebut pemahaman kode dan rancangan layar, tanpa mengklaim implementasi fitur antarmuka baru pada Agustus.

## Bagian yang masih memerlukan penulis

1. Lengkapi kegiatan dan hasil 31 Agustus 2026. Entri ini tidak masuk lembar impor Excel; setelah dikonfirmasi, perbarui teks dan status pada `data/logbook_raif.json` lalu jalankan `make`.
2. Frederiko melengkapi lingkup QA, pendekatan, kasus uji, temuan, pengujian ulang, hasil, jadwal, evaluasi diri, dan logbook. Gunakan penanda `ISIAN FREDERIKO` pada sumber LaTeX untuk menemukan lokasinya. Template Excel tersedia pada `deliverables/template_logbook_frederiko.xlsx`.
3. Lengkapi tanggal pengesahan dan tanggal penyelesaian laporan. NIP/NIDN dosen hanya dicantumkan bila disyaratkan dan telah diketahui.
4. Lengkapi spesifikasi perangkat pada ToR bila diperlukan. Jangan mengambil spesifikasi perangkat dari contoh mahasiswa tahun sebelumnya atau mesin saat ini sebagai fakta perangkat saat KP.
5. Lengkapi jadwal presentasi/penyerahan akhir bila ada. Tidak ada tanggal atau frekuensi rapat harian yang diasumsikan.
6. Tinjau refleksi Ra'if sebagai draf berdasarkan pengalaman teknis yang tercatat. Tidak ada konflik interpersonal atau umpan balik pembimbing yang dikarang.
7. Tinjau seluruh entri logbook sebelum impor. Rekonstruksi hasil kegiatan ditulis berdasarkan aktivitas dan perubahan kode; ketiadaan rekaman hasil eksekusi tidak ditulis sebagai keberhasilan pengujian.

## Pemeriksaan hasil

`make check` mengompilasi kedua dokumen dan memeriksa referensi silang, sitasi, kesesuaian CSV/Excel, pemisahan entri belum lengkap, nama internal yang harus disamarkan, serta pemenggalan kata. Pemeriksaan pola teks membantu peninjauan, tetapi tidak menggantikan pembacaan substansi dokumen.

Pemeriksaan pelaksanaan pada 10 November 2026:

- `make check` lulus: laporan 43 halaman dan ToR 5 halaman; tidak ada referensi silang/sitasi yang belum terselesaikan atau kotak teks melampaui batas halaman.
- Build bersih pada direktori terpisah tanpa `references/` melalui `make -j2 check` lulus.
- Uji pratinjau memeriksa akses kedua PDF, penolakan akses sumber, perubahan sumber, kegagalan kompilasi tanpa mengganti PDF terakhir, serta pemulihan setelah sumber diperbaiki.
- CSV, Excel, dan lampiran konsisten. Workbook dibuka melalui LibreOffice dan 49 entri pada lembar impor diekspor ulang tanpa perubahan isi. Generasi ulang menghasilkan isi berkas yang identik.
- Validasi data menolak tanggal ganda, tanggal di luar periode, teks melampaui 1024 karakter, serta entri bertanda belum lengkap yang keliru dimasukkan sebagai entri final.
- Pemindaian teks PDF tidak menemukan nama internal yang diperiksa atau kata berakhir tanda hubung akibat pemenggalan. Sampul, beberapa halaman bab, bagan organisasi, tabel logbook, dan pengesahan ToR diperiksa secara visual.
- Workflow GitHub Actions disiapkan pada sumber; belum dijalankan di GitHub karena tidak ada push yang dilakukan.
