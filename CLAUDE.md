# Portfolio Project

職務経歴書・スキルシート・自己PRを管理するマークダウンベースのポートフォリオ。
Excelスキルシートの変換、マークダウン整形、案件番号管理を自動化。

## Tech Stack

| カテゴリ | ツール |
|---------|--------|
| ドキュメント | Markdown (.md) |
| データ変換 | Python 3 (pandas, openpyxl, tabulate) |
| リンティング | ESLint + eslint-plugin-markdown |
| パッケージ管理 | pnpm 9.x |
| コード解析 | Serena (Python LSP) |

## Structure

```
portfolio/
├── *.md                    # 職務経歴書、スキルシート、自己PR、案件情報
├── *.py                    # 変換・整形スクリプト群
│   ├── excel_to_markdown.py       # Excel→MD変換（単一/全シート対応）
│   ├── format_skill_sheet_final.py # テーブル整形（nan/NaT除去、空列削除）
│   ├── final_format_skill_sheet.py # 最終整形（空行正規化、列揃え）
│   ├── fix_numbers.py              # 案件番号修正（年月ベースマッピング）
│   └── update_numbers.py           # 案件番号一括リナンバリング
├── data/                   # Cipherセッションデータ
├── old/                    # アーカイブ（空）
├── requirements.txt        # Python依存: pandas, openpyxl, tabulate
├── package.json            # ESLint依存
├── eslint.config.js        # MD内コードブロック検査設定
└── .serena/project.yml     # Serena設定（Python LSP, UTF-8）
```

## Commands

```bash
# セットアップ
pip install -r requirements.txt
pnpm install

# Excel変換
python excel_to_markdown.py スキルシート_O.T_42.xlsx           # 単一シート→MD
python excel_to_markdown.py スキルシート_O.T_42.xlsx -m        # 全シート→個別MD
python excel_to_markdown.py スキルシート_O.T_42.xlsx -s "シート名" -o output.md

# スキルシート整形パイプライン（順序重要）
python format_skill_sheet_final.py   # Step1: nan/NaT除去、空行削除
python final_format_skill_sheet.py   # Step2: 空列削除、列揃え、最終整形

# 案件番号管理
python fix_numbers.py                # 職務経歴書.mdの番号を年月ベースで修正
python update_numbers.py             # 番号を+1でリナンバリング（案件追加時）

# リント
npx eslint .                         # MD内コードブロック検査
```

## Workflows

### スキルシート更新フロー
1. `.xlsx` ファイルを更新
2. `python excel_to_markdown.py *.xlsx -m` で全シートMD変換
3. `python format_skill_sheet_final.py` → `python final_format_skill_sheet.py` で整形
4. 差分確認後コミット

### 案件追加フロー
1. `python update_numbers.py` で既存番号を+1シフト
2. 職務経歴書.mdの先頭に新案件を `| 1 |` で追加
3. `python fix_numbers.py` で番号整合性チェック

## Gotchas

- **整形スクリプトの実行順序**: `format_skill_sheet_final.py` → `final_format_skill_sheet.py` の順。逆にすると空列が残る
- **Pythonスクリプトのハードコードパス**: `fix_numbers.py`, `update_numbers.py`, `format_*` は入力ファイル名がスクリプト内に固定（`スキルシート_O.T_42.md`, `職務経歴書.md`）。別ファイルには引数対応の `excel_to_markdown.py` を使用
- **pandas出力の nan/NaT**: Excel変換後のMDに `nan` `NaT` 文字列が残る。整形スクリプトで除去される
- **ESLint対象**: `.md` ファイル内のコードブロックのみ。マークダウン本文は検査対象外
- **`.gitignore`対象**: `スキルシート_O.T_42.xlsx`（元データ）、`ランサーズ.md`、`ROSCA.md`
- **エンコーディング**: 全ファイルUTF-8。Windows環境ではBOM無しを維持

## Git Conventions

- ブランチ: `main` 直接（個人プロジェクト）
- コミットメッセージ: 日本語、変更内容の要約

## MCP Integration

[byterover-mcp]
- `byterover-store-knowledge`: パターン・解決策を学習時に保存
- `byterover-retrieve-knowledge`: タスク開始時にコンテキスト取得
