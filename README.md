# DarumaOtoshi

llvm-cov show -format=html 出力の余分なフォルダを削除する

```
usage: darumaotoshi [-h] [-i INPUT_FILE] [-o OUTPUT_DIR] [-p] [-f] [-e] [-v]

Remove excess folders from the output of 'llvm-cov show -format=html'.

options:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input INPUT_FILE
                        input HTML file
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        output directory
  -p, --pretty_print    pretty print
  -f, --flat            flat
  -e, --embedded_css    embedded css
  -v, --verbose         verbose
```
