from html.parser import HTMLParser

# HTMLをパースするためのクラスを定義
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Start tag:", tag)
        for attr in attrs:
            print("  Attribute:", attr)

    def handle_endtag(self, tag):
        print("End tag  :", tag)

    def handle_data(self, data):
        print("Data     :", data)

# HTMLを取得
html = ""
with open(r'./tests/bowling_game_cli/index.html', 'r', encoding='utf-8') as file:
    html = file.read()
    print(html)

# HTMLをパース
parser = MyHTMLParser()
parser.feed(html)
parser.close()

