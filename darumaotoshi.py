import os
import shutil
import re
import html
from html.parser import HTMLParser

# index.htmlをパースするためのクラスを定義
class indexHTMLParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.files = []
        self.file_info = { 'href':'', 'data':'' }
        self.append_required = False

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        outputfile.write('<' + tag)
        if tag == 'a':
            link_target = attrs[0][1]
            pattern = r"^coverage/"
            if re.search(pattern, link_target):
                self.file_info['href'] = link_target
                self.append_required = True
            else:
                for attr in attrs:
                    # print("  Attribute:", attr)
                    outputfile.write(' ' + attr[0] + "='" + attr[1] + "'")
                outputfile.write('>')
        else:
            for attr in attrs:
                # print("  Attribute:", attr)
                outputfile.write(' ' + attr[0] + "='" + attr[1] + "'")
            outputfile.write('>')

    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        outputfile.write('</' + tag + '>')

    def handle_data(self, data):
        # print("Data     :", data)
        if self.append_required:
            self.file_info['data'] = data
            self.files.append(self.file_info)
            outputfile.write(' href' + "='" + os.path.normpath(os.path.join('coverage', data) + ".html'>").replace('\\', '/'))
        self.append_required = False
        self.file_info = { 'href':'', 'data':'' }
        outputfile.write(html.escape(data))


# 各ソースのカバレッジデータhtmlをパースするためのクラスを定義
class coverageHTMLParser(HTMLParser):
    def __init__(self, css_path: str, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.convert_str = ''
        self.css_path = css_path

    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        if tag == 'link':
            self.convert_str += ('<' + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                if attr[0] == 'href':
                    self.convert_str += (' ' + 'href' + "='" + self.css_path + "'")
                else:
                    self.convert_str += (' ' + attr[0] + "='" + attr[1] + "'")
            self.convert_str += ('>')
        else:
            self.convert_str += ('<' + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                self.convert_str += (' ' + attr[0] + "='" + attr[1] + "'")
            self.convert_str += ('>')

    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        self.convert_str += ('</' + tag + '>')

    def handle_data(self, data):
        self.convert_str += html.escape(data)



def copy_coverage_html(src_path: str, dst_path: str):
    if os.path.exists(src_path):
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        # shutil.copy(src_path, dst_path)

        relative_path = os.path.normpath(os.path.relpath(output_style_css, dst_dir))
        css_path = relative_path.replace('\\', '/')
        print(css_path)

        with open(dst_path, 'w', encoding='utf-8') as dst_file:
            with open(src_path, 'r', encoding='utf-8') as src_file:
                src_html = src_file.read()

            dst_file.write('<!doctype html>\n')

            # HTMLをパース
            cov_parser = coverageHTMLParser(css_path = css_path)
            cov_parser.feed(src_html)
            cov_parser.close()
            # print(cov_parser.convert_str)
            dst_file.write(cov_parser.convert_str)



# HTMLを取得
html_str = ''
input_index_html = './tests/bowling_game_cli/index.html'
input_dir = os.path.dirname(input_index_html)
# print(input_dir)

output_dir = './output'
os.makedirs(output_dir, exist_ok=True)
src_path = os.path.normpath((os.path.join(input_dir, 'style.css')).replace('\\', '/'))
dst_path = os.path.normpath((os.path.join(output_dir, 'style.css')).replace('\\', '/'))
print('*** ' + src_path + ' -> ' + dst_path)
ret = shutil.copy(src_path, dst_path)

output_style_css = os.path.join(output_dir, 'style.css')
# print(output_style_css)
output_index_html = os.path.join(output_dir, 'index.html')
# print(output_index_html)
with open(output_index_html, 'w', encoding='utf-8') as outputfile:
    with open(input_index_html, 'r', encoding='utf-8') as inputfile:
        html_str = inputfile.read()
        # print(html_str)

    outputfile.write('<!doctype html>\n')

    # HTMLをパース
    parser = indexHTMLParser()
    parser.feed(html_str)
    parser.close()

# print(parser.files)

for file_info in parser.files:
    src_path = os.path.normpath((os.path.join(input_dir, file_info['href'])).replace('\\', '/'))
    dst_path = os.path.normpath((os.path.join(output_dir, os.path.join('coverage', file_info['data'] + '.html'))).replace('\\', '/'))
    print('### ' + src_path + ' -> ' + dst_path)
    copy_coverage_html(src_path, dst_path)
