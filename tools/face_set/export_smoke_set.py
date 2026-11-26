"""Copy the annotated faces into the repository as the small set that the documentation's CI runs on.

    python export_smoke_set.py FOLDER OUT_DIR

FOLDER is what `lmio image FOLDER` annotated: images with a `.ljson` next to them. Only the images that were
saved through landmarker.io (`"reviewed": true`) with all 68 landmarks placed are copied, as the image and a `.pts`
file (counting pixels from 1, as menpo reads them), which is the format of the 300-W data that the examples
are written for. The attribution of the images (FairFace, CC BY 4.0) is copied as well, for those images only.
"""
import argparse
import json
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    copied = []
    for ljson in sorted(args.folder.glob("*.ljson")):
        data = json.loads(ljson.read_text())
        points = data["landmarks"]["points"]
        if not data.get("reviewed") or len(points) != 68 or any(v is None for p in points for v in p):
            print(f"skipping {ljson.name}: not reviewed, or not complete")
            continue
        image = next((ljson.with_suffix(s) for s in (".png", ".jpg", ".jpeg") if ljson.with_suffix(s).exists()), None)
        if image is None:
            continue
        shutil.copy(image, args.out / image.name)
        # LJSON is (row, column); a .pts file is (x, y) = (column, row), counted from 1
        lines = "\n".join(f"{c + 1:.3f} {r + 1:.3f}" for r, c in points)
        (args.out / f"{image.stem}.pts").write_text(f"version: 1\nn_points: 68\n{{\n{lines}\n}}\n")
        copied.append(image.stem)
    source = args.folder / "ATTRIBUTION.txt"
    header = [
        "Images: FairFace, K. Karkkainen and J. Joo, CC BY 4.0, https://huggingface.co/datasets/HuggingFaceM4/FairFace",
        "Landmarks: placed with landmarker.io, starting from MediaPipe Face Landmarker (Apache-2.0), corrected by hand.",
        "",
    ]
    lines = source.read_text().splitlines() if source.exists() else []
    own = [line for line in lines if line.split(":")[0] in copied]
    (args.out / "ATTRIBUTION.txt").write_text("\n".join(header + own) + "\n")
    print(f"{len(copied)} images in {args.out}")


if __name__ == "__main__":
    main()
