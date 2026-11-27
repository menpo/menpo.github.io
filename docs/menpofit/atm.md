---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Active Template Model

1. <a href="#definition">Definition</a>
2. <a href="#warp">Warp Functions</a>
3. <a href="#cost">Cost Function and Optimization</a>
4. <a href="#references">References</a>
5. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/atm/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```

<a id="definition"></a>

# 1. Definition
The aim of deformable image alignment is to find the optimal alignment between a constant template and an input image with respect to the parameters of a parametric shape model.
Active Template Model (ATM) is such method which is inspired by the [Lucas-Kanade Affine Image Alignment](lk.md "Lucas-Kanade Affine Image Alignment") and the [Active Appearance Model](aam.md "Active Appearance Model"). Note that we invented the name "Active Template Model" for the purpose of the Menpo Project. The term is not established in literature. In this page, we provide a basic mathematical definition of an ATM and all its variations that are implemented within `menpofit`.

A shape instance of a deformable object is represented as $\mathbf{s}=\big[x_1,y_1,\ldots,x_L,y_L\big]^{\mathsf{T}}$, a $2L\times 1$ vector consisting of $L$ landmark points coordinates $(x_i,y_i),\forall i=1,\ldots,L$. An ATM is constructed using a template image that is annotated with $L$ landmark points and a set of $N$ shapes $\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$ that are essential for building the shape model. Specifically, it consists of the following parts:

* **Shape Model**  
  The shape model is trained as explained in the [Point Distributon Model section](pdm.md "Point Distribution Model basics"). The training shapes $\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$ are first aligned using Generalized Procrustes Analysis and then an orthonormal basis is created using Principal Component Analysis (PCA) which is further augmented with four eigenvectors that represent the similarity transform (scaling, in-plane rotation and translation). This results in
$$
  \big\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\big\rbrace
$$
  where $\mathbf{U}_s\in\mathbb{R}^{2L\times n}$ is the orthonormal basis of $n$ eigenvectors (including the four similarity components) and $\bar{\mathbf{s}}\in\mathbb{R}^{2L\times 1}$ is the mean shape vector. An new shape instance can be generated as $\mathbf{s}_{\mathbf{p}}=\bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}$, where $\mathbf{p}=\big[p_1,p_2,\ldots,p_n\big]^{\mathsf{T}}$ is the vector of shape parameters.

* **Motion Model**  
  The motion model consists of a warp function $\mathcal{W}(\mathbf{p})$ which is essential for warping the texture related to a shape instance generated with parameters $\mathbf{p}$ into a common `reference_shape`. The `reference_shape` is by default the mean shape $\bar{\mathbf{s}}$, however you can pass in a `reference_shape` of your preference during construction of the ATM.

* **Template**  
  The provided template image $\mathbf{I}_a$ which is annotated with landmarks $\mathbf{s}_a$ is further processed by:
  1. First extracting features using the features function $\mathcal{F}()$ defined by `holistic_features`, i.e. $\mathcal{F}(\mathbf{I}_a)$
  2. Warping the feature-based image into the `reference_shape` in order to get $\mathcal{F}(\mathbf{I}_a)(\mathcal{W}(\mathbf{p}_a))$
  3. Vectorizing the warped image as $\bar{\mathbf{a}} = \mathcal{F}(\mathbf{I}_a)(\mathcal{W}(\mathbf{p}_a))$ where $\bar{\mathbf{a}}\in\mathbb{R}^{M\times 1}$

Let's first load a test image and a template image $\bar{\mathbf{a}}$. We'll load two annotated faces (see [Importing Images](importing.md "Basics on how to import images") for how to get a dataset): the image that the model will be fitted to, and the template.
An ATM has no appearance model, so it can only find what *looks like its template*: the same person, in similar conditions. The template normally comes from another image of the subject (for example the previous frame of a video).
To keep this example self-contained, we take the template from the image itself, as the [Lucas-Kanade](lk.md) example does; the fit then shows how well the shape model and the optimisation work, not how well a template transfers to another face.
```{code-cell} ipython3
:tags: [remove-input]

