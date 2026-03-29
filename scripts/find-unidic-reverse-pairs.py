#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UniDicのひらがなデータから回文ペア（文字を反転させると別の単語になるペア）を抽出
"""

import os
import sys
from collections import defaultdict

def reverse_string(text):
    """
    文字列を反転する
    """
    return text[::-1]

def find_reverse_pairs(input_path, output_path):
    """
    回文ペアを見つける
    """
    print("=" * 60)
    print("UniDic 回文ペア抽出ツール")
    print("=" * 60)
    print(f"\n入力ファイル: {input_path}")
    print("単語を読み込み中...")

    # 単語を読み込んでセットに格納
    words = set()
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            if word:
                words.add(word)

    print(f"読み込み完了: {len(words):,}語")
    print("\n回文ペアを探索中...")

    # 回文ペアを探す
    reverse_pairs = []
    processed = set()  # 重複を避けるため

    for word in words:
        # すでに処理済みの単語はスキップ
        if word in processed:
            continue

        reversed_word = reverse_string(word)

        # 反転した語が存在し、かつ五十音順で先の単語の場合のみ処理
        if reversed_word in words and word <= reversed_word:
            # 自分自身への反転（回文）も含める
            reverse_pairs.append({
                'word1': word,
                'word2': reversed_word,
                'length': len(word),
                'is_palindrome': (word == reversed_word)
            })
            # 両方の単語を処理済みとしてマーク
            processed.add(word)
            if word != reversed_word:  # 回文でない場合のみ
                processed.add(reversed_word)

    # 長さでソート（長い順）、次に単語でソート
    reverse_pairs.sort(key=lambda x: (-x['length'], x['word1']))

    print(f"探索完了: {len(reverse_pairs):,}組の回文ペアを発見")

    # 統計情報を計算
    palindromes = [p for p in reverse_pairs if p['is_palindrome']]
    non_palindromes = [p for p in reverse_pairs if not p['is_palindrome']]

    print(f"\n内訳:")
    print(f"  - 回文（同じ単語）: {len(palindromes):,}語")
    print(f"  - 異なる単語のペア: {len(non_palindromes):,}組")

    # 文字数分布
    length_dist = defaultdict(int)
    for pair in reverse_pairs:
        length_dist[pair['length']] += 1

    print("\n【文字数分布】")
    for length in sorted(length_dist.keys()):
        count = length_dist[length]
        bar = '█' * min(50, count // 10)
        print(f"  {length:2}文字: {count:6,}組 {bar}")

    # ファイルに保存
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# UniDic 回文ペアリスト\n")
        f.write(f"# 総ペア数: {len(reverse_pairs):,}\n")
        f.write(f"# 回文: {len(palindromes):,}語\n")
        f.write(f"# 異なる単語のペア: {len(non_palindromes):,}組\n")
        f.write("\n")

        # 異なる単語のペアを先に出力（より興味深い）
        if non_palindromes:
            f.write("## 異なる単語の回文ペア\n\n")

            # 文字数別に整理
            by_length = defaultdict(list)
            for pair in non_palindromes:
                by_length[pair['length']].append(pair)

            for length in sorted(by_length.keys(), reverse=True):
                pairs = by_length[length]
                f.write(f"### {length}文字 ({len(pairs)}組)\n")
                for pair in pairs:  # 全てのペアを出力
                    f.write(f"{pair['word1']} ↔ {pair['word2']}\n")
                f.write("\n")

        # 回文（同じ単語）も出力
        if palindromes:
            f.write("## 回文（左右対称の単語）\n\n")

            # 文字数別に整理
            by_length = defaultdict(list)
            for pair in palindromes:
                by_length[pair['length']].append(pair['word1'])

            for length in sorted(by_length.keys(), reverse=True):
                words = sorted(by_length[length])
                f.write(f"### {length}文字 ({len(words)}語)\n")
                for i, word in enumerate(words[:50], 1):  # 各文字数で最大50語まで
                    f.write(f"{word}\n")
                if len(words) > 50:
                    f.write(f"... 他 {len(words)-50} 語\n")
                f.write("\n")

    print(f"\n結果を {output_path} に保存しました")

    # サンプル表示
    print("\n【最長の異なる単語ペア（上位10組）】")
    for i, pair in enumerate(non_palindromes[:10], 1):
        print(f"  {i:2}. 「{pair['word1']}」 ↔ 「{pair['word2']}」 ({pair['length']}文字)")

    print("\n【最長の回文（上位10語）】")
    for i, word in enumerate([p['word1'] for p in palindromes[:10]], 1):
        print(f"  {i:2}. 「{word}」 ({len(word)}文字)")

    # 興味深いペアを探す
    interesting_pairs = []
    for pair in non_palindromes:
        word1, word2 = pair['word1'], pair['word2']
        # 3文字以上で、意味がありそうな組み合わせ
        if pair['length'] >= 3 and pair['length'] <= 5:
            interesting_pairs.append(pair)

    if interesting_pairs:
        print("\n【興味深いペア（3-5文字）】")
        for pair in interesting_pairs[:20]:
            print(f"  「{pair['word1']}」 ↔ 「{pair['word2']}」")

    return reverse_pairs

def main():
    """
    メイン処理
    """
    import argparse

    parser = argparse.ArgumentParser(description='辞書ファイルから回文ペアを抽出')
    parser.add_argument('input', help='入力辞書ファイルのパス')
    parser.add_argument('-o', '--output', help='出力ファイルのパス（省略時は入力ファイル名から自動生成）')
    args = parser.parse_args()

    input_file = args.input

    if args.output:
        output_file = args.output
    else:
        base = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join('data', 'pairs', f"{base}-reverse-pairs.txt")

    # ファイルの存在確認
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません")
        sys.exit(1)

    # 処理実行
    find_reverse_pairs(input_file, output_file)

    print("\n処理完了！")

if __name__ == '__main__':
    main()