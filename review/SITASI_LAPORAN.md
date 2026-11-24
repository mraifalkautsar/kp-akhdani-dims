# Arsip sitasi laporan kerja praktik

Arsip ini memuat 15 sitasi yang dilepas sementara dari laporan dan 10 sumber yang dirujuk.

## Lokasi sitasi

Untuk mengembalikan sitasi, cari penggalan yang tercantum di tabel. Sisipkan satu spasi dan perintah LaTeX tepat sebelum titik penutup penggalan tersebut. Nomor baris mengacu pada sumber LaTeX saat arsip dibuat.

| Lokasi | Penggalan penutup kalimat | Perintah LaTeX |
| --- | --- | --- |
| [BabI_Pendahuluan.tex:7](../chapters/BabI_Pendahuluan.tex#L7) | `fondasi tersebut, beberapa kebutuhan proses dapat menggunakan komponen aplikasi yang sama.` | `\citep{rancangan-awal}` |
| [BabII_Organisasi_dan_LKP.tex:5](../chapters/BabII_Organisasi_dan_LKP.tex#L5) | `baik melalui pembangunan aplikasi maupun integrasi dengan sistem yang sudah tersedia.` | `\citep{ars-onboarding}` |
| [BabII_Organisasi_dan_LKP.tex:7](../chapters/BabII_Organisasi_dan_LKP.tex#L7) | `Gambar~\ref{fig:struktur-perusahaan} memperlihatkan susunan tersebut secara ringkas.` | `\citep[hlm.~7]{ars-onboarding}` |
| [BabII_Organisasi_dan_LKP.tex:18](../chapters/BabII_Organisasi_dan_LKP.tex#L18) | `tersebut didukung oleh nilai dedikasi, disiplin, akuntabilitas, sikap melayani, dan komunikasi.` | `\citep{ars-culture}` |
| [BabII_Organisasi_dan_LKP.tex:21](../chapters/BabII_Organisasi_dan_LKP.tex#L21) | `tersebut menghubungkan kebutuhan, rancangan, implementasi, serta pemeriksaan hasil pekerjaan.` | `\citep[hlm.~10]{struktur-tim}` |
| [BabII_Organisasi_dan_LKP.tex:35](../chapters/BabII_Organisasi_dan_LKP.tex#L35) | `sehingga proses yang memiliki kebutuhan berbeda dapat menggunakan fondasi aplikasi yang sama.` | `\citep{rancangan-awal}` |
| [BabIII_Judul_Pekerjaan.tex:8](../chapters/BabIII_Judul_Pekerjaan.tex#L8) | `pada pengelolaan keadaan dan transisi yang dihubungkan dengan metadata proses serta formulir.` | `\citep{rancangan-awal}` |
| [BabIII_Judul_Pekerjaan.tex:24](../chapters/BabIII_Judul_Pekerjaan.tex#L24) | `proses serta riwayat, sedangkan model dokumen digunakan untuk skema formulir dan nilai isian.` | `\citep{artefak-awal}` |
| [BabIII_Judul_Pekerjaan.tex:88](../chapters/BabIII_Judul_Pekerjaan.tex#L88) | `Vue dan TypeScript. Vue menyediakan model antarmuka berbasis komponen dan keadaan reaktif.` | `\citep{vue}` |
| [BabIII_Judul_Pekerjaan.tex:90](../chapters/BabIII_Judul_Pekerjaan.tex#L90) | `menggunakan Node.js dan Express. Express menyediakan penanganan rute serta \textit{middleware}.` | `\citep{express}` |
| [BabIII_Judul_Pekerjaan.tex:90](../chapters/BabIII_Judul_Pekerjaan.tex#L90) | `menggunakan struktur tersebut untuk menghubungkan tindakan pengguna dengan data aplikasi.` | `\citep{artefak-awal}` |
| [BabIII_Judul_Pekerjaan.tex:103](../chapters/BabIII_Judul_Pekerjaan.tex#L103) | `mengikuti struktur permintaan, layanan, repositori, dan skema data pada lingkungan tersebut.` | `\citep{artefak-agustus}` |
| [BabIII_Judul_Pekerjaan.tex:105](../chapters/BabIII_Judul_Pekerjaan.tex#L105) | `\texttt{sqlx}. Pustaka \texttt{sqlx} menyediakan perluasan fasilitas akses data SQL di Go.` | `\citep{sqlx}` |
| [BabIII_Judul_Pekerjaan.tex:181](../chapters/BabIII_Judul_Pekerjaan.tex#L181) | `Vitest menyediakan fasilitas menjalankan pengujian pada lingkungan pengembangan berbasis Vite.` | `\citep{vitest}` |
| [BabIII_Judul_Pekerjaan.tex:208](../chapters/BabIII_Judul_Pekerjaan.tex#L208) | `Cypress untuk memeriksa keandalan antarmuka dan layanan pada sistem pengelolaan alur kerja.` | `\citep{artefak-awal}` |

## Daftar sumber

| Kunci sitasi | Entri referensi |
| --- | --- |
| `express` | Express. t.t. “Express: Node.js Web Application Framework.” Diakses 10 November 2026. [Dokumentasi Express](https://expressjs.com/). |
| `sqlx` | Jmoiron. t.t. “sqlx.” *Go Packages*. Diakses 10 November 2026. [Dokumentasi sqlx](https://pkg.go.dev/github.com/jmoiron/sqlx). |
| `ars-onboarding` | PT Akhdani Reka Solusi. t.t.a. *Company Profile Onboarding*. Materi internal perusahaan tentang bidang layanan dan struktur organisasi. |
| `ars-culture` | PT Akhdani Reka Solusi. t.t.b. *Culture & Core Value*. Materi internal perusahaan. |
| `artefak-awal` | PT Akhdani Reka Solusi. 2026a. Kode sumber dan konfigurasi aplikasi periode Juni–Juli 2026. Artefak pengembangan internal dengan identitas repositori yang disamarkan. |
| `artefak-agustus` | PT Akhdani Reka Solusi. 2026b. Kode sumber dan konfigurasi layanan serta antarmuka periode Agustus 2026. Artefak pengembangan internal dengan identitas repositori yang disamarkan. |
| `rancangan-awal` | Rancangan teknis awal. 2026. Rancangan platform proses bisnis, mesin alur kerja, dan formulir dinamis, 7 Juni. Dokumen internal dengan identitas proyek yang disamarkan. |
| `struktur-tim` | Struktur tim proyek. t.t. Bagan organisasi tim proyek, hlm. 10. Dokumen gambar dan diagram internal dengan identitas proyek yang disamarkan. |
| `vitest` | Vitest. t.t. “Getting Started.” Diakses 10 November 2026. [Dokumentasi Vitest](https://vitest.dev/guide/). |
| `vue` | Vue.js. t.t. “Introduction.” Diakses 10 November 2026. [Dokumentasi Vue.js](https://vuejs.org/guide/introduction.html). |

Rincian lokasi dokumen dan artefak internal ada di [catatan peninjauan penulis](BUKTI_DAN_ISIAN.md).

## Mengaktifkan kembali bagian Referensi

Entri LaTeX asli tersedia di [backmatter/Referensi.tex](../backmatter/Referensi.tex). Setelah memasang kembali sitasi, tambahkan `\input{backmatter/Referensi}` tepat sebelum `\appendix` di [main.tex](../main.tex), lalu jalankan `make check`.
