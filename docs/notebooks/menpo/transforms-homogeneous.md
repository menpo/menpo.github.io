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

# Homogeneous Transforms

```{code-cell}
import numpy as np

from menpo.shape import PointCloud
from menpo.transform import Homogeneous
```

If you know the form of a basic homogeneous transform (like here a mirror along y=x) it's trivial to build a `Homogeneous` to use this operation in Menpo

```{code-cell}
# mirror along y=x
xy_yx = Homogeneous(np.array([[0, 1, 0], 
                              [1, 0, 0], 
                              [0, 0, 1]]))
```

```{code-cell}
s = np.linspace(0, 1)
len(s)
p = np.ones([len(s), 2])
p[:, 1] = s
pc = PointCloud(p)
print(pc)
```

```{code-cell}
%matplotlib inline
pc.view(axes_y_limits=(0.5, 1.5));
```

Let's take a look at what our homogeneous transform is exactly

```{code-cell}
print(xy_yx)
```

Applying this Transform to a `PointCloud` has the desired effect

```{code-cell}
pc_flipped = xy_yx.apply(pc)
```

```{code-cell}
pc_flipped.view(axes_x_limits=(0.5, 1.5));
```

Homogeneous transforms support native composition

```{code-cell}
no_op = xy_yx.compose_before(xy_yx)
print(no_op)
```

```{code-cell}
no_op = xy_yx.compose_after(xy_yx)
print(no_op)
```

```{code-cell}
xy_yx.compose_before_inplace(xy_yx)
print(xy_yx)
```
