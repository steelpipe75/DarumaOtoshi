import html
import os
import re
import shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup
from io import TextIOWrapper


# index.htmlをパースするためのクラスを定義
class indexHTMLParser(HTMLParser):
    def __init__(
        self, out: TextIOWrapper,
        *, convert_charrefs: bool = True
    ) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.files = []
        self.file_info = {"href": "", "data": ""}
        self.append_required = False
        self.out = out

    def handle_starttag(self, tag: str, attrs) -> None:
        # print("Start tag:", tag)
        self.out.write("<" + tag)
        if tag == "a":
            link_target = attrs[0][1]
            pattern = r"^coverage/"
            if re.search(pattern, link_target):
                self.file_info["href"] = link_target
                self.append_required = True
            else:
                for attr in attrs:
                    # print("  Attribute:", attr)
                    self.out.write(" " + attr[0] + "='" + attr[1] + "'")
                self.out.write(">")
        else:
            for attr in attrs:
                # print("  Attribute:", attr)
                self.out.write(" " + attr[0] + "='" + attr[1] + "'")
            self.out.write(">")

    def handle_endtag(self, tag: str) -> None:
        # print("End tag  :", tag)
        self.out.write("</" + tag + ">")

    def handle_data(self, data: str) -> None:
        # print("Data     :", data)
        if self.append_required:
            self.file_info["data"] = data
            self.files.append(self.file_info)
            cov_html_path = os.path.normpath(
                os.path.join("coverage", data + ".html")
            ).replace("\\", "/")
            print(cov_html_path)
            self.out.write(" href" + "='" + cov_html_path + "'>")
        self.append_required = False
        self.file_info = {"href": "", "data": ""}
        self.out.write(html.escape(data))


# 各ソースのカバレッジデータhtmlをパースするためのクラスを定義
class coverageHTMLParser(HTMLParser):
    def __init__(
        self, css_path: str, out: TextIOWrapper,
        *, convert_charrefs: bool = True
    ) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.out = out
        self.css_path = css_path

    def handle_starttag(self, tag: str, attrs) -> None:
        # print("Start tag:", tag)
        if tag == "link":
            self.out.write("<" + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                if attr[0] == "href":
                    self.out.write(" " + "href" + "='" + self.css_path + "'")
                else:
                    self.out.write(" " + attr[0] + "='" + attr[1] + "'")
            self.out.write(">")
        else:
            self.out.write("<" + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                self.out.write(" " + attr[0] + "='" + attr[1] + "'")
            self.out.write(">")

    def handle_endtag(self, tag: str) -> None:
        # print("End tag  :", tag)
        self.out.write("</" + tag + ">")

    def handle_data(self, data: str) -> None:
        self.out.write(html.escape(data))


def copy_coverage_html(
    src_path: str, dst_path: str,
    output_style_css_path: str
) -> None:
    if os.path.exists(src_path):
        dst_dir = os.path.dirname(dst_path)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        # shutil.copy(src_path, dst_path)

        relative_path = os.path.normpath(
            os.path.relpath(output_style_css_path, dst_dir)
        )
        css_path = relative_path.replace("\\", "/")
        # print(css_path)

        with open(dst_path, "w", encoding="utf-8") as dst_file:
            with open(src_path, "r", encoding="utf-8") as src_file:
                src_html = src_file.read()

            dst_file.write("<!doctype html>")

            # HTMLをパース
            cov_parser = coverageHTMLParser(css_path, dst_file)
            cov_parser.feed(src_html)
            cov_parser.close()


def darumaotoshi(input_index_html: str, output_dir: str) -> None:
    input_index_html = os.path.normpath(input_index_html.replace("\\", "/"))

    input_dir = os.path.dirname(input_index_html)
    # print(input_dir)

    os.makedirs(output_dir, exist_ok=True)
    src_path = os.path.normpath(
        (os.path.join(input_dir, "style.css")).replace("\\", "/")
    )
    dst_path = os.path.normpath(
        (os.path.join(output_dir, "style.css")).replace("\\", "/")
    )
    print("*** " + src_path + " -> " + dst_path)
    shutil.copy(src_path, dst_path)

    output_style_css_path = os.path.normpath(
        (os.path.join(output_dir, "style.css")).replace("\\", "/")
    )
    # print(output_style_css_path)
    output_index_html = os.path.normpath(
        (os.path.join(output_dir, "index.html")).replace("\\", "/")
    )
    # print(output_index_html)
    print("@@@ " + input_index_html + " -> " + output_index_html)
    with open(output_index_html, "w", encoding="utf-8") as outputfile:
        with open(input_index_html, "r", encoding="utf-8") as inputfile:
            html_str = inputfile.read()
            # print(html_str)
            soup = BeautifulSoup(html_str, 'html.parser')
            print(soup.prettify())

        outputfile.write("<!doctype html>")

        # HTMLをパース
        parser = indexHTMLParser(outputfile)
        parser.feed(html_str)
        parser.close()

    # print(parser.files)

    for file_info in parser.files:
        src_path = os.path.normpath(
            (os.path.join(input_dir, file_info["href"])).replace("\\", "/")
        )
        cov_html = os.path.join("coverage", file_info["data"] + ".html")
        dst_path = os.path.normpath(
            (os.path.join(output_dir, cov_html)).replace("\\", "/")
        )
        print("### " + src_path + " -> " + dst_path)
        copy_coverage_html(src_path, dst_path, output_style_css_path)


if __name__ == "__main__":
    darumaotoshi("tests/data/c_cmake/bowling_game_cli/index.html", "output/")
