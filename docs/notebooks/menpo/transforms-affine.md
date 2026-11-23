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

# Affine Transforms
Menpo supports the full family of affine 2D and 3D transformations. These operations are simply defined as the operations that preserve straight lines. The affine transformation family is a subclass of the homogenous family that does not allow operations like perspective projection. In this notebook, we will focus on commonly used affine transformations such as translations, scales and rotations.

It's important to note that these transformations will work on both ``PointCloud`` and it's subclasses and ``Image``s (through the use of the ``warp_`` methods). To start with, let's make a few objects to play around with.

```{code-cell}
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from menpo.shape import PointCloud
from menpo.image import Image

# A unit square centered at (0.5, 0.5)
points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
plt.plot(points[:, 0], points[:, 1], 'bo')

# A PointCloud containing a copy of the unit square
pcloud = PointCloud(points)
pcloud.view(new_figure=True)

# A small black image
image = Image.init_blank([100, 100], fill=1)
image.view(new_figure=True);
```

## Translations
The ``Translation`` class is a very simple type of affine transformation that merely translates the given object within its space.

### Applying to ``Shape``s
Let's try applying a ``Translation`` to a ``PointCloud``

```{code-cell}
%matplotlib inline
from menpo.transform import Translation

small_2d_translation = Translation([-5, 5])

translated_pcloud = small_2d_translation.apply(pcloud)
# Notice it is now centered around (-4.5, 5.5)
translated_pcloud.view();
```

#### Applying to ``Image`` instances
Let's try applying a ``Translation`` to an ``Image``.

```{code-cell}
%matplotlib inline
from menpo.image import BooleanImage

small_2d_translation = Translation([-50, 50])

translated_image = image.warp_to_mask(BooleanImage.init_blank([100, 100]), small_2d_translation)
# Notice it is now centered around (-4.5, 5.5)
translated_image.view();
```
