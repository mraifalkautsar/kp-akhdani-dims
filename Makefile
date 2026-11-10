.DEFAULT_GOAL := build
PYTHON ?= python3
LATEXMK ?= latexmk
PORT ?= 8000

.PHONY: build report tor generate doctor check preview watch clean help

build: report tor

doctor:
	@$(PYTHON) scripts/check_dependencies.py

generate:
	$(PYTHON) scripts/build_document.py assets

report: doctor
	$(PYTHON) scripts/build_document.py main --latexmk "$(LATEXMK)"

tor: doctor
	$(PYTHON) scripts/build_document.py tor --latexmk "$(LATEXMK)"

check: build
	$(PYTHON) scripts/build_document.py check

preview:
	$(PYTHON) scripts/preview.py --port $(PORT)

watch: preview

clean:
	@$(PYTHON) scripts/build_document.py clean

help:
	@echo 'make           Build laporan dan ToR (build/main.pdf, build/tor.pdf)'
	@echo 'make preview   Buka localhost:8000; build ulang dan segarkan PDF saat sumber berubah'
	@echo 'make report    Build laporan saja'
	@echo 'make tor       Build ToR saja'
	@echo 'make generate  Perbarui CSV, Excel, dan lampiran dari sumber data logbook'
	@echo 'make check     Build dan periksa PDF serta referensi silang'
	@echo 'make doctor    Periksa dependensi LaTeX'
	@echo 'make clean     Hapus cache build; salinan PDF pada root tetap tersedia'
