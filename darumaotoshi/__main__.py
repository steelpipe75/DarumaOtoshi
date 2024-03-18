import argparse

from darumaotoshi import darumaotoshi


def main():
    input_index_html, output_dir = arg_parse()
    darumaotoshi(input_index_html, output_dir)


def arg_parse():
    parser = argparse.ArgumentParser()

    # 入力HTMLファイルを指定するオプションを追加
    parser.add_argument(
        "-i",
        "--input",
        dest="input_file",
        default="tests/data/c_cmake/bowling_game_cli/index.html",
        help="input HTML file",
    )

    # 出力ディレクトリを指定するオプションを追加
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        default="output",
        help="output directory"
    )

    # コマンドライン引数のパース
    args = parser.parse_args()

    print(f"Processing HTML file: {args.input_file}")
    print(f"Output directory: {args.output_dir}")

    # パースされた引数を使って処理を行う
    return args.input_file, args.output_dir


if __name__ == "__main__":
    main()
