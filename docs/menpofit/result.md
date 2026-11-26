---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Fitting Result

1. <a href="#objects">Result objects</a>
2. <a href="#attributes">Attributes</a>

---------------------------------------

<a id="objects"></a>

## 1. Result Objects
The fitting methods of the `Fitters` presented in the [previous section](fitting.md) return a result object. `menpofit` has three basic fitting result objects:
  - `Result`: Basic fitting result object that holds the final shape, and optionally, the initial shape, ground truth shape and the image.
  - `MultiScaleNonParametricIterativeResult`: The result of a multi-scale iterative fitting procedure. Apart from the final shape, it also stores the shapes acquired at each fitting iteration.
  - `MultiScaleParametricIterativeResult`: The same as `MultiScaleNonParametricIterativeResult` with the difference that the optimization was performed over the parameters of a statistical parametric shape model. Thus, apart from the actual shapes, it also stores the shape parameters acquired per iteration. *Note that in this case, the initial shape that was provided by the user gets reconstructed using the shape model, i.e. it first gets projected in order to get the initial estimation of the shape parameters, and then gets reconstructed with those*. The resulting shape is then used as initialization for the iterative fitting process.


<a id="attributes"></a>

## 2. Attributes
The above result objects can provide some very useful information regarding the fitting procedure. For example, the various shapes can be retrieved as:

**result.final\_shape**  
The final shape of the fitting procedure.

**result.initial\_shape**  
The initial shape of the fitting procedure that was provided by the user.

**result.reconstructed\_initial\_shape**  
The reconstruction of the initial shape that was used to initialise the fitting procedure. It only applies for `MultiScaleParametricIterativeResult`.

**result.image**  
The image on which the fitting procedure was applied.

**result.gt\_shape**  
The ground truth shape associated to the image.

**result.shapes**  
The `list` of shapes acquired at each fitting iteration. It only applies on `MultiScaleNonParametricIterativeResult` and `MultiScaleParametricIterativeResult`.

**result.costs()**  
The cost values per iteration, if they were computed during fitting.

Also, a result can compute some error metrics, in case the `gt_shape` of the image exists:

**result.final\_error()**  
The final fitting error.

**result.initial\_error()**  
The initial fitting error.

**result.errors()**  
The `list` of errors acquired at each fitting iteration. It only applies on `MultiScaleNonParametricIterativeResult` and `MultiScaleParametricIterativeResult`.

For example, with the `result` of the [Fitting](fitting.md) section:

```{code-cell} ipython3
:tags: [remove-input]

from menpo.feature import fast_dsift
from menpofit.aam import HolisticAAM, LucasKanadeAAMFitter, WibergInverseCompositional
from menpo_docs_data import faces
import numpy as np

training_images, test_images = faces()
aam = HolisticAAM(training_images, diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift,
                  batch_size=100)
fitter = LucasKanadeAAMFitter(aam, lk_algorithm_cls=WibergInverseCompositional, n_shape=[3, 20], n_appearance=[30, 150])
image = test_images[0]
gt_shape = image.landmarks["PTS"]
offset = np.random.RandomState(0).randn(2) * 0.04 * np.ptp(gt_shape.points, axis=0).max()
initial_shape = gt_shape.from_vector(gt_shape.as_vector() + np.tile(offset, gt_shape.n_points))
result = fitter.fit_from_shape(image, initial_shape, max_iters=[15, 15], gt_shape=gt_shape)
```

```{code-cell} ipython3
print(type(result).__name__)
print("shapes per iteration:", len(result.shapes))
print("errors per iteration:", np.round(result.errors(), 4))
result.view();
```
