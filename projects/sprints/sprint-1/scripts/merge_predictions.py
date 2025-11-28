#!/usr/bin/env python
import os
import json
import glob


def main():
    outdir = "results/predictions"
    os.makedirs(outdir, exist_ok=True)

    all_preds = []
    for path in glob.glob("results/pred_*/*.json"):
        with open(path) as f:
            data = json.load(f)
            # data が dict の場合はリストに包む
            if isinstance(data, dict):
                data = [data]
            for d in data:
                # YOLO API 出力から filename を必ず追加
                if "path" in d:
                    d["filename"] = os.path.basename(d["path"])
                elif "name" in d:
                    d["filename"] = d["name"]
                else:
                    d["filename"] = "UNKNOWN"
                all_preds.append(d)

    out_path = os.path.join(outdir, "predictions.json")
    with open(out_path, "w") as f:
        json.dump(all_preds, f, indent=2)

    print(f"Merged {len(all_preds)} predictions into {out_path}")


if __name__ == "__main__":
    main()
