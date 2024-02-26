import os
import shutil
from html.parser import HTMLParser

# HTMLをパースするためのクラスを定義
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        outputfile.write('<' + tag)
        for attr in attrs:
            # print("  Attribute:", attr)
            outputfile.write(' ' + attr[0] + "='" + attr[1] + "'")
        if tag == 'a':
            outputfile.write('>')
        else:
            outputfile.write('>\n')

    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        outputfile.write('</' + tag + '>\n')

    def handle_data(self, data):
        # print("Data     :", data)
        outputfile.write(data)

def make_dir_helper(target_path):
    if not os.path.exists(target_path):
        os.makedirs(target_path)

# HTMLを取得
html = ''
input_index_html = './tests/bowling_game_cli/index.html'
input_dir = os.path.dirname(input_index_html)
# print(input_dir)

output_dir = './output'
make_dir_helper(output_dir)
ret = shutil.copy(os.path.join(input_dir, 'style.css'), os.path.join(output_dir, 'style.css'))

output_style_css = os.path.join(output_dir, 'style.css')
# print(output_style_css)
output_index_html = os.path.join(output_dir, 'index.html')
# print(output_index_html)
with open(output_index_html, 'w', encoding='utf-8') as outputfile:
    with open(input_index_html, 'r', encoding='utf-8') as inputfile:
        html = inputfile.read()
        # print(html)

    outputfile.write('<!doctype html>\n')

    # HTMLをパース
    parser = MyHTMLParser()
    parser.feed(html)
    parser.close()

