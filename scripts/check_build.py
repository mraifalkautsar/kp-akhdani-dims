"""Validasi keluaran build; isian draf bukan kesalahan kompilasi."""

from pathlib import Path
import re
import subprocess
import shutil
import sys


def main():
    errors = []
    for name in ("main", "tor"):
        pdf = Path("build") / f"{name}.pdf"
        log = pdf.with_suffix(".log")
        if not pdf.is_file() or pdf.stat().st_size < 1024 or not pdf.read_bytes().startswith(b"%PDF-"):
            errors.append(f"PDF tidak valid: {pdf}")
        if not log.is_file():
            errors.append(f"Log tidak ditemukan: {log}")
            continue
        contents = log.read_text(errors="replace")
        for pattern in (
            r"(?:Reference|Citation) .+ undefined",
            r"There were undefined (?:references|citations)",
            r"Label\(s\) may have changed",
            r"multiply[- ]defined",
            r"Fatal error occurred",
        ):
            if re.search(pattern, contents, re.IGNORECASE):
                errors.append(f"Referensi/kompilasi belum bersih pada {log}: {pattern}")
        if shutil.which("pdfinfo") and pdf.is_file():
            result = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
            if result.returncode:
                errors.append(f"PDF gagal dibaca: {pdf}")
            else:
                pages = re.search(r"^Pages:\s+(\d+)", result.stdout, re.MULTILINE)
                print(f"{pdf}: {pages.group(1) if pages else '?'} halaman")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Kedua PDF valid; referensi silang dan sitasi terselesaikan.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
