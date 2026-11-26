---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Running Experiments

A complete example, from the images to a figure of the results: load the images, train a deformable model (an AAM here), fit it on a set of images and
evaluate the fits. It is the experiment that most papers about landmark localisation run.

1. <a href="#import">Import the training and the fitting images</a>
2. <a href="#training">Train the model</a>
3. <a href="#fitting">Fit the model</a>
4. <a href="#results">Results</a>

---------------------------------------

<a id="import"></a>

## 1. Import the training and the fitting images
The training and the testing images come from two disjoint sets (for example the `trainset` and `testset` folders of LFPW). They are pre-processed in the same way,
see [Importing Images](importing.md). Here the set that this website builds on is split in two:

```{code-cell} ipython3
from menpo_docs_data import faces

training_images, test_images = faces()
len(training_images), len(test_images)
```

<a id="training"></a>

## 2. Train the model
```{code-cell} ipython3
from menpo.feature import fast_dsift
from menpofit.aam import HolisticAAM

aam = HolisticAAM(training_images, group='PTS', diagonal=150, scales=(0.5, 1.0),
                  holistic_features=fast_dsift, max_shape_components=20,
                  max_appearance_components=150, verbose=True)
```

The model is trained once and can be saved to disk (`mio.export_pickle(aam, 'aam.pkl')`) to be loaded in the experiments that vary only the fitting.

<a id="fitting"></a>

## 3. Fit the model
A fitter is built from the trained model, with the number of shape and appearance components to use per scale. Every test image is fitted from an initial shape; in an
experiment on real data the initial shape comes from a face detector (see [menpodetect](../menpodetect/index.md) and `fit_from_bb`). Here it is the ground truth,
moved by 4% of the face size, so that the experiment can be repeated exactly:

```{code-cell} ipython3
import numpy as np
from menpofit.aam import LucasKanadeAAMFitter, WibergInverseCompositional

fitter = LucasKanadeAAMFitter(aam, lk_algorithm_cls=WibergInverseCompositional,
                              n_shape=[3, 12], n_appearance=[20, 30])


def shifted(shape, seed, proportion=0.04):
    span = np.ptp(shape.points, axis=0).max()
    offset = np.random.RandomState(seed).randn(2) * proportion * span
    return shape.from_vector(shape.as_vector() + np.tile(offset, shape.n_points))


results = []
for i, image in enumerate(test_images):
    gt_shape = image.landmarks['PTS']
    results.append(fitter.fit_from_shape(image, shifted(gt_shape, seed=i),
                                         max_iters=[15, 15], gt_shape=gt_shape))
```

<a id="results"></a>

## 4. Results
Each result knows the error of its initial and of its final shape. The error is the mean point-to-point distance divided by the size of the ground truth shape, so it can be
compared between images:

```{code-cell} ipython3
initial_errors = [result.initial_error() for result in results]
final_errors = [result.final_error() for result in results]

print("initial:", np.round(initial_errors, 4))
print("final:  ", np.round(final_errors, 4))
```

Experiments are usually reported as a *cumulative error distribution* (CED): the proportion of images that are fitted with an error smaller than each value.

```{code-cell} ipython3
from menpofit.visualize import plot_cumulative_error_distribution

plot_cumulative_error_distribution([initial_errors, final_errors], error_range=(0, 0.15, 0.005),
                                   legend_entries=['Initial', 'Final'], figure_size=(6, 4));
```

With several models or fitters, give one list of errors per curve to compare them in the same figure. To look at the fits one by one, use
`visualize_fitting_results(results)` of [menpowidgets](../menpowidgets/main_menpofit_widgets.md) in a notebook.
