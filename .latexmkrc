# Dipakai oleh build lokal dan GitHub Actions.
$pdf_mode = 1;
$out_dir = 'build';
$aux_dir = 'build';
$pdflatex = 'pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 %O %S';
$max_repeat = 6;
$recorder = 1;
