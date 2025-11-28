#!/usr/bin/env python3
import os
import csv
import hashlib
import re
import shutil
from PIL import Image

VALID_EXT = {".jpg", ".jpeg", ".png"}


def get_image_info(path):
    """画像のサイズ・解像度・フォーマットを返す"""
    if not os.path.exists(path):
        return ("-", "-", "-")
    size = os.path.getsize(path)
    if size == 0:
        return ("0KB", "-", "-")
    try:
        with Image.open(path) as img:
            resolution = f"{img.width}x{img.height}"
            fmt = img.format
    except Exception:
        resolution, fmt = "-", "-"
    return (f"{size//1024}KB", resolution, fmt)


def get_hash(path):
    """MD5ハッシュを返す（重複検出用）"""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return None
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_filepaths(base_dir):
    """サブディレクトリを含めて画像ファイルの相対パスを収集（not-good以下は除外）"""
    filepaths = set()
    for root, _, files in os.walk(base_dir):
        # not-good 以下は対象外
        if "not-good" in root:
            continue
        for f in files:
            ext = os.path.splitext(f.lower())[1]
            if ext in VALID_EXT:
                relpath = os.path.relpath(os.path.join(root, f), base_dir)
                filepaths.add(relpath)
    return filepaths


def natural_key(path):
    """自然順ソート用キー"""
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", path)
    ]


def main(output_csv):
    raw_dir = "raw"
    resized_dir = "resized"

    # raw と resized のファイルパスを突き合わせ
    filepaths = collect_filepaths(raw_dir) | collect_filepaths(resized_dir)

    rows = []
    hash_map = {}

    for relpath in sorted(filepaths, key=natural_key):
        raw_path = os.path.join(raw_dir, relpath)
        resized_path = os.path.join(resized_dir, relpath)

        raw_size, raw_res, raw_fmt = get_image_info(raw_path)
        resized_size, resized_res, resized_fmt = get_image_info(resized_path)

        # 重複チェック（raw優先）
        h = get_hash(raw_path) or get_hash(resized_path)
        duplicate = "-"
        if h:
            if h in hash_map:
                duplicate = hash_map[h]
                # ★ 重複が見つかった場合は resized 側を not-good に移動
                if os.path.exists(resized_path):
                    ng_dir = os.path.join(resized_dir, "not-good")
                    os.makedirs(ng_dir, exist_ok=True)
                    dest_path = os.path.join(ng_dir, os.path.basename(resized_path))
                    shutil.move(resized_path, dest_path)
            else:
                hash_map[h] = relpath

        rows.append(
            [
                relpath,
                raw_size,
                raw_res,
                raw_fmt,
                resized_size,
                resized_res,
                resized_fmt,
                duplicate,
                "",  # content_validity（人力）
                "",  # watermark（人力）
                "",  # variation（人力）
                "",  # annotation（人力）
            ]
        )

    # CSV出力
    header = [
        "filename",
        "raw_size",
        "raw_resolution",
        "raw_format",
        "resized_size",
        "resized_resolution",
        "resized_format",
        "duplicate",
        "content_validity",
        "watermark",
        "variation",
        "annotation",
    ]
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python create_checklist_template.py <output_csv>")
        sys.exit(1)
    main(sys.argv[1])
