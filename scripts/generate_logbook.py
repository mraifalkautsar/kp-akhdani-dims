"""Hasilkan CSV, Excel, dan lampiran LaTeX dari satu sumber logbook tersanitasi."""

import csv
from datetime import date
import io
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
HEADERS = ("Tanggal", "Kegiatan", "Hasil")
MONTHS = ("", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember")
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def load_entries(filename="data/logbook_raif.json"):
    entries = json.loads((ROOT / filename).read_text())
    dates = []
    for entry in entries:
        day = date.fromisoformat(entry["tanggal"])
        if not date(2026, 6, 22) <= day <= date(2026, 8, 31):
            raise ValueError(f"Tanggal di luar periode KP: {day}")
        dates.append(day)
        if entry["status"] not in ("tercatat", "rekonstruksi", "perlu_dilengkapi"):
            raise ValueError(f"Status tidak dikenal: {day}")
        for field in ("kegiatan", "hasil"):
            if not isinstance(entry[field], str) or not entry[field].strip() or len(entry[field]) > 1024:
                raise ValueError(f"{day}: {field} wajib diisi dan maksimal 1024 karakter")
            if entry["status"] != "perlu_dilengkapi" and "PERLU DILENGKAPI" in entry[field]:
                raise ValueError(f"{day}: isian belum lengkap tidak boleh masuk lembar impor")
    if len(set(dates)) != len(dates) or dates != sorted(dates):
        raise ValueError("Tanggal harus unik dan berurutan")
    return entries


def xml_bytes(element):
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)


def sheet(rows, table=False):
    ET.register_namespace("", NS)
    root = ET.Element(f"{{{NS}}}worksheet")
    views = ET.SubElement(root, "sheetViews")
    view = ET.SubElement(views, "sheetView", workbookViewId="0")
    ET.SubElement(view, "pane", ySplit="1", topLeftCell="A2", activePane="bottomLeft", state="frozen")
    columns = ET.SubElement(root, "cols")
    for index, width in enumerate((16, 75, 75) if table else (105,), 1):
        ET.SubElement(columns, "col", min=str(index), max=str(index), width=str(width), customWidth="1")
    data = ET.SubElement(root, "sheetData")
    for number, values in enumerate(rows, 1):
        row = ET.SubElement(data, "row", r=str(number))
        for index, value in enumerate(values):
            cell = ET.SubElement(row, "c", r=f"{chr(65+index)}{number}", t="inlineStr", s="1" if number == 1 else "2")
            text = ET.SubElement(ET.SubElement(cell, "is"), "t")
            text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            text.text = str(value)
    if table:
        ET.SubElement(root, "autoFilter", ref=f"A1:C{len(rows)}")
    return xml_bytes(root)


