import argparse

from darumaotoshi import darumaotoshi


def main():
    dict_args = arg_parse()
    darumaotoshi(
        dict_args["input_file"],
        dict_args["output_dir"],
        pretty_print=dict_args["pretty_print"],
        flat=dict_args["flat"],
        embedded_css=dict_args["embedded_css"],
        verbose=dict_args["verbose"]
    )


def arg_parse():
    parser = argparse.ArgumentParser(
        prog="darumaotoshi",
        description="Remove excess folders from the output of 'llvm-cov show -format=html'."
    )

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

    parser.add_argument(
        "-p",
        "--pretty_print",
        action="store_true",
        help="pretty print"
    )

    parser.add_argument(
        "-f",
        "--flat",
        action="store_true",
        help="flat"
    )

    parser.add_argument(
        "-e",
        "--embedded_css",
        action="store_true",
        help="embedded css"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="verbose"
    )

    # コマンドライン引数のパース
    args = parser.parse_args()

    if args.verbose:
        print(f"Processing HTML file: {args.input_file}")
        print(f"Output directory: {args.output_dir}")
        print(f"Pretty Print: {args.pretty_print}")
        print(f"Flat: {args.flat}")
        print(f"Embedded CSS: {args.embedded_css}")
        print(f"Verbose: {args.verbose}")

    return {
        "input_file": args.input_file,
        "output_dir": args.output_dir,
        "pretty_print": args.pretty_print,
        "flat": args.flat,
        "embedded_css": args.embedded_css,
        "verbose": args.verbose
    }


if __name__ == "__main__":
    main()
