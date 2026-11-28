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

# Active Appearance Models - Advanced
The aim of this notebook is to showcase some of the more advanced features that are available for building and fitting AAMs using ``menpo`` and ``menpofit``. 

Note that this notebook assumes that the user has previously gone through the AAMs Basic notebook and he/she is already familiar with the basic AAMs and `Menpo` concepts explained in there. The AAMs Basic notebook shows us how through the use of the `HolisticAAM` and the `LucasKanadeAAMFitter` classes one can easily build and fit basic AAMs using `Menpo`. In reality, `Menpo`'s framework for AAMs is a lot more powerful and we will proceed to show how a large variety of different AAMs and different fitting algorithms can be used by simply specifying the right keyword arguments on the two classes.

The complete list of the available keyword arguments for `HolisticAAM` and their corresponding detailed explanations can be found in Menpo's documentation. Remember that their documentation can be checked at any time from the IPython Notebook by simply running:

```{code-cell}
from menpofit.aam import HolisticAAM

HolisticAAM??
```

This notebook is structured in several short sections, each one explaining a different advanced concept related to `Menpo`'s framework for building and fitting AAMs. Specifically:

1. Loading data
2. Building and fitting AAMs with user-defined appearance features
3. Fitting AAMs using different `LucasKanade` based algorithms.
4. Patch-Based AAM building and fitting
5. Fitting AAMs using `Menpo's` Supervised Descent (SD) framework

Note that, in general, these sections are fairly detached from one another and the order in which they are listed bellow is not specifically relevant.

+++

## 1. Loading data

+++

All the following sections will rely on some training and testing data to build and fit their respective AAMs. Once again, we will rely on the training and test sets of the LFPW database for this purpose.

Note that the necessary steps required for acquiring the LFPW database are explained in detail in the AAMs Basics notebook and the user is simply referred to that notebook for this matter.

Let us define the function `load_database()` for loading a set of images, cropping them and converting them to greyscale

```{code-cell}
%matplotlib inline
from pathlib import Path
import menpo.io as mio

# method to load a database
def load_database(path_to_images, crop_percentage, max_images=None):
    images = []
    # load landmarked images
    for i in mio.import_images(path_to_images, max_images=max_images, verbose=True):
        # crop image
        i = i.crop_to_landmarks_proportion(crop_percentage)
        
        # convert it to grayscale if needed
        if i.n_channels == 3:
            i = i.as_greyscale(mode='luminosity')
            
        # append it to the list
        images.append(i)
    return images
```

and also define the path to the LFPW database.

Note that the necessary steps required for acquiring the LFPW dataset used throughout this notebook were previously explained in the AAMs Basics notebook and we simply refer the user to that notebook for this matter.

```{code-cell}
from menpo_docs_data import lfpw_like_directory
path_to_lfpw = lfpw_like_directory()  # your data: Path('/path/to/lfpw')
```

Load and visualize the __training__ images with a crop proportion of 10%:

```{code-cell}
training_images = load_database(path_to_lfpw / 'trainset', 0.1)
```

```{code-cell}
from menpowidgets import visualize_images

visualize_images(training_images)
```

Load and visualize 5 __test__ images with a crop proportion of 50%:

```{code-cell}
test_images = load_database(path_to_lfpw / 'testset', 0.5, max_images=5)
```

```{code-cell}
visualize_images(test_images)
```

## 2. Building and fitting AAMs with user-defined appearance features

+++

One of the most powerful and general characteristics of the `HolisticAAM` class is that it allows the user to build AAMs with arbitrarily user-defined appearance features. Instead of restricting the user to a set of predefined appearance features, `Menpo` allows him/her to define new features (perhaps simple combinations of existing image features supported by Menpo or perhaps completely new (even discriminative!) features designed by the user) and pass them to the `HolisticAAM`.

All that is required is that the user decorates his/her desired feature computation using one of the feature decorators defined in Menpo, i.e. `@ndfeature`, `@imgfeature` or `@winitfeature`. The two first decorators allow the user to define feature computations in terms of simple `numpy` arrays and `Menpo` images. The third decorator supports the definition of features that rely on a cell/block structure (like **HOG** or **SIFT**). Note that, the only computation that needs to be defined by the user defined feature funtion is the pure feature computation over the image pixels; landmarks and mask attached to the image are handled by the previous decorators.

