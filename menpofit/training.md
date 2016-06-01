Training
========

1. [Multi-Scale Models](#multiscale)
2. [Holistic vs. Patch Features](#features)
3. [Incremental Training](#incremental)
4. [Training Example](#example)

---------------------------------------

### <a name="multiscale"></a>1. Multi-Scale Models
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

### <a name="features"></a>2. Holistic vs. Patch Features
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


### <a name="incremental"></a>3. Incremental Training
Most deformable models that exist in `menpofit` can be trained in an **incremental** fashion. This can be very useful
in case you want to train a very powerful model on a large amount of training images, which would be impossible to
do at once due to memory constraints. The incremental training can be performed by using the **batch_size**
parameter, which will split the provided set of training images into batches of the specified size.


### <a name="example"></a>4. Training Example
Given the above basic assumptions and using the `training_images` loaded in the [Importing Images](importing.md) section,
an example of a typical call for training a deformable model using `HolisticAAM` is:

```python
from menpofit.aam import HolisticAAM
from menpo.feature import fast_dsift

aam = HolisticAAM(training_images, reference_shape=None,
                  diagonal=180, scales=(0.25, 0.5, 1.0),
                  holistic_features=igo, verbose=True)
```

The `verbose` flag allows printing the training progress:
```
- Computing reference shape                                                     Computing batch 0
- Building models
  - Scale 0: Done
  - Scale 1: Scaling images: [=         ] 14% (119/811) - 00:00:01 remaining
```

<center>
  <img src="media/face_shape_model.gif" alt="AAM on human face" width="55%">
  <img src="media/face_aam_model.gif" alt="AAM on human face" width="40%">
</center>

Information about any trained model can be retrieved by:

```python
print(aam)
```

which returns:

```
Holistic Active Appearance Model
 - Images scaled to diagonal: 200.00
 - Images warped with DifferentiablePiecewiseAffine transform
 - Scales: [0.25, 0.5, 1.0]
   - Scale 0.25
     - Holistic feature: igo
     - Appearance model class: PCAModel
       - 810 appearance components
     - Shape model class: OrthoPDM
       - 132 shape components
       - 4 similarity transform parameters
   - Scale 0.5
     - Holistic feature: igo
     - Appearance model class: PCAModel
       - 810 appearance components
     - Shape model class: OrthoPDM
       - 132 shape components
       - 4 similarity transform parameters
   - Scale 1.0
     - Holistic feature: igo
     - Appearance model class: PCAModel
       - 810 appearance components
     - Shape model class: OrthoPDM
       - 132 shape components
       - 4 similarity transform parameters
```
