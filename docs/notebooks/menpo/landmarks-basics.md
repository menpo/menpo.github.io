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

# Landmarks Basics
In Menpo, we recognise the importance of annotating data. Annotations are most commonly defined as a set of coordinates on an image or a mesh that define points of interest. For example, an image may be annotated in order to provide a set of landmarks that define the major features of the face (the contour of the eyes or mouth). 

Menpo tightly couples core data types, `Image` and `PointCloud`/`PointGraph`/`TriMesh`, with landmarks. We also reuse our types here, as all landmarks are, at their core, a ``PointCloud``. This means landmarks themselves can be transformed and visualised just like any other ``PointCloud``. If you are unsure about the features of the ``PointCloud`` class, we suggest you check out the notebooks in the `Shape` package!

In the following we present:

1. `LandmarkManager`
2. Automatically Labelling Landmarks
3. Removing Labels
4. Re-assigning landmarks
5. Widgets

Lets begin with the `io` package and demonstrate how easy it is to load images in that are landmarked!

```{code-cell}
%matplotlib inline
import numpy as np
import os
import menpo.io as mio

images = list(mio.import_images(f"{mio.data_dir_path()}/*"))
print('Found {} images'.format(len(images)))

# Grab the first image
img = images[0]

img.view_landmarks();
```

In this case, images have been automatically loaded with some landmark information attached. We can confirm that by accessing the property *.landmarks* on the images.

```{code-cell}
print('Is img landmarked?')
print(' - {}'.format(img.landmarks.has_landmarks))

print('How many landmark groups does it have?')
print(' - {}'.format(img.landmarks.n_groups))
    
print('What labels do these groups have?')
for g in img.landmarks.group_labels:
    print(' - {}'.format(g))
```

## 1. LandmarkManager

+++

Every `Landmarkable` object contains a `LandmarkManager`. The `LandmarkManager` is responsible for maintaining multiple sets of landmarks per object. For example, after running a deformable model alignment the image is returned with both the initial shape *and* the final shape after fitting.

The `LandmarkManager` acts like a smart dictionary for storing landmarks. So Landmarks are stored inside of the manager and accessible by string keys that define a ``group_label`` for the landmark group.

Let's see what it looks like for an image to have two sets of landmarks by simply duplicating the Breaking Bad landmarks.

```{code-cell}
from menpo.transform import Translation
import matplotlib.pyplot as plt

# Grab the landmarks - this syntax will be explained shortly!
landmarks = img.landmarks['PTS']
# Store a new landmark group called 'translated_landmarks'
img.landmarks['translated_landmarks'] = Translation([50, -700]).apply(landmarks)

plt.subplot(121)
img.view_landmarks(group='PTS');
plt.subplot(122)
img.view_landmarks(group='translated_landmarks');
```

The landmarks can also be plotted on the same figure

```{code-cell}
viewer = img.view_landmarks(group='PTS', marker_face_colour='r', marker_edge_colour='k');
img.view_landmarks(group='translated_landmarks', figure_id=viewer.figure_id, marker_face_colour='g', marker_edge_colour='k');
```

The image above clearly shows two seperate sets of landmarks, and the legend shows their relative colours on the right of the image.

As a sanity check, let's check that there are now two group labels on our image!

```{code-cell}
print('What labels do these groups have?')
for g in img.landmarks.group_labels:
    print(' - {}'.format(g))
```

## 2. LandmarkGroup

+++

A ``LandmarkManager`` contains a number of ``Shape``s. These are plain old ``PointCloud`` objects that define the spatial layout of the landmarks. There are also special subclasses of the ``Shape`` class that can can be labelled such that each point has a different semantic meaning (``LabelledPointUndirectedGraph``).

Lets take a square and label the corners by example

```{code-cell}
from menpo.image import Image
from menpo.shape import LabelledPointUndirectedGraph, PointCloud

square_image = Image.init_blank([100, 100])
# You can create an "empty" shape with a default "all" label
square_image.landmarks['square'] = LabelledPointUndirectedGraph.init_with_all_label(
    np.array([[20, 20], [20, 80], [80, 80], [80, 20]]), 
    np.eye(4)  # This identity matrix defines "no connectivity"
)
```

