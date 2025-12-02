#!/usr/bin/env python3
"""
dl_openimages.py
FiftyOne を利用して Open Images Dataset V7 から指定クラスの画像をダウンロードするスクリプト
"""

import argparse
import os
import fiftyone.zoo as foz
import fiftyone.types as fot


def download_images(
    class_name: str, limit: int, split: str, outdir: str = "public_raw"
):
    # 出力先は split サブディレクトリを作らず、クラス直下に統一
    target_dir = os.path.join(outdir, class_name.replace(" ", "_"))
    os.makedirs(target_dir, exist_ok=True)

    print(
        f"Downloading {limit} images for class '{class_name}' (split={split}) into {target_dir}"
    )

    dataset = foz.load_zoo_dataset(
        "open-images-v7",
        split=split,
        label_types=["classifications"],
        classes=[class_name],
        max_samples=limit,
        only_matching=True,
        dataset_name=None,  # キャッシュを無効化
    )

    dataset.export(
        export_dir=target_dir, dataset_type=fot.ImageDirectory, overwrite=False
    )


def main():
    parser = argparse.ArgumentParser(
        description="Download images from Open Images Dataset V7 using FiftyOne"
    )
    parser.add_argument(
        "--class",
        dest="class_name",
        required=True,
        help="ダウンロード対象のクラス名 (例: Bear, Dog, Person)",
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="ダウンロード枚数上限 (default=100)"
    )
    parser.add_argument(
        "--split",
        type=str,
        default="validation",
        choices=["train", "validation", "test"],
        help="使用するデータセットsplit (train/validation/test)",
    )
    args = parser.parse_args()

    download_images(args.class_name, args.limit, args.split)


if __name__ == "__main__":
    main()
