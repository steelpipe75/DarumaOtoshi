from html.parser import HTMLParser

# HTMLをパースするためのクラスを定義
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        # print("Start tag:", tag)
        outputfile.write('<' + tag)
        for attr in attrs:
            print("  Attribute:", attr)
            outputfile.write(' ' + attr[0] + "='" + attr[1] + "'")
        outputfile.write('>\n')

    def handle_endtag(self, tag):
        # print("End tag  :", tag)
        outputfile.write('</' + tag + '>\n')

    def handle_data(self, data):
        # print("Data     :", data)
        outputfile.write(data + '\n')

# HTMLを取得
html = ""
with open(r'./output.html', 'w', encoding='utf-8') as outputfile:
    with open(r'./tests/bowling_game_cli/index.html', 'r', encoding='utf-8') as inputfile:
        html = inputfile.read()
        # print(html)

    outputfile.write('<!doctype html>\n')

    # HTMLをパース
    parser = MyHTMLParser()
    parser.feed(html)
    parser.close()

