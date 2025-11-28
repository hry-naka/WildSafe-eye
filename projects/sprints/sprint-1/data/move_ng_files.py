#!/usr/bin/env python3
import os
import csv
import shutil
import datetime


def move_ng_files(csv_path):
    # 日付タグを作成
    date_tag = datetime.datetime.now().strftime("%Y%m%d-%H%M")
    ng_raw_dir = os.path.join("raw", "not-good", date_tag)
    ng_resized_dir = os.path.join("resized", "not-good", date_tag)
    os.makedirs(ng_raw_dir, exist_ok=True)
    os.makedirs(ng_resized_dir, exist_ok=True)

    with open(csv_path, newline="", encoding="cp932") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # content_validity / annotation / variation のいずれかが ng なら対象
            if any(
                row[col] == "ng"
                for col in ["content_validity", "annotation", "variation"]
            ):
                relpath = row["filename"]
                raw_path = os.path.join("raw", relpath)
                resized_path = os.path.join("resized", relpath)

                if os.path.exists(raw_path):
                    shutil.move(
                        raw_path, os.path.join(ng_raw_dir, os.path.basename(raw_path))
                    )
                if os.path.exists(resized_path):
                    shutil.move(
                        resized_path,
                        os.path.join(ng_resized_dir, os.path.basename(resized_path)),
                    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python move_ng_files.py <checklist_csv>")
        sys.exit(1)
    move_ng_files(sys.argv[1])
