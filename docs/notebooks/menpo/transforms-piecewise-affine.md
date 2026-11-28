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

# Piecewise Affine Transforms

```{code-cell}
import numpy as np
from menpo.transform import PiecewiseAffine
```

We build a `PiecewiseAffine` by supplying two sets of points and a shared triangle list

```{code-cell}
from menpo.shape import TriMesh, PointCloud
a = np.array([[0, 0], [1, 0], [0, 1], [1, 1],
              [-0.5, -0.7], [0.8, -0.4], [0.9, -2.1]])
b = np.array([[0,0], [2, 0], [-1, 3], [2, 6],
              [-1.0, -0.01], [1.0, -0.4], [0.8, -1.6]])
tl = np.array([[0,2,1], [1,3,2]])

src = TriMesh(a, tl)
src_points = PointCloud(a)
tgt = PointCloud(b)

pwa = PiecewiseAffine(src_points, tgt)
```

Lets make a random 5000 point `PointCloud` in the unit square and view it 

```{code-cell}
%matplotlib inline
# points_s = PointCloud(np.random.rand(10000).reshape([-1,2]))
points_f = PointCloud(np.random.rand(10000).reshape([-1,2]))
points_f.view()
```

Now lets see the effect having warped

```{code-cell}
t_points_f = pwa.apply(points_f);
t_points_f.view()
```

```{code-cell}
test = np.array([[0.1,0.1], [0.7, 0.9], 
                 [0.2,0.3], [0.5, 0.6]])
```

```{code-cell}
pwa.index_alpha_beta(test)
```
