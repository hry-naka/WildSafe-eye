#!/usr/bin/env python
import argparse
import os
import json
from glob import glob
from ultralytics import YOLO


def run_predict_for_dir(model, category_dir, outdir):
    results = model.predict(source=category_dir, save=True)
    preds = []
    for r in results:
        preds.append(
            {
                "path": r.path,
                "filename": os.path.basename(r.path),
                "boxes": r.boxes.xyxy.tolist(),
                "scores": r.boxes.conf.tolist(),
                "classes": r.boxes.cls.tolist(),
            }
        )
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "predictions.json"), "w") as f:
        json.dump(preds, f, indent=2)
    print(f"Saved {len(preds)} predictions to {outdir}/predictions.json")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run predictions for all subdirectories under data/resized",
    )
    parser.add_argument(
        "--category",
        type=str,
        help="Run predictions for a specific category (subdirectory name)",
    )
    parser.add_argument(
        "--model", type=str, default="yolov8n.pt", help="YOLO model to use"
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        default="data/resized",
        help="Base directory containing categories",
    )
    parser.add_argument(
        "--results_dir", type=str, default="results", help="Output results directory"
    )
    args = parser.parse_args()

    model = YOLO(args.model)

    if args.all:
        categories = [
            d for d in glob(os.path.join(args.base_dir, "*")) if os.path.isdir(d)
        ]
        for category_dir in categories:
            name = os.path.basename(category_dir)
            outdir = os.path.join(args.results_dir, f"pred_{name.replace(' ', '_')}")
            print(f"=== Processing: {name} ===")
            run_predict_for_dir(model, category_dir, outdir)
    elif args.category:
        category_dir = os.path.join(args.base_dir, args.category)
        if not os.path.isdir(category_dir):
            raise FileNotFoundError(f"{category_dir} does not exist")
        outdir = os.path.join(
            args.results_dir, f"pred_{args.category.replace(' ', '_')}"
        )
        print(f"=== Processing: {args.category} ===")
        run_predict_for_dir(model, category_dir, outdir)
    else:
        print("Please specify either --all or --category <name>")


if __name__ == "__main__":
    main()