Now, let's label each corner:

```{code-cell}
square_image.landmarks['square'] = (
    square_image.landmarks['square']
    .add_label('bottom_left', [2])
    .add_label('top_left', [0])
    .add_label('bottom_right', [3])
    .add_label('top_right', [1])
)

square_image.view_landmarks(group='square', marker_size=100, render_legend=True);
```

```{code-cell}
print('The semantic labels now are:')
for l in square_image.landmarks['square'].labels:
    print(' - {}'.format(l))
```

There are a couple of things to note here:

  - You access semantic labels using the ``*_label()`` methods on a ``LabelledPointUndirectedGraph`` instance
  - The new semantic labels are defined as lists of indexes into the ``LabelledPointUndirectedGraph`` object. Therefore, each set of semantic labels can have many indexes.
  - The ``LabelledPointUndirectedGraph`` can contain as many sets of semantic labels as needed
  - The semantic labels are prefixed with the group label
  
Since we provide a list of indices, we could define a new set of semantic labels for the points on the left and right seperately!

```{code-cell}
square_image.landmarks['square'] = (
    square_image.landmarks['square']
    .add_label('left', [0, 3])
    .add_label('right', [1, 2])
)

square_image.view_landmarks(group='square', marker_size=100, render_legend=True);
```

The problem is that it is very difficult to see what is going on, since all of the semantic labels are getting rendered on top of each other! In order to get around this, ``LabelledPointUndirectedGraph`` makes it easy to create a new ``LabelledPointUndirectedGraph`` with (or without) a given set of labels.

```{code-cell}
left_right_landmark_group = square_image.landmarks['square'].with_labels(['left', 'right'])

print('Landmark group has the following labels: ')
for g in left_right_landmark_group.labels:
    print('  - ' + g)
    
left_right_landmark_group.view(marker_size=100);
```

Notice that viewing a single landmark group does **not** view the underlying object as well. You must use ``view_landmarks`` to view the underlying object behind the landmarks!

Also, keep in mind that this newly created group is not assigned to the image. If we view the original again, we still see all the labels!

```{code-cell}
square_image.view_landmarks(render_legend=True);
```

As we described before, we can easily set a 'mask' on our underlying PointCloud that defines a semantic labelling. This has nice behaviour because it allows us to single out indices in to our PointCloud that have particular semantic meanings to us. What if we want to access those masked PointClouds though?

```{code-cell}
lmark_group = square_image.landmarks['square']

for semantic_label in lmark_group.labels:
    print('Label is: {}'.format(semantic_label))
    print('  Sub-PointCloud is: {}'.format(lmark_group.get_label(semantic_label)))
```

Notice the different number of points returned for each PointCloud, becase each PointCloud is a *subset* of the original PointCloud!

+++

## 3. Automatically Labelling Landmarks

+++

A semantic meaning can be added to a group of existing landmarks by labelling them with a predefined labelling function. This will effectively create a new landmark group with the appropiate semantic labels. For example, let's label the Breaking Bad image with the semantic annotations [from the IBUG team](http://ibug.doc.ic.ac.uk/resources/facial-point-annotations/).

```{code-cell}
from menpo.landmark import labeller, face_ibug_68_to_face_ibug_68

# Label some landmarks
labeller(img, 'PTS', face_ibug_68_to_face_ibug_68)

print('How many landmark groups does it have have?')
print(' - {}'.format(img.landmarks.n_groups))
    
print('What labels do these groups have?')
for g in img.landmarks:
    print(' - {}'.format(g))

print('ibug_face_68 semantic labels are?')
for l in img.landmarks['face_ibug_68'].labels:
    print(' - {}'.format(l))
```

We can now view the entire group, containing all semantic labels that seperate particular areas such as the eyes, nose, mouth etc

```{code-cell}
# View a particular group
img.landmarks['face_ibug_68'].view();
```

