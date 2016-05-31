Point Distribution Model
========================

1. [Definition](#definition)
2. [Active components](#active)
3. [Generating new instances](#synthesis)
4. [Visualization](#visualization)
5. [Projection and reconstruction](#projection_and_reconstruction)
6. [Deformable objects](#objects)

---------------------------------------

<div style="background-color: #F2DEDE; width: 100%; border: 1px solid #A52A2A; padding: 1%;">
<p style="float: left;"><i class="fa fa-exclamation-circle" aria-hidden="true" style="font-size:4em; padding-right: 20%; padding-bottom: 20%; padding-top: 20%;"></i></p>
We highly recommend that you render all matplotlib figures <b>inline</b> the Jupyter notebook for the best `menpowidgets` experience.
This can be done by running</br>
<center><code>%matplotlib inline</code></center>
in a cell. Note that you only have to run it once and not in every rendering cell.
</div>


### <a name="definition"></a>1. Definition
A Point Distribution Model (PDM) is a statistical parametric model of the shape of the deformable obect, which is an essential part for many state-of-the-art deformable models.

Let us denote a shape instance of an object with $$L$$ landmark points as a $$2L\times 1$$ vector
$$
\mathbf{s}=[x_1, y_1, x_2, y_2, \ldots, x_L, y_L]^T
$$
which consists of the Cartesian coordinates of the points $$(x_i, y_i), \forall i=1,\ldots,L$$.
Assume that we have a set of $$N$$ training shapes $$\left\lbrace \mathbf{s}^1, \mathbf{s}^2, \ldots, \mathbf{s}^N \right\rbrace$$.
For this demonstration, we will load all the shapes of LFPW trainset:
```python
from pathlib import Path
import menpo.io as mio
from menpo.visualize import print_progress

path_to_lfpw = Path('/path/to/lfpw/trainset/')

training_shapes = []
for lg in print_progress(mio.import_landmark_files(path_to_lfpw / '*.pts', verbose=True)):
    training_shapes.append(lg['all'])
```
and visualize them as:
```python
%matplotlib inline
from menpowidgets import visualize_pointclouds

visualize_pointclouds(training_shapes)
```
<video width="100%" autoplay loop>
  <source src="visualize_pointclouds.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

The construction of a PDM commonly involves the following steps:
  1. Align the set of training shapes using Generalized Procrustes Analysis, which will remove the similarity transform components (scaling, in-plane rotation, translation) from the shapes.
  2. Apply Principal Component Analysis (PCA) on the aligned shapes. This involves first centering the aligned shapes by subtracting the mean shape $$\bar{\mathbf{s}}$$ and then computing the basis of eigenvectors $$\mathbf{U}_s\in\mathbb{R}^{2L\times N-1}$$.
  3. Further augment the acquired subspace with four eigenvectors that control the global similarity transform of the object, re-orthonormalize [[1](#1)] and keep the first $$n$$ eigenvectors. This results to a linear shape model of the form
  $$
  \left\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\right\rbrace
  $$
  where $$\mathbf{U}_s\in\mathbb{R}^{2L\times n}$$ is an orthonormal basis of $$n$$ eigenvectors and $$\bar{\mathbf{s}}$$ is the mean shape vector.

The above procedure can be very easily performed using `menpofit`'s `OrthoPDM` class as:
```python
from menpofit.modelinstance import OrthoPDM

shape_model = OrthoPDM(training_shapes, max_n_components=None)
```
Information about the PCA model that exists in the PDM can be retrieved as:
```python
print(shape_model)
```
which prints:
```
Point Distribution Model with Similarity Transform
 - total # components:      136
 - # similarity components: 4
 - # PCA components:        132
 - # active components:     4 + 132 = 136
 - centred:                 True
 - # features:              136
 - kept variance:           7.6e+03  100.0%
 - noise variance:          0.025  0.0%
 - components shape:        (132, 136)
```

### <a name="active"></a>2. Active Components
Note that in the previous printing message all the available components are active.
This means that when using the model for any kind of operations such as projection or reconstruction,
then the whole subspace will be used. Normally, you need to use less components in order to remove
the noise that is captured by the last components. This can be done by setting the
number of active components either by explicitly defining the desired number as
```python
shape_model.n_active_components = 20
```
or by providing the percentage of variance to be kept as
```python
shape_model.n_active_components = 0.95
```
Let's print again the `OrthoPDM` object
```python
print(shape_model)
```
which would now return
```
Point Distribution Model with Similarity Transform
 - total # components:      136
 - # similarity components: 4
 - # PCA components:        132
 - # active components:     4 + 16 = 20
 - centred:                 True
 - # features:              136
 - kept variance:           7.3e+03  95.2%
 - noise variance:          3.1  0.0%
 - components shape:        (16, 136)
```

### <a name="synthesis"></a>3. Generating New Instances
A new shape instance can be generated as
$$
\mathbf{s} = \bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}
$$
where $$\mathbf{p}=[p_1, p_2, \ldots, p_n]^T$$ is the shape parameters vector.

You can generate a new shape instance using only the similarity model (which will
naturally apply a similarity transform on the mean shape) as
```python
instance = shape_model.similarity_model.instance([100., -300., 0., 0.])
instance.view(render_axes=False);
```
<center>
  <img src="instance_similarity.png" alt="instance_similarity" style="width: 40%">
</center>

Similarly, a new instance using only the PCA components can be generated as
```python
instance = shape_model.model.instance([2., -2., 2., 1.5], normalized_weights=True)
instance.view(render_axes=False);
```
<center>
  <img src="instance_pca.png" alt="instance_pca" style="width: 40%">
</center>

Note that in this case, the weights that are provided are normalized with respect to the corresponding eigenvalues.


A combined instance using all the components can be generated by using the `from_vector_inplace()` method as
```python
params = [100., -300., 0., 0., 140., -100., 15., 5.]
shape_model.from_vector(params).target.view(render_axes=False);
```
which returns the following instance
<center>
  <img src="instance.png" alt="instance" style="width: 40%">
</center>


### <a name="visualization"></a>4. Visualization
The PCA components of the `OrthoPDM` can be explored using an interactive widget as:
```python
from menpowidgets import visualize_shape_model
visualize_shape_model(shape_model.model)
```
<video width="100%" autoplay loop>
  <source src="../basics/view_shape_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="projection_and_reconstruction"></a>5. Projection and Reconstruction
A shape instance $$\mathbf{s}$$ can be theoretically projected into a given shape model $$\left\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\right\rbrace$$ as
$$
\mathbf{p} = {\mathbf{U}_s}^T (\mathbf{s} - \bar{\mathbf{s}})
$$
Similarly, the reconstruction $$\hat{\mathbf{s}}$$ of a shape instance is done as:
$$
\hat{\mathbf{s}} \approx \bar{\mathbf{s}} + \mathbf{U}_s{\mathbf{U}_s}^T (\mathbf{s} - \bar{\mathbf{s}})
$$

`OrthoPDM` makes it very easy to reconstruct a shape isntance by setting its `target`.
Let's load Einstein's shape, reconstruct it
using the active components (similarity and PCA) and visualize the result:
```python
import matplotlib.pyplot as plt

# Import shape and reconstruct
shape = mio.import_builtin_asset.einstein_pts().lms
shape_model.set_target(shape)

# Visualize
plt.subplot(121)
shape.view(render_axes=False, axes_x_limits=0.05, axes_y_limits=0.05)
plt.gca().set_title('Original shape')
plt.subplot(122)
shape_model.target.view(render_axes=False, axes_x_limits=0.05, axes_y_limits=0.05)
plt.gca().set_title('Reconstructed shape');
```
<center>
  <img src="reconstruction.png" alt="reconstruction">
</center>

The procedure that is applied inside `set_target()` involves the following steps:
```python
import matplotlib.pyplot as plt
from menpo.transform import AlignmentAffine

# Import shape
shape = mio.import_builtin_asset.einstein_pts().lms

# Find the affine transform that normalizes the shape
# with respect to the mean shape
transform = AlignmentAffine(shape, shape_model.model.mean())

# Normalize shape and project it
normalized_shape = transform.apply(shape)
weights = shape_model.model.project(normalized_shape)
print("Weights: {}".format(weights))

# Reconstruct the normalized shape
reconstructed_normalized_shape = shape_model.model.instance(weights)

# Apply the pseudoinverse of the affine tansform
reconstructed_shape = transform.pseudoinverse().apply(reconstructed_normalized_shape)

# Visualize
plt.subplot(121)
shape.view(render_axes=False, axes_x_limits=0.05, axes_y_limits=0.05)
plt.gca().set_title('Original shape')
plt.subplot(122)
reconstructed_shape.view(render_axes=False, axes_x_limits=0.05, axes_y_limits=0.05)
plt.gca().set_title('Reconstructed shape');
```


### <a name="objects"></a>6. Deformable Objects
Of course the example of this page was based on the human face for demonstration purposes.
The Menpo Project is _not_ specific to the human face and can be used for any kind of deformable object.
As an example, here are indicative parametric shape models for various deformable objects, such as
the human body (skeleton), human hand, cat face and car sideview.
<center>
  <img src="body_model.gif" alt="body_model" style="width:19%;">
  <img src="hand_model.gif" alt="hand_model" style="width:24%;">
  <img src="cat_model.gif" alt="cat_model" style="width:24%;">
  <img src="car_model.gif" alt="car_model" style="width:26%;">
</center>
