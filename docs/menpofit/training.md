---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Training

1. <a href="#multiscale">Multi-Scale Models</a>
2. <a href="#features">Holistic vs. Patch Features</a>
3. <a href="#incremental">Incremental Training</a>
4. <a href="#example">Training Example</a>

---------------------------------------

<a id="multiscale"></a>

## 1. Multi-Scale Models
All the methods implemented in `menpofit` are built in a **multi-scale** manner, i.e. in multiple resolutions.
In all our core classes, this is controlled using the following three parameters:

**reference_shape** (`PointCloud`)  
First, the size of the training images is normalized by rescaling them so that the scale of their ground truth shapes matches the scale of this reference shape. In case no reference shape is provided by the user, then the mean of the ground shapes is used. This step is essential in order to ensure consistency among the extracted features of the images.

**diagonal** (`int`)  
This parameter is used to rescale the reference shape so that the diagonal of its bounding box matches the provided value. This rescaling takes place before normalizing the training images' size. Thus, this parameter controls the resolution of the model at the highest scale.

**scales** (`tuple` of `float`)  
A tuple with the scale value at each level, provided in ascending order, i.e. from lowest to highest scale. These values are proportional to the final resolution achieved through the reference shape normalization.

The multi-scale training pattern followed by all `menpofit` methods is summarized in the following _pseudocode_:
```
REQUIRE: images, shapes
PARAMETERS: reference_shape, diagonal, scales
1. IF reference_shape IS None:
2.     reference_shape = mean_pointcloud(shapes)
3. reference_shape = reference_shape.rescale_to_diagonal(diagonal)
4. scaled_images, scaled_shapes = rescale_to_reference_shape(images, shapes,
5.                                                           reference_shape)
6. FOR scale IN scales:
7.     scaled_images, scaled_shapes = rescale(images, shapes, scale)
8.     scale_model = train_model(scaled_images, scaled_shapes)
```

<a id="features"></a>

## 2. Holistic vs. Patch Features
The methods implemented in `menpofit` can be roughly separated in two categories, based on the appearance representation approach:
* **Holistic Models:** These are models that use a holistic appearance,
  which means that the whole texture that lies within the deformable object is taken into account.
* **Patch-based Models:** These are models that employ a patch-based appearance representation, which means
  that rectangular patches are extracted that are centered around each landmark point.

Both hositic and patch-based methods have a **holistic\_features** argument which expects the `callable` that will
be used for extracting features from the training images. The patch-based methods build _on top_ of the computed
holistic features in order to extract patches and can have two behaviours depending on their nature:
1. Those that simply extract patches from the **holistic\_features** representation of the training images, given a **patch_shape**.
2. Those that extract patches from the **holistic\_features** representation of the training images, given a **patch_shape**, and
   additionally compute some **patch_features**.


<a id="incremental"></a>

## 3. Incremental Training
Most deformable models that exist in `menpofit` can be trained in an **incremental** fashion. This can be very useful
in case you want to train a very powerful model on a large amount of training images, which would be impossible to
do at once due to memory constraints. The incremental training can be performed by using the **batch_size**
parameter, which will split the provided set of training images into batches of the specified size.


<a id="example"></a>

## 4. Training Example
Given the above basic assumptions and using the `training_images` loaded in the [Importing Images](importing.md) section,
an example of a typical call for training a deformable model using `HolisticAAM` is:

```{code-cell} ipython3
:tags: [remove-input]

# `training_images` as in the Importing Images section: small annotated faces, pre-processed
from menpo_docs_data import faces

training_images, _ = faces()
```

```{code-cell} ipython3
from menpofit.aam import HolisticAAM
from menpo.feature import fast_dsift

aam = HolisticAAM(training_images, reference_shape=None,
                  diagonal=150, scales=(0.5, 1.0),
                  holistic_features=fast_dsift, batch_size=100, verbose=True)
```

The `verbose` flag prints the training progress. `batch_size` trains the model in batches of images, with an incremental PCA, so that thousands of training images do not have to be in memory at once (the features of a image are several times its size). The images are best given as a `LazyList`, which `mio.import_images` returns, so that they are not loaded either. Information about any trained model can be retrieved by:

```{code-cell} ipython3
print(aam)
```

The number of components is capped by the number of training images, so a model trained on many images has many more.
`max_shape_components` and `max_appearance_components` set an upper limit when training; to use fewer components
afterwards, trim the models, see the [Point Distribution Model](pdm.md) page.
