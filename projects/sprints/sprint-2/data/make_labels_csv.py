#!/usr/bin/env python3
import os
import argparse
import csv
from collections import defaultdict


def make_labels_csv(input_dir, output_csv):
    rows = []
    class_counts = defaultdict(int)

    for class_name in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, class_name)
        if not os.path.isdir(class_dir):
            continue
        for fname in os.listdir(class_dir):
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                filepath = os.path.join(class_dir, fname)
                rows.append([filepath, class_name])
                class_counts[class_name] += 1

    # CSV出力
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filepath", "label"])
        writer.writerows(rows)

    print(f"Labels CSV generated: {output_csv} ({len(rows)} entries)")
    for cls, count in class_counts.items():
        print(f"  {cls}: {count} images")


def main():
    parser = argparse.ArgumentParser(
        description="Generate labels CSV from image directories"
    )
    parser.add_argument(
        "--input", required=True, help="入力ディレクトリ (例: public_resized)"
    )
    parser.add_argument(
        "--output", required=True, help="出力CSVファイル (例: public_labels.csv)"
    )
    args = parser.parse_args()

    make_labels_csv(args.input, args.output)


if __name__ == "__main__":
    main()
