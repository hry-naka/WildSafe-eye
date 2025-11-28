# Sprint-1 README

# Sprint-1 README

> **注記**: このREADMEは Sprint-1 (2025/11/10〜2025/11/28) の成果物です。  
> Sprint終了時点で凍結されており、今後更新されません。失敗も含めてKnow-howとして参照可能です。

---

## 1. 計画
- ゴール: 評価スクリプト雛形完成（FP/FNを数値化できる状態）
- 成果物: 評価レポート（初期精度の観察）、検証コード、ログ
- 判定基準: 
   - FP/FNを定量的に算出できること
   - 環境カテゴリのバリエーションが他カテゴリと同程度に収集できていること
   - 300データの人力チェックにかかる工数（時間）が測定・収集できていること（「100枚ごとにかかった時間」を記録しておく）

---

## 2. 手順・仕様

- データ準備: 熊映像＋類似動物＋環境映像
- 実行環境: Python 3.10.13, YOLOv8n, OpenCV, ffmpeg, pandas
- 試験条件: 昼夜／近遠距離／遮蔽ありなし
- 評価方法: IoU ≥ 0.5 を検出成功とみなし、FN/FP率を算出
- 出力: JSONログ（ラベル／信頼度／時刻）、混同行列、距離別リコール

本プロジェクトは Python 仮想環境上で動作します。以下の手順で環境を再現できます。

### 2.1 環境準備
#### 2.1.1 pyenvでグローバルを3.10.13に変更
```bash
pyenv global 3.10.13
exec $SHELL -l
python -V
python3 -V
```
3.10.13になっていることを確認する

#### 2.1.2 仮想環境を作り直す
既存の `.venv` を削除して、新しい環境を作成します：
```bash
rm -rf .venv
python3 -m venv .venv
```

#### 2.1.3 有効化して依存パッケージを再インストール
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 2.2 データ収集

#### dl-raw-multi.py
- 概要: Pexels API を利用して検索語ごとに画像をダウンロードする
- 検索語はコード内にハードコーディングされ、サブカテゴリとして定義される
  - bear: 熊関連（例: bear, grizzly bear, brown bear）
  - dog: 犬／狼関連（例: dog, wolf, husky）
  - human: 人間関連（例: human, person, hiker）
  - env: 環境関連（例: forest, mountain, river, snow）
- 使用方法:
  ```bash
  cd data #画像データ関連の作業はdata配下で実施
  python dl-raw-multi.py bear --limit 400
  python dl-raw-multi.py env --limit 200
  python dl-raw-multi.py all --limit 100   # 全カテゴリ
  python dl-raw-multi.py env --limit 200 --force-overwrite
  python dl-raw-multi.py                   # 引数省略時は all と同じ
  ```
- 引数:
  - 第一引数: サブカテゴリ（bear, dog, human, env, all）
  - `--limit`: 各検索語ごとのダウンロード枚数上限（デフォルト100）
- 出力: `raw/<検索語>/` 以下に画像ファイルを保存
- 備考: APIキーは.env内に `PEXELS_API_KEY` に設定しておくこと
- 備考: デフォルトでは既存ファイルを上書きしません。既存ファイルを上書きしたい場合は `--force-overwrite` を指定してください。指定しない場合は不足分が追加DLされます。

---

### 2.3 リサイズ（サイズの統一）
#### resize_images.py
- 概要: `raw/` 以下の画像を一括リサイズし、`resized/` に保存する
- 入力: `raw/<カテゴリ>/` 以下の画像群
- 出力: `resized/<カテゴリ>/` 以下にリサイズ済み画像を保存
- 使用方法:
  ```bash
  python resize_images.py --width 640 --height 480
  ```
  - `--width` : 出力画像の幅（省略時は640）
  - `--height`: 出力画像の高さ（省略時は480）
- 備考: デフォルトでは既存ファイルを上書きしません。既存ファイルを上書きしたい場合は `--force-overwrite` を指定してください。

**利用上の注意：DL前のバックアップ**
   - 新たに画像をDLする前に、既存の `data/raw/` をバックアップしておく:
     ```bash
     tar zcvf old-raw/raw-<日付>-<回数>.tar.gz raw
     ```
   - バックアップ後に `raw/` `resized/` を削除してクリーンな状態にする:
     ```bash
     rm -rf raw
     rm -rf resized
     ```

