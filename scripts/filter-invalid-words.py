#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
不正な日本語を除外するフィルタリングスクリプト

除外基準:
1. 小字（ぁぃぅぇぉっゃゅょ）から始まる
2. ーから始まる
3. っで終わる
4. ゐが含まれる
5. ゑが含まれる
6. んから始まる
7. 連続するー（ーー以上）が含まれる
"""

import re
import sys
import os

# フィルタリング基準の定義
FILTERS = [
    ("小字から始まる", re.compile(r'^[ぁぃぅぇぉっゃゅょ]')),
    ("ーから始まる", re.compile(r'^ー')),
    ("っで終わる", re.compile(r'っ$')),
    ("ゐが含まれる", re.compile(r'ゐ')),
    ("ゑが含まれる", re.compile(r'ゑ')),
    ("んから始まる", re.compile(r'^ん')),
    ("連続するー", re.compile(r'ー{2,}')),
]


def filter_words(input_path, output_path):
    """
    不正な日本語を除外してフィルタリング済みリストを生成
    """
    print(f"入力ファイル: {input_path}")
    print("フィルタリング中...")

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"総行数: {total_lines:,}")

    # 基準ごとの除外カウント
    excluded_counts = {name: 0 for name, _ in FILTERS}
    filtered_words = set()

    for i, line in enumerate(lines, 1):
        word = line.strip()
        if not word:
            continue

        excluded = False
        for name, pattern in FILTERS:
            if pattern.search(word):
                excluded_counts[name] += 1
                excluded = True
                break  # 最初に一致した基準でカウント

        if not excluded:
            filtered_words.add(word)

        if i % 100000 == 0:
            print(f"進捗: {i:,} / {total_lines:,} ({i * 100 // total_lines}%)")

    # ソートして保存
    sorted_words = sorted(filtered_words)

    with open(output_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(word + '\n')

    # 統計サマリー
    total_excluded = total_lines - len(filtered_words)
    print(f"\n{'=' * 50}")
    print("フィルタリング結果")
    print(f"{'=' * 50}")
    print(f"元の語数:     {total_lines:>10,}")
    print(f"\n除外内訳:")
    for name, _ in FILTERS:
        count = excluded_counts[name]
        if count > 0:
            print(f"  {name}: {count:>10,}")
    print(f"\n除外合計:     {total_excluded:>10,}")
    print(f"残った語数:   {len(sorted_words):>10,}")
    print(f"\n結果を {output_path} に保存しました")

    # サンプル表示
    print(f"\n【フィルタリング後の先頭30語】")
    for i, word in enumerate(sorted_words[:30], 1):
        print(f"  {i:2}. {word}")

    return sorted_words


def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/dict/unidic-raw.txt'

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '-filtered.txt'

    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません")
        sys.exit(1)

    print("=" * 50)
    print("不正語フィルタリングツール")
    print("=" * 50)

    filter_words(input_file, output_file)

    print("\n処理完了！")


if __name__ == '__main__':
    main()
