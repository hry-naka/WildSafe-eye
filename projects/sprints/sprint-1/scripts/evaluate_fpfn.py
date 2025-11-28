#!/usr/bin/env python
import os
import json
import pandas as pd
import matplotlib.pyplot as plt


def evaluate(pred_file, labels_file, outdir):
    # 予測結果をロード
    with open(pred_file) as f:
        preds = json.load(f)

    # filename -> predicted_class の辞書を作成
    pred_dict = {}
    for d in preds:
        fname = d["filename"]
        # YOLOの出力は複数クラスがあり得るが、ここでは最初のクラスだけを採用
        if d["classes"]:
            pred_class = d["classes"][0]
        else:
            pred_class = None
        pred_dict[fname] = pred_class

    # ラベルをロード
    df = pd.read_csv(labels_file)

    y_true = []
    y_pred = []
    for _, row in df.iterrows():
        fname = row["filename"]
        true_label = row["label"]
        pred_label = pred_dict.get(fname, None)
        y_true.append(true_label)
        y_pred.append(pred_label)

    # 結果を保存
    results = pd.DataFrame({"true": y_true, "pred": y_pred})
    results.to_csv(os.path.join(outdir, "fpfn_results.csv"), index=False)

    # 混同行列を作成
    cm = pd.crosstab(
        pd.Series(y_true, name="True"), pd.Series(y_pred, name="Pred"), dropna=False
    )
    cm.to_csv(os.path.join(outdir, "confusion_matrix.csv"))

    # 可視化
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, cmap="Blues")
    plt.xticks(range(len(cm.columns)), cm.columns, rotation=90)
    plt.yticks(range(len(cm.index)), cm.index)
    plt.colorbar()
    plt.title("Confusion Matrix (Classification)")
    plt.savefig(os.path.join(outdir, "confusion_matrix.png"))
    plt.close()

    print("Evaluation complete. Results saved to", outdir)


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--pred", required=True, help="Path to merged predictions.json")
    parser.add_argument("--labels", required=True, help="Path to labels.csv")
    parser.add_argument("--outdir", required=True, help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    evaluate(args.pred, args.labels, args.outdir)


if __name__ == "__main__":
    main()
