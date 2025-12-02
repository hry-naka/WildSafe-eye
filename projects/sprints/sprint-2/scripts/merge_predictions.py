#!/usr/bin/env python
import os
import json
import glob
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="入力ディレクトリ (例: results/public_predictions)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="出力ファイル (例: results/public_predictions.json)",
    )
    args = parser.parse_args()

    all_preds = []
    for path in glob.glob(os.path.join(args.input, "*.json")):
        with open(path) as f:
            data = json.load(f)
            if isinstance(data, dict):
                data = [data]
            for d in data:
                if "path" in d:
                    d["filename"] = os.path.basename(d["path"])
                elif "name" in d:
                    d["filename"] = d["name"]
                else:
                    d["filename"] = "UNKNOWN"
                all_preds.append(d)

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(all_preds, f, indent=2)

    print(f"Merged {len(all_preds)} predictions into {args.output}")


if __name__ == "__main__":
    main()
