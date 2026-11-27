---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Fitting

1. <a href="#fitter">Fitter objects</a>
2. <a href="#fit">Fitting Methods</a>

---------------------------------------

<a id="fitter"></a>

## 1. Fitter Objects
`menpofit` has specialised classes for performing a fitting process that are called `Fitters`.
All `Fitter` objects are subclasses of one of the following (in `menpofit.fitter`):
  * `MultiScaleNonParametricFitter`: multi-scale non-parametric fitting method, i.e. a method that does not optimise over a parametric shape model
    but directly optimizes the coordinates of the landmarks
  * `MultiScaleParametricFitter`: multi-scale parametric fitting method, i.e. a method that optimises over the parameters of a statistical shape model

The behaviour of `Fitter` classes can differ depending on the deformable model.
For example, a Lucas-Kanade AAM fitter (`LucasKanadeAAMFitter`) assumes that you have trained an AAM model
(the `aam` we trained in the [Training](training.md) section) and can be created as:

```{code-cell} ipython3
:tags: [remove-input]

# the `aam` of the Training section, and an image to fit
from menpo.feature import fast_dsift
from menpofit.aam import HolisticAAM
from menpo_docs_data import faces

training_images, test_images = faces()
aam = HolisticAAM(training_images, diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift,
                  batch_size=100)
```

```{code-cell} ipython3
from menpofit.aam import LucasKanadeAAMFitter, WibergInverseCompositional

fitter = LucasKanadeAAMFitter(aam,
                              lk_algorithm_cls=WibergInverseCompositional,
                              n_shape=[3, 20], n_appearance=[30, 150])
```

The constructor of the `Fitter` takes the number of shape and appearance components to use at each scale from `n_shape` and
`n_appearance`, and also performs all the necessary pre-computations of the selected algorithm. It works on a *trimmed copy* of the
models: the `aam` you pass in is not modified, so one trained model can serve any number of fitters with different numbers of
components (see [Point Distribution Model](pdm.md) for trimming).

```{code-cell} ipython3
aam.shape_models[0].model.n_components, fitter.aam.shape_models[0].model.n_components
```

However, there are deformable models that are directly defined through a `Fitter` object,
which is responsible for training the model. `SupervisedDescentFitter` is a good example.
The reason for that is that the fitting process is utilised during the building procedure,
thus the functionality of a `Fitter` is required. Such models can be trained as:

```{code-cell} ipython3
from menpofit.sdm import SupervisedDescentFitter, NonParametricNewton

sd_fitter = SupervisedDescentFitter(training_images[:20],
                                    sd_algorithm_cls=NonParametricNewton,
                                    n_iterations=2, n_perturbations=3,
                                    verbose=True)
```

Information about any `Fitter` object can be retrieved as:

```{code-cell} ipython3
print(sd_fitter)
```

<a id="fit"></a>

## 2. Fitting Methods
All the deformable models that are currently implemented in `mnepofit`,
which are the state-of-the-art approaches in current literature,
aim to find a *local optimum* of the cost function that they try to optimise, given an initialization.
The initialization can be seen as an initial estimation of the target shape.
`Fitter` objects provide two functions for fitting a model to an image:

```python
result = fitter.fit_from_shape(image, initial_shape, max_iters=20, gt_shape=None,
                               return_costs=False, **kwargs)
```

or

```python
result = fitter.fit_from_bb(image, bounding_box, max_iters=20, gt_shape=None,
                            return_costs=False, **kwargs)
```

They only differ on the type of initialization. `fit_from_shape` expects a `PointCloud` as the `initial_shape`.
On the other hand, the `bounding_box` argument of `fit_from_bb` is a `PointDirectedGraph` of 4 vertices that
represents the initial bounding box. The bounding box is used in order to align the model's reference shape and
use the resulting `PointCloud` as the initial shape. Such a bounding box can be retrieved using the detection methods
of `menpodetect`. The rest of the options are:

**max\_iters** (`int` or `list` of `int`)  
Defines the maximum number of iterations. If `int`, then it specifies the maximum number of iterations over all scales.
If `list` of `int`, then it specifies the maximum number of iterations per scale.
Note that this does not apply on all deformable models.
For example, it can control the number of iterations of a Lucas-Kanade optimization algorithm,
but it does not affect the fitting of a cascaded-regression method (e.g. SDM) which has a predefined number of cascades (iterations).

**gt\_shape** (`PointCloud` or ``None``)  
The ground truth shape associated to the image. **This is *only* useful to compute the final fitting error.**
It is *not* used, of course, at any internal stage of the optimisation.

**return\_costs** (`bool`)  
If ``True``, then the cost function values will be computed during the fitting procedure.
Then these cost values will be assigned to the returned `fitting_result`.
Note that the costs computation increases the computational cost of the fitting.
The additional computation cost depends on the fitting method.
Thus, this option should only be used for research purposes.
Finally, this argument does not apply to all deformable models.

**kwargs** (`dict`)  
Additional keyword arguments that can be passed to specific models.

Putting it together, fitting the test images from a shifted ground truth (the initial shape is moved by 4% of the face size, as a
detector's box would be off):

```{code-cell} ipython3
:tags: [remove-output]
import numpy as np


def shifted(shape, seed, proportion=0.04):
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))


initial_errors, final_errors = [], []
for i, image in enumerate(test_images):
    gt_shape = image.landmarks["PTS"]
    result = fitter.fit_from_shape(image, shifted(gt_shape, seed=i),
                                   max_iters=[15, 15], gt_shape=gt_shape)
    initial_errors.append(result.initial_error())
    final_errors.append(result.final_error())

print("mean initial error: {:.4f}   mean final error: {:.4f}".format(
    np.mean(initial_errors), np.mean(final_errors)))
```

The error is normalised by the size of the face, so it is comparable between images. What this page *shows* of the result is from
`HolisticAAM`s trained on the **LFPW training set** ({{ fitting_n_train }} images, from the 300-W download; its licence is for non-commercial research, so it is not
part of this site: [download it](https://ibug.doc.ic.ac.uk/resources/300-W/) and point the code at it), fitting {{ fitting_detector_n_faces }}
faces that it has not seen (a hand-annotated set of [FairFace](https://github.com/joojs/fairface) faces, CC BY 4.0). The code of the page runs
every time the site is built, on a much smaller set, which only shows that it works.

From the ground truth moved by 4% of the face size, the mean error goes from {{ fitting_shifted_initial }} to {{ fitting_shifted_final }}.
Red is where the fit starts, green where it ends, and cyan is the ground truth:

```{figure} /_static/examples/fitting_shifted.png
:width: 60%
:alt: six faces, each with the starting shape and the fitted shape of the AAM from a shifted ground truth
```

From the box of a detector (`fit_from_bb` with `menpodetect`'s OpenCV detector, whose boxes are looser than the ground truth),
which is what you have in practice, the start is much worse, and the mean error goes from {{ fitting_detector_initial }} to
{{ fitting_detector_final }}. Most faces converge, and one does not (the fifth): the fitting is local, it finds the minimum near where
it starts, so a start that is too far off, or a face that does not look like the training faces, can end in the wrong place.

```{figure} /_static/examples/fitting_detector.png
:width: 60%
:alt: six faces, each with the starting shape from a detector box and the fitted shape of the AAM
```
