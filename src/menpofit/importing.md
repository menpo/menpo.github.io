Importing Images
================

1. [Data format](#data)
2. [Simple "lazy" import](#lazy)
3. ["Non-lazy" import with pre-processing?](#preprocessing)
4. [Smart "lazy" import with pre-processing!](#smart)

---------------------------------------

### 1. Data Format {#data}
In order to train a deformable model, we need to have a set of training images with ground truth annotations of the landmark points.
The input/output package of `menpo` is very powerful and makes images and landmarks loading extremely easy.
It supports the vast majority of image formats, as well as various landmark file formats (e.g. PTS, LJSON, etc.).

The human face is the most common deformable object used in current literature of deformable modelling. This is mainly
due to the fact that there are many manually annotated and publicly available databases of human face.
Thus, we will be using the human face for the purpose of this tutorial.

In order to continue, you can download some facial annotated databases from the IBUG website:
<center>
  <a href="http://ibug.doc.ic.ac.uk/resources/facial-point-annotations/" title="Download facial annotated databases">
  http://ibug.doc.ic.ac.uk/resources/facial-point-annotations/
  </a>
</center>
for example `LFPW` database ("in-the-wild", 811 and 224 training and testing images, respectively).
Note that you have to enter your details (name, affiliation, email) before download.


### 2. Simple "Lazy" Import {#lazy}
The downloaded images along with their landmarks can be easily imported as:

```python
import menpo.io as mio
path_to_images = '/path/to/lfpw/trainset/'
training_images = mio.import_images(path_to_images, verbose=True)
```

The default behaviour of `import_images()` imports and attaches the landmark files that share the same filename stem as the images.
The group name of the attached landmarks is based on the extension of the landmark file. This means
that it is much more convenient to locate the landmark files in the same directory as the image files.
However, this behavior can be customised using the `landmark_resolver` argument of `import_images()`
(see the <a href="http://menpo.readthedocs.io/en/stable/api/menpo/io/import_images.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>).

Note that `import_images()` returns a **`LazyList`**. Therefore, the above call will return immediately and indexing into the
returned list will load an image at run time. This can be very useful for visualizing the images with:

```python
%matplotlib inline
from menpowidgets import visualize_images
visualize_images(training_images)
```

where the images get loaded when asked to be rendered.


### 3. "Non-Lazy" Import With Pre-Processing {#preprocessing}
Given that many deformabe models require significant memory for training, it is wise in general to
reduce memory usage of training data as much as possible. This can be done by applying
some simple pre-processing steps on the images. Examples of such pre-processing involve:
  * **Crop** the images around their landmark points, since this is the only region we need for training
  * **Convert** RGB images into **greyscale** which is supported by most feature functions.
  * **Rescale** the images to a reasonable size.
  * Store images as **uint8** instead of double precision.
This pre-processing can be done by looping over the `LazyList` as:

```python
import menpo.io as mio
from menpo.visualize import print_progress

path_to_images = '/path/to/lfpw/trainset/'
training_images = []
for img in print_progress(mio.import_images(path_to_images, verbose=True)):
    # convert to greyscale
    if img.n_channels == 3:
        img = img.as_greyscale()
    # crop to landmarks bounding box with an extra 20% padding
    img = img.crop_to_landmarks_proportion(0.2)
    # rescale image if its diagonal is bigger than 400 pixels
    d = img.diagonal()
    if d > 400:
        img = img.rescale(400.0 / d)
    # append to list
    training_images.append(img)
```

The `print_progress()` function allows us to view the loading progress by printing a nice progress bar and remaining time estimation:

```
Found 811 assets, index the returned LazyList to import.
[================    ] 82% (673/811) - 00:00:04 remaining
```

The above process will return a `list`, which means that all the images are actually loaded in memory.

Let's make things tidier:

```python
import menpo.io as mio
from menpo.visualize import print_progress

def process(image, crop_proportion=0.2, max_diagonal=400):
    if image.n_channels == 3:
        image = image.as_greyscale()
    image = image.crop_to_landmarks_proportion(crop_proportion)
    d = image.diagonal()
    if d > max_diagonal:
        image = image.rescale(float(max_diagonal) / d)
    return image

path_to_images = '/path/to/lfpw/trainset/'
training_images = []
for img in print_progress(mio.import_images(path_to_images, verbose=True)):
    training_images.append(process(img))
```

The `list` of images can once again be visualized using `menpowidgets` as:

```python
%matplotlib inline
from menpowidgets import visualize_images
visualize_images(training_images)
```

This importing procedure is much better due to the pre-processing step, but we
lost all the nice and memory-efficient properties of `LazyList`. It would be really useful if we could
pre-process the images and _keep_ the "lazy" property!

### 4. Smart "Lazy" Import With Pre-Processing! {#smart}
We take advantage of `.map()` function of `LazyList` in order to be able to pre-process the images and _keep_ the "lazy" property.
Specifically, using the same `process()` function as before, we can do:

```python
import menpo.io as mio

def process(image, crop_proportion=0.2, max_diagonal=400):
    if image.n_channels == 3:
        image = image.as_greyscale()
    image = image.crop_to_landmarks_proportion(crop_proportion)
    d = image.diagonal()
    if d > max_diagonal:
        image = image.rescale(float(max_diagonal) / d)
    return image

path_to_images = '/path/to/lfpw/trainset/'
training_images = mio.import_images(path_to_images, verbose=True)
training_images = training_images.map(process)
```

which will _instantly_ return a `LazyList` with the pre-processed images. These can be visualized as:

```python
%matplotlib inline
from menpowidgets import visualize_images
visualize_images(training_images)
```

where each image will be loaded and pre-processed when indexed for visualization.

<video width="100%" autoplay loop>
  <source src="media/visualize_images_lfpw.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

In case you wish to get rid of the `LazyList` and load the images in memory, it can be easily done as:

```python
from menpo.visualize import print_progress
training_images_non_lazy = list(print_progress(training_images))
```
