#!/usr/bin/env python3
import argparse
import os
import requests
from dotenv import load_dotenv

# .envから読み込む
load_dotenv()
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if not PEXELS_API_KEY:
    raise RuntimeError(
        "PEXELS_API_KEY が設定されていません。 .env を確認してください。"
    )

# ハードコーディングされた検索語セット
CATEGORIES = {
    "bear": [
        "bear close up",
        "bear in snow",
        "bear walking",
        "bear in forest",
        "bear in river",
    ],
    "dog": ["domestic dog", "wolf in forest", "husky sled dog"],
    "human": ["hiker in forest", "runner outdoors", "person close up portrait"],
    "env": [
        "dense forest landscape",
        "snowy mountain",
        "river scenery",
        "snow covered trees",
    ],
}

BASE_URL = "https://api.pexels.com/v1/search"


def download_images(keyword, limit, outdir, force_overwrite=False):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": keyword, "per_page": limit}
    resp = requests.get(BASE_URL, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()
    os.makedirs(outdir, exist_ok=True)
    for i, photo in enumerate(data.get("photos", [])):
        url = photo["src"]["large"]
        fname = os.path.join(outdir, f"{keyword}_{i}.jpg")
        if os.path.exists(fname) and not force_overwrite:
            print(f"Skip existing file: {fname}")
            continue
        img = requests.get(url)
        with open(fname, "wb") as f:
            f.write(img.content)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "subcategory",
        nargs="?",
        default="all",
        choices=["bear", "dog", "human", "env", "all"],
        help="ダウンロード対象のサブカテゴリ",
    )
    parser.add_argument("--limit", type=int, default=100, help="各検索語ごとのDL枚数")
    parser.add_argument(
        "--force-overwrite", action="store_true", help="既存ファイルを上書きする"
    )
    args = parser.parse_args()

    if args.subcategory == "all":
        targets = CATEGORIES.values()
    else:
        targets = [CATEGORIES[args.subcategory]]

    for group in targets:
        for keyword in group:
            outdir = os.path.join("raw", keyword)
            print(f"Downloading {args.limit} images for {keyword}...")
            download_images(keyword, args.limit, outdir, args.force_overwrite)


if __name__ == "__main__":
    main()
