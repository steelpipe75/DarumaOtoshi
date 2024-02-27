import os
import shutil
import re
from html.parser import HTMLParser

# HTMLをパースするためのクラスを定義
class indexHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.link_targets = []
        self.data_list = []
        self.data_append_required = False

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        outputfile.write('<' + tag)
        for attr in attrs:
            # print("  Attribute:", attr)
            outputfile.write(' ' + attr[0] + "='" + attr[1] + "'")
        if tag == 'a':
            link_target = attrs[0][1]
            pattern = r"^coverage/"
            if re.search(pattern, link_target):
                self.link_targets.append(link_target)
                self.data_append_required = True
            outputfile.write('>')
        else:
            outputfile.write('>\n')

    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        outputfile.write('</' + tag + '>\n')

    def handle_data(self, data):
        # print("Data     :", data)
        outputfile.write(data)
        if self.data_append_required:
            self.data_list.append(data)
        self.data_append_required = False

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
    parser = indexHTMLParser()
    parser.feed(html)
    parser.close()

    print(parser.link_targets)
    print(parser.data_list)

