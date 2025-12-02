# Sprint-2 README

> **注記**: このREADMEは Sprint-2 (2025/12/01〜2025/12/12) の成果物です。  
> Sprint終了時点で凍結されており、今後更新されません。失敗も含めてKnow-howとして参照可能です。

---

## 1. 計画
- ゴール: 公開データ（Open Images）を用いた分類器ベータ版の実装
- 成果物: 識別器コード、初期モデル、動作ログ
- 判定基準:
  - 熊クラスを含む公開データで分類器が動作すること
  - FP/FNを算出できる状態になっていること

---

## 2. 手順・仕様

- データ準備: Open Images Dataset から熊／犬／人／環境カテゴリを抽出
- 実行環境: Python 3.10.13, YOLOv8n, OpenCV, pandas
- 試験条件: 公開データを用いた分類タスク（座標情報は利用しない）
- 評価方法: 混同行列による分類精度の観察
- 出力: JSONログ（ラベル／信頼度）、混同行列、FP/FN結果

---

### 2.1 公開データの選定理由
- Googleが提供する大規模公開データセットであること
- 熊／犬／人／環境など対象カテゴリが揃っていること
- アノテーション情報が豊富で、将来的に物体検出タスクにも拡張可能であること
- 今回は「熊がいるか／いないか」を分類することが目的なので、座標情報は利用せずラベルのみを使用

---

### 2.2 データダウンロード

#### dl_openimages.py
- 概要: Open Images Dataset V7 から指定カテゴリの画像をダウンロードする
- 使用方法:
  ```bash
  cd data
  python dl_openimages.py --class Bear --limit 20 --split train
  python dl_openimages.py --class Dog --limit 20 --split validation
  python dl_openimages.py --class Person --limit 20 --split test
  python dl_openimages.py --class Tree --limit 20 --split train
  ```
- 引数:
  - `--class`: ダウンロード対象のクラス名（例: Bear, Dog, Person, Tree）
  - `--limit`: ダウンロード枚数上限（デフォルト100）
  - `--split`: 使用するデータセット split（train / validation / test）
- 出力: `public_raw/<class>/` 以下に画像ファイルを保存

##### データ取得に関する注意点

Open Images Dataset V7 のクラス指定によるダウンロードでは、指定クラスに関連する画像が必ずしも「主対象」として写っているとは限らない。例えば `Bear` クラスには、熊の剥製・ぬいぐるみ・絵画・背景に小さく写っているケースなどが含まれる場合がある。

そのため、本プロジェクトでは以下の運用ルールを採用する：

- 目標枚数の **倍程度の枚数**を `--limit` で指定してダウンロードする  
- ダウンロード後に **目視確認を行い、不要な画像を削除**する  
- 削除した枚数や理由を README に記録し、再現性を担保する  
- 最終的に残った画像を分類タスク用の `public_labels.csv` に反映する  

##### Sprint-2での運用

Sprint-2では分類器の動作確認と FP/FN の出力確認が目的であるため、各クラス（Bear / Dog / Person / Tree）で **10枚程度**を目標とし、`--limit` には **20** を指定する。偏りやノイズがあっても、動作確認ができれば十分とする。

---

### 2.3 リサイズ（サイズの統一）

- Sprint-1で作成した `resize_images.py` を改修し、入力／出力ディレクトリを指定できるようにした
- 入力: `public_raw/<class>/`
- 出力: `public_resized/<class>/`
- 使用方法:
  ```bash
  python resize_images.py --input public_raw --output public_resized --width 640 --height 480
  ```
- 引数:
  - `--input`: 入力ディレクトリ（例: public_raw）
  - `--output`: 出力ディレクトリ（例: public_resized）
  - `--width`: リサイズ後の幅（デフォルト640）
  - `--height`: リサイズ後の高さ（デフォルト480）

- 注意:
  - リサイズを行うと座標情報とのズレが発生するため、物体検出タスクでは利用できない
  - Sprint-2では分類タスクをトライするため、効率化（YOLO内部でのリサイズ処理を回避）のためリサイズを行う
  - 将来的に検出タスクへ移行する際は、リサイズ前の画像を利用すること

---

### 2.4 公開データの人力チェック（データ品質）
- 公開データセット（Open Images Dataset）を利用するため、人力による全件チェックは不要。
- ただし、主要クラス（熊・犬・人・環境）については、サンプル確認を行いラベル品質を確認する。
- 誤ラベルが見つかった場合は、除外または修正を行う。

---

### 2.5 ラベルCSVの生成
- Sprint-1で修正した `make_labels_csv.py` を流用
- 入力: `public_resized/<class>/`
- 出力: `public_labels.csv`
- 使用方法:
  ```bash
  python make_labels_csv.py --input public_resized --output public_labels.csv
  ```

---

### 2.6 推論と評価

1. YOLO推論  
   ```bash
   cd ..
   python scripts/run_predict.py --input data/public_resized --outdir results/public_predictions
   ```
2. 予測結果の結合  
   ```bash
   python scripts/merge_predictions.py --input results/public_predictions --output results/public_predictions.json
   ```
3. 評価スクリプト実行  
   ```bash
   python scripts/evaluate_fpfn.py --pred results/public_predictions.json --labels data/public_labels.csv --outdir results
   ```

---

## 3. 出力ファイルの見方

| ファイル名 | 内容 | 備考 |
|------------|------|------|
| `public_labels.csv` | 公開データのラベル一覧（分類タスク用） | 座標情報は含まれない |
| `fpfn_results.csv` | 真のラベルと予測ラベルの突き合わせ | FP/FNの確認に使用 |
| `confusion_matrix.csv` | ラベルごとの分類結果を集計した表 | 誤分類傾向を数値で把握可能 |
| `confusion_matrix.png` | 混同行列のヒートマップ画像 | 誤分類傾向を視覚的に確認できる |

> 🔍 **参考**: 混同行列（Confusion Matrix）とは？  
> https://scikit-learn.org/stable/visualizations.html#confusion-matrix  
> https://en.wikipedia.org/wiki/Confusion_matrix  

---

## 4. 今後の展望
- Sprint-3で公開データを用いた分類器の精度評価を実施予定
- Sprint-4以降で独自性データの収集を開始し、公開データと組み合わせて精度改善を図る
- 将来的には物体検出タスクに拡張し、距離推計や警報レベル制御に発展させる
