# ディレクトリ構成

このドキュメントでは、`src/`フォルダ以下のディレクトリ構成について説明します。

## 概要

```plaintext
src/
├── data/           # データ読み込みと前処理
└── modules/        # 主要なモジュール群
```

## ディレクトリの詳細

### data/
| コンポーネント | 説明 | 主要なファイル |
|----------------|------|----------------|
| データバリデーション | データの整合性チェックとスキーマ定義 | `schema.py` |

### modules/
| コンポーネント | 説明 | ディレクトリ/ファイル |
|----------------|------|----------------------|
| 可視化 | 可視化モジュールのコンフィギュレーション | `plotly/` |


## 備考
- 各モジュールの詳細な説明は、それぞれのディレクトリ内のREADMEを参照してください
- 開発環境のセットアップについては、プロジェクトルートの`README.md`を参照してください
