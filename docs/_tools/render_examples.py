"""Make the figures and numbers that the pages show from models trained on the 300-W training set.

    MENPO_DOCS_300W=/path/to/300w python docs/_tools/render_examples.py [PAGE ...]
    python docs/_tools/render_examples.py --smoke [PAGE ...]      # the small set, to test this script

The pages that train a model run their code in CI on a small set of faces, which only shows that the code
runs. What they *show* (the figures, the errors) comes from here: for each page this runs the code cells of
the page on the 300-W training set (3148 images, `_ext/menpo_docs_data.py`; not part of this repository, its
licence is for non-commercial research) and fits menpo's built-in faces (never in the training set), then
writes pictures to `docs/_static/examples/` and the numbers to `docs/_static/examples/results.json`, which
`conf.py` makes available to the pages as substitutions (`{{ name }}`).

Run it again, and commit what it writes, when a release changes what the models do.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

DOCS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DOCS / "_ext"))
import menpo_docs_data as data  # noqa: E402

START = "#ff3b30"
FINAL = "#34c759"
TRUTH = "#00e5ff"


# ---- running the code of a page
def run_cells(page):
    """Run the code cells of a page in one namespace, as the build does, and return it."""
    text = (DOCS / "menpofit" / f"{page}.md").read_text()
    namespace = {"__name__": "__main__"}
    for cell in re.findall(r"```\{code-cell\} ipython3\n(.*?)```", text, re.S):
        lines = [line for line in cell.splitlines() if not line.startswith(":")]
        lines = [line for line in lines if not line.lstrip().startswith(("%", "!"))]
        exec(compile("\n".join(lines), f"{page}.md", "exec"), namespace)
    return namespace


# ---- drawing
def draw(axis, image, shapes, title):
    axis.imshow(image.pixels[0], cmap="gray")
    for shape, colour in shapes:
        axis.scatter(shape.points[:, 1], shape.points[:, 0], s=5, c=colour, linewidths=0)
    axis.set_title(title, fontsize=8)
    axis.axis("off")


def fit_figure(path, images, results):
    """One row per image: where the fit starts (red) and where it ends (green), with the truth (cyan)."""
    fig, axes = plt.subplots(len(images), 2, figsize=(5.2, 2.7 * len(images)))
    for row, (image, result) in zip(axes, zip(images, results)):
        truth = image.landmarks["PTS"]
        draw(row[0], image, [(truth, TRUTH), (result.initial_shape, START)], f"start: {result.initial_error():.3f}")
        draw(row[1], image, [(truth, TRUTH), (result.final_shape, FINAL)], f"fitted: {result.final_error():.3f}")
    fig.tight_layout()
    fig.savefig(path, dpi=100)
    plt.close(fig)


def summarise(results):
    return {
        "initial": float(np.mean([r.initial_error() for r in results])),
        "final": float(np.mean([r.final_error() for r in results])),
    }


def detector_boxes(images):
    from menpodetect import load_opencv_frontal_face_detector

    detect = load_opencv_frontal_face_detector()
    boxes = []
    for image in images:
        found = detect(image.copy())
        boxes.append(found[0] if found else None)
    return boxes


# ---- the pages
def render_fitting(namespace, out):
    """The AAM of the page, fitted from a shifted ground truth (the page's own protocol) and from the box
    of a face detector (what you have in practice)."""
    fitter, images, shifted = namespace["fitter"], namespace["test_images"], namespace["shifted"]
    results = {"n_train": len(namespace["training_images"])}

    shifted_fits = [
        fitter.fit_from_shape(image, shifted(image.landmarks["PTS"], seed=i), max_iters=[15, 15],
                              gt_shape=image.landmarks["PTS"])
        for i, image in enumerate(images)
    ]
    fit_figure(out / "fitting_shifted.png", images, shifted_fits)
    results["shifted"] = summarise(shifted_fits)

    boxes = detector_boxes(images)
    kept = [(image, box) for image, box in zip(images, boxes) if box is not None]
    detector_fits = [
        fitter.fit_from_bb(image, box, max_iters=[15, 5], gt_shape=image.landmarks["PTS"]) for image, box in kept
    ]
    fit_figure(out / "fitting_detector.png", [image for image, _ in kept], detector_fits)
    results["detector"] = summarise(detector_fits)
    results["detector"]["n_faces"] = len(kept)
    return results


PAGES = {"fitting": render_fitting}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", nargs="*", help=f"default: all of {', '.join(PAGES)}")
    parser.add_argument("--smoke", action="store_true", help="the small set of the repository, written to a temporary folder")
    args = parser.parse_args()

    if not args.smoke and not data.using_300w():
        raise SystemExit("set MENPO_DOCS_300W to the folder of the 300-W download (or use --smoke)")
    out = DOCS / "_static" / "examples"
    if args.smoke:
        import tempfile

        out = Path(tempfile.mkdtemp(prefix="menpo-examples-"))
    out.mkdir(parents=True, exist_ok=True)

    results_file = out / "results.json"
    results = json.loads(results_file.read_text()) if results_file.exists() else {}
    for page in args.pages or PAGES:
        start = time.time()
        results[page] = PAGES[page](run_cells(page), out)
        results_file.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
        print(f"{page}: {json.dumps(results[page])}  ({time.time() - start:.0f} s)", flush=True)
    print(f"written to {out}")


if __name__ == "__main__":
    main()
