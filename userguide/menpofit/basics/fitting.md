Fitting
=======

1. [Fitter objects](#fitter)
2. [Fitting Methods](#fit)

---------------------------------------

### <a name="fitter"></a>1. Fitter Objects
`menpofit` has specialised classes for performing a fitting process that are called `Fitters`.
All `Fitter` objects are subclasses of one of the following:
  * `MultiScaleNonParametricFitter`: multi-scale non-parametric fitting method, i.e. a method that does not optimise over a parametric shape model
    but directly optimizes the coordinates of the landmarks
  * `MultiScaleParametricFitter`: multi-scale parametric fitting method, i.e. a method that optimises over the parameters of a statistical shape model

from `menpofit.fitter`.

The behaviour of `Fitter` classes can differ depending on the deformable model.
For example, a Lucas-Kanade AAM fitter (`LucasKanadeAAMFitter`) assumes that you have trained an AAM model
(assume the `aam` we trained in the [Training](training.md) section) and can be created as:

```python
from menpofit.aam import LucasKanadeAAMFitter, WibergInverseCompositional

fitter = LucasKanadeAAMFitter(aam,
                              lk_algorithm_cls=WibergInverseCompositional,
                              n_shape=[5, 10, 15], n_appearance=150)
```

The constructor of the `Fitter` will set the active shape and appearance components based on `n_shape` and `n_appearance` respectively,
and will also perform all the necessary pre-computations based on the selected algorithm.

However, there are deformable models that are directly defined through a `Fitter` object,
which is responsible for training the model. `SupervisedDescentFitter` is a good example.
The reason for that is that the fitting process is utilised during the building procedure,
thus the functionality of a `Fitter` is required. Such models can be trained as:

```python
from menpofit.sdm import SupervisedDescentFitter, NonParametricNewton

fitter = SupervisedDescentFitter(training_images,
                                 sd_algorithm_cls=NonParametricNewton,
                                 verbose=True)
```

Information about any `Fitter` object can be retrieved as:

```python
print(fitter)
```


### <a name="fit"></a>2. Fitting Methods
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