from menpo_docs_data import faces_directory

path_to_images = faces_directory()
```

```{code-cell} ipython3
from pathlib import Path
import menpo.io as mio

# the same preprocessing as in the Importing Images section
image = mio.import_image(sorted(Path(path_to_images).glob('*.png'))[0])
image = image.crop_to_landmarks_proportion(0.5)

template = image.copy()
```

The image and template can be visualized as:
```{code-cell} ipython3
import matplotlib.pyplot as plt

plt.subplot(121)
image.view()
plt.gca().set_title('Input Image')

plt.subplot(122)
template.view_landmarks(marker_face_colour='white', marker_edge_colour='black',
                        marker_size=4)
plt.gca().set_title('Template');
```
Let's also load the shapes of LFPW trainset that will be used in order to train the PDM:
```{code-cell} ipython3
from menpo.visualize import print_progress

training_shapes = []
for path in print_progress(sorted(Path(path_to_images).glob('*.pts'))):
    training_shapes.append(mio.import_landmark_file(path, group='PTS'))
```

The shapes can be visualized using a widget as:
```python
from menpowidgets import visualize_shapes_2d
visualize_shapes_2d(training_shapes)
```

<a id="warp"></a>

## 2. Warp Functions
With an abuse of notation, let us define
$$
\mathbf{t}(\mathcal{W}(\mathbf{p}))\equiv \mathcal{F}(\mathbf{I})(\mathcal{W}(\mathbf{p}))
$$
as the feature-based warped $M\times 1$ vector of an image $\mathbf{I}$ given its shape instance generated with parameters $\mathbf{p}$.

`menpofit` provides five different ATM versions, which differ on the way that this appearance warping $\mathbf{t}(\mathcal{W}(\mathbf{p}))$ is performed.
Specifically:

**HolisticATM**  
The `HolisticATM` uses a holistic appearance representation obtained by warping the texture into the reference frame
with a non-linear warp function $\mathcal{W}(\mathbf{p})$. Two such warp functions are currently supported:
Piecewise Affine Warp and Thin Plate Spline. The reference frame is the mask of the mean shape's convex hull.

**MaskedATM**  
The `MaskedATM` uses the same warp logic as the `HolisticATM`. The only difference between them is that the
reference frame consists of rectangular mask patches centered around the landmarks instead of the convex hull of the mean shape.

**LinearATM**  
The `LinearATM` is an experimental variation that utilizes a linear warp function $\mathcal{W}(\mathbf{p})$ in the motion model, thus a _dense_ statistical shape model which has one shape point per pixel in the reference frame. The advantage is that the linear nature of such warp function makes the computation of its Jacobian trivial.

**LinearMaskedATM**  
Similar to the relation between `HolisticATM` and `MaskedATM`, a `LinearMaskedATM` is exactly the same with a
`LinearATM`, with the difference that the reference frame is masked.

**PatchATM**  
A `PatchATM` represents the appearance in a patch-based fashion, i.e. rectangular patches are extracted around the landmark points.
Thus, the warp function $\mathbf{t}(\mathcal{W}(\mathbf{p}))$ simply _samples_ the patches centered around the landmarks of the shape instance generated with parameters $\mathbf{p}$.

Let's now create a `HolisticATM` using Dense SIFT features:
```{code-cell} ipython3
from menpofit.atm import HolisticATM
from menpo.feature import fast_dsift

atm = HolisticATM(template, training_shapes, group='PTS',
                  diagonal=180, scales=(0.25, 1.0),
                  holistic_features=fast_dsift, verbose=True)
