# エクセルファイルをMarkdownに変換するスクリプト

このスクリプトは、Excelファイル（.xlsx, .xls）をMarkdown形式に変換するPythonツールです。

## 機能

- 単一シートの変換
- 全シートの個別ファイル変換
- 日本語対応
- カスタム出力ファイル名指定
- 特定シートの指定変換

## インストール

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

または個別にインストール：

```bash
pip install pandas openpyxl tabulate
```

## 使用方法

### 基本的な使用方法

```bash
python excel_to_markdown.py ファイル名.xlsx
```

### オプション

- `-o, --output`: 出力ファイル名を指定
- `-s, --sheet`: 特定のシート名を指定
- `-m, --multi`: 全シートを個別ファイルに変換
- `-d, --output-dir`: 出力ディレクトリを指定（--multi使用時）

### 使用例

#### 1. 基本的な変換（最初のシート）
```bash
python excel_to_markdown.py data.xlsx
```

#### 2. 特定のシートを変換
```bash
python excel_to_markdown.py data.xlsx -s "Sheet2"
```

#### 3. 出力ファイル名を指定
```bash
python excel_to_markdown.py data.xlsx -o output.md
```

#### 4. 全シートを個別ファイルに変換
```bash
python excel_to_markdown.py data.xlsx -m
```

#### 5. 全シートを指定ディレクトリに変換
```bash
python excel_to_markdown.py data.xlsx -m -d output_folder
```

## 出力形式

生成されるMarkdownファイルは以下の形式になります：

```markdown
# ファイル名

## シート: シート名

| 列1 | 列2 | 列3 |
|-----|-----|-----|
| データ1 | データ2 | データ3 |
| ... | ... | ... |
```

## 対応ファイル形式

- Excel 2007以降 (.xlsx)
- Excel 97-2003 (.xls)

## 注意事項

- 日本語のファイル名・シート名に対応しています
- 大きなファイルの場合、処理に時間がかかる場合があります
- 出力ファイルはUTF-8エンコーディングで保存されます

## トラブルシューティング

### よくあるエラー

1. **FileNotFoundError**: 指定したExcelファイルが見つからない
   - ファイルパスが正しいか確認してください

2. **ModuleNotFoundError**: 必要なライブラリがインストールされていない
   - `pip install -r requirements.txt` を実行してください

3. **PermissionError**: 出力ファイルに書き込み権限がない
   - 出力先のディレクトリの権限を確認してください

