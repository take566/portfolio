# 推奨コマンド集

## セットアップ
```bash
# 依存関係のインストール
pip install -r requirements.txt

# または個別インストール
pip install pandas openpyxl tabulate
```

## Excel to Markdown変換
```bash
# 基本的な変換（最初のシート）
python excel_to_markdown.py data.xlsx

# 特定のシートを変換
python excel_to_markdown.py data.xlsx -s "Sheet2"

# 出力ファイル名を指定
python excel_to_markdown.py data.xlsx -o output.md

# 全シートを個別ファイルに変換
python excel_to_markdown.py data.xlsx -m

# 全シートを指定ディレクトリに変換
python excel_to_markdown.py data.xlsx -m -d output_folder
```

## Windows固有コマンド
```bash
# ディレクトリ一覧
dir

# ファイル検索
dir *.py /s

# 現在のディレクトリ
pwd

# ディレクトリ移動
cd directory_name
```

## Git操作
```bash
git status
git add .
git commit -m "message"
git push
```