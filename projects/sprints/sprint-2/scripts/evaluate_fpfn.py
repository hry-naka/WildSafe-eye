#!/usr/bin/env python
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import argparse


def evaluate(pred_file, labels_file, outdir):
    with open(pred_file) as f:
        preds = json.load(f)

    pred_dict = {}
    for d in preds:
        fname = d["filename"]
        pred_class = d["classes"][0] if d.get("classes") else None
        pred_dict[fname] = pred_class

    df = pd.read_csv(labels_file)

    y_true, y_pred = [], []
    for _, row in df.iterrows():
        filepath = row["filepath"]
        fname = os.path.basename(filepath)
        true_label = row["label"]
        pred_label = pred_dict.get(fname, None)
        y_true.append(true_label)
        y_pred.append(pred_label)

    results = pd.DataFrame({"true": y_true, "pred": y_pred})
    results.to_csv(os.path.join(outdir, "fpfn_results.csv"), index=False)

    cm = pd.crosstab(
        pd.Series(y_true, name="True"), pd.Series(y_pred, name="Pred"), dropna=False
    )
    cm.to_csv(os.path.join(outdir, "confusion_matrix.csv"))

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
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pred",
        required=True,
        help="予測結果JSON (例: results/public_predictions.json)",
    )
    parser.add_argument(
        "--labels", required=True, help="ラベルCSV (例: data/public_labels.csv)"
    )
    parser.add_argument(
        "--outdir", required=True, help="出力ディレクトリ (例: results)"
    )
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    evaluate(args.pred, args.labels, args.outdir)


if __name__ == "__main__":
    main()
