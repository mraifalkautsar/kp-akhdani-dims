"""Build otomatis dan pratinjau PDF lokal, tanpa menyajikan sumber/referensi."""

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import subprocess
import threading
import time
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
STOP = threading.Event()
LOCK = threading.Lock()
STATE = {"building": True, "success": None, "updated": None}

PAGE = """<!doctype html>
<html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>Pratinjau dokumen KP</title>
<style>
body{margin:0;font:15px system-ui;background:#eee;color:#222}
header{padding:12px 20px;background:white;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
button,a{font:inherit}button{padding:6px 12px;cursor:pointer}
#status{margin-left:auto}iframe{display:block;border:0;width:100%;height:calc(100vh - 68px)}
</style>
<header><strong>Dokumen KP · Draf</strong>
<button onclick="select('main')">Laporan</button><button onclick="select('tor')">ToR</button>
<a id="download" href="/main.pdf" target="_blank">Buka PDF</a>
<a href="/build.log" target="_blank">Log build</a><span id="status">Menyiapkan build…</span></header>
<iframe title="Pratinjau PDF" id="pdf"></iframe>
<script>
let selected='main', versions={}, shown={};
function select(name){selected=name;document.getElementById('download').href='/'+name+'.pdf';show(true)}
function show(force=false){
 const version=versions[selected];
 if(version&&(force||shown[selected]!==version)){
  document.getElementById('pdf').src='/'+selected+'.pdf?v='+version;
  shown[selected]=version;
 }
}
async function update(){try{
 const response=await fetch('/status.json',{cache:'no-store'});const state=await response.json();
 document.getElementById('status').textContent=state.building?'Sedang build…':
  state.success?'Build berhasil · '+new Date(state.updated*1000).toLocaleTimeString():
  'Build gagal · lihat log';
 versions=state.versions;show();
}catch{document.getElementById('status').textContent='Server tidak terhubung'} }
update();setInterval(update,1500);
</script></html>"""


def snapshot():
    files = [ROOT / ".latexmkrc", ROOT / "Makefile", *ROOT.glob("*.tex")]
    for directory in ("frontmatter", "chapters", "backmatter", "appendices", "shared", "figures", "data", "scripts"):
        files.extend(p for p in (ROOT / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    result = {}
    for path in files:
        try:
            stat = path.stat()
            result[str(path)] = (stat.st_mtime_ns, stat.st_size)
        except FileNotFoundError:
            pass
    return result


def status():
    with LOCK:
        result = dict(STATE)
    # Tampilkan versi hanya setelah build selesai agar browser tidak membaca PDF parsial.
    result["versions"] = {}
    if not result["building"]:
        for name in ("main", "tor"):
            path = ROOT / f"{name}.pdf"  # salinan dari build terakhir yang berhasil
            if path.is_file():
                result["versions"][name] = str(path.stat().st_mtime_ns)
    return result


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlsplit(self.path).path
        if route == "/":
            body, mime = PAGE.encode(), "text/html; charset=utf-8"
        elif route == "/status.json":
            body, mime = json.dumps(status()).encode(), "application/json"
        elif route in ("/main.pdf", "/tor.pdf", "/build.log"):
            path = BUILD / "preview.log" if route == "/build.log" else ROOT / route[1:]
            try:
                body = path.read_bytes()
            except FileNotFoundError:
                self.send_error(404, "PDF belum tersedia; periksa status build.")
                return
            mime = "text/plain; charset=utf-8" if route == "/build.log" else "application/pdf"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *_):
        pass


def build():
    BUILD.mkdir(exist_ok=True)
    with LOCK:
        STATE["building"] = True
    print("Membangun laporan dan ToR…", flush=True)
    with (BUILD / "preview.log").open("w") as log:
        process = subprocess.Popen(["make", "build"], cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        try:
            while process.poll() is None and not STOP.wait(0.2):
                pass
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
    with LOCK:
        STATE.update(building=False, success=process.returncode == 0, updated=time.time())
    print("Build berhasil." if process.returncode == 0 else "Build gagal. Lihat log pada halaman pratinjau.", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    except OSError as error:
        parser.exit(1, f"Tidak dapat membuka port {args.port}: {error}. Coba PORT lain.\n")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    signal.signal(signal.SIGTERM, lambda *_: STOP.set())
    print(f"Pratinjau: http://127.0.0.1:{args.port} — Ctrl+C untuk berhenti.", flush=True)
    previous = None
    try:
        while not STOP.is_set():
            current = snapshot()
            if current != previous:
                previous = current
                build()
            STOP.wait(0.7)
    except KeyboardInterrupt:
        pass
    finally:
        STOP.set()
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
