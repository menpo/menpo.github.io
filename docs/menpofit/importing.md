---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Importing Images

1. <a href="#data">Data format</a>
2. <a href="#lazy">Simple "lazy" import</a>
3. <a href="#preprocessing">"Non-lazy" import with pre-processing</a>
4. <a href="#smart">Smart "lazy" import with pre-processing</a>

---------------------------------------

<a id="data"></a>

## 1. Data Format
In order to train a deformable model, we need to have a set of training images with ground truth annotations of the landmark points.
The input/output package of `menpo` is very powerful and makes images and landmarks loading extremely easy.
It supports the vast majority of image formats, as well as various landmark file formats (e.g. PTS, LJSON, etc.).

The human face is the most common deformable object used in current literature of deformable modelling. This is mainly
due to the fact that there are many manually annotated and publicly available databases of human faces.
Thus, we will be using the human face for the purpose of this tutorial.

You can download facial databases with 68 point annotations from the [iBUG website](https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/),
for example 300-W or LFPW (you have to accept the terms of use of each database). Put the images and their `.pts` files in one directory.

```{code-cell} ipython3
:tags: [remove-input]

# The page is built on a small set of annotated faces: use it where you would use your own folder.
from menpo_docs_data import faces_directory

path_to_images = faces_directory()
```

In the examples below, `path_to_images` is the directory with your images, for example `'/path/to/lfpw/trainset/'`.

<a id="lazy"></a>

## 2. Simple "Lazy" Import
The images along with their landmarks can be imported as:

```{code-cell} ipython3
import menpo.io as mio

training_images = mio.import_images(path_to_images, verbose=True)
```

The default behaviour of `import_images()` imports and attaches the landmark files that share the same filename stem as the images.
The group name of the attached landmarks is based on the extension of the landmark file (`PTS` for `.pts` files). This means
that it is much more convenient to locate the landmark files in the same directory as the image files.
However, this behavior can be customised using the `landmark_resolver` argument of
{py:func}`import_images() <menpo.io.import_images>`.

Note that `import_images()` returns a **`LazyList`**. Therefore, the above call returns immediately and indexing into the
returned list will load an image at run time. This can be very useful for visualizing the images with:

```python
from menpowidgets import visualize_images
visualize_images(training_images)
```

where the images get loaded when asked to be rendered.

```{code-cell} ipython3
image = training_images[0]
image, image.landmarks.group_labels
```

<a id="preprocessing"></a>

## 3. "Non-Lazy" Import With Pre-Processing
Given that many deformable models require significant memory for training, it is wise in general to
reduce memory usage of training data as much as possible. This can be done by applying
some simple pre-processing steps on the images. Examples of such pre-processing involve:
  * **Crop** the images around their landmark points, since this is the only region we need for training
  * **Convert** RGB images into **greyscale** which is supported by most feature functions.
  * **Rescale** the images to a reasonable size.
  * Store images as **uint8** instead of double precision.

This pre-processing can be done by looping over the `LazyList`:

```{code-cell} ipython3
from menpo.visualize import print_progress

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

len(training_images)
```

The `print_progress()` function allows us to view the loading progress by printing a nice progress bar and remaining time estimation.
The above process returns a `list`, which means that all the images are actually loaded in memory.

Let's make things tidier:

```{code-cell} ipython3
def process(image, crop_proportion=0.2, max_diagonal=400):
    if image.n_channels == 3:
        image = image.as_greyscale()
    image = image.crop_to_landmarks_proportion(crop_proportion)
    d = image.diagonal()
    if d > max_diagonal:
        image = image.rescale(float(max_diagonal) / d)
    return image


training_images = []
for img in print_progress(mio.import_images(path_to_images, verbose=True)):
    training_images.append(process(img))
```

The `list` of images can once again be visualized using `menpowidgets`:

```python
from menpowidgets import visualize_images
visualize_images(training_images)
```

This importing procedure is much better due to the pre-processing step, but we
lost all the nice and memory-efficient properties of `LazyList`. It would be really useful if we could
pre-process the images and _keep_ the "lazy" property!

<a id="smart"></a>

## 4. Smart "Lazy" Import With Pre-Processing
We take advantage of the `.map()` function of `LazyList` in order to pre-process the images and _keep_ the "lazy" property.
Using the same `process()` function as before:

```{code-cell} ipython3
training_images = mio.import_images(path_to_images, verbose=True)
training_images = training_images.map(process)
```

This _instantly_ returns a `LazyList` with the pre-processed images. Each image is loaded and pre-processed when it is indexed:

```{code-cell} ipython3
training_images[0].view_landmarks(group="PTS", render_numbering=False);
```

In case you wish to get rid of the `LazyList` and load the images in memory, it can be easily done as:

```{code-cell} ipython3
training_images_non_lazy = list(print_progress(training_images))
len(training_images_non_lazy)
```
