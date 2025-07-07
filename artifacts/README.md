# Artifacts ディレクトリ構造

```
artifacts/
├── models/              # 学習済みモデル
│   ├── {model_name}/
│   │   ├── version_001/
│   │   │   ├── model.pth       # PyTorch state dict
│   │   │   ├── config.json     # モデル設定
│   │   │   └── metadata.json   # 学習指標とメタデータ
│   │   └── version_002/
│   └── {other_model}/
└── checkpoints/         # 学習途中の一時保存
```

## 格納内容

- `model.pth`: モデルの重み
- `config.json`: モデルのアーキテクチャとハイパーパラメータ
- `metadata.json`: 学習時の損失値、エポック数、タイムスタンプ

実験の追跡と再現性のため、モデルのバージョンは個別のディレクトリで管理されます。