---

### 2.4 人力チェック

#### 人力チェックテンプレート出力ツール仕様
`python create_checklist_template.py <output_csv>`

##### 目的
- 画像データの正常性チェックを自動化し、人力確認が必要な観点をテンプレート化する
- 工数測定の基盤を整備する
- 重複画像を自動的に検出し、resized 配下から除外することで人力チェック対象を削減する

##### 適用対象
- raw/ と resized/ の両方を参照する
- 人力チェックは基本的に resized データを対象とする
- raw に関する情報は参考値として出力する
- resized 配下で重複が検出された場合は、自動的に `resized/not-good/` に移動される（raw 側は移動しない）
- `not-good/` 以下は次回以降の実行時に対象外となる

##### 出力仕様
- size / resolution / format は raw と resized の両方を出力する
- 出力CSVの列構成例:
  - `filename`
  - `raw_size`, `raw_resolution`, `raw_format`
  - `resized_size`, `resized_resolution`, `resized_format`
  - `duplicate`
  - `content_validity`（人力確認欄）
  - `watermark`（人力確認欄）
  - `variation`（人力確認欄）
  - `annotation`（人力確認欄）

##### 備考
- ファイル名はカテゴリ付き相対パスで出力される（例: `bear close up/bear close up_0.jpg`）
- 出力順序は自然順ソート（例: `_0.jpg` → `_1.jpg` → `_2.jpg` → … → `_10.jpg`）

---

## チェック観点

### 2.4.1 画像の品質・形式が妥当か？
- ファイルサイズ（0バイト検出） → raw/resized_size を参照
- 解像度（幅×高さ） → raw/resized_resolution を参照
- フォーマット（JPEG/PNG判定） → raw/resized_format を参照

### 2.4.2 コンテンツの妥当性 : `content_validity` に確認結果を記入
- 検索語に沿った画像か（例: "bear" で人間写真が混入していないか）
- 類似カテゴリとの混同がないか（例: dog と wolf）
- 環境カテゴリで対象動物が写っている誤混入がないか

### 2.4.3 透かし・ノイズ : `watermark` に確認結果を記入
- 透かし文字やロゴが入っていないか
- 広告画像やコラージュが混ざっていないか
- OCRで拾えそうな透かしがある場合は候補として記録

### 2.4.4 重複・バリエーション
- **重複（自動化）**: ハッシュ比較で検出し、重複ファイル名を出力 → `duplicate` 列に記録
- **バリエーション（人力）**: 類似画像の判定は人間が確認 → `variation` に記録

### 2.4.5 ラベル付け前提確認 : `annotation` に確認結果を記入
- 正例についてのみチェック
- 対象が明確に写っているか（小さすぎない／隠れていない）
- アノテーション困難な画像（極端なブレ、暗すぎるなど）を除外するか判断

#### 判定ガイド

##### variationあり（OK扱い）
- 顔の向きが異なる → 正面／斜め／横顔  
- 表情が異なる → 口の開閉、目の向き  
- 構図や背景が異なる → アップ／引き／角度違い  
- 動きが異なる → 歩く／止まる／泳ぐ  

##### variationなし（類似とみなす）
- 明るさや色味だけ違う（フィルター違い）  
- トリミングだけ違う（ほぼ同じ構図）  
- サイズや解像度だけ違う（raw/resizedの差）  

##### 正例（熊あり画像）
- 熊を矩形で囲む想定でチェック
- variationタグを付与（人力で付けたものをground truthとして扱う） 　#tmplate出力にタグ列を追加する（backlog） 
- variationタグの記入例：bear_by_river, dog_closeup, snowy_forest_with_cabin
- 判別可能性（サイズ・遮蔽・明るさ）を確認  

##### 負例（熊なし画像）
- 矩形は不要  
- 熊がいないことを確認  
- カテゴリ（env, dog, human）を記録  　# template出力にカテゴリ列を追加（backlog）
- 誤検出しやすい「ハードネガティブ」を整理  #　`hard negative`列の追加（backlog）FP分析用に活用予定

