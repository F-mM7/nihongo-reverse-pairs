#!/usr/bin/env python3
"""
UniDicひらがな単語リストを正規表現で検索するスクリプト
"""
import re
import sys
from pathlib import Path

def search_words(pattern, file_path, ignore_case=False, show_line_numbers=True):
    """
    正規表現パターンで単語を検索

    Args:
        pattern: 正規表現パターン
        file_path: 検索対象ファイルパス
        ignore_case: 大文字小文字を無視（ひらがなのみなので通常は不要）
        show_line_numbers: 行番号を表示

    Returns:
        マッチした単語のリスト
    """
    flags = re.IGNORECASE if ignore_case else 0
    try:
        regex = re.compile(pattern, flags)
    except re.error as e:
        print(f"エラー: 無効な正規表現パターン - {e}")
        return []

    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                # 行番号と矢印を除去して単語部分のみ取得
                # フォーマット: "    123→あいうえお"
                if '→' in line:
                    word = line.split('→', 1)[1]
                else:
                    word = line

                if regex.search(word):
                    if show_line_numbers:
                        matches.append(f"{line_num:6d}→{word}")
                    else:
                        matches.append(word)

    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません - {file_path}")
        return []
    except Exception as e:
        print(f"エラー: ファイル読み込み中にエラーが発生しました - {e}")
        return []

    return matches

def main():
    """メイン処理"""
    import argparse

    parser = argparse.ArgumentParser(
        description='UniDicひらがな単語リストを正規表現で検索',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # "あい"で始まる単語を検索
  python search_hiragana_words.py "^あい"

  # "ん"で終わる単語を検索
  python search_hiragana_words.py "ん$"

  # "っ"を含む単語を検索
  python search_hiragana_words.py "っ"

  # 3文字の単語を検索
  python search_hiragana_words.py "^.{3}$"

  # "あ"で始まり"う"で終わる単語
  python search_hiragana_words.py "^あ.*う$"

  # 同じ文字が2回以上連続する単語
  python search_hiragana_words.py "(.)\\1"

  # 回文（前から読んでも後ろから読んでも同じ）を検索
  # ※簡易的な2-3文字の回文のみ
  python search_hiragana_words.py "^(.)(.)(\\1)$|^(.)(.)(.)(\\2)(\\1)$"
"""
    )

    parser.add_argument('pattern',
                       help='検索する正規表現パターン')
    parser.add_argument('-f', '--file',
                       default='data/unidic-kana-words-complete-hiragana.txt',
                       help='検索対象ファイル（デフォルト: data/unidic-kana-words-complete-hiragana.txt）')
    parser.add_argument('-n', '--no-line-numbers',
                       action='store_true',
                       help='行番号を表示しない')
    parser.add_argument('-c', '--count',
                       action='store_true',
                       help='マッチ件数のみ表示')
    parser.add_argument('-l', '--limit',
                       type=int,
                       help='表示する結果の最大数')

    args = parser.parse_args()

    # ファイルパスを解決
    if not Path(args.file).is_absolute():
        # 相対パスの場合、スクリプトの親ディレクトリを基準にする
        script_dir = Path(__file__).parent.parent
        file_path = script_dir / args.file
    else:
        file_path = Path(args.file)

    # 検索実行
    matches = search_words(
        args.pattern,
        file_path,
        show_line_numbers=not args.no_line_numbers
    )

    # 結果表示
    if args.count:
        print(f"マッチ件数: {len(matches)}")
    else:
        if matches:
            print(f"検索パターン: {args.pattern}")
            print(f"マッチ件数: {len(matches)}")
            print("-" * 40)

            display_matches = matches[:args.limit] if args.limit else matches
            for match in display_matches:
                print(match)

            if args.limit and len(matches) > args.limit:
                print(f"\n... 他 {len(matches) - args.limit} 件")
        else:
            print(f"パターン '{args.pattern}' にマッチする単語が見つかりませんでした。")

    return 0 if matches else 1

if __name__ == '__main__':
    sys.exit(main())