#!/usr/bin/env python3
import os
import argparse
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def resize_images(raw_dir, resized_dir, width, height, force_overwrite=False):
    for root, _, files in os.walk(raw_dir):
        for fname in files:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                infile = os.path.join(root, fname)
                rel_path = os.path.relpath(root, raw_dir)
                outfile_dir = os.path.join(resized_dir, rel_path)
                os.makedirs(outfile_dir, exist_ok=True)

                outfile = os.path.join(outfile_dir, os.path.splitext(fname)[0] + ".jpg")

                if os.path.exists(outfile) and not force_overwrite:
                    print(f"Skip existing resized file: {outfile}")
                    continue

                try:
                    with Image.open(infile) as img:
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        img = img.resize((width, height))
                        img.save(outfile, "JPEG")
                except Exception as e:
                    os.makedirs("results", exist_ok=True)
                    with open("results/resize_errors.txt", "a") as f:
                        f.write(f"Error resizing {infile}: {e}\n")
                    print(f"Error resizing {infile}: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, default=640, help="出力画像の幅")
    parser.add_argument("--height", type=int, default=480, help="出力画像の高さ")
    parser.add_argument(
        "--force-overwrite", action="store_true", help="既存ファイルを上書きする"
    )
    args = parser.parse_args()

    raw_dir = "raw"
    resized_dir = "resized"

    resize_images(raw_dir, resized_dir, args.width, args.height, args.force_overwrite)


if __name__ == "__main__":
    main()
