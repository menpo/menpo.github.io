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

# Constrained Local Models - Basics
The aim of this notebook is to showcase how one can build and fit CLMs to images using ``menpofit``.

Note that this notebook assumes that the user has previously gone through the AAMs Basics notebook and he/she is already familiar with the basics of `Menpo`'s Deformable Model Fitting framework explained in there.

+++

## 1. Loading data

```{code-cell}
from menpo_docs_data import lfpw_like_directory
%matplotlib inline
from pathlib import Path


path_to_lfpw = lfpw_like_directory()  # your data: Path('/path/to/lfpw')
```

```{code-cell}
import menpo.io as mio

training_images = []
# load landmarked images
for i in mio.import_images(path_to_lfpw / 'trainset', verbose=True):
    # crop image
    i = i.crop_to_landmarks_proportion(0.1)
    # convert it to grayscale if needed
    if i.n_channels == 3:
        i = i.as_greyscale(mode='luminosity')
    # append it to the list
    training_images.append(i)
```

```{code-cell}
from menpowidgets import visualize_images

visualize_images(training_images)
```

## 2. Build a CLM with default parameters

+++

Building a CLM using `Menpo` can be done using a single line of code.

```{code-cell}
from menpofit.clm import CLM


clm = CLM(
    training_images, 
    verbose=True,
    group='PTS',
    diagonal=200
)
```

```{code-cell}
print(clm)
```

```{code-cell}
from menpowidgets import visualize_clm
visualize_clm(clm)
```

## 3. Fit the previous CLM

+++

In `Menpo`, CLMs can be fitted to images by creating `Fitter` objects around them. 

One of the most popular algorithms for fitting CLMs is the `Regularized Landmark Mean-Shift` algorithm. In order to fit our CLM using this algorithm using `Menpo`, the user needs to define a `GradientDescentCLMFitter` object. This can be done again using a single line of code!!!

```{code-cell}
from menpofit.clm import GradientDescentCLMFitter

fitter = GradientDescentCLMFitter(clm, n_shape=[6, 12])
```

Fitting a `GradientDescentCLMFitter` to an image is as simple as calling its `fit` method. Let's try it by fitting some images of the LFPW database test set!!!

```{code-cell}
import menpo.io as mio

# load test images
test_images = []
for i in mio.import_images(path_to_lfpw / 'testset', max_images=5, verbose=True):
    # crop image
    i = i.crop_to_landmarks_proportion(0.5)
    # convert it to grayscale if needed
    if i.n_channels == 3:
        i = i.as_greyscale(mode='luminosity')
    # append it to the list
    test_images.append(i)
```

Note that for the purpose of this simple fitting demonstration we will just fit the first 5 images of the LFPW test set.

```{code-cell}
from menpofit.fitter import noisy_shape_from_bounding_box

fitting_results = []

for i in test_images:
    gt_s = i.landmarks['PTS']
    # generate perturbed landmarks
    s = noisy_shape_from_bounding_box(gt_s, gt_s.bounding_box())
    # fit image
    fr = fitter.fit_from_shape(i, s, gt_shape=gt_s) 
    fitting_results.append(fr)

    # print fitting error
    print(fr)
```

```{code-cell}
from menpowidgets import visualize_fitting_results

visualize_fitting_results(fitting_results)
```
