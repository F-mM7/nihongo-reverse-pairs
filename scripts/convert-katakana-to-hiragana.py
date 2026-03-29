#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
カタカナを平仮名に変換するスクリプト
平仮名に対応する文字がないカタカナ（ヴなど）は保持する
"""

import sys
import os

def katakana_to_hiragana(text):
    """
    カタカナを平仮名に変換

    Unicode上でカタカナとひらがなは96文字の差がある
    ただし「ヴ」「ヵ」「ヶ」などは平仮名に対応する文字がないので保持
    """
    result = []

    for char in text:
        # カタカナの範囲: U+30A1-U+30F6
        # ひらがなの範囲: U+3041-U+3096
        code = ord(char)

        # 通常のカタカナ（ァ-ヶ）の範囲
        if 0x30A1 <= code <= 0x30F6:
            # 平仮名に変換できない特殊なカタカナ
            # ヴ(U+30F4), ヵ(U+30F5), ヶ(U+30F6) は保持
            if code in [0x30F4, 0x30F5, 0x30F6]:
                result.append(char)
            else:
                # 96を引いて平仮名に変換
                hiragana_code = code - 96
                result.append(chr(hiragana_code))

        # 長音記号「ー」(U+30FC)はそのまま保持
        elif code == 0x30FC:
            result.append(char)

        # カタカナの「ヽ」(U+30FD)と「ヾ」(U+30FE)も対応する平仮名に変換
        elif code == 0x30FD:  # カタカナの「ヽ」
            result.append('ゝ')  # 平仮名の「ゝ」(U+309D)
        elif code == 0x30FE:  # カタカナの「ヾ」
            result.append('ゞ')  # 平仮名の「ゞ」(U+309E)

        # その他の文字（ひらがな、漢字など）はそのまま
        else:
            result.append(char)

    return ''.join(result)

def process_file(input_path, output_path):
    """
    ファイル全体を処理
    """
    # 重複を除去するためセットを使用
    converted_words = set()

    print(f"入力ファイル: {input_path}")
    print("カタカナを平仮名に変換中...")

    # ファイルを読み込んで変換
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    print(f"総行数: {total_lines:,}")

    # 各行を変換
    for i, line in enumerate(lines, 1):
        word = line.strip()
        if word:
            converted = katakana_to_hiragana(word)
            converted_words.add(converted)

        # 進捗表示
        if i % 50000 == 0:
            print(f"進捗: {i:,} / {total_lines:,} ({i*100//total_lines}%)")

    # ソートして保存
    sorted_words = sorted(converted_words)

    print(f"\n変換完了:")
    print(f"元の単語数: {total_lines:,}")
    print(f"変換後のユニーク単語数: {len(sorted_words):,}")

    # ファイルに保存
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(word + '\n')

    print(f"\n結果を {output_path} に保存しました")

    # サンプル表示
    print("\n【変換例（最初の30語）】")
    for i, word in enumerate(sorted_words[:30], 1):
        print(f"  {i:2}. {word}")

    # カタカナが残っている単語を探す
    katakana_remaining = []
    for word in sorted_words:
        if any('ァ' <= c <= 'ヶ' for c in word):
            katakana_remaining.append(word)

    if katakana_remaining:
        print(f"\n【平仮名に変換できないカタカナを含む単語】（{len(katakana_remaining)}語）")
        for i, word in enumerate(katakana_remaining[:20], 1):
            print(f"  {i:2}. {word}")
        if len(katakana_remaining) > 20:
            print(f"  ... 他 {len(katakana_remaining)-20} 語")

    return sorted_words

def main():
    """
    メイン処理
    """
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'data/unidic-kana-words-complete.txt'

    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # 出力ファイル名を自動生成
        base_name = os.path.splitext(input_file)[0]
        output_file = base_name + '-hiragana.txt'

    # ファイルの存在確認
    if not os.path.exists(input_file):
        print(f"エラー: 入力ファイル '{input_file}' が見つかりません")
        sys.exit(1)

    print("=" * 60)
    print("カタカナ → 平仮名 変換ツール")
    print("=" * 60)

    # 処理実行
    process_file(input_file, output_file)

    print("\n処理完了！")

if __name__ == '__main__':
    main()