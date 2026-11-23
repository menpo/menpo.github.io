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

training_images, test_images = faces(n_train=40, n_test=4)
```

```{code-cell} ipython3
from menpofit.sdm import SupervisedDescentFitter, NonParametricNewton

fitter = SupervisedDescentFitter(training_images, group='PTS',
                                 sd_algorithm_cls=NonParametricNewton,
                                 diagonal=100, scales=(0.5, 1.0),
                                 patch_shape=(9, 9), n_iterations=3,
                                 n_perturbations=5, verbose=True)
print(fitter)
```

Training perturbs the bounding box of the ground truth shape `n_perturbations` times per image, unless you give `bounding_box_group_glob`.
Fit from a bounding box (for example from [menpodetect](../menpodetect/index.md)) or from an initial shape:

```{code-cell} ipython3
import numpy as np


def shifted(shape, seed, proportion=0.04):
    """The ground truth moved by a few percent of the face size, like a detector's box."""
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))

image = test_images[0]
gt_shape = image.landmarks['PTS']
result = fitter.fit_from_shape(image, shifted(gt_shape, 0), gt_shape=gt_shape)
print("initial error: {:.4f}   final error: {:.4f}".format(result.initial_error(), result.final_error()))
```

The number of cascade levels is `n_iterations`, so `max_iters` does not apply. `SDM` is the same cascade with the usual choices already made:

```{code-cell} ipython3
from menpofit.sdm import SDM

sdm = SDM(training_images[:20], group='PTS', diagonal=100, scales=(0.5, 1.0),
          patch_shape=(9, 9), n_iterations=2, n_perturbations=3)
sdm.fit_from_shape(image, shifted(gt_shape, 0), gt_shape=gt_shape).final_error()
```

```{admonition} Memory
:class: warning
The regression matrices have as many rows as the shape has coordinates and as many columns as the features of all the patches
(landmarks x pixels of a patch x channels), and training holds all the perturbed samples at once. Use the `batch_size` argument to train in batches
(incremental training), and a smaller `patch_shape` or fewer scales if you run out of memory.
```

<a id="1"></a>

## References
[1] X. Xiong, and F. De la Torre. "Supervised descent method and its applications to face alignment", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2013.
