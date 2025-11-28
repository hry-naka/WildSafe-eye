#!/usr/bin/env python
import os
import csv


def main():
    base_dir = "resized"
    out_csv = "labels.csv"

    rows = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                filepath = os.path.relpath(os.path.join(root, file), base_dir)
                label = os.path.basename(root)
                filename = file  # basenameのみ追加
                rows.append([filepath, label, filename])

    with open(out_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filepath", "label", "filename"])
        writer.writerows(rows)

    print(f"Saved {len(rows)} entries to {out_csv}")


if __name__ == "__main__":
    main()