def xlsx(sheets):
    """Tulis workbook OOXML sederhana menggunakan pustaka standar Python."""
    buffer = io.BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        def add(name, content):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, content)

        contents = ET.Element("Types", xmlns="http://schemas.openxmlformats.org/package/2006/content-types")
        ET.SubElement(contents, "Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
        ET.SubElement(contents, "Default", Extension="xml", ContentType="application/xml")
        for part, kind in [("/xl/workbook.xml", "sheet.main"), ("/xl/styles.xml", "styles")]:
            ET.SubElement(contents, "Override", PartName=part, ContentType=f"application/vnd.openxmlformats-officedocument.spreadsheetml.{kind}+xml")
        for index in range(1, len(sheets)+1):
            ET.SubElement(contents, "Override", PartName=f"/xl/worksheets/sheet{index}.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml")
        add("[Content_Types].xml", xml_bytes(contents))
        relns = "http://schemas.openxmlformats.org/package/2006/relationships"
        reltype = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
        rootrels = ET.Element("Relationships", xmlns=relns)
        ET.SubElement(rootrels, "Relationship", Id="rId1", Type=reltype+"officeDocument", Target="xl/workbook.xml")
        add("_rels/.rels", xml_bytes(rootrels))
        workbook = ET.Element("workbook", xmlns=NS)
        children = ET.SubElement(workbook, "sheets")
        rels = ET.Element("Relationships", xmlns=relns)
        for index, (name, rows, table) in enumerate(sheets, 1):
            ET.SubElement(children, "sheet", name=name, sheetId=str(index), **{f"{{{reltype[:-1]}}}id": f"rId{index}"})
            ET.SubElement(rels, "Relationship", Id=f"rId{index}", Type=reltype+"worksheet", Target=f"worksheets/sheet{index}.xml")
            add(f"xl/worksheets/sheet{index}.xml", sheet(rows, table))
        ET.SubElement(rels, "Relationship", Id=f"rId{len(sheets)+1}", Type=reltype+"styles", Target="styles.xml")
        add("xl/workbook.xml", xml_bytes(workbook))
        add("xl/_rels/workbook.xml.rels", xml_bytes(rels))
        add("xl/styles.xml", '''<?xml version="1.0" encoding="UTF-8"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>
<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf>
<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" applyAlignment="1"><alignment wrapText="1" vertical="top"/></xf></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>''')
    return buffer.getvalue()


def escape_tex(text):
    replacements = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
    return "".join(replacements.get(character, character) for character in text)


def tex(entries, caption=r"Logbook kegiatan Muhammad Ra'if Alkautsar", label="tab:logbook-raif"):
    lines = [r"% Dihasilkan dari data JSON; jangan sunting berkas ini.",
             r"\begingroup\footnotesize\singlespacing\setlength{\tabcolsep}{4pt}",
             r"\setlength{\parindent}{0pt}",
             r"\begin{longtable}{@{}P{1.6cm}P{5.8cm}P{5.8cm}@{}}",
             f"\\caption{{{caption}}}\\label{{{label}}}\\\\",
             r"\toprule\textbf{Tanggal} & \textbf{Kegiatan} & \textbf{Hasil}\\\midrule\endfirsthead",
             r"\multicolumn{3}{l}{\textit{Logbook kegiatan (lanjutan)}}\\\toprule",
             r"\textbf{Tanggal} & \textbf{Kegiatan} & \textbf{Hasil}\\\midrule\endhead",
             r"\midrule\multicolumn{3}{r}{\textit{Bersambung ke halaman berikutnya}}\\\endfoot",
             r"\bottomrule\endlastfoot"]
    for entry in entries:
        day = date.fromisoformat(entry["tanggal"])
        day_label = f"{day.day} {MONTHS[day.month]}" + r"\newline " + str(day.year)
        lines.append(day_label + " & " + escape_tex(entry["kegiatan"]) + " & " + escape_tex(entry["hasil"]) + r"\\[4pt]")
        lines.append(r"\midrule")
    lines.extend([r"\end{longtable}", r"\endgroup", ""])
    return "\n".join(lines).encode()


def write_if_changed(path, content):
    path.parent.mkdir(exist_ok=True)
    if not path.exists() or path.read_bytes() != content:
        temporary = path.with_suffix(path.suffix + ".tmp")
        temporary.write_bytes(content)
        temporary.replace(path)


def main():
    entries_raif = load_entries("data/logbook_raif.json")
    rows_raif = [HEADERS] + [(entry["tanggal"], entry["kegiatan"], entry["hasil"]) for entry in entries_raif]
    output_raif = io.StringIO(newline="")
    csv.writer(output_raif).writerows(rows_raif)
    write_if_changed(ROOT / "deliverables/logbook_raif.csv", output_raif.getvalue().encode("utf-8-sig"))
    complete_raif = [HEADERS] + [row for entry, row in zip(entries_raif, rows_raif[1:]) if entry["status"] != "perlu_dilengkapi"]
    pending_raif = [HEADERS] + [row for entry, row in zip(entries_raif, rows_raif[1:]) if entry["status"] == "perlu_dilengkapi"]
    instructions_raif = [("Petunjuk penggunaan",), ("Impor hanya sheet Template Logbook; sheet Perlu Dilengkapi bukan data final.",),
                         ("Tanggal menggunakan YYYY-MM-DD. Kegiatan dan Hasil maksimal 1024 karakter masing-masing.",),
                         ("Entri 25 Agustus direkonstruksi dari perubahan kode milik mahasiswa. Tinjau sebelum mengunggah.",),
                         ("Periksa kembali semua entri sebelum impor. Tanggal yang sudah ada pada portal jangan diimpor ulang.",)]
    write_if_changed(ROOT / "deliverables/logbook_raif.xlsx", xlsx([
        ("Template Logbook", complete_raif, True), ("Perlu Dilengkapi", pending_raif, True), ("Petunjuk", instructions_raif, False)]))
    write_if_changed(ROOT / "deliverables/template_logbook_frederiko.xlsx", xlsx([
        ("Template Logbook", [HEADERS], True),
        ("Petunjuk", [("Logbook Frederiko Eldad Mugiyono (13523147)",), ("Isi satu baris setiap hari; jangan memasukkan kegiatan Ra'if sebagai kegiatan sendiri.",),
                      ("Kolom: Tanggal (YYYY-MM-DD), Kegiatan, Hasil. Maksimal 1024 karakter per kegiatan dan hasil.",)], False)]))
    write_if_changed(ROOT / "generated/logbook_raif.tex", tex(entries_raif, "Logbook kegiatan Muhammad Ra'if Alkautsar", "tab:logbook-raif"))
    print(f"Logbook Ra'if: {len(entries_raif)} entri; {len(complete_raif)-1} siap ditinjau untuk impor, {len(pending_raif)-1} belum lengkap.")

    frederiko_json = ROOT / "data/logbook_frederiko.json"
    if frederiko_json.exists():
        entries_frederiko = load_entries("data/logbook_frederiko.json")
        rows_frederiko = [HEADERS] + [(entry["tanggal"], entry["kegiatan"], entry["hasil"]) for entry in entries_frederiko]
        output_frederiko = io.StringIO(newline="")
        csv.writer(output_frederiko).writerows(rows_frederiko)
        write_if_changed(ROOT / "deliverables/logbook_frederiko.csv", output_frederiko.getvalue().encode("utf-8-sig"))
        instructions_frederiko = [("Petunjuk penggunaan",),
                                  ("Logbook Frederiko Eldad Mugiyono (13523147)",),
                                  ("Tanggal menggunakan YYYY-MM-DD. Kegiatan dan Hasil maksimal 1024 karakter masing-masing.",)]
        write_if_changed(ROOT / "deliverables/logbook_frederiko.xlsx", xlsx([
            ("Template Logbook", rows_frederiko, True), ("Petunjuk", instructions_frederiko, False)]))
        write_if_changed(ROOT / "generated/logbook_frederiko.tex", tex(entries_frederiko, "Logbook kegiatan Frederiko Eldad Mugiyono", "tab:logbook-frederiko"))
        print(f"Logbook Frederiko: {len(entries_frederiko)} entri berhasil diproses.")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError) as error:
        print(f"Data logbook tidak valid: {error}", file=sys.stderr)
        sys.exit(1)
