#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スキルシートのマークダウンファイルを見やすく整形するスクリプト
"""

import re
from pathlib import Path


def clean_cell_value(cell):
    """セルの値をクリーンアップ"""
    cell = cell.strip()
    # nan、NaTを削除
    if cell in ['nan', 'NaT']:
        return ''
    # 空文字列を返す
    if not cell:
        return ''
    return cell


def process_table_line(line):
    """テーブル行を処理"""
    if not line.strip().startswith('|') or not line.strip().endswith('|'):
        return line
    
    # セルを分割
    cells = line.split('|')
    # 先頭と末尾の空要素を除外
    if len(cells) < 3:
        return line
    
    cells = cells[1:-1]
    # 各セルをクリーンアップ
    cleaned_cells = [clean_cell_value(cell) for cell in cells]
    
    # 行を再構築
    return '| ' + ' | '.join(cleaned_cells) + ' |'


def is_separator_line(line):
    """セパレータ行かどうかを判定"""
    return bool(re.match(r'^\|[\s\-\|:]+\|$', line.strip()))


def is_empty_table_row(line):
    """テーブル行が空かどうかを判定"""
    if not line.strip().startswith('|') or not line.strip().endswith('|'):
        return False
    
    cells = line.split('|')[1:-1]
    return all(not cell.strip() or cell.strip() in ['nan', 'NaT'] for cell in cells)


def format_markdown_file(input_file, output_file=None):
    """マークダウンファイルを整形"""
    if output_file is None:
        output_file = input_file
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    in_table = False
    table_rows = []
    prev_was_separator = False
    prev_was_empty = False
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n\r')
        
        # テーブル行の判定
        is_table_row = line.strip().startswith('|') and line.strip().endswith('|')
        is_sep = is_separator_line(line)
        
        if is_table_row and not is_sep:
            # テーブル行を処理
            if not in_table:
                # テーブル開始
                in_table = True
                table_rows = []
                # 前のセクションを出力
                if output_lines and output_lines[-1] and not output_lines[-1].startswith('|'):
                    output_lines.append('')
            
            # 行をクリーンアップ
            cleaned_line = process_table_line(line)
            
            # 空の行はスキップ
            if is_empty_table_row(cleaned_line):
                i += 1
                continue
            
            table_rows.append(cleaned_line)
            prev_was_separator = False
            prev_was_empty = False
            i += 1
        elif is_sep:
            # セパレータ行：テーブルを出力
            if in_table and table_rows:
                # テーブルを出力
                if len(table_rows) > 0:
                    # 最初の行をヘッダーとして出力
                    header = table_rows[0]
                    output_lines.append(header)
                    
                    # セパレータを作成
                    num_cols = len(header.split('|')) - 2
                    separator = '| ' + ' | '.join(['---'] * num_cols) + ' |'
                    output_lines.append(separator)
                    
                    # 残りの行を出力
                    for row in table_rows[1:]:
                        output_lines.append(row)
                    
                    output_lines.append('')
                
                table_rows = []
                in_table = False
            
            # セパレータ行はスキップ（既に追加済み）
            prev_was_separator = True
            prev_was_empty = False
            i += 1
        else:
            # テーブル外の行
            if in_table and table_rows:
                # テーブルが終了（セパレータなし）
                # テーブルを出力
                if len(table_rows) > 0:
                    header = table_rows[0]
                    output_lines.append(header)
                    num_cols = len(header.split('|')) - 2
                    separator = '| ' + ' | '.join(['---'] * num_cols) + ' |'
                    output_lines.append(separator)
                    
                    for row in table_rows[1:]:
                        output_lines.append(row)
                    
                    output_lines.append('')
                
                table_rows = []
                in_table = False
            
            # 通常の行を処理
            # nan、NaTのみの行はスキップ
            if line.strip() and not re.match(r'^\s*(nan|NaT)\s*$', line.strip()):
                # 空行の処理
                if not line.strip():
                    if not prev_was_empty:
                        output_lines.append('')
                        prev_was_empty = True
                else:
                    output_lines.append(line)
                    prev_was_empty = False
            elif not line.strip():
                if not prev_was_empty:
                    output_lines.append('')
                    prev_was_empty = True
            
            prev_was_separator = False
            i += 1
    
    # 最後のテーブルを処理
    if in_table and table_rows:
        if len(table_rows) > 0:
            header = table_rows[0]
            output_lines.append(header)
            num_cols = len(header.split('|')) - 2
            separator = '| ' + ' | '.join(['---'] * num_cols) + ' |'
            output_lines.append(separator)
            
            for row in table_rows[1:]:
                output_lines.append(row)
            
            output_lines.append('')
    
    # 末尾の空行を削除
    while output_lines and not output_lines[-1].strip():
        output_lines.pop()
    
    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
        if output_lines:
            f.write('\n')
    
    print(f"整形完了: {output_file}")
    print(f"行数: {len(lines)} -> {len(output_lines)}")


if __name__ == '__main__':
    input_file = 'スキルシート_O.T_42.md'
    format_markdown_file(input_file)




