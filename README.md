# WildSafe-Eye

## 概要
野生動物（特に熊）の検知・識別を目的としたプロジェクトです。  
公開データセットと独自性データを組み合わせ、分類 → 物体検出 → 距離推計 → ヒステリシス挙動確認へと段階的に発展させていきます。

## プロジェクトの目的
- 熊の存在を分類器で検知
- 物体検出による位置情報の取得
- 距離推計による警報レベル制御
- ヒステリシス挙動の安定性確認
- 現場環境に即した独自性データの収集と活用

## スプリント計画
- Sprint-1: データ取得・リサイズ・正常性チェック
- Sprint-2: 公開データを用いた分類器ベータ版
- Sprint-3: 分類器の精度評価（FP/FN定量化）
- Sprint-4: 独自性データの収集方法確立
- Sprint-5: 独自性データのアノテーション方法確立
- Sprint-6: 距離推計の導入
- Sprint-7: ヒステリシス挙動の安定性確認

## ディレクトリ構成
```
WildSafe-Eye/
├── docs/          # 計画・設計資料
├── projects/
│   └── sprints/   # 各スプリント成果物
├── scripts/       # 推論・評価用スクリプト
├── data/          # データ関連（raw/resizedは.gitignore対象）
└── results/       # 実行結果（.gitignore対象）
```

## セットアップ
```bash
# Python環境準備
pyenv global 3.10.13
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 実行例
`project/sprints/sprint-?/README.md`を参照

## ライセンス
MIT License


