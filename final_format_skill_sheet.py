#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スキルシートのマークダウンファイルを最終的に整形するスクリプト
- 空の列を削除
- 不要なセパレータを削除
- 読みやすい形式に整形
"""

import re
from pathlib import Path


def clean_cell(cell):
    """セルをクリーンアップ"""
    cell = cell.strip()
    if cell in ['nan', 'NaT', '']:
        return ''
    return cell


def is_empty_column(col_index, rows):
    """指定された列が空かどうかを判定"""
    for row in rows:
        if col_index < len(row) and row[col_index].strip():
            return False
    return True


def remove_empty_columns(rows):
    """空の列を削除"""
    if not rows:
        return rows
    
    # 最大列数を取得
    max_cols = max(len(row) for row in rows) if rows else 0
    
    # 空の列のインデックスを取得（後ろから）
    empty_cols = []
    for col_idx in range(max_cols):
        if is_empty_column(col_idx, rows):
            empty_cols.append(col_idx)
    
    # 空の列を削除（後ろから削除）
    if empty_cols:
        for row in rows:
            for col_idx in reversed(empty_cols):
                if col_idx < len(row):
                    row.pop(col_idx)
    
    return rows


def format_markdown_file(input_file, output_file=None):
    """マークダウンファイルを最終的に整形"""
    if output_file is None:
        output_file = input_file
    
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output_lines = []
    in_table = False
    table_rows = []
    
    i = 0
    while i < len(lines):
        line = lines[i].rstrip('\n\r')
        
        # テーブル行の判定
        is_table_row = line.strip().startswith('|') and line.strip().endswith('|')
        is_separator = is_table_row and re.match(r'^\|[\s\-\|:]+\|$', line.strip())
        
        if is_table_row and not is_separator:
            # テーブル行を処理
            if not in_table:
                # 前のセクションを出力
                if output_lines and output_lines[-1] and not output_lines[-1].startswith('|'):
                    output_lines.append('')
                in_table = True
                table_rows = []
            
            # セルを分割してクリーンアップ
            cells = [clean_cell(cell) for cell in line.split('|')[1:-1]]
            table_rows.append(cells)
            i += 1
        elif is_separator:
            # セパレータ行：テーブルを処理して出力
            if in_table and table_rows:
                # 空の列を削除
                table_rows = remove_empty_columns(table_rows)
                
                # 空の行を削除
                table_rows = [row for row in table_rows if any(cell.strip() for cell in row)]
                
                # テーブルを出力
                if table_rows:
                    # 最大列数を取得
                    max_cols = max(len(row) for row in table_rows) if table_rows else 0
                    
                    # 全ての行を同じ列数に揃える
                    for row in table_rows:
                        while len(row) < max_cols:
                            row.append('')
                    
                    # ヘッダー行を出力
                    header = table_rows[0]
                    output_lines.append('| ' + ' | '.join(header) + ' |')
                    
                    # セパレータを出力
                    output_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
                    
                    # データ行を出力
                    for row in table_rows[1:]:
                        output_lines.append('| ' + ' | '.join(row) + ' |')
                    
                    output_lines.append('')
                
                table_rows = []
                in_table = False
            
            # セパレータ行はスキップ
            i += 1
        else:
            # テーブル外の行
            if in_table and table_rows:
                # テーブルが終了（セパレータなし）
                # 空の列を削除
                table_rows = remove_empty_columns(table_rows)
                
                # 空の行を削除
                table_rows = [row for row in table_rows if any(cell.strip() for cell in row)]
                
                # テーブルを出力
                if table_rows:
                    max_cols = max(len(row) for row in table_rows) if table_rows else 0
                    
                    for row in table_rows:
                        while len(row) < max_cols:
                            row.append('')
                    
                    header = table_rows[0]
                    output_lines.append('| ' + ' | '.join(header) + ' |')
                    output_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
                    
                    for row in table_rows[1:]:
                        output_lines.append('| ' + ' | '.join(row) + ' |')
                    
                    output_lines.append('')
                
                table_rows = []
                in_table = False
            
            # 通常の行を追加
            if line.strip():
                output_lines.append(line)
            elif output_lines and output_lines[-1].strip():
                # 空行は1つだけ保持
                output_lines.append('')
            
            i += 1
    
    # 最後のテーブルを処理
    if in_table and table_rows:
        table_rows = remove_empty_columns(table_rows)
        table_rows = [row for row in table_rows if any(cell.strip() for cell in row)]
        
        if table_rows:
            max_cols = max(len(row) for row in table_rows) if table_rows else 0
            
            for row in table_rows:
                while len(row) < max_cols:
                    row.append('')
            
            header = table_rows[0]
            output_lines.append('| ' + ' | '.join(header) + ' |')
            output_lines.append('| ' + ' | '.join(['---'] * len(header)) + ' |')
            
            for row in table_rows[1:]:
                output_lines.append('| ' + ' | '.join(row) + ' |')
            
            output_lines.append('')
    
    # 末尾の空行を削除
    while output_lines and not output_lines[-1].strip():
        output_lines.pop()
    
    # 連続する空行を削除（最大2行まで）
    cleaned_output = []
    prev_empty_count = 0
    for line in output_lines:
        if not line.strip():
            prev_empty_count += 1
            if prev_empty_count <= 2:  # 最大2つの連続する空行まで許可
                cleaned_output.append('')
        else:
            prev_empty_count = 0
            cleaned_output.append(line)
    
    # ファイルに書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_output))
        if cleaned_output:
            f.write('\n')
    
    print(f"最終整形完了: {output_file}")
    print(f"行数: {len(lines)} -> {len(cleaned_output)}")


if __name__ == '__main__':
    input_file = 'スキルシート_O.T_42.md'
    format_markdown_file(input_file)




