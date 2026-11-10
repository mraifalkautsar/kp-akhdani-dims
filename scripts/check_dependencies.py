"""Periksa dependensi tanpa menginstal atau mengubah lingkungan pengguna."""

import shutil
import subprocess
import sys


def main():
    missing = [name for name in ("latexmk", "pdflatex", "kpsewhich") if not shutil.which(name)]
    if not missing:
        for name in (
            "indonesian.ldf", "newtxtext.sty", "newtxmath.sty", "tikz.sty",
            "natbib.sty", "xurl.sty", "titlesec.sty", "tocloft.sty",
        ):
            result = subprocess.run(["kpsewhich", name], capture_output=True, text=True)
            if result.returncode or not result.stdout.strip():
                missing.append(name)
    if missing:
        print("Dependensi belum tersedia: " + ", ".join(missing), file=sys.stderr)
        print("Lihat bagian instalasi pada README.md.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
