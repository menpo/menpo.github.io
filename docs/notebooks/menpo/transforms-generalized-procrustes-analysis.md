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

# Generalized Procrustes Analysis
Generalized Procrustes Analysis is an iterative technique for optimally rigidly aligning a set of shapes. The contents of this notebook are:

1. Simple example
2. Example with faces

First, let's import everything we need.

```{code-cell}
%matplotlib inline
from pathlib import Path

from menpo.transform import GeneralizedProcrustesAnalysis
from menpo.shape import PointCloud

import numpy as np
import matplotlib.pyplot as plt
```

## 1. Simple example

+++

Let's make three `PointCloud` instances

```{code-cell}
src_1 = PointCloud(np.array([[-1.0, -1.0],
                             [1.0, -1.0],
                             [1.0, 1.0],
                             [-1.0, 1.0]]))

src_2 = PointCloud(np.array([[0.0, 0.0],
                             [1.5, 0.1],
                             [1.5, 1.5],
                             [0.1, 1.5]]))

src_3 = PointCloud(np.array([[-2.0, 0.0],
                             [0.0, 3.0],
                             [2.0, 0.0],
                             [0.0, -3.0]]))
```

```{code-cell}
viewer = src_1.view(marker_face_colour='r', marker_size=80);
src_2.view(figure_id=viewer.figure_id, marker_face_colour='g', marker_size=80);
src_3.view(figure_id=viewer.figure_id, marker_face_colour='b', marker_size=80);
plt.legend(['src_1', 'src_2', 'src_3']);
```

`GeneralizedProcrustesAnalysis` accepts a list of `Shape` instances upon construction. This causes it to run it's iterative alignment process.

```{code-cell}
gpa = GeneralizedProcrustesAnalysis([src_1, src_2, src_3])
```

Printing the object gives you a summary of what happened

```{code-cell}
print(gpa)
```

GeneralizedProcrustesAnalysis provides a property called `.transforms`, which gives one transform per source that aligns it to the target frame. The target frame is also accessable at `.target`

```{code-cell}
print('There are {} transforms'.format(len(gpa.transforms)))
print('Each transform is a {}'.format(type(gpa.transforms[0])))
print('The target: {}'.format(gpa.target))
```

The optimal transform found to align `src_1` is:

```{code-cell}
src_1_similarity = gpa.transforms[0]
print(src_1_similarity)
```

and for `src_2` we used:

```{code-cell}
src_2_similarity = gpa.transforms[1]
print(src_2_similarity)
```

`src_1_similarity` has a `source` which is the same as `src_1`:

```{code-cell}
print(src_1_similarity.source)
print(np.all(src_1 == src_1_similarity.source))
```

The target of this object was set in the first iteration of the algorithm to the mean of all the sources:

```{code-cell}
print(src_1_similarity.target)
```

Its simple to check how the alignment did

```{code-cell}
colours_list = ['r' ,'g', 'b']
for i, (t, a_c) in enumerate(zip(gpa.transforms, gpa.sources)):
    aligned_src = t.apply(a_c)
    aligned_src.view(marker_face_colour=colours_list[i], marker_size=10);
plt.legend(['src_1', 'src_2', 'src_3']);
```

## 2. Example with faces

+++

In this example, we will use one of the most popular and widely used annotated facial databases, the Labeled Faces Parts in the Wild (LFPW) database. Both images and corresponding facial landmark annotations are publicly available and can be downloaded from the following link: 

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

Let's load the shapes

```{code-cell}
import menpo.io as mio
shapes = [s['PTS'] for s in mio.import_landmark_files(path_to_lfpw / 'trainset' / '*.pts', verbose=True)]
```

We can visualize them using the `visualize_pointclouds` widget.

```{code-cell}
from menpowidgets import visualize_shapes_2d

visualize_shapes_2d(shapes)
```

It is very easy to align the shapes

```{code-cell}
from menpo.transform import Translation

# centralize shapes
centered_shapes = [Translation(-s.centre()).apply(s) for s in shapes]

# align centralized shape using Procrustes Analysis
gpa = GeneralizedProcrustesAnalysis(centered_shapes)

print(gpa)

# get the aligned shapes
aligned_shapes = [s.aligned_source() for s in gpa.transforms]
```

Let's see the result!

```{code-cell}
n_shapes = 101

plt.subplot(121)
plt.title('Before GPA')
for s in shapes[:n_shapes]:
    s.view(axes_x_limits=10, axes_y_limits=10)
    
plt.subplot(122)
plt.title('After GPA')
for s in aligned_shapes[:n_shapes]:
    s.view()
```