Notice that viewing the landmark group itself directly from the manager does not view the object behind it. Also note that the landmarks are incorrectly rotated because the group does not know that its landmarks are actually within the image domain, where the axes are different. To view a particular group we can use the ``group`` kwarg of the ``view_landmarks`` method as follows:

```{code-cell}
# View a particular group
img.view_landmarks(group='face_ibug_68', render_legend=True);
```

We can also view a particular semantic label, like the nose

```{code-cell}
# View a particular group and label
img.view_landmarks(group='face_ibug_68', with_labels='jaw', render_markers=False, line_width=10, line_colour='r');
```

Or visualize multiple labels

```{code-cell}
img.view_landmarks(group='face_ibug_68', with_labels=['nose', 'jaw'], 
                   render_markers=False, line_width=2, line_colour=['r', [0, 0, 1]], render_legend=True);
```

And of course we can do the inverse, create a group **without** a particular set of landmarks

```{code-cell}
img.view_landmarks(group='face_ibug_68', without_labels=['jaw'], render_legend=True);
```

## 4. Removing Labels

+++

As a short aside, you might not want to delete a specific label. Or, you might want to get rid of the imported 'PTS' label and only keep your newly semantically labelled 'ibug_face_68' group. Fortunately, the ``LandmarkManager`` and ``LandmarkGroup`` can be modified to remove labels too.

```{code-cell}
# Add a 'face' label to the 'face_ibug_68' group
img.landmarks['face_ibug_68'] = img.landmarks['face_ibug_68'].add_label('face', range(68))

print('Breaking Bad (face_ibug_68) has labels:')
for l in img.landmarks['face_ibug_68'].labels:
    print(' - {}'.format(l))
    
# Delete the 'all' label
img.landmarks['face_ibug_68'] = img.landmarks['face_ibug_68'].remove_label('face')

print('Breaking Bad (face_ibug_68) NOW has labels:')
for l in img.landmarks['face_ibug_68'].labels:
    print(' - {}'.format(l))
```

```{code-cell}
# Delete the 'ibug_face_68' group
del img.landmarks['face_ibug_68']

if 'face_ibug_68' not in img.landmarks:
    print("Breaking Bad does not contain the 'face_ibug_68' group")
```

## 5.  Re-assigning landmarks

+++

If you have a set of landmarks on one image, or even if you just have a ``PointCloud`` that you want to set as landmarks, this is equally simple.

```{code-cell}
other_img = images[1]

img.landmarks['someone_elses_landmarks'] = other_img.landmarks['PTS']
img.landmarks['a_pointcloud'] = PointCloud(np.array([[500, 500], [500, 1000], [1000, 500], [1000, 1000]]))

img.view_landmarks(group='someone_elses_landmarks');
img.view_landmarks(new_figure=True, group='a_pointcloud', marker_size=10, marker_face_colour='w', marker_edge_colour='r');
```

## 6. Widget

+++

Landmarks can be very easily visualized using widgets. The image widget has a specific _Landmarks options_ tab that allows to browse through the available landmarks of an `Image`. Note that the _Viewer options_ includes several rendering options. Note that the widget functionality is provided by the menpowidgets project and should be installed separately using conda (`conda install -c conda-forge menpowidgets`).

```{code-cell}
from menpowidgets import view_widget 

view_widget(img)
```

It's also possible to use `view_widget()` directly on a `LandmarkManager`

```{code-cell}
view_widget(img.landmarks)
```

...and of course directly on `PointCloud`s.

```{code-cell}
view_widget(img.landmarks['PTS'])
```

Finally, note that the widgets can visualize a `list` of `LandmarkManager`(s) or `PointCloud`(s) (the same for `list` of `Image`s).

```{code-cell}
from menpowidgets import visualize_landmarks_2d, visualize_shapes_2d

# visualize list of LandmarkManager objects
visualize_landmarks_2d([images[2].landmarks, images[0].landmarks, images[1].landmarks])
```

```{code-cell}
# same can be done for PointCloud objects of course
visualize_shapes_2d([images[2].landmarks['LJSON'], 
                     images[0].landmarks['a_pointcloud'], 
                     images[1].landmarks['PTS']])
```
