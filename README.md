# DarumaOtoshi

llvm-cov show -format=html 出力の余分なフォルダを削除する

```
usage: darumaotoshi [-h] [-o OUTPUT_DIR] [-p] [-f] [-e] [-v] input_file

Remove excess folders from the output of 'llvm-cov show -format=html'.

positional arguments:
  input_file            input HTML file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output OUTPUT_DIR
                        output directory
  -p, --pretty_print    pretty print
  -f, --flat            flat
  -e, --embedded_css    embedded css
  -v, --verbose         verbose
```
