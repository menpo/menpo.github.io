---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Supervised Descent Method

1. <a href="#definition">Definition</a>
2. <a href="#training">Training and fitting</a>
3. <a href="https://menpofit.readthedocs.io/en/latest/api/menpofit/sdm/index.html">API Documentation</a>

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```

<a id="definition"></a>

## 1. Definition
The Supervised Descent Method (SDM) [<a href="#1">1</a>] replaces the iterative optimisation of a cost function by a *cascade of regressors* learned from data.
Given the features $\phi(\mathbf{I}, \mathbf{s}^{(k)})$ extracted at the current shape $\mathbf{s}^{(k)}$ (for example SIFT or HOG patches around the landmarks),
level $k$ of the cascade predicts the update of the shape:
$$
\mathbf{s}^{(k+1)} = \mathbf{s}^{(k)} + \mathbf{R}^{(k)}\phi\big(\mathbf{I}, \mathbf{s}^{(k)}\big) + \mathbf{b}^{(k)}
$$
The regressors are trained one level at a time, on training shapes perturbed around the ground truth: each level learns to undo the errors that the
previous levels left. In `menpofit` the model *is* the fitter, because the fitting process is used during training. `SupervisedDescentFitter`
takes the choice of regression in `sd_algorithm_cls`; `SDM` and `RegularizedSDM` are ready-made choices.

<a id="training"></a>

## 2. Training and fitting
```{code-cell} ipython3
:tags: [remove-input]

# a small set of annotated faces: the training images and some to fit
from menpo_docs_data import faces

training_images, test_images = faces()
```

The recipe below is a cascade of four stages. Each stage is a regression with its own scale and patch size: the first two work at half the resolution, on a large patch (32 x 32 pixels, then 24 x 24), and the last two at the full
resolution, on smaller ones (24 x 24, then 16 x 16), so the cascade looks at the whole face first and at the details when it is close. The features are computed on every patch: `hellinger_vector_128_dsift` is
one SIFT descriptor of 128 values for a whole square patch, normalised with the Hellinger norm [<a href="#2">2</a>]. This is the feature of the paper [<a href="#1">1</a>], and it has 68 x 128 = 8,704 values per sample whatever the size of the patches,
so large patches are affordable. The training starts are the bounding box of the ground truth, made square (the box of a face detector is square) and perturbed in scale and translation (the noise is that of a detector's box: large in scale). `scales` lists one scale per stage, so `n_iterations=4` is one level of regression per stage:

```{code-cell} ipython3
:tags: [remove-output, record-model]
from functools import partial

import numpy as np
from menpo.feature import hellinger_vector_128_dsift
from menpo.shape import bounding_box
from menpofit.fitter import noisy_shape_from_bounding_box
from menpofit.sdm import RegularizedSDM


def perturbed_square_box(gt_box, example_box):
    """The example box made square, with noise of 20% on its scale and 10% on its translation."""
    lower, _ = example_box.bounds()
    edge = np.max(example_box.range())
    square = bounding_box(lower, lower + np.array((edge, edge)))
    return noisy_shape_from_bounding_box(gt_box, square, noise_percentage=[0.2, 0, 0.1])


fitter = RegularizedSDM(training_images, group='PTS', alpha=200.0,
                        patch_features=partial(hellinger_vector_128_dsift, dtype=np.float32),
                        patch_shape=[(32, 32), (24, 24), (24, 24), (16, 16)],
                        diagonal=200, scales=(0.5, 0.5, 1.0, 1.0),
                        n_iterations=4, n_perturbations=20,
                        perturb_from_gt_bounding_box=perturbed_square_box)
