---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Constrained Local Model

1. <a href="#definition">Definition</a>
2. <a href="#training">Training and fitting</a>
3. <a href="#experts">Using your own experts</a>
4. <a href="https://menpofit.readthedocs.io/en/latest/api/menpofit/clm/index.html">API Documentation</a>

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```

<a id="definition"></a>

## 1. Definition
A Constrained Local Model (CLM) combines a [shape model](pdm.md) with a set of *experts*, one per landmark. An expert looks at the patch around
a landmark and returns a *response map*, the likelihood that the landmark is at each pixel of the patch. Fitting alternates between asking the experts where
their landmarks are and finding the shape of the model that best explains those answers.

In `menpofit` the experts are **correlation filters** [<a href="#1">1</a>], trained in the Fourier domain on patches extracted around the
landmarks (with a `context_shape` of image around each patch). The shape is regularised by the PDM with `max_shape_components` components.

Two fitting algorithms are available in `menpofit.clm`:

**RegularisedLandmarkMeanShift** [<a href="#2">2</a>]  
Moves every landmark towards the peak of its response (a mean shift on the response map, weighted by `kernel_covariance`) and then projects
the result onto the shape model, with `rho` weighing the regularisation.

**ActiveShapeModel** [<a href="#3">3</a>]  
Searches along each landmark's patch for the best response and projects the new landmarks onto the shape model.

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
from menpo.feature import fast_dsift
from menpofit.clm import CLM

clm = CLM(training_images, group='PTS', diagonal=100, scales=(0.5, 1.0),
          patch_shape=(15, 15), context_shape=(30, 30), max_shape_components=20,
          holistic_features=fast_dsift, batch_size=100)
print(clm)
```

```{recorded-output} model
```

The correlation filters work on the features of `holistic_features`: dense SIFT descriptors (`fast_dsift`) are much better than raw pixels. The fitter takes the number of shape components to use at each scale (on a trimmed copy of the model, see [Fitting](fitting.md)). Use few: the experts are local and noisy, so the shape model has to do most of the work. The experiment code of [<a href="#4">4</a>] uses `[3, 6]` (3 at the coarse scale, 6 at the fine one); `[3, 12]` gave the same error in our test (0.0322, against 0.0327). in our own test on the page's data, 10 or 20 components with smaller patches left the fit worse than its start, and `ActiveShapeModel` was no better than its start either, so the example uses `RegularisedLandmarkMeanShift`:

```{code-cell} ipython3
:tags: [remove-output, record-fit]
from menpofit.clm import GradientDescentCLMFitter, RegularisedLandmarkMeanShift

import numpy as np


def shifted(shape, seed, proportion=0.04):
    """The ground truth moved by a few percent of the face size, like a detector's box."""
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))


fitter = GradientDescentCLMFitter(clm, gd_algorithm_cls=RegularisedLandmarkMeanShift, n_shape=[3, 12])

initial_errors, final_errors = [], []
for i, image in enumerate(test_images):
    gt_shape = image.landmarks['PTS']
    result = fitter.fit_from_shape(image, shifted(gt_shape, i), max_iters=20, gt_shape=gt_shape)
    initial_errors.append(result.initial_error())
    final_errors.append(result.final_error())

print("mean initial error: {:.4f}   mean final error: {:.4f}".format(
    np.mean(initial_errors), np.mean(final_errors)))
```

```{recorded-output} fit
```

The last result:

```{code-cell} ipython3
:tags: [remove-output, record-view]
result.view(render_initial_shape=True);
```

```{recorded-output} view
```

The experts can be inspected too, in a notebook with `menpowidgets.visualize_clm` or `visualize_expert_ensemble`.

<a id="experts"></a>

## 3. Using your own experts
The experts are an `ExpertEnsemble`. To drive the CLM with the responses of your own classifier (for example a neural network that
predicts a heat map for each landmark), subclass `ConvolutionBasedExpertEnsemble` and implement `predict_response`, which returns the response
maps of the patches around the landmarks of a shape, and a `_train` that does nothing since your classifier is already trained.
The class and the methods it must provide:

```{code-cell} ipython3
from menpofit.clm.expert.ensemble import ConvolutionBasedExpertEnsemble

[name for name in ("n_experts", "search_shape", "predict_response", "predict_probability", "_train")
 if hasattr(ConvolutionBasedExpertEnsemble, name)]
```

This is the least documented part of `menpofit`; if you build something with it and would like it to be a documented example, please open an issue.

### Settings to start from
| Setting | Value here | What it does |
|:--|:--|:--|
| `patch_shape`, `context_shape` | `(15, 15)`, `(30, 30)` | The patch each expert is trained to find the landmark in, and the image around it that the filter is trained on. |
| `holistic_features` | `fast_dsift` | Dense SIFT features, which the experts need (see above). |
| `diagonal`, `scales` | `100`, `(0.5, 1.0)` | The resolution of the model. |
| `n_shape` (fitter) | `[3, 12]` | Components of the shape model used while fitting: use few. |
| `gd_algorithm_cls` | `RegularisedLandmarkMeanShift` | In our test it improved a good start; `ActiveShapeModel` did not. |
| `max_iters` | `20` | With 3 iterations the improvement was smaller (0.0469 to 0.0419 against 0.0322 with 20). |

<a id="1"></a>

## References
[1] D.S. Bolme, J.R. Beveridge, B.A. Draper, and Y.M. Lui. "Visual Object Tracking using Adaptive Correlation Filters", CVPR, 2010.

<a id="2"></a>

[2] J.M. Saragih, S. Lucey, and J.F. Cohn. "Deformable model fitting by regularized landmark mean-shift", International Journal of Computer Vision, vol. 91, no. 2, pp. 200-215, 2011.

<a id="3"></a>

[3] T.F. Cootes, C.J. Taylor, D.H. Cooper, and J. Graham. "Active Shape Models - their training and application", Computer Vision and Image Understanding, vol. 61, no. 1, pp. 38-59, 1995.

<a id="4"></a>

[4] J. Alabort-i-Medina, and S. Zafeiriou. "Unifying holistic and parts-based deformable model fitting", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2015.
