---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---


<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../_static/logo/menpowidgets.png" alt="menpowidgets" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpowidgets" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpowidgets.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpowidgets">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpowidgets/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

# Main MenpoFit widgets

These are the widgets for visualizing the objects of [`menpofit`](../menpofit/index.md). Install them with `pip install "menpowidgets[menpofit]"`.

| Function | Shows |
|---|---|
| `visualize_aam`, `visualize_patch_aam` | an AAM: its shape and appearance parameters and the instance they generate |
| `visualize_atm`, `visualize_patch_atm` | an ATM |
| `visualize_clm` | a CLM: the shape model and the response of the experts |
| `visualize_expert_ensemble` | the experts of a CLM |
| `visualize_appearance_model`, `visualize_patch_appearance_model` | the appearance model of an AAM |
| `visualize_shape_model_2d` | the shape models of any multi-scale model |
| `visualize_fitting_results` | a list of fitting results, with the iterations, the errors and the ground truth |

```{note}
The widgets on this page were created when the website was built, so what you see is the initial state of each one, drawn by the real code.
The controls do not respond here, because the plots are drawn by Python: run the code in a Jupyter notebook for the interactive version.
```

```{code-cell} ipython3
:tags: [remove-input]

# a small AAM and some fitting results, as in the AAM guide
from menpo.feature import fast_dsift
from menpofit.aam import HolisticAAM, LucasKanadeAAMFitter
from menpo_docs_data import faces

training_images, test_images = faces(n_train=40, n_test=4)
aam = HolisticAAM(training_images, diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift)
fitter = LucasKanadeAAMFitter(aam, n_shape=[3, 12], n_appearance=[20, 30])

import numpy as np
results = []
for i, image in enumerate(test_images):
    gt_shape = image.landmarks['PTS']
    offset = np.random.RandomState(i).randn(2) * 0.04 * np.ptp(gt_shape.points, axis=0).max()
    initial_shape = gt_shape.from_vector(gt_shape.as_vector() + np.tile(offset, gt_shape.n_points))
    results.append(fitter.fit_from_shape(image, initial_shape, max_iters=[15, 15], gt_shape=gt_shape))
```

## Models
`visualize_aam` has a slider for each shape and appearance parameter (`mode='multiple'`, or one slider and a menu with `mode='single'`),
and a tab per scale:

```{code-cell} ipython3
from menpowidgets import visualize_aam

visualize_aam(aam)
```

The shape models alone, as a list with one model per scale:

```{code-cell} ipython3
from menpowidgets import visualize_shape_model_2d

visualize_shape_model_2d([shape_model.model for shape_model in aam.shape_models])
```

## Fitting results
`visualize_fitting_results` browses the results of the fitter, with the shapes of every iteration, the error per iteration and the ground truth.

```{code-cell} ipython3
from menpowidgets import visualize_fitting_results

visualize_fitting_results(results)
```

A single result has the same widget as a method, `result.view_widget()`.