print(fitter)
```

```{recorded-output} model
```

Training perturbs the bounding box of the ground truth shape `n_perturbations` times per image, unless you give `bounding_box_group_glob`.
Fit from a bounding box (for example from [menpodetect](../menpodetect/index.md)) or from an initial shape. The number of cascade levels is
`n_iterations`, so `max_iters` does not apply (like `max_iters` of the other fitters, an `int` is the total, shared out over the scales: here one level for each of the four scales). This fits the test faces from the box of a face detector,
and from the ground truth moved by 4% of the face size:

```{code-cell} ipython3
:tags: [remove-output, record-fit]
from menpodetect import load_opencv_frontal_face_detector

detect = load_opencv_frontal_face_detector()


def shifted(shape, seed, proportion=0.04):
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))


shifted_results, box_results = [], []
for i, image in enumerate(test_images):
    gt_shape = image.landmarks['PTS']
    shifted_results.append(fitter.fit_from_shape(image, shifted(gt_shape, i), gt_shape=gt_shape))
    boxes = detect(image.copy())
    if boxes:
        box_results.append(fitter.fit_from_bb(image, boxes[0], gt_shape=gt_shape))

for name, results in (("the shifted ground truth", shifted_results), ("the box of the detector", box_results)):
    print("from {} ({} faces): mean error {:.4f} -> {:.4f}".format(
        name, len(results), np.mean([r.initial_error() for r in results]),
        np.mean([r.final_error() for r in results])))
```

```{recorded-output} fit
```

## 3. Choosing the regression
`RegularizedSDM` penalises large regression weights (`alpha`, 0.0001 by default). This matters when there are few training images: each regressor has one weight per
feature (the pixels of all the patches) and the plain least-squares solution that `SDM` and `SupervisedDescentFitter(sd_algorithm_cls=NonParametricNewton)` use
needs far more perturbed samples than features, or it over-fits and the cascade diverges. With only a few training images (as in the build of this page, which runs on a handful), `SDM` makes the error *larger*
by orders of magnitude; give it hundreds of images and more perturbations, or use the regularised version.

### The families of regressors
`sd_algorithm_cls` is a choice on two axes, which is why `menpofit.sdm` has so many classes.

**What is regressed, and from which features**

| Family | Features | Regressed to | Class names |
|:--|:--|:--|:--|
| Non-parametric | patches around the current landmarks | the update of the landmarks | `NonParametric...` |
| Parametric shape | patches around the current landmarks | the update of the parameters of a shape model (PDM) | `ParametricShape...` |
| Parametric appearance | the appearance of the face in a model of appearance (weights, projected-out or centred, as for the AAM, see its [supervised descent section](aam.md)) | the update of the landmarks | `ParametricAppearance...` |
| Fully parametric | as parametric appearance | the update of the shape parameters | `FullyParametric...` |

The non-parametric family is the one of the original paper and what `SDM` and `RegularizedSDM` use. Regressing shape parameters (`ParametricShape`) constrains every update to plausible
shapes, at the cost of the detail that a shape model with few components cannot express. The appearance families add an appearance model, so the regression works on features relative to a model of what a face looks like instead of on raw patches.

**How the regression is solved**

| Suffix | Regression |
|:--|:--|
| `Newton` | ridge regression (`IRLRegression`, penalty `alpha`): the usual choice |
| `GaussNewton` | the Gauss-Newton form of the same regression (`IIRLRegression`) |
| `PCRRegression` | principal component regression: the features are projected on their principal components before the regression |
| `OptimalRegression` | multivariate regression with optimal reconstruction of the targets |
| `OPPRegression` | multivariate regression with orthogonal Procrustes reconstruction of the targets |

All of them are used in the same way, with the same fitting results. This builds one of each family with a few training perturbations, only to show the names; train yours on far more
(`n_perturbations`) and with real features:

```{code-cell} ipython3
:tags: [remove-output]
from menpofit.sdm import (SupervisedDescentFitter, NonParametricNewton, NonParametricPCRRegression,
                          ParametricShapeNewton, ParametricAppearanceWeightsNewton,
                          FullyParametricWeightsNewton)

