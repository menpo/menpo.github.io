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

# Supervised Descent Method - Basics
The aim of this notebook is to showcase how one can build and fit SDMs to images using `Menpo`.

Note that this notebook assumes that the user has previously gone through the AAMs Basics notebook and he/she is already familiar with the basics of `Menpo`'s Deformable Model Fitting framework explained in there.

+++

## 1. Loading data

+++

In this notebook, we will use the training and test sets of the LFPW database for the training and fitting SDMs.

Note that the necessary steps required for acquiring the LFPW database are explained in detail in the AAMs Basics notebook and the user is simply referred to that notebook for this matter.

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

## 2. Train a SDM with default parameters

+++

Trainign an SDM using `Menpo` is rather straight forward and can be done using a single line of code.
As expected, the SDM training takes some time.

```{code-cell}
from menpofit.sdm import RegularizedSDM
# Note that we use fast dense sift features
# and thus cyvlfeat must be installed (use conda)
from menpo.feature import vector_128_dsift

fitter = RegularizedSDM(
    training_images, 
    verbose=True,
    group='PTS',
    diagonal=200,
    n_perturbations=30,
    n_iterations=2,
    patch_features=vector_128_dsift,
    patch_shape=(24, 24),
    alpha=10
)
```

```{code-cell}
print(fitter)
```

## 3. Fit the previous SDM

+++

Let's try fitting the SDM to some images of the LFPW database test set!!!

```{code-cell}
import menpo.io as mio

# load test images
test_images = []
for i in mio.import_images(path_to_lfpw / 'testset' / '*.png', max_images=5, verbose=True):
    # crop image
    i = i.crop_to_landmarks_proportion(0.5)
    # convert it to grayscale if needed
    if i.n_channels == 3:
        i = i.as_greyscale(mode='luminosity')
    # append it to the list
    test_images.append(i)
```

Note that for the purpose of this simple fitting demonstration we will just fit the first 5 images of the LFPW test set.

Fitting a SDM to an image is as simple as calling its `fit` method:

```{code-cell}
from menpofit.fitter import noisy_shape_from_bounding_box

fitting_results = []

for i in test_images:
    gt_s = i.landmarks['PTS']
    # generate perturbed landmarks
    bb = noisy_shape_from_bounding_box(fitter.reference_shape.bounding_box(), 
                                       gt_s.bounding_box())
    # fit image
    fr = fitter.fit_from_bb(i, bb, gt_shape=gt_s) 
    fitting_results.append(fr)

    # print fitting error
    print(fr)
```

```{code-cell}
from menpowidgets import visualize_fitting_results

visualize_fitting_results(fitting_results)
```
