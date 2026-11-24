"""Periksa format keluaran logbook dan teks dokumen yang akan dibagikan."""

import csv
from datetime import date
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile


def spreadsheet_rows(path, number):
    ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    with ZipFile(path) as archive:
        archive.testzip()
        root = ET.fromstring(archive.read(f"xl/worksheets/sheet{number}.xml"))
        return [["".join(cell.itertext()) for cell in row.findall("s:c/s:is", ns)]
                for row in root.findall("s:sheetData/s:row", ns)]


def main():
    headers = ["Tanggal", "Kegiatan", "Hasil"]
    entries = json.loads(Path("data/logbook_raif.json").read_text())
    with Path("deliverables/logbook_raif.csv").open(encoding="utf-8-sig", newline="") as source:
        rows = list(csv.reader(source))
    assert rows[0] == headers, "Nama kolom CSV berubah"
    assert len(rows) == len(entries)+1, "Jumlah entri CSV tidak sesuai sumber"
    dates = [date.fromisoformat(row[0]) for row in rows[1:]]
    assert dates == sorted(set(dates)), "Tanggal CSV harus unik dan berurutan"
    assert all(len(row) == 3 and all(0 < len(cell) <= 1024 for cell in row[1:]) for row in rows[1:]), "Kolom logbook tidak valid"
    book = Path("deliverables/logbook_raif.xlsx")
    complete, pending = spreadsheet_rows(book, 1), spreadsheet_rows(book, 2)
    assert complete[0] == pending[0] == headers, "Nama kolom Excel berubah"
    expected_complete = [row for row, entry in zip(rows[1:], entries) if entry["status"] != "perlu_dilengkapi"]
    expected_pending = [row for row, entry in zip(rows[1:], entries) if entry["status"] == "perlu_dilengkapi"]
    assert complete[1:] == expected_complete, "Isi lembar impor Excel berbeda dari CSV"
    assert pending[1:] == expected_pending, "Entri belum lengkap harus terpisah dari lembar impor"
    assert spreadsheet_rows(Path("deliverables/template_logbook_frederiko.xlsx"), 1) == [headers], "Template Frederiko harus kosong"

    frederiko_source = Path("data/logbook_frederiko.json")
    if frederiko_source.exists():
        people = [("Raif", {entry["tanggal"]: entry for entry in entries}),
                  ("Riko", {entry["tanggal"]: entry for entry in json.loads(frederiko_source.read_text())})]
        combined_path = Path("deliverables/logbook_gabungan.xlsx")
        combined = spreadsheet_rows(combined_path, 1)
        assert combined[0] == headers, "Nama kolom logbook gabungan berubah"
        days = sorted(set().union(*(records.keys() for _, records in people)))
        assert [row[0] for row in combined[1:]] == days, "Tanggal gabungan harus unik dan mencakup kedua logbook"
        for row in combined[1:]:
            for index, field in enumerate(("kegiatan", "hasil"), 1):
                expected = "\n".join(f"{name}: " + (records[row[0]][field] if row[0] in records
                                     else f"Catatan {field} belum tersedia untuk tanggal ini.")
                                     for name, records in people)
                assert row[index] == expected, f"Isi gabungan berbeda dari sumber: {row[0]} {field}"
                assert len(row[index]) <= 1024, f"Gabungan terlalu panjang: {row[0]} {field}"
        with ZipFile(combined_path) as archive:
            ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
            workbook = ET.fromstring(archive.read("xl/workbook.xml"))
            assert len(workbook.findall("s:sheets/s:sheet", ns)) == 1, "Berkas gabungan harus berisi satu sheet"
        print(f"Logbook gabungan konsisten: {len(combined)-1} tanggal unik, dua nama pada baris terpisah.")

    if shutil.which("pdftotext"):
        for name in ("main", "tor"):
            text = subprocess.check_output(["pdftotext", "-layout", f"build/{name}.pdf", "-"], text=True)
            assert not re.search(r"\b(?:PLN|DIMS|MDG|BPO)\b|PLN\s*Click", text, re.IGNORECASE), f"Identitas internal pada {name}.pdf"
            assert not re.search(r"[A-Za-z]-\s*\n", text), f"Pemenggalan kata pada {name}.pdf"
            assert "Lorem ipsum" not in text, f"Teks contoh pada {name}.pdf"
    print(f"Logbook konsisten: {len(rows)-1} entri; {len(complete)-1} pada lembar impor, {len(pending)-1} perlu dilengkapi.")
    print("Pemeriksaan anonimisasi dan pemenggalan kata selesai.")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, KeyError) as error:
        print(f"Pemeriksaan dokumen gagal: {error}", file=sys.stderr)
        sys.exit(1)
