#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UniDic辞書から全ての仮名表記を抽出するスクリプト（完全版）
MeCabバイナリ辞書形式の詳細な解析を行う
"""

import struct
import sys
import os
import re
from collections import defaultdict

def extract_all_kana_strings(content):
    """
    バイナリデータから全ての仮名文字列を網羅的に抽出
    """
    kana_words = set()

    # ひらがなとカタカナの正規表現パターン
    hiragana_pattern = r'[ぁ-ゔー]+'
    katakana_pattern = r'[ァ-ヴー]+'
    kana_pattern = r'[ぁ-ゔァ-ヴー]+'

    # スライディングウィンドウでデータを走査
    window_size = 1024 * 1024  # 1MBずつ処理
    overlap = 1024  # オーバーラップ部分

    pos = 0
    total_size = len(content)

    while pos < total_size:
        # ウィンドウサイズ分のデータを取得
        end_pos = min(pos + window_size, total_size)
        window = content[pos:end_pos]

        # UTF-8としてデコード試行（エラーは無視）
        try:
            text = window.decode('utf-8', errors='ignore')

            # ひらがな・カタカナの文字列を全て抽出
            matches = re.findall(kana_pattern, text)

            for match in matches:
                # 2文字以上の単語のみ収集
                if len(match) >= 2 and len(match) <= 20:  # 20文字以下に制限
                    # 特殊文字の繰り返しは除外
                    if not re.match(r'^ー+$', match):
                        kana_words.add(match)
        except:
            pass

        # 進捗表示
        if pos % (10 * 1024 * 1024) == 0:  # 10MBごとに進捗表示
            progress = (pos * 100) // total_size
            print(f"進捗: {progress}% ({pos:,} / {total_size:,} bytes)")
            print(f"現在の抽出単語数: {len(kana_words):,}")

        # 次の位置へ（オーバーラップを考慮）
        pos += window_size - overlap

    return kana_words

def extract_from_char_bin(char_bin_path):
    """
    char.binファイルからも仮名を抽出
    """
    kana_words = set()

    try:
        with open(char_bin_path, 'rb') as f:
            content = f.read()

            # UTF-8としてデコード試行
            text = content.decode('utf-8', errors='ignore')

            # 仮名文字列を抽出
            kana_pattern = r'[ぁ-ゔァ-ヴー]+'
            matches = re.findall(kana_pattern, text)

            for match in matches:
                if len(match) >= 2 and len(match) <= 20:
                    kana_words.add(match)

    except Exception as e:
        print(f"char.bin処理エラー: {e}")

    return kana_words

def extract_from_text_files(unidic_dir):
    """
    UniDicディレクトリ内のテキストファイルからも仮名を抽出
    """
    kana_words = set()

    # テキストファイルのパターン
    text_files = ['rewrite.def', 'unk.def', 'feature.def']

    for filename in text_files:
        filepath = os.path.join(unidic_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                    # 仮名文字列を抽出
                    kana_pattern = r'[ぁ-ゔァ-ヴー]+'
                    matches = re.findall(kana_pattern, content)

                    for match in matches:
                        if len(match) >= 2 and len(match) <= 20:
                            kana_words.add(match)

            except Exception as e:
                print(f"{filename}処理エラー: {e}")

    return kana_words

def main():
    """
    メイン処理
    """
    unidic_dir = 'dictionaries/unidic-cwj-202512'
    sys_dic_path = os.path.join(unidic_dir, 'sys.dic')
    char_bin_path = os.path.join(unidic_dir, 'char.bin')
    unk_dic_path = os.path.join(unidic_dir, 'unk.dic')
    output_path = 'data/unidic-kana-words-complete.txt'

    print("UniDic辞書から全ての仮名表記を抽出中...")
    print("=" * 60)

    all_kana_words = set()

    # 1. sys.dicから抽出
    print("\n1. sys.dic (メイン辞書) を解析中...")
    print("-" * 40)

    if os.path.exists(sys_dic_path):
        with open(sys_dic_path, 'rb') as f:
            content = f.read()
            print(f"ファイルサイズ: {len(content):,} bytes")

            # 全体を走査して仮名を抽出
            kana_words = extract_all_kana_strings(content)
            all_kana_words.update(kana_words)
            print(f"sys.dicから抽出: {len(kana_words):,}語")

    # 2. char.binから抽出
    print("\n2. char.bin (文字定義) を解析中...")
    print("-" * 40)

    char_words = extract_from_char_bin(char_bin_path)
    all_kana_words.update(char_words)
    print(f"char.binから抽出: {len(char_words):,}語")

    # 3. unk.dicから抽出
    print("\n3. unk.dic (未知語辞書) を解析中...")
    print("-" * 40)

    if os.path.exists(unk_dic_path):
        with open(unk_dic_path, 'rb') as f:
            content = f.read()
            unk_words = extract_all_kana_strings(content)
            all_kana_words.update(unk_words)
            print(f"unk.dicから抽出: {len(unk_words):,}語")

    # 4. テキストファイルから抽出
    print("\n4. 定義ファイル (.def) を解析中...")
    print("-" * 40)

    text_words = extract_from_text_files(unidic_dir)
    all_kana_words.update(text_words)
    print(f"定義ファイルから抽出: {len(text_words):,}語")

    # 結果をソート
    sorted_words = sorted(all_kana_words)

    print("\n" + "=" * 60)
    print(f"総抽出単語数: {len(sorted_words):,}語")

    # ファイルに保存
    os.makedirs('data', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in sorted_words:
            f.write(word + '\n')

    print(f"結果を {output_path} に保存しました")

    # サンプル表示
    print("\n【サンプル（最初の30語）】")
    for i, word in enumerate(sorted_words[:30], 1):
        print(f"  {i:2}. {word}")

    print("\n【サンプル（最後の30語）】")
    for i, word in enumerate(sorted_words[-30:], len(sorted_words)-29):
        print(f"  {i:,}. {word}")

    # 文字数分布
    length_dist = defaultdict(int)
    for word in sorted_words:
        length_dist[len(word)] += 1

    print("\n【文字数分布】")
    for length in sorted(length_dist.keys()):
        count = length_dist[length]
        bar = '█' * min(50, count // 100)
        print(f"  {length:2}文字: {count:6,}語 {bar}")

    # ひらがな・カタカナの分布
    hiragana_words = [w for w in sorted_words if re.match(r'^[ぁ-ゔー]+$', w)]
    katakana_words = [w for w in sorted_words if re.match(r'^[ァ-ヴー]+$', w)]
    mixed_words = [w for w in sorted_words if w not in hiragana_words and w not in katakana_words]

    print("\n【文字種別分布】")
    print(f"  ひらがなのみ: {len(hiragana_words):,}語")
    print(f"  カタカナのみ: {len(katakana_words):,}語")
    print(f"  混在: {len(mixed_words):,}語")

if __name__ == '__main__':
    main()