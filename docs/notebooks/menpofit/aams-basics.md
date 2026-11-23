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

# Active Appearance Models - Basics
This notebook provides a basic tutorial on Active Appearance Models (AAMs). AAMs are generative parametric models that describe the shape and appearance of a certain object class; e.g. the human face. In a typical application, these models are matched against input images to obtain the set of parameters that best describe a particular instance of the object being modelled.

The aim of this short notebook is to showcase how one can build and fit AAMs to images using ``menpo`` and ``menpofit``. It includes the following sections:

1. Acquiring data
2. Loading and visualizing data
3. Building a simple AAM
4. Fit a simple AAM

+++

## 1. Acquiring data

+++

AAMs are typically build from a large collection of annotated images. In this notebook we will build AAMs from annotated images of the human face and, consequently, this is the object our AAMs will model.

The Breaking Bad image in `Menpo`'s data folder is a good example of this kind of annotated images:

```{code-cell}
%matplotlib inline
from pathlib import Path

import menpo.io as mio
from menpo.visualize import print_progress

breakingbad = mio.import_builtin_asset.breakingbad_jpg()
breakingbad = breakingbad.crop_to_landmarks_proportion(0.5)
breakingbad.view_landmarks();
```

In this notebook, we will build AAMs using one of the most popular and widely used annotated facial databases, the Labeled Faces Parts in the Wild (LFPW) database. Both images and corresponding facial landmark annotations are publicly available and can be downloaded from the following link: 

* http://ibug.doc.ic.ac.uk/download/annotations/lfpw.zip/ 

In order to continue with this notebook, the user is required to simply: 
 
* Click on the previous link.
* Fill out the form with his/her details. 
* Proceed to download the LFPW database. 
* Unzip and save the LFPW database to a location of his/her like.
* Paste the path to the local copy of the LFPW database on the next cell.
 
Note that the `.zip` file containing the whole annotated database is of approximately 350MB.

```{code-cell}
from menpo_docs_data import lfpw_like_directory
path_to_lfpw = lfpw_like_directory()  # your data: Path('/path/to/lfpw')
```

## 2. Loading and visualizing data

+++

The first step in building our AAM will be to import all the images and annotations of the training set of LFPW database. Luckily, `Menpo`'s `io` module allows us to do exactly that using only a few lines of code:

```{code-cell}
import menpo.io as mio

training_images = []
# load landmarked images
for i in mio.import_images(path_to_lfpw / 'trainset', verbose=True):
    # crop image
    i = i.crop_to_landmarks_proportion(0.1)
    # convert it to greyscale if needed
    if i.n_channels == 3:
        i = i.as_greyscale(mode='luminosity')
    # append it to the list
    training_images.append(i)
```

The previous cell loads all the images of the LFPW together with their corresponding landmark annotations.

Note that here the images are cropped in order to save some valuable memory space and, for simplicity, also converted to greyscale.

The `Menpo` ecosystem is well equiped with a series of predefined Jupyter Notebook widgets for the most common data visualization tasks. In order to check if the data has been correctly imported we will use the ``visualize_images`` widget. Note that menpowidgets must be installed before widgets can be used.

```{code-cell}
from menpowidgets import visualize_images

visualize_images(training_images)
```

## 3. Building a simple AAM

+++

Deformable models, in general, and AAMs, in particular, are a one of the core concept of `Menpo` and all efforts have been put to facilitate their usage. In fact, given a list of training images, an AAM can be built using a single line of code.

```{code-cell}
from menpofit.aam import HolisticAAM
from menpo.feature import no_op

# build AAM
aam = HolisticAAM(
    training_images,
    group='PTS',
    verbose=True,
    holistic_features=no_op, 
    diagonal=120, 
    scales=1
)
```

Note that here we import a feature to use from `menpo.features`. In this very basic case we actually do not want to use a feature at all - so we use the special `no_op` feature that does nothing. Features are in general required to get good fitting performance, hence the default `feature_type` is actually `igo`.

