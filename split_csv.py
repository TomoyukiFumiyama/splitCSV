#!/usr/bin/env python3
import csv
import os
import argparse


def split_csv(input_path: str, rows_per_file: int, outdir: str, encoding: str, newline: str = "") -> None:
    # 分割行数のバリデーション
    if rows_per_file <= 0:
        raise ValueError("--rows は 1 以上の整数を指定してください。")

    # 出力先ディレクトリを作成（存在してもOK）
    os.makedirs(outdir, exist_ok=True)

    # 入力ファイル名から出力ファイル名のベースを作成
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    ext = ext if ext else ".csv"

    def out_path(index: int) -> str:
        # 出力ファイル名: <元ファイル名>_part01.csv のように採番
        return os.path.join(outdir, f"{name}_part{index:02d}{ext}")

    # newline="" は csv モジュール推奨（改行の二重化を避ける）
    with open(input_path, "r", encoding=encoding, newline=newline) as f:
        reader = csv.reader(f)

        # 1行目（ヘッダー）を取得
        try:
            header = next(reader)
        except StopIteration:
            raise ValueError("入力CSVが空です。ヘッダー行を含むCSVを指定してください。")

        file_index = 1               # 出力ファイル番号（1始まり）
        rows_in_current = 0          # 現在の出力ファイルに書き込んだデータ行数（ヘッダー除く）

        # 最初の出力ファイルを開いてヘッダーを書き込む
        out_f = open(out_path(file_index), "w", encoding=encoding, newline=newline)
        writer = csv.writer(out_f)
        writer.writerow(header)

        try:
            for row in reader:
                # 指定行数に到達したら、新しいファイルへ切り替える
                if rows_in_current >= rows_per_file:
                    out_f.close()
                    file_index += 1
                    rows_in_current = 0

                    out_f = open(out_path(file_index), "w", encoding=encoding, newline=newline)
                    writer = csv.writer(out_f)
                    writer.writerow(header)

                # 1行書き込み
                writer.writerow(row)
                rows_in_current += 1
        finally:
            # 例外が起きてもファイルを確実に閉じる
            out_f.close()

    print(f"完了: {file_index} 個のファイルを作成しました（出力先: {outdir}）")


def main():
    parser = argparse.ArgumentParser(
        description="CSVを指定行数ごとに分割し、各ファイルにヘッダーを付与して出力します。"
    )
    parser.add_argument("input", help="入力CSVのパス")
    parser.add_argument(
        "--rows",
        type=int,
        default=2000,
        help="1ファイルあたりのデータ行数（ヘッダー除く）。デフォルト: 2000"
    )
    parser.add_argument(
        "--outdir",
        default=None,
        help="出力先ディレクトリ。未指定の場合は <入力CSVのディレクトリ>/split"
    )
    parser.add_argument(
        "--encoding",
        default="utf-8-sig",
        help="ファイルの文字コード。デフォルト: utf-8-sig（Excel系CSVで扱いやすい）"
    )
    args = parser.parse_args()

    input_path = os.path.abspath(args.input)

    # 入力ファイル存在チェック
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_path}")

    # 出力先が未指定なら <入力CSVのディレクトリ>/split
    outdir = args.outdir
    if outdir is None:
        outdir = os.path.join(os.path.dirname(input_path), "split")

    split_csv(input_path=input_path, rows_per_file=args.rows, outdir=outdir, encoding=args.encoding)


if __name__ == "__main__":
    main()