The next cell shows a simple example of such a function, in which **igo** features are computed on an feature image that was already obtained by computing **igo** features:

```{code-cell}
from menpo.feature import imgfeature, igo

@imgfeature
def custom_double_igo(image):
    return igo(igo(image))
```

```{code-cell}
custom_double_igo(training_images[0]).view();
```

We can now build an AAM using our new feature representation with the following command:

```{code-cell}
from menpofit.aam import HolisticAAM


aam = HolisticAAM(
    training_images,
    group='PTS',
    verbose=True,
    holistic_features=custom_double_igo, 
    diagonal=120, 
    scales=(0.5, 1.0)
)
```

```{code-cell}
:tags: [remove-output, record-holistic]
print(aam)
```

```{recorded-output} holistic
```

Let us now visualize the AAM model

```{code-cell}
from menpowidgets import visualize_aam
visualize_aam(aam)
```

The trained AAM can be used to fit the loaded testing images using the following commands:

```{code-cell}
from menpofit.aam import LucasKanadeAAMFitter

fitter = LucasKanadeAAMFitter(aam, n_shape=[6, 12], n_appearance=0.5)
```

```{code-cell}
:tags: [remove-output, record-holisticfit]
from menpofit.fitter import noisy_shape_from_bounding_box

fitting_results = []

for i in test_images:
    # obtain original landmarks
    gt_s = i.landmarks['PTS']
    
    # generate perturbed landmarks
    s = noisy_shape_from_bounding_box(gt_s, gt_s.bounding_box())
    
    # fit image
    fr = fitter.fit_from_shape(i, s, gt_shape=gt_s) 
    fitting_results.append(fr)
    
    print(fr)
```

```{recorded-output} holisticfit
```

Let's have a look at the fitting results:

```{code-cell}
from menpowidgets import visualize_fitting_results

visualize_fitting_results(fitting_results)
```

## 4. Patch-Based AAM building and fitting

+++

All the previous AAM examples were using a holistic appearance representation, i.e. the whole face was employed as an appearance vector. Herein, we show how to build and fit a patch-based AAM. This means that the appearance representation consists of small patches extracted around each of the landmark points.

The patch-based AAM builder, `PatchAAM`, has the same parameters as the `HolisticAAM`, with the addition of the `patch_shape` parameter. We'll train such an AAM using IGOs with double angles as feature representation:

```{code-cell}
from menpofit.aam import PatchAAM
from menpo.feature import double_igo

patch_based_aam = PatchAAM(
    training_images,
    group='PTS',
    verbose=True,
    holistic_features=double_igo, 
    diagonal=120, 
    scales=(0.5, 1.0)
)
```

```{code-cell}
:tags: [remove-output, record-patch]
print(patch_based_aam)
```

```{recorded-output} patch
```

```{code-cell}
from menpowidgets import visualize_patch_aam
visualize_patch_aam(patch_based_aam)
```

The fitting of the trained Patch-Based AAM can use any of the algorithms of the `LucasKanadeAAMFitter` presented in the previous section as:

```{code-cell}
fitter = LucasKanadeAAMFitter(patch_based_aam, 
                              n_shape=[3, 12], 
                              n_appearance=50)
```

```{code-cell}
:tags: [remove-output, record-patchfit]
from menpofit.fitter import noisy_shape_from_bounding_box

fitting_results = []

for i in test_images:
    # obtain original landmarks
    gt_s = i.landmarks['PTS']
    
    # generate perturbed landmarks
    s = noisy_shape_from_bounding_box(gt_s, gt_s.bounding_box())
    
    # fit image
    fr = fitter.fit_from_shape(i, s, gt_shape=gt_s) 
    fitting_results.append(fr)
    
    print(fr)
```

```{recorded-output} patchfit
```

```{code-cell}
visualize_fitting_results(fitting_results)
```
