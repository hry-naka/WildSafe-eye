# プロジェクト運営ルール（PoC-Sprint方針）

## 1. ドキュメント運用
- 母体ドキュメント（Plan / Test Spec / Checklist）は常に最新を維持
- Sprint README は「計画／仕様／チェックリスト」の3要素を必須構成とする
- Sprint終了時に README を凍結し、履歴として残す（失敗もKnow-how）
- 母体に成果を反映したら、PoC関連3ファイル（Plan / Test Spec / Checklist）は統合後に削除可能

## 2. ディレクトリ構成
- `sprints/` 配下に Sprintごとの作業ディレクトリを作成
  - README.md（凍結注記あり）
  - scripts/（試行錯誤コード）
  - data/（データ収集・クレンジング・アノテーション用スクリプト＋データ）
  - results/（Sprint固有ログ）
- `rc/` 配下に安定版を集約
  - README.md（安定版の説明のみ、リリース直結）
  - scripts/（再現性確認済みコード）
  - data/（構造雛形のみ）
  - results/（判定基準を満たした成果物）

## 3. 再現性担保
- README に最低限の環境条件（Pythonバージョン＋主要ライブラリ）を記載
- 再現できなかった場合は母体ドキュメントに追記
- RC配下は「再現性確認済み」の成果物のみを残す

## 4. バックログ管理
- `docs/00_overview/01_plan.md` に直近数Sprintのラフスケッチ＋バックログ母体を記載
- Sprint完了時には該当スプリントのラフスケッチを削除し、未来のスプリントのみ残す