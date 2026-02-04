````markdown
# CSV Splitter (split_csv.py)

大容量CSVを、指定行数ごとに複数ファイルへ分割するスクリプトです。  
**ヘッダー（1行目）を保持**し、分割後の各CSVにもヘッダーを付与します。  
macOS の **Python3**（標準ライブラリのみ）で動作します。

---

## できること

- CSVを **N行ごと**に分割（デフォルト：2000行）
- **ヘッダーを保持**（各ファイル先頭に同じヘッダーを出力）
- 大きいCSVでも、**1行ずつ読み書き**するためメモリ消費が少ない

---

## 動作環境

- macOS
- Python 3.x（推奨：3.8+）
- 追加ライブラリ不要

Pythonの確認：

```bash
python3 --version
````

---

## ファイル構成（例）

```
.
├── split_csv.py
└── README.md
```

---

## 使い方

### 1) 実行（デフォルト設定）

```bash
python3 split_csv.py /path/to/input.csv
```

* `input.csv` と同じディレクトリ内に `split/` フォルダを作成し、そこへ出力します
* 分割単位は **2000行**（ヘッダー除く）

出力例：

```
split/
├── input_part01.csv
├── input_part02.csv
├── input_part03.csv
├── input_part04.csv
└── input_part05.csv
```

---

## オプション

### 行数を変更する（例：2000行）

```bash
python3 split_csv.py input.csv --rows 2000
```

### 出力先ディレクトリを指定する

```bash
python3 split_csv.py input.csv --outdir ./out
```

### エンコーディングを指定する

```bash
python3 split_csv.py input.csv --encoding utf-8
```

> デフォルトは `utf-8-sig` です（Excel系のCSVで文字化けしにくい）。

---

## よくある注意点

* **ヘッダーありCSV前提**です（1行目をヘッダーとして扱います）
* 1万行のCSVを `--rows 2000` で分割すると、基本的に **5ファイル**になります
  端数がある場合は最後のファイルだけ少なくなります
* ファイルが空の場合はエラーになります

---

## トラブルシューティング

### Permission denied / 実行権限のエラー

基本は `python3 split_csv.py ...` でOKです。
直接実行したい場合は権限付与：

```bash
chmod +x split_csv.py
./split_csv.py input.csv
```

### 文字化けする

エンコーディングを切り替えて試してください：

```bash
python3 split_csv.py input.csv --encoding utf-8
python3 split_csv.py input.csv --encoding cp932
```

---

## ライセンス

必要に応じて追記してください（例：MIT / Proprietary など）。

```