```
and visualize it:
```python
from menpowidgets import visualize_shape_model_2d
visualize_shape_model_2d([sm.model for sm in atm.shape_models])
```
```python
from menpowidgets import visualize_atm
visualize_atm(atm)
```

<a id="cost"></a>

### 3. Cost Function and Optimization
Fitting an ATM on a test image involves the optimization of the following cost function
$$
\arg\min_{\mathbf{p}} \big\lVert \mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}} \big\rVert^{2}
$$
with respect to the shape parameters. Note that this cost function is exactly the same as in the case of [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") for Affine Image Alignment. The only difference has to do with the nature of the transform - and thus $\mathbf{p}$ - that is used in the motion model $\mathcal{W}(\mathbf{p})$. Similarly, the cost function is very similar to the one of an [Active Appearance Model](aam.md "Active Appearance Model (AAM)") with the difference that an ATM has no appearance subspace.

The optimization of the ATM deformable image alignment is performed with the Lucas-Kanade gradient descent algorithm.
This is the same as in the case of affine image transform, so you can refer to the [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") chapter
for more information. We currently support Inverse-Compositional and Forward-Compositional optimization.

Let's now create a `Fitter` using the ATM we created, as:
```{code-cell} ipython3
from menpofit.atm import LucasKanadeATMFitter, InverseCompositional

fitter = LucasKanadeATMFitter(atm,
                              lk_algorithm_cls=InverseCompositional, n_shape=[5, 15])
```

Information about the fitter can be retrieved as:
```{code-cell} ipython3
:tags: [remove-output, record-fitter]
print(fitter)
```

```{recorded-output} fitter
```

Let's now fit the ATM on the `image` we loaded in the beginning.
We will use the OpenCV face detector from [`menpodetect`](../menpodetect/index.md), in order to acquire an initial bounding box, as:
```{code-cell} ipython3
from menpodetect import load_opencv_frontal_face_detector

# Load detector
detect = load_opencv_frontal_face_detector()

# Detect
bboxes = detect(image)
print("{} detected faces.".format(len(bboxes)))

# View
if len(bboxes) > 0:
    image.view_landmarks(group='opencv_0', line_colour='white',
                         render_markers=False, line_width=3);
```
and fit the ATM. An ATM has no appearance model to guide it, so it needs a start that is close to the object: compare the box of the detector (loose) with the ground truth moved by 4% of the face size (what you have when you track an object from one frame to the next):
```{code-cell} ipython3
:tags: [remove-output, record-fit]
import numpy as np

gt_shape = image.landmarks['PTS']

# from the box of the detector
from_box = fitter.fit_from_bb(image, bboxes[0], max_iters=60, gt_shape=gt_shape)
print("from the detector's box:  {:.4f} -> {:.4f}".format(from_box.initial_error(), from_box.final_error()))

# from the ground truth, moved by 4% of the face size
span = np.ptp(gt_shape.points, axis=0).max()
offset = np.random.RandomState(0).randn(2) * 0.04 * span
initial_shape = gt_shape.from_vector(gt_shape.as_vector() + np.tile(offset, gt_shape.n_points))
result = fitter.fit_from_shape(image, initial_shape, max_iters=20, gt_shape=gt_shape)
print("from the shifted shape:   {:.4f} -> {:.4f}".format(result.initial_error(), result.final_error()))
```

```{recorded-output} fit
```

The result can be visualized as:
```{code-cell} ipython3
:tags: [remove-output, record-view]
result.view(render_initial_shape=True);
```

```{recorded-output} view
```
or using a widget as:
```python
from menpowidgets import visualize_fitting_results
visualize_fitting_results(result)
```
Remember that the shape per iteration can be retrieved as
```{code-cell} ipython3
len(result.shapes)
```

Similarly, the shape parameters per iteration can be obtained as (an ATM has a fixed template, so there are no appearance parameters):
```{code-cell} ipython3
print(len(result.shape_parameters), result.shape_parameters[0].shape)
```


<a id="references"></a>

### 4. References
<p id="1">[1] I. Matthews, and S. Baker. "Active Appearance Models Revisited", International Journal of Computer Vision, vol. 60, no. 2, pp. 135-164, 2004.</p>
