"""Faces for the examples that train and fit models.

The site's code cells import this module (``from menpo_docs_data import ...``) so that the data
handling is written once.

**Test faces** are always the last ``N_TEST`` of the small set of FairFace images that is committed in
``docs/_data/faces`` (annotated with the 68 points of the iBUG layout by hand; CC BY 4.0, see its
ATTRIBUTION.txt). They are never part of a training set.

**Training faces** are one of two sets:

1. The rest of that small set. Enough to check that the code of every example runs (what CI does), not to
   train a model that fits well.
2. ``$MENPO_DOCS_300W``: the folder of the 300-W download (``afw``, ``helen``, ``lfpw``, ...). The 3148
   images of its training set (``afw``, ``helen/trainset``, ``lfpw/trainset``) are what the figures and numbers
   of the pages are made from (``docs/_tools/render_examples.py``). Its licence is for non-commercial research:
   the data and the models trained on it are not part of this repository; get it from
   https://ibug.doc.ic.ac.uk/resources/300-W/.

menpo's built-in faces (Lenna, Einstein, Takeo, Breaking Bad) have landmarks too, and are used where any face
will do (``builtin_faces``): most of them look away from the camera, which a model trained to fit frontal faces
cannot be asked to follow.
"""

import os
from pathlib import Path

import menpo.io as mio
from menpo.base import LazyList

HERE = Path(__file__).resolve().parent
SMOKE_DIRECTORY = HERE.parent / "_data" / "faces"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
# the folders of the 300-W download that make its training set (3148 images)
TRAINING_FOLDERS_300W = ("afw", "helen/trainset", "lfpw/trainset")
# built-in faces with 68 landmarks, in the order the examples use them
BUILTIN_FACES = ("lenna.png", "einstein.jpg", "takeo.ppm", "breakingbad.jpg")
# how many of the small set are kept for testing
N_TEST = 6


def _cache_dir():
    return Path(os.environ.get("MENPO_DOCS_CACHE", Path.home() / ".cache" / "menpo-docs"))


def root_300w():
    """The folder of the 300-W download, or ``None`` if ``$MENPO_DOCS_300W`` is not set."""
    env = os.environ.get("MENPO_DOCS_300W")
    return Path(env).expanduser() if env else None


def using_300w():
    return root_300w() is not None


def _smoke_paths():
    return sorted(p for p in SMOKE_DIRECTORY.glob("*") if p.suffix.lower() in IMAGE_SUFFIXES and p.with_suffix(".pts").exists())


def _link(source, folder, prefix=""):
    link = folder / f"{prefix}{source.name}"
    if not link.exists():
        link.symlink_to(source)


def faces_directory():
    """A directory of annotated training faces (images with ``.pts`` files), as links: the training set of
    300-W if ``$MENPO_DOCS_300W`` is set, otherwise the small set of this repository without its test faces."""
    root = root_300w()
    out = _cache_dir() / ("train300w" if root else "train_small")
    out.mkdir(parents=True, exist_ok=True)
    if root is None:
        for image in _smoke_paths()[:-N_TEST]:
            _link(image, out)
            _link(image.with_suffix(".pts"), out)
        return out
    for folder in TRAINING_FOLDERS_300W:
        source = root / "images" / folder if (root / "images").is_dir() else root / folder
        if not source.is_dir():
            raise RuntimeError(f"{source} is not a folder: $MENPO_DOCS_300W is the folder of the 300-W download")
        for image in sorted(source.iterdir()):
            if image.suffix.lower() in IMAGE_SUFFIXES and image.with_suffix(".pts").exists():
                for path in (image, image.with_suffix(".pts")):
                    _link(path, out, f"{folder.replace('/', '_')}_")
    return out


def _annotated_paths():
    paths = sorted(p for p in faces_directory().rglob("*") if p.suffix.lower() in IMAGE_SUFFIXES)
    return [p for p in paths if p.with_suffix(".pts").exists()]


def _prepare(image):
    image = image.crop_to_landmarks_proportion(0.3, group="PTS")
    # as the examples do: nothing needs more than a diagonal of 400 pixels, and the 300-W images are large
    if image.diagonal() > 400:
        image = image.rescale(400.0 / image.diagonal())
    return image.as_greyscale() if image.n_channels == 3 else image


def _load(path):
    return _prepare(mio.import_image(path))


def _builtin(name):
    image = mio.import_builtin_asset(name)
    # the 68 point group is called 'PTS' in all the examples (Lenna's is 'LJSON')
    for label in list(image.landmarks.group_labels):
        if image.landmarks[label].n_points == 68 and label != "PTS":
            image.landmarks["PTS"] = image.landmarks[label]
    return _prepare(image)


def builtin_faces(n=4):
    """menpo's built-in faces with their 68 landmarks as ``'PTS'``: greyscale, cropped around the landmarks."""
    return [_builtin(name) for name in BUILTIN_FACES[:n]]


def test_faces(n=N_TEST):
    """The faces to fit: the last ``n`` of the small committed set, greyscale and cropped around their
    landmarks (``'PTS'``), never in a training set."""
    return [_load(p) for p in _smoke_paths()[-n:]]


def faces(n_train=None, n_test=N_TEST):
    """``(training_images, test_images)``: greyscale, cropped around the landmarks, with a 68 point
    landmark group called ``'PTS'``. The same images on every call. The training images are those of
    `faces_directory()` (``n_train`` of them, or all); the test images are `test_faces`, never in the
    training set."""
    paths = _annotated_paths()
    if n_train is not None:
        paths = paths[:n_train]
    if not paths:
        raise RuntimeError(f"no annotated faces in {faces_directory()}")
    # loaded one at a time, when a model asks for it: the 3148 images of 300-W do not fit in memory at once
    return LazyList.init_from_iterable(paths, f=_load), test_faces(n_test)


def lfpw_like_directory(n_train=None, n_test=N_TEST):
    """A directory laid out like the LFPW download (``trainset/`` and ``testset/``): links to the training
    faces and to the test faces. The notebooks were written for LFPW: with your own copy, point
    ``path_to_lfpw`` at it instead."""
    root = _cache_dir() / ("lfpw_like_300w" if using_300w() else "lfpw_like")
    train, test = root / "trainset", root / "testset"
    train.mkdir(parents=True, exist_ok=True)
    test.mkdir(parents=True, exist_ok=True)
    paths = _annotated_paths()
    for image in paths[:n_train] if n_train is not None else paths:
        _link(image, train)
        _link(image.with_suffix(".pts"), train)
    for image in _smoke_paths()[-n_test:]:
        _link(image, test)
        _link(image.with_suffix(".pts"), test)
    return root
