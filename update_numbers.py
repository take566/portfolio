#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
職務経歴書.mdの案件番号を一括で更新するスクリプト
"""

import re

def update_case_numbers():
    """案件番号を一括で更新する"""
    
    # ファイルを読み込み
    with open('職務経歴書.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 案件番号のマッピング（新しい番号）
    number_mapping = {
        '| 5  |': '| 6  |',
        '| 6  |': '| 7  |',
        '| 7  |': '| 8  |',
        '| 8  |': '| 9  |',
        '| 9  |': '| 10 |',
        '| 10 |': '| 11 |',
        '| 11 |': '| 12 |',
        '| 12 |': '| 13 |',
        '| 13 |': '| 14 |',
        '| 14 |': '| 15 |',
        '| 15 |': '| 16 |',
        '| 16 |': '| 17 |',
        '| 17 |': '| 18 |',
        '| 18 |': '| 19 |',
        '| 19 |': '| 20 |',
        '| 20 |': '| 21 |',
        '| 21 |': '| 22 |',
        '| 22 |': '| 23 |',
        '| 23 |': '| 24 |',
        '| 24 |': '| 25 |',
        '| 25 |': '| 26 |',
        '| 26 |': '| 27 |',
        '| 27 |': '| 28 |',
        '| 28 |': '| 29 |',
    }
    
    # 番号を置換
    for old_num, new_num in number_mapping.items():
        content = content.replace(old_num, new_num)
    
    # ファイルに書き込み
    with open('職務経歴書.md', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("案件番号の更新が完了しました。")

if __name__ == "__main__":
    update_case_numbers()
