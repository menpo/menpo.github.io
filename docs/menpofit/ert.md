# Ensemble of Regression Trees

1. <a href="#definition">Definition</a>
2. <a href="#usage">Training and fitting</a>
3. <a href="https://menpofit.readthedocs.io/en/latest/api/menpofit/dlib/index.html">API Documentation</a>

---------------------------------------

<a id="definition"></a>

## 1. Definition
The Ensemble of Regression Trees method [<a href="#1">1</a>] is a cascade like the [Supervised Descent Method](sdm.md), but each level is a *gradient boosted ensemble
of regression trees* that compare the intensities of pairs of pixels, indexed relative to the current shape. It is fast (about a millisecond per face)
and the model is small. `menpofit` wraps the implementation of [dlib](http://dlib.net/), which also does the training.

<a id="usage"></a>

## 2. Training and fitting
`DlibERT` needs `dlib`, which is an optional dependency of `menpofit` (`pip install "menpofit[dlib]"`; dlib compiles from source on some platforms, so this
page shows the code without running it):

```python
from menpofit.dlib import DlibERT

fitter = DlibERT(training_images, group='PTS', scales=(1.0,),
                 n_iterations=10, n_perturbations=5)
result = fitter.fit_from_bb(image, bounding_box)
```

`scales` and `n_iterations` define the cascade; every scale is a separate dlib model. As with the other cascades, training perturbs the bounding box of the
ground truth shapes `n_perturbations` times. The result has the same interface as the other fitting results, see [Fitting Result](result.md).

The trained model is pickled with `menpo.io.export_pickle`, like the other models (dlib objects included).

<a id="1"></a>

## References
[1] V. Kazemi, and J. Sullivan. "One millisecond face alignment with an ensemble of regression trees", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014.
