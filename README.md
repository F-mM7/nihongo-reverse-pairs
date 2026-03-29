# nihongo-reverse-pairs

日本語の倒語（逆読み）ペアを複数の辞書から探索するデータ・スクリプト集です。

## 概要

UniDic・BUTA・一般辞書などのかな単語リストから、ひらがな逆順およびヘボン式ローマ字逆順で倒語になるペアを抽出します。

### 例

| 方式 | ペア例 |
|------|--------|
| ひらがな逆順 | いなか ↔ かない、くろうと ↔ とうろく |
| ローマ字逆順 | いけ(ike) ↔ えき(eki) |

## ディレクトリ構造

```
nihongo-reverse-pairs/
├── data/
│   ├── dict/                           # 辞書ソースデータ
│   │   ├── raw/                        # 辞書生データ
│   │   ├── unidic-filtered.txt         # UniDic（フィルタ済み）
│   │   ├── buta.txt                    # BUTA辞書
│   │   └── ippan.txt                   # 一般辞書
│   ├── pairs/                          # かな逆順ペア（スクリプト出力）
│   │   ├── unidic-reverse-pairs.txt
│   │   ├── ippan-reverse-pairs.txt
│   │   └── pairs-detailed.txt
│   └── romaji-pairs/                   # ローマ字逆順ペア（スクリプト出力）
│       ├── unidic-romaji-reverse-pairs.txt
│       ├── ippan-romaji-reverse-pairs.txt
│       └── buta-romaji-reverse-pairs.txt
├── docs/
│   ├── good-pairs.txt                  # 良い回文ペア（キュレーション済み）
│   └── check/                          # 確認用チェックリスト
├── scripts/                            # Pythonスクリプト
│   ├── find-unidic-reverse-pairs.py    # かな回文ペア検索
│   ├── find-romaji-reverse-pairs.py    # ローマ字回文ペア検索
│   ├── extract-unidic-complete.py      # UniDicデータ抽出
│   ├── convert-katakana-to-hiragana.py # カタカナ→ひらがな変換
│   ├── filter-invalid-words.py         # 不正語フィルタ
│   └── search_hiragana_words.py        # ひらがな単語検索
└── src/                                # React + TypeScript（フロントエンド）
```

## ライセンス

MIT