variants = [NonParametricNewton, NonParametricPCRRegression, ParametricShapeNewton,
            ParametricAppearanceWeightsNewton, FullyParametricWeightsNewton]
for algorithm in variants:
    SupervisedDescentFitter(training_images, group='PTS', sd_algorithm_cls=algorithm,
                            diagonal=100, scales=(0.5, 1.0), patch_shape=(9, 9),
                            n_iterations=2, n_perturbations=4)
    print(algorithm.__name__, "trained")
```

`SupervisedDescentFitter` is the general class: `sd_algorithm_cls` chooses between the non-parametric regressors (the landmarks are the regression target) and the parametric ones
(the parameters of a shape model are), with Newton, Gauss-Newton, PCR (principal component regression) and optimal regression solvers:

```python
from menpofit.sdm import SupervisedDescentFitter, NonParametricNewton

fitter = SupervisedDescentFitter(training_images, group='PTS',
                                 sd_algorithm_cls=NonParametricNewton,
                                 diagonal=100, scales=(0.5, 1.0),
                                 patch_shape=(9, 9), n_iterations=3,
                                 n_perturbations=8)
```

```{admonition} Memory
:class: warning
The regression of a level has as many rows as the shape has coordinates and as many columns as the features of all the patches, and its matrix of normal equations is (features x features): the model of this page has 8,704 features, which is 0.6 GB for that matrix, and training on the 811 images of LFPW peaked at 4.4 GB. Features grow with the number of patches, the size of a patch and the channels of the features, and the matrix with their square: dense SIFT images (8 channels) with 9 x 9 patches have 44,000 features and a matrix of 15 GB. `batch_size` is not available for the supervised descent models in menpofit {{ menpofit_version }}, so if you run out of memory use fewer training images, a smaller `n_perturbations`, smaller features or fewer scales.
```

### Settings to start from
These are the settings of the example above; the numbers are from our test, on the faces of this page (the errors of 6 faces, see [Which model should I use?](choosing.md)).

| Setting | Value here | What it does |
|:--|:--|:--|
| `patch_features` | `hellinger_vector_128_dsift` | One SIFT descriptor of 128 values per patch, Hellinger normalised: 8,704 features per sample, whatever the patch size. Plain `vector_128_dsift` fitted a close start much less well (0.046 against 0.019 from the ground truth moved by 4% of the face size). A holistic dense SIFT image (`holistic_features=fast_dsift`) with 5 x 5 patches gave 0.052 and 0.055 (from the shifted ground truth and from the detector's box) in our tests, and with 9 x 9 patches 0.100 and 0.079. |
| `scales`, `patch_shape` | `(0.5, 0.5, 1.0, 1.0)`, 32 x 32 to 16 x 16 | One stage per scale: large patches at half the resolution, smaller ones at the full resolution. |
| `n_iterations` | `4` | One level per stage. The total is shared out over the scales. |
| `perturb_from_gt_bounding_box` | square box, noise of 20% on scale and 10% on translation | How the training starts are made. The regressors only learn to correct the errors they were trained on, so the perturbations should look like the starts you will fit from: with noise of 3% on the scale and 5% on the translation the fit from the detector's box ended at 0.098, with 10% and 10% at 0.040 and with 20% and 10% at 0.029; from the ground truth moved by 4% of the face size all three gave 0.018. The box of the detector is square, so the training box is made square. |
| `n_perturbations` | `20` | How many perturbed starts per training image. The regression needs many more samples than features. |
| `alpha` | `200` (the default is `0.0001`) | The ridge penalty of `RegularizedSDM`. Choose it on held-out images; it depends on the features. With raw pixel patches the default over-fits (a mean error of 0.294 from a start of 0.047). |

<a id="1"></a>

## References
[1] X. Xiong, and F. De la Torre. "Supervised descent method and its applications to face alignment", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2013.

<a id="2"></a>

[2] R. Arandjelovic, and A. Zisserman. "Three things everyone should know to improve object retrieval", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2012.
