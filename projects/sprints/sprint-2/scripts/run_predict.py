#!/usr/bin/env python
import argparse
import os
import json
from glob import glob
from ultralytics import YOLO


def run_predict(model, input_dir, outdir):
    categories = [d for d in glob(os.path.join(input_dir, "*")) if os.path.isdir(d)]
    all_preds = []
    for category_dir in categories:
        name = os.path.basename(category_dir)
        print(f"=== Processing: {name} ===")
        results = model.predict(source=category_dir, save=True)
        for r in results:
            all_preds.append(
                {
                    "path": r.path,
                    "filename": os.path.basename(r.path),
                    "boxes": r.boxes.xyxy.tolist(),
                    "scores": r.boxes.conf.tolist(),
                    "classes": r.boxes.cls.tolist(),
                    "category": name,
                }
            )
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "predictions.json")
    with open(out_path, "w") as f:
        json.dump(all_preds, f, indent=2)
    print(f"Saved {len(all_preds)} predictions to {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", required=True, help="入力ディレクトリ (例: data/public_resized)"
    )
    parser.add_argument(
        "--outdir",
        required=True,
        help="出力ディレクトリ (例: results/public_predictions)",
    )
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="YOLOモデル")
    args = parser.parse_args()

    model = YOLO(args.model)
    run_predict(model, args.input, args.outdir)


if __name__ == "__main__":
    main()
