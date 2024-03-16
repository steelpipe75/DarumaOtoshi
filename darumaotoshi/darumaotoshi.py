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
        self, *, convert_charrefs: bool = True
    ) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.__files = []
        self.__file_info = {"href": "", "data": ""}
        self.__append_required = False
        self.__outputstr = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        # print("Start tag:", tag)
        self.__outputstr += ("<" + tag)
        if tag == "a":
            link_target = attrs[0][1]
            pattern = r"^coverage/"
            if re.search(pattern, link_target):
                self.__file_info["href"] = link_target
                self.__append_required = True
            else:
                for attr in attrs:
                    # print("  Attribute:", attr)
                    self.__outputstr += (" " + attr[0] + "='" + attr[1] + "'")
                self.__outputstr += (">")
        else:
            for attr in attrs:
                # print("  Attribute:", attr)
                self.__outputstr += (" " + attr[0] + "='" + attr[1] + "'")
            self.__outputstr += (">")

    def handle_endtag(self, tag: str) -> None:
        # print("End tag  :", tag)
        self.__outputstr += ("</" + tag + ">")

    def handle_data(self, data: str) -> None:
        # print("Data     :", data)
        if self.__append_required:
            self.__file_info["data"] = data
            self.__files.append(self.__file_info)
            cov_html_path = os.path.normpath(
                os.path.join("coverage", data + ".html")
            ).replace("\\", "/")
            print(cov_html_path)
            self.__outputstr += (" href" + "='" + cov_html_path + "'>")
        self.__append_required = False
        self.__file_info = {"href": "", "data": ""}
        self.__outputstr += (html.escape(data))

    def get_files(self) -> str:
        return self.__files

    def get_outputstr(self) -> str:
        return self.__outputstr


# 各ソースのカバレッジデータhtmlをパースするためのクラスを定義
class coverageHTMLParser(HTMLParser):
    def __init__(
        self, css_path: str, *, convert_charrefs: bool = True
    ) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.__outputstr = ""
        self.__css_path = css_path

    def handle_starttag(self, tag: str, attrs) -> None:
        # print("Start tag:", tag)
        if tag == "link":
            self.__outputstr += ("<" + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                if attr[0] == "href":
                    self.__outputstr += (" " + "href" + "='" + self.__css_path + "'")
                else:
                    self.__outputstr += (" " + attr[0] + "='" + attr[1] + "'")
            self.__outputstr += (">")
        else:
            self.__outputstr += ("<" + tag)
            for attr in attrs:
                # print("  Attribute:", attr)
                self.__outputstr += (" " + attr[0] + "='" + attr[1] + "'")
            self.__outputstr += (">")

    def handle_endtag(self, tag: str) -> None:
        # print("End tag  :", tag)
        self.__outputstr += ("</" + tag + ">")

    def handle_data(self, data: str) -> None:
        self.__outputstr += (html.escape(data))

    def get_outputstr(self) -> str:
        return self.__outputstr


def copy_coverage_html(
    src_path: str, dst_path: str,
    output_style_css_path: str,
    pretty_print
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
            cov_parser = coverageHTMLParser(css_path)
            cov_parser.feed(src_html)
            outputstr = cov_parser.get_outputstr()
            if pretty_print:
                soup = BeautifulSoup(outputstr, 'html.parser')
                outputstr = soup.prettify()
            dst_file.write(outputstr)
            cov_parser.close()


def darumaotoshi(input_index_html: str, output_dir: str, pretty_print=False) -> None:
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
    print("src_path = " + src_path)
    print("dst_path = " + dst_path)
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
            # soup = BeautifulSoup(html_str, 'html.parser')
            # print(soup.prettify())

        outputfile.write("<!doctype html>")

        # HTMLをパース
        parser = indexHTMLParser()
        parser.feed(html_str)
        outputstr = parser.get_outputstr()
        if pretty_print:
            soup = BeautifulSoup(outputstr, 'html.parser')
            outputstr = soup.prettify()
        outputfile.write(outputstr)
        parser.close()

    # print(parser.files)

    for file_info in parser.get_files():
        src_path = os.path.normpath(
            (os.path.join(input_dir, file_info["href"])).replace("\\", "/")
        )
        cov_html = os.path.join("coverage", file_info["data"] + ".html")
        dst_path = os.path.normpath(
            (os.path.join(output_dir, cov_html)).replace("\\", "/")
        )
        print("### " + src_path + " -> " + dst_path)
        copy_coverage_html(src_path, dst_path, output_style_css_path, pretty_print)


if __name__ == "__main__":
    darumaotoshi("tests/data/c_cmake/bowling_game_cli/index.html", "output/", True)
