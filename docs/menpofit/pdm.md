---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Point Distribution Model

1. <a href="#definition">Definition</a>
2. <a href="#trimming">Trimming components</a>
3. <a href="#synthesis">Generating new instances</a>
4. <a href="#visualization">Visualization</a>
5. <a href="#projection_and_reconstruction">Projection and reconstruction</a>
6. [API documentation](https://menpofit.readthedocs.io/en/stable/api/menpofit/modelinstance/OrthoPDM.html)

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```

<a id="definition"></a>

## 1. Definition
A Point Distribution Model (PDM) is a statistical parametric model of the shape of the deformable object, which is an essential part for many state-of-the-art deformable models.

Let us denote a shape instance of an object with $L$ landmark points as a $2L\times 1$ vector
$$
\mathbf{s}=[x_1, y_1, x_2, y_2, \ldots, x_L, y_L]^T
$$
which consists of the Cartesian coordinates of the points $(x_i, y_i), \forall i=1,\ldots,L$.
Assume that we have a set of $N$ training shapes $\left\lbrace \mathbf{s}^1, \mathbf{s}^2, \ldots, \mathbf{s}^N \right\rbrace$.

With your own data, load the shapes from landmark files with `menpo.io`. Landmark files are imported as a dictionary of
landmark groups (a `.pts` file has the single group `PTS`), so pick the group out of it. This is the usual way
to get a list of shapes:

```python
from pathlib import Path
import menpo.io as mio

training_shapes = [
    mio.import_landmark_file(path, group="PTS")
    for path in Path("/path/to/lfpw/trainset/").glob("*.pts")
]
```

```{tip}
`mio.import_landmark_file(path)` without `group` returns a *dictionary* of groups, not a shape. Passing that
dictionary to a model gives `'dict' object has no attribute 'centre'`.
```

So that this page can run without a dataset, we instead generate 40 random deformations of the built-in Einstein shape:

```{code-cell} ipython3
import numpy as np
import menpo.io as mio
from menpo.shape import PointCloud

base = mio.import_builtin_asset.einstein_pts()["PTS"]

rng = np.random.RandomState(0)
training_shapes = [
    PointCloud(base.points + rng.randn(*base.points.shape) * 3.0) for _ in range(40)
]
len(training_shapes), training_shapes[0].n_points
```

You can look at the shapes with the interactive widget (in a notebook):

```python
from menpowidgets import visualize_shapes_2d
visualize_shapes_2d(training_shapes)
```

The construction of a PDM commonly involves the following steps:
  1. Align the set of training shapes using Generalized Procrustes Analysis, which will remove the similarity transform components (scaling, in-plane rotation, translation) from the shapes.
  2. Apply Principal Component Analysis (PCA) on the aligned shapes. This involves first centering the aligned shapes by subtracting the mean shape $\bar{\mathbf{s}}$ and then computing the basis of eigenvectors $\mathbf{U}_s\in\mathbb{R}^{2L\times N-1}$.
  3. Further augment the acquired subspace with four eigenvectors that control the global similarity transform of the object, re-orthonormalize [<a href="#1">1</a>] and keep the first $n$ eigenvectors. This results to a linear shape model of the form
$$
  \left\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\right\rbrace
$$
  where $\mathbf{U}_s\in\mathbb{R}^{2L\times n}$ is an orthonormal basis of $n$ eigenvectors and $\bar{\mathbf{s}}$ is the mean shape vector.

The above procedure is performed by `menpofit`'s `OrthoPDM` class:

```{code-cell} ipython3
from menpofit.modelinstance import OrthoPDM

shape_model = OrthoPDM(training_shapes, max_n_components=None)
print(shape_model)
```

<a id="trimming"></a>

## 2. Trimming components
The model above keeps every component. When using it for projection or reconstruction, the whole subspace is used,
including the last components, which mostly capture noise. To remove them, **trim** the model. `trim_components` returns
a new, smaller model and leaves the original unchanged; the arrays of the new model are read-only views, so it costs
no memory. Give either the number of PCA components to keep:

```{code-cell} ipython3
small_model = shape_model.trim_components(10)
print(small_model)
```

or the proportion of variance to keep:

```{code-cell} ipython3
print(shape_model.trim_components(0.95))
```

The original is not modified, so you can derive several models from one:

```{code-cell} ipython3
shape_model.n_components, small_model.n_components
```

To trim a model in place instead, use `trim_components_inplace(n)`. It rebinds the model's arrays to the trimmed views, and,
like every `*_inplace` method in menpo, never writes into the existing arrays (so models that share them are not affected).

```{admonition} Upgrading from menpo 0.12
:class: warning
`n_active_components` has been removed, and with it assigning to it (`model.n_active_components = 20`), the `components`
setter and `increment()`. Replace `model.n_active_components = n` with `model = model.trim_components(n)`, or
`model.trim_components_inplace(n)` to keep modifying the same object. `trim_components(n)` used to trim in place; it now
returns the trimmed model, so code that ignores the return value no longer changes anything.
```

<a id="synthesis"></a>

## 3. Generating new instances
A new shape instance can be generated as
$$
\mathbf{s} = \bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}
$$
where $\mathbf{p}=[p_1, p_2, \ldots, p_n]^T$ is the shape parameters vector.

You can generate a new shape instance using only the similarity model (which will
naturally apply a similarity transform on the mean shape) as

```{code-cell} ipython3
instance = small_model.similarity_model.instance([100.0, -300.0, 0.0, 0.0])
instance.view(render_axes=False);
```

Similarly, a new instance using only the PCA components can be generated as

```{code-cell} ipython3
instance = small_model.model.instance([2.0, -2.0, 2.0, 1.5], normalized_weights=True)
instance.view(render_axes=False);
```

Note that in this case, the weights that are provided are normalized with respect to the corresponding eigenvalues.

A combined instance using all the components can be generated with `from_vector`:

```{code-cell} ipython3
params = [100.0, -300.0, 0.0, 0.0, 140.0, -100.0, 15.0, 5.0] + [0.0] * (small_model.n_parameters - 8)
small_model.from_vector(params).target.view(render_axes=False);
```

<a id="visualization"></a>

## 4. Visualization
The PCA components of the `OrthoPDM` can be explored with an interactive widget in a notebook:

```python
from menpowidgets import visualize_shape_model_2d
visualize_shape_model_2d(small_model.model)
```

<a id="projection_and_reconstruction"></a>

## 5. Projection and reconstruction
A shape instance $\mathbf{s}$ can be theoretically projected into a given shape model $\left\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\right\rbrace$ as
$$
\mathbf{p} = {\mathbf{U}_s}^T (\mathbf{s} - \bar{\mathbf{s}})
$$
Similarly, the reconstruction $\hat{\mathbf{s}}$ of a shape instance is done as:
$$
\hat{\mathbf{s}} \approx \bar{\mathbf{s}} + \mathbf{U}_s{\mathbf{U}_s}^T (\mathbf{s} - \bar{\mathbf{s}})
$$

`OrthoPDM` makes it very easy to reconstruct a shape instance by setting its `target`.
Let's reconstruct a new shape using the similarity and PCA components, and visualize the result:

```{code-cell} ipython3
import matplotlib.pyplot as plt

# a shape that was not in the training set
shape = PointCloud(base.points + np.random.RandomState(1).randn(*base.points.shape) * 3.0)
small_model.set_target(shape)

plt.subplot(121)
shape.view(render_axes=False)
plt.gca().set_title("Original shape")
plt.subplot(122)
small_model.target.view(render_axes=False)
plt.gca().set_title("Reconstructed shape");
```

The procedure that is applied inside `set_target()` involves the following steps:

```{code-cell} ipython3
from menpo.transform import AlignmentAffine

# Find the affine transform that normalizes the shape with respect to the mean shape
transform = AlignmentAffine(shape, small_model.model.mean())

# Normalize the shape and project it
normalized_shape = transform.apply(shape)
weights = small_model.model.project(normalized_shape)
print("Weights:", np.round(weights, 2))

# Reconstruct the normalized shape and apply the pseudoinverse of the affine transform
reconstructed_normalized_shape = small_model.model.instance(weights)
reconstructed_shape = transform.pseudoinverse().apply(reconstructed_normalized_shape)

plt.subplot(121)
shape.view(render_axes=False)
plt.gca().set_title("Original shape")
plt.subplot(122)
reconstructed_shape.view(render_axes=False)
plt.gca().set_title("Reconstructed shape");
```

<a id="1"></a>

## References
[1] J. Alabort-i-Medina, and S. Zafeiriou. "A Unified Framework for Compositional Fitting of Active Appearance Models", arXiv:1601.00199.
