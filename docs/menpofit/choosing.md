---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Which model should I use?

`menpofit` has many methods, and you will mostly choose between four families. This page says what each is good at, then trains one of each on the same data and fits the same faces, so the numbers are comparable.

## 1. The short version

| If you ... | use | because |
|:--|:--|:--|
| want the most accurate fit, and have a few hundred annotated images | an [SDM](sdm.md) (`RegularizedSDM`) | in the test below it had the lowest error from both starts (0.019 from a close start, 0.029 from the box of a detector) and a fit takes 0.03 s, about twenty times less than the AAM. It needs its features and the training starts chosen for the task, which the [SDM page](sdm.md) explains |
| want a model of the appearance of the face, or a good fit from a detector's box with a model that can synthesise faces | an [AAM](aam.md) (`HolisticAAM` with Lucas-Kanade) | it reduced the error of the detector's box about fourfold (0.19 to 0.043), and its appearance model generates faces |
| want a fit from a detector's box that is close to the AAM and faster | a [CLM](clm.md) | 0.19 to 0.037 in 0.09 s |
| need a millisecond fit and can install `dlib` | [ERT](ert.md) (`DlibERT`) | a fast cascade of regression trees (not tested here, dlib is optional) |
| already have a good initial shape (tracking: the previous frame) | an [SDM](sdm.md), an [AAM](aam.md) or a [CLM](clm.md); an [ATM](atm.md) when you have a template of the object | they all improved the shifted start (0.047) to 0.02 to 0.03 in the test; ATM needs a template that looks like the target |
| want a prior over the relations between landmarks | [APS](aps.md) | it models them with a graph; in this test it refined a good start a little and did not recover from a loose box |
| are not working with faces | any of them | the models do not depend on the object; give them your landmarks |

Two things matter more than the choice of model. First, **the initialisation**: an AAM started from the ground truth shifted by 4% of the face and one started from a detector's box are different problems (see [Fitting](fitting.md)). Second, **the training data**: a model fits well the kind of faces it has been trained on.

## 2. Training and fitting one of each
The code below trains a model of each family on the training images, with settings taken from the papers that introduced them (the other pages of this guide explain each choice), and fits the test faces from two
initialisations: the ground truth moved by 4% of the face size, and the box of the OpenCV face detector. It records the time that training and fitting take.
The numbers shown are from the LFPW training set (811 images) on a desktop CPU; the cell runs in the build of the site on a few images, which only shows that it works.

```{code-cell} ipython3
:tags: [remove-input]

from menpo_docs_data import faces

training_images, test_images = faces()
```