#### 参考：（create_checklist_template.pyに機能統合済）
```     
  ##### check_duplicates.py
  - 概要: `raw/` 以下の画像群から重複画像を検出し、ログに記録する
  - 処理: 平均ハッシュ（`imagehash.average_hash`）を用いて類似画像を判定
  - 出力: `results/duplicates_log.txt` に重複ペアを記録
  - 使用方法:
    ```bash
    python check_duplicates.py --input raw --threshold 0
    ```
    - `--input`: 検査対象の画像ディレクトリ（デフォルトは `raw/`）
    - `--threshold`: ハッシュ距離の許容値（0なら完全一致、1以上で類似も検出）
  - 注意事項:完全一致はこのツールを用いて除外すること、類似は基本的に目視確認する
```     

#### 人力チェックのファイル整理
#### NGファイル移動ツール

- 人力チェック完了後、CSVに `ng` が記入されたファイルを自動で not-good に移動する
- 使用方法:
  ```bash
  python move_ng_files.py checklist.csv
  ```


3. ラベルCSVの生成
#### make_labels_csv.py
- 概要: `resized/` 以下の画像を走査し、ラベルCSVを生成する
- 入力: `resized/<カテゴリ>/` 以下の画像群
- 出力: `labels.csv`（実行ディレクトリ直下に生成される）
- 使用方法:
  ```bash
  python make_labels_csv.py
  ```

###　3.はSprint-1では実施しない
```
3. アノテーションツールのインストールと起動
3.1.　インストール
```bash
pip install pyqt5 lxml
git clone https://github.com/heartexlabs/labelImg.git
cd labelImg
pyrcc5 -o libs/resources.py resources.qrc
```

3.2.　起動
```bash
python labelImg/labelImg.py
```

3.3. ラベリング作業
• 画像フォルダを開く → resized/ を指定
• 保存フォーマット選択 → YOLO形式か Pascal VOC形式を選ぶ
• 矩形描画 → マウスで対象を囲み、ラベル名を入力
• 保存 → 各画像ごとに .txt (YOLO) または .xml (VOC) が生成される

3.4. 出力確認
• YOLO形式なら resized/<カテゴリ>/<画像名>.txt に座標＋ラベルが保存される
• これを labels.csv に統合するか、YOLOの学習に直接利用できる
```

---

### FP/FN数値化までの手順

1. **推論実行**
   - YOLOv8n を用いて `data/resized/` 以下の画像を推論する
   - 出力形式: JSON（画像ファイル名、検出ラベル、信頼度、座標）
   - 保存先: `results/pred_<カテゴリ名>/predictions.json`
   - 使用方法（例: scripts/run_predict.py）:
     ```bash
     python scripts/run_predict.py --all
     ```
     - `--all`: `data/resized/` 以下の全カテゴリを対象に推論
     - `--category <カテゴリ名>`: 特定カテゴリのみ推論

2. **予測結果の結合**
   - 各カテゴリの `predictions.json` を1つにまとめる
   - 保存先: `results/predictions/predictions.json`
   - 使用方法:
     ```bash
     python scripts/merge_predictions.py
     ```

3. **評価スクリプトの実行**
   - 入力: 結合済み予測JSON (`results/predictions/predictions.json`) + ラベルCSV (`data/labels.csv`)
   - 出力:
     - `results/fpfn_results.csv`
     - `results/confusion_matrix.csv`
     - `results/confusion_matrix.png`
   - 使用方法:
     ```bash
     python scripts/evaluate_fpfn.py --pred results/predictions/predictions.json --labels data/labels.csv --outdir results
     ```

---

## 出力ファイルの見方

| ファイル名 | 内容 | 備考 |
|------------|------|------|
| `fpfn_results.csv` | 各画像の真のラベルと予測ラベルを一覧化 | FP/FNの突き合わせに使用。空欄は未検出を示す |
| `confusion_matrix.csv` | ラベルごとの分類結果を集計した表 | モデルがどのラベルをどれだけ誤分類したかを数値で把握可能 |
| `confusion_matrix.png` | 混同行列のヒートマップ画像 | 誤分類傾向を視覚的に確認できる。色が濃いほど分類数が多い |

> 🔍 **参考**: 混同行列（Confusion Matrix）とは？  
> https://scikit-learn.org/stable/visualizations.html#confusion-matrix  
> https://en.wikipedia.org/wiki/Confusion_matrix  
> モデルの分類性能を可視化するための基本的な評価指標です。

---

