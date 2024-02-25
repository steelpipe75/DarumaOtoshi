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
html = "<html><body><p>Hello, World!</p></body></html>"

# HTMLをパース
parser = MyHTMLParser()
parser.feed(html)
parser.close()

