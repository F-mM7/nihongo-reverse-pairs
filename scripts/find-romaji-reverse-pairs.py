#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ひらがな単語リストからヘボン式ローマ字倒語ペアを抽出
（ローマ字に変換して逆順にしたときに別の単語になるペア）

例: いけ (ike) → eki → えき
"""

import argparse
import os
import sys
from datetime import datetime


class HepburnConverter:
    """ヘボン式ローマ字変換クラス"""

    def __init__(self):
        self.hiragana_to_romaji = {}
        self.romaji_to_hiragana = {}
        self._build_tables()

    def _build_tables(self):
        """変換テーブルを構築"""
        # ひらがな → ローマ字 (拗音は先に定義して優先度を上げる)
        mappings = [
            # 拗音（3文字→2文字）
            ('きゃ', 'kya'), ('きゅ', 'kyu'), ('きょ', 'kyo'),
            ('しゃ', 'sha'), ('しゅ', 'shu'), ('しょ', 'sho'),
            ('ちゃ', 'cha'), ('ちゅ', 'chu'), ('ちょ', 'cho'),
            ('にゃ', 'nya'), ('にゅ', 'nyu'), ('にょ', 'nyo'),
            ('ひゃ', 'hya'), ('ひゅ', 'hyu'), ('ひょ', 'hyo'),
            ('みゃ', 'mya'), ('みゅ', 'myu'), ('みょ', 'myo'),
            ('りゃ', 'rya'), ('りゅ', 'ryu'), ('りょ', 'ryo'),
            ('ぎゃ', 'gya'), ('ぎゅ', 'gyu'), ('ぎょ', 'gyo'),
            ('じゃ', 'ja'), ('じゅ', 'ju'), ('じょ', 'jo'),
            ('ぢゃ', 'ja'), ('ぢゅ', 'ju'), ('ぢょ', 'jo'),
            ('びゃ', 'bya'), ('びゅ', 'byu'), ('びょ', 'byo'),
            ('ぴゃ', 'pya'), ('ぴゅ', 'pyu'), ('ぴょ', 'pyo'),
            # 清音
            ('あ', 'a'), ('い', 'i'), ('う', 'u'), ('え', 'e'), ('お', 'o'),
            ('か', 'ka'), ('き', 'ki'), ('く', 'ku'), ('け', 'ke'), ('こ', 'ko'),
            ('さ', 'sa'), ('し', 'shi'), ('す', 'su'), ('せ', 'se'), ('そ', 'so'),
            ('た', 'ta'), ('ち', 'chi'), ('つ', 'tsu'), ('て', 'te'), ('と', 'to'),
            ('な', 'na'), ('に', 'ni'), ('ぬ', 'nu'), ('ね', 'ne'), ('の', 'no'),
            ('は', 'ha'), ('ひ', 'hi'), ('ふ', 'fu'), ('へ', 'he'), ('ほ', 'ho'),
            ('ま', 'ma'), ('み', 'mi'), ('む', 'mu'), ('め', 'me'), ('も', 'mo'),
            ('や', 'ya'), ('ゆ', 'yu'), ('よ', 'yo'),
            ('ら', 'ra'), ('り', 'ri'), ('る', 'ru'), ('れ', 're'), ('ろ', 'ro'),
            ('わ', 'wa'), ('ゐ', 'i'), ('ゑ', 'e'), ('を', 'o'),
            ('ん', 'n'),
            # 濁音
            ('が', 'ga'), ('ぎ', 'gi'), ('ぐ', 'gu'), ('げ', 'ge'), ('ご', 'go'),
            ('ざ', 'za'), ('じ', 'ji'), ('ず', 'zu'), ('ぜ', 'ze'), ('ぞ', 'zo'),
            ('だ', 'da'), ('ぢ', 'ji'), ('づ', 'zu'), ('で', 'de'), ('ど', 'do'),
            ('ば', 'ba'), ('び', 'bi'), ('ぶ', 'bu'), ('べ', 'be'), ('ぼ', 'bo'),
            # 半濁音
            ('ぱ', 'pa'), ('ぴ', 'pi'), ('ぷ', 'pu'), ('ぺ', 'pe'), ('ぽ', 'po'),
            # 小文字
            ('ぁ', 'a'), ('ぃ', 'i'), ('ぅ', 'u'), ('ぇ', 'e'), ('ぉ', 'o'),
            ('ゃ', 'ya'), ('ゅ', 'yu'), ('ょ', 'yo'),
            # 特殊
            ('ー', '-'),
            ('ヴ', 'vu'),
            ('ゔ', 'vu'),
        ]

        for hiragana, romaji in mappings:
            self.hiragana_to_romaji[hiragana] = romaji

        # ローマ字 → ひらがな（逆変換用）
        # 長いものを優先するために順序を考慮
        reverse_mappings = [
            # 拗音（3文字）
            ('sha', 'しゃ'), ('shu', 'しゅ'), ('sho', 'しょ'),
            ('cha', 'ちゃ'), ('chu', 'ちゅ'), ('cho', 'ちょ'),
            ('tsu', 'つ'),
            ('kya', 'きゃ'), ('kyu', 'きゅ'), ('kyo', 'きょ'),
            ('nya', 'にゃ'), ('nyu', 'にゅ'), ('nyo', 'にょ'),
            ('hya', 'ひゃ'), ('hyu', 'ひゅ'), ('hyo', 'ひょ'),
            ('mya', 'みゃ'), ('myu', 'みゅ'), ('myo', 'みょ'),
            ('rya', 'りゃ'), ('ryu', 'りゅ'), ('ryo', 'りょ'),
            ('gya', 'ぎゃ'), ('gyu', 'ぎゅ'), ('gyo', 'ぎょ'),
            ('bya', 'びゃ'), ('byu', 'びゅ'), ('byo', 'びょ'),
            ('pya', 'ぴゃ'), ('pyu', 'ぴゅ'), ('pyo', 'ぴょ'),
            # 2文字
            ('shi', 'し'), ('chi', 'ち'),
            ('ka', 'か'), ('ki', 'き'), ('ku', 'く'), ('ke', 'け'), ('ko', 'こ'),
            ('sa', 'さ'), ('su', 'す'), ('se', 'せ'), ('so', 'そ'),
            ('ta', 'た'), ('te', 'て'), ('to', 'と'),
            ('na', 'な'), ('ni', 'に'), ('nu', 'ぬ'), ('ne', 'ね'), ('no', 'の'),
            ('ha', 'は'), ('hi', 'ひ'), ('fu', 'ふ'), ('he', 'へ'), ('ho', 'ほ'),
            ('ma', 'ま'), ('mi', 'み'), ('mu', 'む'), ('me', 'め'), ('mo', 'も'),
            ('ya', 'や'), ('yu', 'ゆ'), ('yo', 'よ'),
            ('ra', 'ら'), ('ri', 'り'), ('ru', 'る'), ('re', 'れ'), ('ro', 'ろ'),
            ('wa', 'わ'),
            ('ga', 'が'), ('gi', 'ぎ'), ('gu', 'ぐ'), ('ge', 'げ'), ('go', 'ご'),
            ('za', 'ざ'), ('ji', 'じ'), ('zu', 'ず'), ('ze', 'ぜ'), ('zo', 'ぞ'),
            ('da', 'だ'), ('de', 'で'), ('do', 'ど'),
            ('ba', 'ば'), ('bi', 'び'), ('bu', 'ぶ'), ('be', 'べ'), ('bo', 'ぼ'),
            ('pa', 'ぱ'), ('pi', 'ぴ'), ('pu', 'ぷ'), ('pe', 'ぺ'), ('po', 'ぽ'),
            ('ja', 'じゃ'), ('ju', 'じゅ'), ('jo', 'じょ'),
            ('vu', 'ゔ'),
            # 1文字
            ('a', 'あ'), ('i', 'い'), ('u', 'う'), ('e', 'え'), ('o', 'お'),
            ('n', 'ん'),
        ]

        for romaji, hiragana in reverse_mappings:
            self.romaji_to_hiragana[romaji] = hiragana

    def _get_next_consonant(self, text: str) -> str:
        """次の文字のローマ字の最初の子音を取得"""
        if not text:
            return ''

        # 2文字の拗音をチェック
        if len(text) >= 2:
            two_char = text[:2]
            if two_char in self.hiragana_to_romaji:
                romaji = self.hiragana_to_romaji[two_char]
                return romaji[0] if romaji else ''

        # 1文字をチェック
        one_char = text[0]
        if one_char in self.hiragana_to_romaji:
            romaji = self.hiragana_to_romaji[one_char]
            # 母音のみの場合は空文字を返す
            if romaji in ('a', 'i', 'u', 'e', 'o', 'n'):
                return romaji[0] if romaji == 'n' else ''
            return romaji[0] if romaji else ''

        return ''

    def to_romaji(self, hiragana: str) -> str:
        """ひらがな → ローマ字変換"""
        result = []
        i = 0

        while i < len(hiragana):
            # 促音の処理
            if hiragana[i] == 'っ':
                # 次の子音を重ねる
                if i + 1 < len(hiragana):
                    next_consonant = self._get_next_consonant(hiragana[i + 1:])
                    if next_consonant and next_consonant not in 'aiueon':
                        result.append(next_consonant)
                    # 次の文字が母音や「ん」の場合は促音を無視
                i += 1
                continue

            # 2文字マッチを優先（拗音）
            if i + 1 < len(hiragana):
                two_char = hiragana[i:i + 2]
                if two_char in self.hiragana_to_romaji:
                    result.append(self.hiragana_to_romaji[two_char])
                    i += 2
                    continue

            # 1文字マッチ
            one_char = hiragana[i]
            if one_char in self.hiragana_to_romaji:
                romaji_char = self.hiragana_to_romaji[one_char]

                # 撥音「ん」の後に母音・や行が続く場合はアポストロフィで区切る
                # 例: うんい → un'i（うに uni と区別）、あんや → an'ya（あにゃ anya と区別）
                if one_char == 'ん' and i + 1 < len(hiragana):
                    next_romaji = None
                    # 次の文字のローマ字を確認（2文字拗音を優先チェック）
                    if i + 2 < len(hiragana):
                        two_next = hiragana[i + 1:i + 3]
                        if two_next in self.hiragana_to_romaji:
                            next_romaji = self.hiragana_to_romaji[two_next]
                    if next_romaji is None:
                        next_char = hiragana[i + 1]
                        if next_char in self.hiragana_to_romaji:
                            next_romaji = self.hiragana_to_romaji[next_char]
                    if next_romaji and next_romaji[0] in 'aiueoy':
                        romaji_char = "n'"

                result.append(romaji_char)
            else:
                # 変換不可文字はそのまま保持（後で除外する）
                result.append(one_char)
            i += 1

        romaji = ''.join(result)

        # 撥音「ん」の後処理: m/b/p前でm
        # n + b → mb, n + m → mm, n + p → mp
        import re
        romaji = re.sub(r'n([bmp])', r'm\1', romaji)

        return romaji

    def to_hiragana(self, romaji: str) -> str | None:
        """ローマ字 → ひらがな変換（変換不可の場合はNone）"""
        result = []
        i = 0
        romaji = romaji.lower()

        # 撥音の前処理: m + b/m/p → n + b/m/p に復元
        import re
        romaji = re.sub(r'm([bmp])', r'n\1', romaji)

        while i < len(romaji):
            matched = False

            # 長いマッチから試す（3文字→2文字→1文字）
            for length in [3, 2, 1]:
                if i + length <= len(romaji):
                    substr = romaji[i:i + length]
                    if substr in self.romaji_to_hiragana:
                        result.append(self.romaji_to_hiragana[substr])
                        i += length
                        matched = True
                        break

            if not matched:
                # 特殊処理
                if romaji[i] == '-':
                    result.append('ー')
                    i += 1
                elif romaji[i] == "'":
                    # アポストロフィは n の直後にのみ有効（んの曖昧性解消）
                    # 例: n'a → んあ、n'ya → んや
                    # 不正な位置（例: a'nan）は変換不可
                    if i == 0 or romaji[i - 1] != 'n':
                        return None
                    i += 1
                elif i + 1 < len(romaji) and romaji[i] == romaji[i + 1]:
                    # 重複子音は促音
                    # ただし母音の重複は除外
                    if romaji[i] not in 'aiueon':
                        result.append('っ')
                        i += 1  # 次の文字は通常処理
                    else:
                        # 母音の重複は変換不可
                        return None
                else:
                    # 変換不可
                    return None

        return ''.join(result)


def find_romaji_reverse_pairs(input_path: str, output_path: str, encoding: str = 'utf-8'):
    """ローマ字ベースの倒語ペアを検索"""
    print("=" * 60)
    print("ヘボン式ローマ字倒語ペア抽出ツール")
    print("=" * 60)
    print(f"\n入力ファイル: {input_path}")
    print(f"エンコーディング: {encoding}")
    print("単語を読み込み中...")

    # 単語を読み込んでセットに格納
    words = set()
    with open(input_path, 'r', encoding=encoding) as f:
        for line in f:
            word = line.strip()
            if word:
                words.add(word)

    print(f"読み込み完了: {len(words):,}語")

    converter = HepburnConverter()

    print("ローマ字変換とペア探索中...")

    # 倒語ペアを検索
    pairs = []
    processed = set()
    conversion_errors = 0
    reverse_errors = 0

    for word in words:
        if word in processed:
            continue

        # ひらがな → ローマ字
        romaji = converter.to_romaji(word)

        # ローマ字を逆順に
        reversed_romaji = romaji[::-1]

        # 逆順ローマ字 → ひらがな
        reversed_hiragana = converter.to_hiragana(reversed_romaji)

        if reversed_hiragana is None:
            reverse_errors += 1
            continue

        # 逆変換結果が単語リストに存在するか
        if reversed_hiragana in words:
            # ペアを追加（五十音順で若い方を左に）
            if word <= reversed_hiragana:
                pair = (word, reversed_hiragana)
            else:
                pair = (reversed_hiragana, word)

            # 重複チェック
            if pair not in [(p[0], p[1]) for p in pairs]:
                pairs.append(pair)

            processed.add(word)
            processed.add(reversed_hiragana)

    # ソート：五十音順（ペアの左側の単語を基準）
    pairs.sort(key=lambda x: x[0])

    # 統計情報
    palindromes = [p for p in pairs if p[0] == p[1]]
    non_palindromes = [p for p in pairs if p[0] != p[1]]

    print(f"\n探索完了:")
    print(f"  - 総ペア数: {len(pairs):,}")
    print(f"  - 回文（同じ単語）: {len(palindromes):,}語")
    print(f"  - 異なる単語のペア: {len(non_palindromes):,}組")
    print(f"  - 逆変換失敗: {reverse_errors:,}語")

    # ファイルに保存
    today = datetime.now().strftime('%Y-%m-%d')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# ヘボン式ローマ字倒語ペアリスト\n")
        f.write(f"# 総ペア数: {len(pairs):,}\n")
        f.write(f"# 回文: {len(palindromes):,}語\n")
        f.write(f"# 異なる単語のペア: {len(non_palindromes):,}組\n")
        f.write(f"# 生成日: {today}\n")
        f.write("\n")

        for word1, word2 in pairs:
            f.write(f"{word1} ↔ {word2}\n")

    print(f"\n結果を {output_path} に保存しました")

    # サンプル表示
    print("\n【サンプル（先頭20組）】")
    for i, (word1, word2) in enumerate(pairs[:20], 1):
        romaji1 = converter.to_romaji(word1)
        romaji2 = converter.to_romaji(word2)
        if word1 == word2:
            print(f"  {i:2}. 「{word1}」 ({romaji1}) [回文]")
        else:
            print(f"  {i:2}. 「{word1}」 ↔ 「{word2}」 ({romaji1} ↔ {romaji2})")

    return pairs


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='ひらがな単語リストからヘボン式ローマ字倒語ペアを抽出'
    )
    parser.add_argument(
        'input',
        nargs='?',
        default='data/unidic-kana-words-complete-hiragana.txt',
        help='入力ファイル（ひらがな単語リスト）'
    )
    parser.add_argument(
        'output',
        nargs='?',
        default='data/romaji-pairs/unidic-romaji-reverse-pairs.txt',
        help='出力ファイル'
    )
    parser.add_argument(
        '-e', '--encoding',
        default='utf-8',
        help='入力ファイルのエンコーディング（デフォルト: utf-8）'
    )

    args = parser.parse_args()

    # ファイルの存在確認
    if not os.path.exists(args.input):
        print(f"エラー: 入力ファイル '{args.input}' が見つかりません")
        sys.exit(1)

    # 処理実行
    find_romaji_reverse_pairs(args.input, args.output, args.encoding)

    print("\n処理完了！")


if __name__ == '__main__':
    main()
