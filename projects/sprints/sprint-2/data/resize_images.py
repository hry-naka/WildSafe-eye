#!/usr/bin/env python3
import os
import argparse
from PIL import Image
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


def resize_images(input_dir, output_dir, width, height, force_overwrite=False):
    for root, _, files in os.walk(input_dir):
        for fname in files:
            if fname.lower().endswith((".jpg", ".jpeg", ".png")):
                infile = os.path.join(root, fname)
                rel_path = os.path.relpath(root, input_dir)
                outfile_dir = os.path.join(output_dir, rel_path)
                os.makedirs(outfile_dir, exist_ok=True)

                outfile = os.path.join(outfile_dir, os.path.splitext(fname)[0] + ".jpg")

                if os.path.exists(outfile) and not force_overwrite:
                    print(f"Skip existing resized file: {outfile}")
                    continue

                try:
                    with Image.open(infile) as img:
                        if img.mode != "RGB":
                            img = img.convert("RGB")
                        img = img.resize((width, height), Image.LANCZOS)
                        img.save(outfile, "JPEG")
                        print(f"Resized: {infile} -> {outfile}")
                except Exception as e:
                    os.makedirs("results", exist_ok=True)
                    with open("results/resize_errors.txt", "a") as f:
                        f.write(f"Error resizing {infile}: {e}\n")
                    print(f"Error resizing {infile}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Resize images to a fixed size")
    parser.add_argument(
        "--input", required=True, help="入力ディレクトリ (例: public_raw)"
    )
    parser.add_argument(
        "--output", required=True, help="出力ディレクトリ (例: public_resized)"
    )
    parser.add_argument("--width", type=int, default=640, help="出力画像の幅")
    parser.add_argument("--height", type=int, default=480, help="出力画像の高さ")
    parser.add_argument(
        "--force-overwrite", action="store_true", help="既存ファイルを上書きする"
    )
    args = parser.parse_args()

    resize_images(
        args.input, args.output, args.width, args.height, args.force_overwrite
    )


if __name__ == "__main__":
    main()
