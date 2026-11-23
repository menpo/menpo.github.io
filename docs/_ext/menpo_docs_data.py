"""Small sets of annotated faces for the examples that train and fit models.

The site's code cells import this module (``from menpo_docs_data import ...``) so that the
data handling is written once. Where the images come from is decided in one place:

1. ``$MENPO_DOCS_FACES``: a directory of images with ``.pts`` files next to them
   (searched recursively). Used for local development.
2. ``data.toml``: ``url`` and ``sha256`` of a ``.tar.gz``/``.zip`` of such a directory. It is
   downloaded once, checked against the checksum and cached (``$MENPO_DOCS_CACHE`` or
   ``~/.cache/menpo-docs``). CI caches that directory between runs.
"""

import hashlib
import os
import tarfile
import tomllib
import urllib.request
import zipfile
from pathlib import Path

import menpo.io as mio

HERE = Path(__file__).resolve().parent
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}


def _cache_dir():
    return Path(os.environ.get("MENPO_DOCS_CACHE", Path.home() / ".cache" / "menpo-docs"))


def _download(url, sha256, dest):
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / Path(url).name
    if not archive.exists():
        urllib.request.urlretrieve(url, archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != sha256:
        archive.unlink()
        raise RuntimeError(f"{url}: sha256 {digest} does not match data.toml ({sha256})")
    out = dest / "faces"
    if not out.exists():
        if archive.suffix == ".zip":
            zipfile.ZipFile(archive).extractall(out)
        else:
            tarfile.open(archive).extractall(out, filter="data")
    return out


def faces_directory():
    env = os.environ.get("MENPO_DOCS_FACES")
    if env:
        return Path(env)
    config = tomllib.loads((HERE.parent / "data.toml").read_text()).get("faces", {})
    if not config.get("url"):
        raise RuntimeError(
            "No face data for the examples: set MENPO_DOCS_FACES to a directory of images "
            "with .pts files, or fill in docs/data.toml"
        )
    return _download(config["url"], config["sha256"], _cache_dir())


def _load(path):
    image = mio.import_image(path).crop_to_landmarks_proportion(0.3)
    return image.as_greyscale() if image.n_channels == 3 else image


def faces(n_train=40, n_test=4):
    """``(training_images, test_images)``: greyscale, cropped around the landmarks, with a
    68 point landmark group called ``'PTS'``. The same images on every call."""
    paths = sorted(
        p for p in faces_directory().rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES
    )
    paths = [p for p in paths if p.with_suffix(".pts").exists()]
    if len(paths) < n_train + n_test:
        raise RuntimeError(f"need {n_train + n_test} annotated images, found {len(paths)}")
    images = [_load(p) for p in paths[: n_train + n_test]]
    return images[:n_train], images[n_train:]