```{code-cell} ipython3
:tags: [remove-output, record-compare]
import time
import numpy as np
from menpo.feature import fast_dsift
from menpo.shape import UndirectedGraph
from functools import partial
from menpo.feature import hellinger_vector_128_dsift
from menpo.shape import bounding_box
from menpodetect import load_opencv_frontal_face_detector
from menpofit.fitter import noisy_shape_from_bounding_box
from menpofit.aam import HolisticAAM, LucasKanadeAAMFitter, WibergInverseCompositional
from menpofit.aps import GenerativeAPS, GaussNewtonAPSFitter
from menpofit.clm import CLM, GradientDescentCLMFitter, RegularisedLandmarkMeanShift
from menpofit.sdm import RegularizedSDM


def perturbed_square_box(gt_box, example_box):
    """The example box made square, with noise of 20% on its scale and 10% on its translation."""
    lower, _ = example_box.bounds()
    edge = np.max(example_box.range())
    square = bounding_box(lower, lower + np.array((edge, edge)))
    return noisy_shape_from_bounding_box(gt_box, square, noise_percentage=[0.2, 0, 0.1])


def shifted(shape, seed, proportion=0.04):
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))


def chain(indices):
    return list(zip(indices[:-1], indices[1:]))


detect = load_opencv_frontal_face_detector()
boxes = [detect(image.copy()) for image in test_images]
detected = [(image, found[0]) for image, found in zip(test_images, boxes) if found]


def train(name, build):
    start = time.time()
    model = build()
    print("{:5s} trained in {:4.0f} s".format(name, time.time() - start))
    return model


def evaluate(name, fit_from_shape, fit_from_bb, **options):
    row = {}
    start = time.time()
    results = [fit_from_shape(image, shifted(image.landmarks['PTS'], i), gt_shape=image.landmarks['PTS'])
               for i, image in enumerate(test_images)]
    row['shifted'] = np.mean([r.final_error() for r in results])
    row['initial'] = np.mean([r.initial_error() for r in results])
    row['seconds'] = (time.time() - start) / len(test_images)
    results = [fit_from_bb(image, box, gt_shape=image.landmarks['PTS']) for image, box in detected]
    row['detector'] = np.mean([r.final_error() for r in results]) if results else float('nan')
    row['detector_initial'] = np.mean([r.initial_error() for r in results]) if results else float('nan')
    return name, row


rows = []

aam = train('AAM', lambda: HolisticAAM(training_images, group='PTS', diagonal=150, scales=(0.5, 1.0),
                                       holistic_features=fast_dsift, max_shape_components=20,
                                       max_appearance_components=150, batch_size=100))
fitter = LucasKanadeAAMFitter(aam, lk_algorithm_cls=WibergInverseCompositional, n_shape=[3, 12], n_appearance=[25, 50])
rows.append(evaluate('AAM', lambda i, s, **k: fitter.fit_from_shape(i, s, max_iters=[15, 15], **k),
                     lambda i, b, **k: fitter.fit_from_bb(i, b, max_iters=[15, 5], **k)))
del aam, fitter

sdm = train('SDM', lambda: RegularizedSDM(training_images, group='PTS', alpha=200.0,
                                          patch_features=partial(hellinger_vector_128_dsift, dtype=np.float32),
                                          patch_shape=[(32, 32), (24, 24), (24, 24), (16, 16)],
                                          diagonal=200, scales=(0.5, 0.5, 1.0, 1.0),
                                          n_iterations=4, n_perturbations=20,
                                          perturb_from_gt_bounding_box=perturbed_square_box))
rows.append(evaluate('SDM', sdm.fit_from_shape, sdm.fit_from_bb))
del sdm

clm = train('CLM', lambda: CLM(training_images, group='PTS', diagonal=100, scales=(0.5, 1.0), patch_shape=(15, 15),
                               context_shape=(30, 30), max_shape_components=20, holistic_features=fast_dsift,
                               batch_size=100))
fitter = GradientDescentCLMFitter(clm, gd_algorithm_cls=RegularisedLandmarkMeanShift, n_shape=[3, 12])
rows.append(evaluate('CLM', lambda i, s, **k: fitter.fit_from_shape(i, s, max_iters=20, **k),
                     lambda i, b, **k: fitter.fit_from_bb(i, b, max_iters=20, **k)))
del clm, fitter

edges = (chain(list(range(17))) + chain(list(range(17, 22))) + chain(list(range(22, 27)))
         + chain(list(range(27, 34))) + chain([33, 32, 31, 30]) + chain(list(range(33, 36)))
         + chain(list(range(36, 42)) + [36]) + chain(list(range(42, 48)) + [42])
         + chain(list(range(48, 60)) + [48]) + chain(list(range(60, 68)) + [60]))
aps = train('APS', lambda: GenerativeAPS(training_images, group='PTS',
                                         appearance_graph=UndirectedGraph.init_from_edges(np.array(edges), 68),
                                         diagonal=100, scales=(0.5, 1.0), patch_shape=(17, 17),
                                         max_shape_components=25, n_appearance_components=150))
fitter = GaussNewtonAPSFitter(aps, n_shape=[3, 12], weight=200.)
rows.append(evaluate('APS', lambda i, s, **k: fitter.fit_from_shape(i, s, max_iters=30, **k),
                     lambda i, b, **k: fitter.fit_from_bb(i, b, max_iters=30, **k)))

print()
print("faces: {} from a shifted ground truth, {} from the detector's box".format(len(test_images), len(detected)))
print("{:5s} {:>9s} {:>9s} {:>9s} {:>9s} {:>10s}".format('model', 'shifted', '->', 'detector', '->', 'sec/face'))
for name, row in rows:
    print("{:5s} {:9.4f} {:9.4f} {:9.4f} {:9.4f} {:10.2f}".format(
        name, row['initial'], row['shifted'], row['detector_initial'], row['detector'], row['seconds']))
```

```{recorded-output} compare
```

The columns are, in order: the mean error of the shifted start, and after fitting from it (`shifted` and the `->` after it); the mean error of the detector's box, and after fitting from it (`detector` and the next `->`); and the time that a fit takes on one CPU (the lower the errors the better; see [Fitting Result](result.md) for how the error is measured).
With so few test faces the differences between models of similar error are not significant: read it as an order of magnitude and as a check that nothing is broken, not as a ranking. The
[ERT](ert.md) of dlib is left out because it is an optional dependency; install it and add a `DlibERT` row in the same way.
