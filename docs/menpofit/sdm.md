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

```{code-cell} ipython3
:tags: [remove-output, record-model]
from menpofit.sdm import RegularizedSDM

fitter = RegularizedSDM(training_images, group='PTS', alpha=100.0, diagonal=100, scales=(0.5, 1.0),
                        patch_shape=(9, 9), n_iterations=3, n_perturbations=8)
print(fitter)
```

```{recorded-output} model
```

Training perturbs the bounding box of the ground truth shape `n_perturbations` times per image, unless you give `bounding_box_group_glob`.
Fit from a bounding box (for example from [menpodetect](../menpodetect/index.md)) or from an initial shape. The number of cascade levels is
`n_iterations`, so `max_iters` does not apply (like `max_iters` of the other fitters, an `int` is the total, shared out over the scales, so the 3 of this model are 2 levels at the coarse scale and 1 at the fine one; give a list for one number per scale):

```{code-cell} ipython3
:tags: [remove-output, record-fit]
import numpy as np

initial_errors, final_errors = [], []
for image in test_images:
    gt_shape = image.landmarks['PTS']
    result = fitter.fit_from_bb(image, gt_shape.bounding_box(), gt_shape=gt_shape)
    initial_errors.append(result.initial_error())
    final_errors.append(result.final_error())

print("mean initial error: {:.4f}   mean final error: {:.4f}".format(
    np.mean(initial_errors), np.mean(final_errors)))
```

```{recorded-output} fit
```

(Here the box is that of the ground truth, to keep the example self-contained; in practice it comes from a detector, which is looser.)

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
The regression matrices have as many rows as the shape has coordinates and as many columns as the features of all the patches
(landmarks x pixels of a patch x channels), and training holds all the perturbed samples at once. `batch_size` is not available for the supervised descent models, so if you run out of memory use fewer training images, a smaller `n_perturbations`, a smaller `patch_shape`, or fewer scales.
```

### Settings to start from
| Setting | Value here | What it does |
|:--|:--|:--|
| `n_iterations` | `3` (here), `6` (the default of `RegularizedSDM`) | The number of cascade levels, shared out over the scales. |
| `n_perturbations` | `8` (here), `30` (the default) | How many perturbed starts per training image. More gives the regressors more examples, and multiplies the memory. |
| `alpha` | `100` (the default is `0.0001`) | The ridge penalty of `RegularizedSDM`. Raw pixel patches have thousands of features, and with the default penalty the regressors over-fit: on the data of this page the default gave a mean error of 0.294 after fitting from a start of 0.047 (8 perturbations; 0.061 with 20), against 0.031 with `alpha=100`. Choose it on held-out images. |
| `patch_shape` | `(9, 9)` (here), `(17, 17)` (the default) | The patch around each landmark that the features are taken from. |
| `holistic_features` | `no_op` (default) | Raw pixels. Try `fast_dsift` first when you want better features; it multiplies the number of features by 8. |

<a id="1"></a>

## References
[1] X. Xiong, and F. De la Torre. "Supervised descent method and its applications to face alignment", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2013.
