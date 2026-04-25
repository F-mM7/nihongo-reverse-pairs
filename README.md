# nihongo-reverse-pairs

日本語の倒語（逆読み）ペアを複数の辞書から探索するスクリプト・データ集です。

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
│   ├── dict/                                # 辞書ソースデータ
│   │   ├── unidic-filtered.txt              # UniDic（フィルタ済み）
│   │   ├── buta.txt                         # BUTA辞書
│   │   └── ippan.txt                        # 一般辞書
│   ├── pairs/                               # かな逆順ペア（スクリプト出力）
│   │   ├── unidic-reverse-pairs.txt
│   │   ├── ippan-reverse-pairs.txt
│   │   └── pairs-detailed.txt
│   └── romaji-pairs/                        # ローマ字逆順ペア（スクリプト出力）
│       ├── unidic-romaji-reverse-pairs.txt
│       ├── ippan-romaji-reverse-pairs.txt
│       └── buta-romaji-reverse-pairs.txt
├── docs/
│   ├── good-pairs.txt                       # 良ペアのキュレーション
│   └── check/                               # 確認用チェックリスト
│       ├── unidic-check.txt
│       ├── ippan-check.txt
│       └── romaji-check.txt
├── scripts/                                 # Python スクリプト
│   ├── extract-unidic-complete.py           # UniDic 抽出
│   ├── convert-katakana-to-hiragana.py      # カタカナ→ひらがな変換
│   ├── filter-invalid-words.py              # 不正語フィルタ
│   ├── find-unidic-reverse-pairs.py         # かな逆順ペア検索
│   ├── find-romaji-reverse-pairs.py         # ローマ字逆順ペア検索
│   └── search_hiragana_words.py             # ひらがな単語検索
└── src/                                     # Vite + React + TypeScript（現状は雛形のみ・未実装）
```

> **注**: `src/` の React 部分は Vite テンプレートの雛形が残っているのみで、UI は未実装です。本リポジトリの本体は `scripts/` の Python スクリプト群とその出力 (`data/`) です。

## ライセンス

MIT
