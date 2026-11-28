---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Visualizing Objects
In the Menpo Project, we take an opinionated stance that visualization is a key part of generating research.
Therefore, we tried to make the mental overhead of visualizing objects as low as possible.

We also took a strong step towards simple visualization by integrating some of our objects with visualization widgets for the Jupyter notebook.
Remember that our widgets live on their own repository, called [**menpowidgets**](../menpowidgets/index.md).

1. <a href="#models">Visualizing Models</a>
2. <a href="#result">Visualizing Fitting Result</a>

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```


<a id="models"></a>

## 1. Visualizing Models
All `menpofit` models provide functionalities for visualizing themselves. For example,
the AAM that we trained in the [Training](training.md) section can be visualized with an interactive widget as:

```python
from menpowidgets import visualize_aam
visualize_aam(aam)
```

We can visualize only the multi-scale shape model as:

```python
from menpowidgets import visualize_shape_model_2d
visualize_shape_model_2d([sm.model for sm in aam.shape_models])
```

or the appearance models as:

```python
from menpowidgets import visualize_appearance_model
visualize_appearance_model(aam.appearance_models)
```

The same visualization widgets can be found in other models, such as ATM, CLM etc.


```{code-cell} ipython3
:tags: [remove-input]

# an AAM and a fitting result to visualize
from menpo.feature import fast_dsift
from menpofit.aam import HolisticAAM, LucasKanadeAAMFitter
from menpo_docs_data import faces

training_images, test_images = faces()
aam = HolisticAAM(training_images, diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift, batch_size=100)
fitter = LucasKanadeAAMFitter(aam, n_shape=[3, 12], n_appearance=[20, 30])
image = test_images[0]
gt_shape = image.landmarks['PTS']
import numpy as np
initial_shape = gt_shape.from_vector(gt_shape.as_vector() + 0.04 * np.ptp(gt_shape.points, axis=0).max())
result = fitter.fit_from_shape(image, initial_shape, max_iters=[15, 15], gt_shape=gt_shape)
```

<a id="result"></a>

## 2. Visualizing Fitting Result
The fitting result objects shown returned by the fitting methods in the [Fitting](fitting.md) section can be easily visualized.
Specifically, the initial and final shapes can be rendered as:

```{code-cell} ipython3
:tags: [remove-output, record-view]
result.view(render_initial_shape=True);
```

```{recorded-output} view
```
Similarly, the shapes acquired at each iteration can be visualized as:

```{code-cell} ipython3
:tags: [remove-output, record-iterations]
result.view_iterations();
```

```{recorded-output} iterations
```
and the corresponding errors as:

```{code-cell} ipython3
:tags: [remove-output, record-errors]
result.plot_errors();
```

```{recorded-output} errors
```
Finally, a fitting result can also be analysed through an interactive widget as:

```python
from menpowidgets import visualize_fitting_results
visualize_fitting_results(result)
```
