---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.7
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Active Template Model - Basics
This notebook provides a basic tutorial on Active Template Models (ATMs). ATMs are used to perform image alignment driven by a statistical shape model.

+++

## 1. Loading shapes

+++

The first step in building our ATM will be to import all the annotations of the training set of LFPW database. Luckily, `Menpo`'s `io` module allows us to do exactly that using only a few lines of code:

```{code-cell}
from menpo_docs_data import lfpw_like_directory
from pathlib import Path

path_to_lfpw = lfpw_like_directory()  # your data: Path('/path/to/lfpw')
```

```{code-cell}
import menpo.io as mio

training_shapes = []
# load landmarked images
for i in mio.import_landmark_files(path_to_lfpw / 'trainset' / '*.pts', verbose=True):
    training_shapes.append(i['PTS'])
```

The previous cell loads all the PTS files of the LFPW.

The `Menpo` ecosystem is well equiped with a series of predefined IPython Notebook widgets for the most common data visualization tasks. In order to check if the data has been correctly imported we will use the ``visualize_shapes_2d`` widget. Note that menpowidgets must be installed in order to use the widgets functionality.

```{code-cell}
%matplotlib inline
from menpowidgets import visualize_shapes_2d

visualize_shapes_2d(training_shapes)
```

## 2. Building a simple ATM

+++

In order to build an ATM, we need to load a template image. This will be the first image of the LFPW training set.

```{code-cell}
template_image = mio.import_image(sorted((path_to_lfpw / 'trainset').glob('*.png'))[0])
template_image.view_landmarks();
```

It is very easy to build the ATM

```{code-cell}
from menpofit.atm import HolisticATM

# build ATM
atm = HolisticATM(
    template_image, 
    training_shapes,
    group='PTS',
    verbose=True,
    diagonal=150
)
```

As first class citizens of `Menpo`, AAMs can be printed just like any other `Menpo` object (e.g. `Images` or `PointClouds)`:

```{code-cell}
:tags: [remove-output, record-model]
print(atm)
```

```{recorded-output} model
```

We can also visualize the ATM model

```{code-cell}
from menpowidgets import visualize_atm
visualize_atm(atm)
```

## 3. Fit a simple ATM 

+++

In ``menpofit``, ATMs can be fitted to images by creating `Fitter` objects around them. 

One of the most popular and well known family of algorithms for fitting ATMs is the one based around the original `Lucas-Kanade` algorithm for Image Alignment. In order to fit our AAM using an algorithms of the previous family, `Menpo` allows the user to define a `LucasKanadeATMFitter` object. Again, using a single line of code!!!

```{code-cell}
from menpofit.atm import LucasKanadeATMFitter

# define Lucas-Kanade based ATM fitter
fitter = LucasKanadeATMFitter(atm, n_shape=[6, 12])
```

The previous cell has created a `LucasKanadeATMFitter` that will fit images using 6 and 12 shape components at its two scales.

+++

Fitting a `LucasKanadeATMFitter` to an image is as simple as calling its `fit` method. An ATM has no model of appearance: it can only find what looks like its template, so the template of a real application comes from another image of the same subject (for example the previous frame of a video). To keep this example self-contained, we fit the image that the template was taken from, starting from a perturbation of its ground truth!!!

```{code-cell}
test_image = template_image
from menpowidgets import visualize_images
visualize_images([test_image])
```

```{code-cell}
:tags: [remove-output, record-fit]
from menpofit.fitter import noisy_shape_from_bounding_box

# obtain groubnd truth (original) landmarks
gt_s = test_image.landmarks['PTS']

# generate initialization landmarks
initial_s = noisy_shape_from_bounding_box(gt_s, gt_s.bounding_box())

# fit image
fitting_result = fitter.fit_from_shape(test_image, initial_s, gt_shape=gt_s)

# print fitting error
print(fitting_result)
```

```{recorded-output} fit
```

Let's visualize the result using the widget

```{code-cell}
from menpowidgets import visualize_fitting_results
visualize_fitting_results([fitting_result])
```