As first class citizens of `Menpo`, AAMs can be printed just like any other `Menpo` object (e.g. `Images` or `PointClouds)`:

```{code-cell}
print(aam)
```

Printing an AAM is the easiest way to retrieve its specific characteristics. For example, printing the previous AAM tells us that it was built using pixel intensities (no_op features), amongst several other things.

AAMs also define an instance method that allows us to generate novel AAM instances by applying a set of particular weights to the components of their shape and apperance models:

```{code-cell}
# using default parameters
aam.instance().view();

# varying shape parameters
aam.instance(shape_weights=[1.0, 0.5, -2.1]).view(new_figure=True);

# varying appearance parameters
aam.instance(appearance_weights=[2.7, 3.5, 0.9]).view(new_figure=True);

# varying both
aam.instance(shape_weights=[1.0, 0.5, -2.1], appearance_weights=[2.7, 3.5, 0.9]).view(new_figure=True);
```

Furthermore, ``menpofit`` is equiped with a powerfull widget that allow us to explore AAMs:

```{code-cell}
from menpowidgets import visualize_aam
visualize_aam(aam)
```

You can also independently visualize the shape and the appearance models using widgets

```{code-cell}
from menpowidgets import visualize_shape_model_2d
visualize_shape_model_2d([sm.model for sm in aam.shape_models])
```

```{code-cell}
from menpowidgets import visualize_appearance_model
visualize_appearance_model(aam.appearance_models)
```

## 4. Fit a simple AAM 

+++

In `Menpo`, AAMs can be fitted to images by creating `Fitter` objects around them. 

One of the most popular and well known family of algorithms for fitting AAMs is the one based around the original `Lucas-Kanade` algorithm for Image Alignment. In order to fit our AAM using an algorithms of the previous family, `Menpo` allows the user to define a `LucasKanadeAAmFitter` object. Again, using a single line of code!!!

```{code-cell}
from menpofit.aam import LucasKanadeAAMFitter

# define Lucas-Kanade based AAM fitter
fitter = LucasKanadeAAMFitter(aam, n_shape=0.9, n_appearance=0.9)
```

The previous cell has created a `LucasKanadeAAMFitter` that will fit images using 90% of the variance present on the AAM's shape and appearance models and that will use the default `LucasKanade` algorithm for fitting AAMs.

+++

Fitting a `LucasKanadeAAMFitter` to an image is as simple as calling its `fit_from_shape` method. Let's try it by fitting some images of the LFPW database test set!!!

```{code-cell}
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

# fit images
for i in test_images:
    # obtain ground truth (original) landmarks
    gt_s = i.landmarks['PTS']
    
    # generate initialization shape
    initial_s = noisy_shape_from_bounding_box(gt_s, gt_s.bounding_box())
    
    # fit image
    fr = fitter.fit_from_shape(i, initial_s, gt_shape=gt_s)
    fitting_results.append(fr)
    
    # print fitting error
    print(fr)
```

`Menpo`'s `Fitter` objects save the result of their fittings using Menpo's `FittingResult` objects. Being a `Fitter` object itself, the `LucasKanadeAAMFitter` is no exception to the rule and, consequently, the result obtained by executing the previous cell is a list of `FittingResult` objects.

`FittingResult` objects are core `Menpo` objects that allow the user to print, visualize and analyse the results produced by `Fitter` objects. Like all `Menpo`'s core objects `FittingResult` are printable. Note that, they were printed inside of the previous fitting  loop in order to display the final fitting error for each fitted image.

Apart from being printable, `FittingResult` objects also allow the user to quickly visualize the initial shape from which the fitting algorithm started from and the final fitting result:

```{code-cell}
fr = fitting_results[1]
```

```{code-cell}
fr.image.view(new_figure=True);
fr.final_shape.view();

fr.image.view(new_figure=True);
fr.initial_shape.view(marker_face_colour='blue');
```

```{code-cell}
from menpowidgets import visualize_fitting_results
visualize_fitting_results([fr])
```

Again, there exist a `menpofit` IPython Notebook widget that facilitates the visualization of `FittingResult`.

```{code-cell}
from menpowidgets import visualize_fitting_results

visualize_fitting_results(fitting_results)
```
