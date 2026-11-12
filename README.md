# Dokumen kerja praktik

Laporan bersama dan ToR ditulis dengan LaTeX. Isi dokumen masih dalam penyusunan;
penanda `[ISIAN: ...]` dan `[ISIAN FREDERIKO: ...]` menunjukkan data yang perlu dilengkapi.

## Lihat PDF sambil menulis

```bash
make preview
```

Buka **http://127.0.0.1:8000**. Pilih Laporan atau ToR. Perubahan pada sumber
LaTeX dan gambar memicu build ulang; PDF pada browser diperbarui setelah build
berhasil. Jika build gagal, halaman menampilkan status gagal dan menyediakan log,
sementara PDF hasil build terakhir tetap dapat dilihat. Tekan `Ctrl+C` untuk berhenti.
Gunakan `make preview PORT=8001` jika port 8000 sedang dipakai. `make watch` adalah
alias perintah ini. Server hanya mendengarkan koneksi lokal dan hanya menyediakan
PDF serta log build; folder referensi tidak disajikan.

## Build sekali

```bash
make          # laporan dan ToR
make report   # laporan saja
make tor      # ToR saja
make check    # build, validasi PDF, logbook, anonimisasi, dan pemenggalan kata
make generate # perbarui keluaran logbook tanpa mengompilasi PDF
```

Hasil utama berada di `build/main.pdf` dan `build/tor.pdf`. Build yang berhasil juga
memperbarui salinan `main.pdf` dan `tor.pdf` pada root agar mudah dibuka di editor.
`make clean` membersihkan folder build; salinan pada root tetap menjadi hasil
build terakhir. `latexmk` otomatis mengulang kompilasi untuk menyelesaikan daftar
isi dan referensi silang. Tidak diperlukan akses ke folder `references` untuk build.

## Dependensi

Diperlukan Python 3, GNU Make, `latexmk`, dan TeX Live dengan bahasa Indonesia,
paket LaTeX tambahan, serta font New TX. Tidak ada dependensi Python tambahan.
Pada Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  make python3 latexmk poppler-utils \
  texlive-latex-extra texlive-fonts-extra texlive-lang-other texlive-science
make doctor
```

Paket font TeX Live berukuran besar. Jika TeX Live lengkap sudah terpasang,
cukup jalankan `make doctor`. Pada macOS, gunakan MacTeX dan GNU Make/Python 3;
pada Windows, jalankan perintah di WSL dengan dependensi di atas.

## GitHub Actions

Workflow **Build laporan dan ToR** berjalan pada push, pull request, atau melalui
**Actions → Build laporan dan ToR → Run workflow** setelah berkas workflow masuk
ke GitHub. Buka hasil run, lalu unduh artefak **dokumen-kp** untuk mendapatkan
kedua PDF. Workflow hanya mengunggah dua PDF, menggunakan proses `make check`
yang sama dengan build lokal, dan tidak menerbitkan situs web.

## Penyuntingan

- Identitas, pembimbing, dan tanggal: `shared/metadata.tex`.
- Isi laporan: `frontmatter/`, `chapters/`, `backmatter/`, dan `appendices/`.
- Isi ToR bersama: `shared/tor-body.tex`, digunakan oleh laporan dan `tor.tex`.
- Sumber logbook: `data/logbook_raif.json`; hasil CSV/Excel: `deliverables/`.
- Pengaturan LaTeX bersama: `shared/preamble.tex`; pengaturan build: `.latexmkrc`.

Logbook Ra'if memiliki 50 entri yang tersedia untuk ditinjau sebelum impor. Entri
31 Agustus memuat kegiatan penutupan kerja praktik dengan pemaparan dari President
Director. CSV dan sheet **Template Logbook** pada Excel memuat seluruh entri;
sheet **Perlu Dilengkapi** saat ini kosong. Impor hanya sheet **Template Logbook**.
Entri 25 Agustus direkonstruksi dari perubahan kode milik Ra'if. Template Excel
Frederiko disediakan kosong agar ia mengisi kegiatannya sendiri. Perubahan data
logbook otomatis digunakan saat `make`, sehingga CSV, Excel, dan lampiran laporan
tetap berasal dari satu sumber. Jangan menyunting berkas di `generated/`.

Proses build memakai penguncian berkas, sehingga `make` atau `make check` tetap
dapat dijalankan saat pratinjau aktif. PDF pada root diganti secara atomik setelah
kompilasi berhasil; build yang gagal tidak mengganti salinan hasil terakhir.

Pemenggalan kata otomatis dengan tanda hubung dinonaktifkan untuk laporan dan ToR.
Catatan bukti dan daftar isian tersedia di `review/BUKTI_DAN_ISIAN.md` untuk
peninjauan penulis; berkas tersebut bukan bagian PDF maupun artefak CI.

Dokumen dalam `references/` adalah bahan internal untuk penulisan, bukan keluaran
yang diunggah oleh pipeline. Simpan anonimisasi saat menambahkan materi laporan.
