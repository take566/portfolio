#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
エクセルファイルをMarkdownに変換するスクリプト
"""

import pandas as pd
import argparse
import os
import sys
from pathlib import Path


def excel_to_markdown(excel_file, output_file=None, sheet_name=None):
    """
    エクセルファイルをMarkdownに変換する関数
    
    Args:
        excel_file (str): 入力エクセルファイルのパス
        output_file (str): 出力Markdownファイルのパス（省略時は自動生成）
        sheet_name (str): 変換するシート名（省略時は最初のシート）
    
    Returns:
        str: 生成されたMarkdownファイルのパス
    """
    
    try:
        # エクセルファイルの存在確認
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"エクセルファイルが見つかりません: {excel_file}")
        
        # エクセルファイルを読み込み
        if sheet_name:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
        else:
            # シート名が指定されていない場合は最初のシートを読み込み
            excel_data = pd.read_excel(excel_file, sheet_name=None)
            sheet_name = list(excel_data.keys())[0]
            df = excel_data[sheet_name]
        
        print(f"シート '{sheet_name}' を読み込みました")
        print(f"データサイズ: {df.shape[0]} 行 × {df.shape[1]} 列")
        
        # 出力ファイル名の決定
        if output_file is None:
            excel_path = Path(excel_file)
            output_file = excel_path.stem + ".md"
        
        # Markdown形式に変換
        markdown_content = []
        
        # ファイル名をタイトルとして追加
        title = Path(excel_file).stem
        markdown_content.append(f"# {title}\n")
        
        # シート名をサブタイトルとして追加
        markdown_content.append(f"## シート: {sheet_name}\n")
        
        # データフレームをMarkdownテーブルに変換
        markdown_table = df.to_markdown(index=False)
        markdown_content.append(markdown_table)
        
        # ファイルに保存
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(markdown_content))
        
        print(f"Markdownファイルを生成しました: {output_file}")
        return output_file
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return None


def excel_to_markdown_multi_sheet(excel_file, output_dir=None):
    """
    エクセルファイルの全シートを個別のMarkdownファイルに変換する関数
    
    Args:
        excel_file (str): 入力エクセルファイルのパス
        output_dir (str): 出力ディレクトリ（省略時はカレントディレクトリ）
    
    Returns:
        list: 生成されたMarkdownファイルのパスのリスト
    """
    
    try:
        # エクセルファイルの存在確認
        if not os.path.exists(excel_file):
            raise FileNotFoundError(f"エクセルファイルが見つかりません: {excel_file}")
        
        # 出力ディレクトリの設定
        if output_dir is None:
            output_dir = "."
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 全シートを読み込み
        excel_data = pd.read_excel(excel_file, sheet_name=None)
        
        generated_files = []
        
        for sheet_name, df in excel_data.items():
            print(f"シート '{sheet_name}' を処理中...")
            
            # 出力ファイル名の決定
            safe_sheet_name = "".join(c for c in sheet_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            output_file = os.path.join(output_dir, f"{Path(excel_file).stem}_{safe_sheet_name}.md")
            
            # Markdown形式に変換
            markdown_content = []
            
            # ファイル名をタイトルとして追加
            title = Path(excel_file).stem
            markdown_content.append(f"# {title}\n")
            
            # シート名をサブタイトルとして追加
            markdown_content.append(f"## シート: {sheet_name}\n")
            
            # データフレームをMarkdownテーブルに変換
            markdown_table = df.to_markdown(index=False)
            markdown_content.append(markdown_table)
            
            # ファイルに保存
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(markdown_content))
            
            generated_files.append(output_file)
            print(f"  → {output_file}")
        
        print(f"\n合計 {len(generated_files)} 個のMarkdownファイルを生成しました")
        return generated_files
        
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
        return []


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='エクセルファイルをMarkdownに変換します')
    parser.add_argument('excel_file', help='変換するエクセルファイルのパス')
    parser.add_argument('-o', '--output', help='出力Markdownファイルのパス')
    parser.add_argument('-s', '--sheet', help='変換するシート名（省略時は最初のシート）')
    parser.add_argument('-m', '--multi', action='store_true', 
                       help='全シートを個別のMarkdownファイルに変換')
    parser.add_argument('-d', '--output-dir', help='出力ディレクトリ（--multiオプション使用時）')
    
    args = parser.parse_args()
    
    if args.multi:
        # 全シートを個別ファイルに変換
        generated_files = excel_to_markdown_multi_sheet(args.excel_file, args.output_dir)
        if generated_files:
            print("\n生成されたファイル:")
            for file_path in generated_files:
                print(f"  - {file_path}")
    else:
        # 単一シートを変換
        output_file = excel_to_markdown(args.excel_file, args.output, args.sheet)
        if output_file:
            print(f"\n変換完了: {output_file}")


if __name__ == "__main__":
    main()

