"""Jalankan build secara bergantian agar pratinjau dan make tidak bertabrakan."""

import argparse
import fcntl
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("main", "tor", "assets", "check", "clean"))
    parser.add_argument("--latexmk", default="latexmk")
    args = parser.parse_args()
    with (ROOT / ".build.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if args.target == "clean":
            shutil.rmtree(ROOT / "build", ignore_errors=True)
            return 0
        if args.target in ("main", "assets"):
            result = subprocess.run([sys.executable, "scripts/generate_logbook.py"], cwd=ROOT)
            if result.returncode or args.target == "assets":
                return result.returncode
        if args.target == "check":
            for script in ("check_build.py", "check_documents.py"):
                result = subprocess.run([sys.executable, f"scripts/{script}"], cwd=ROOT)
                if result.returncode:
                    return result.returncode
            return 0
        result = subprocess.run([args.latexmk, f"{args.target}.tex"], cwd=ROOT)
        if result.returncode:
            return result.returncode
        temporary = ROOT / "build" / f"{args.target}.export.pdf"
        shutil.copyfile(ROOT / "build" / f"{args.target}.pdf", temporary)
        temporary.replace(ROOT / f"{args.target}.pdf")
        return 0


if __name__ == "__main__":
    sys.exit(main())
