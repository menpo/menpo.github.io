Active Template Model
=====================

1. [Definition](#definition)
2. [Warp Functions](#warp)
3. [Cost Function and Optimization](#cost)
4. [References](#references)
5. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/atm/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

### <a name="definition"></a>1. Definition
The aim of deformable image alignment is to find the optimal alignment between a constant template and an input image with rspect to the parameters of a parametric shape model.
Active Template Model (ATM) is such method which is inspired by the [Lucas-Kanade Affine Image Alignment](lk.md "Lucas-Kanade Affine Image Alignment") and the [Active Appearance Model](aam.md "Active Appearance Model"). Note that we invented the name "Active Template Model" for the purpose of the Menpo Project. The term is not established in literature. In this page, we provide a basic mathematical definition of an ATM and all its variations that are implemented within `menpofit`.

A shape instance of a deformable object is represented as $$\mathbf{s}=\big[x_1,y_1,\ldots,x_L,y_L\big]^{\mathsf{T}}$$, a $$2L\times 1$$ vector consisting of $$L$$ landmark points coordinates $$(x_i,y_i),\forall i=1,\ldots,L$$. An ATM is constructed using a template image that is annotated with $$L$$ landmark points and a set of $$N$$ shapes $$\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$$ that are essential for building the hsape model. Specifically, it consists of the following parts:

* **Shape Model**  
  The shape model is trained as explained in the [Point Distributon Model section](pdm.md "Point Distribution Model basics"). The training shapes $$\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$$ are first aligned using Generalized Procrustes Analysis and then an orthonormal basis is created using Principal Component Analysis (PCA) which is further augmented with four eigenvectors that represent the similarity transform (scaling, in-plane rotation and translation). This results in
  $$
  \big\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\big\rbrace
  $$
  where $$\mathbf{U}_s\in\mathbb{R}^{2L\times n}$$ is the orthonormal basis of $$n$$ eigenvectors (including the four similarity components) and $$\bar{\mathbf{s}}\in\mathbb{R}^{2L\times 1}$$ is the mean shape vector. An new shape instance can be generated as $$\mathbf{s}_{\mathbf{p}}=\bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}$$, where $$\mathbf{p}=\big[p_1,p_2,\ldots,p_n\big]^{\mathsf{T}}$$ is the vector of shape parameters.

* **Motion Model**  
  The motion model consists of a warp function $$\mathcal{W}(\mathbf{p})$$ which is essential for warping the texture related to a shape instance generated with parameters $$\mathbf{p}$$ into a common `reference_shape`. The `reference_shape` is by default the mean shape $$\bar{\mathbf{s}}$$, however you can pass in a `reference_shape` of your preference during construction of the ATM.

* **Template**  
  The provided template image $$\mathbf{I}_a$$ which is annotated with landmarks $$\mathbf{s}_a$$ is further processed by:
  1. First extracting features using the features function $$\mathcal{F}()$$ defined by `holistic_features`, i.e. $$\mathcal{F}(\mathbf{I}_a)$$
  2. Warping the feature-based image into the `reference_shape` in order to get $$\mathcal{F}(\mathbf{I}_a)(\mathcal{W}(\mathbf{p}_a))$$
  3. Vectorizing the warped image as $$\bar{\mathbf{a}} = \mathcal{F}(\mathbf{I}_a)(\mathcal{W}(\mathbf{p}_a))$$ where $$\bar{\mathbf{a}}\in\mathbb{R}^{M\times 1}$$

Let's first load a test image and a template image $$\bar{\mathbf{a}}$$. We'll load two images of the same person (Amanda Peet, actress)
from LFPW trainset (see [Importing Images](importing.md "Basics on how to import images") for download instructions).
```python
from pathlib import Path
import menpo.io as mio

path_to_lfpw = Path('/path/to/lfpw/trainset/')

image = mio.import_image(path_to_lfpw / 'image_0004.png')
image = image.crop_to_landmarks_proportion(0.5)

template = mio.import_image(path_to_lfpw / 'image_0005.png')
template = template.crop_to_landmarks_proportion(0.5)
```

The image and template can be visualized as:
```python
%matplotlib inline
import matplotlib.pyplot as plt

plt.subplot(121)
image.view()
plt.gca().set_title('Input Image')

plt.subplot(122)
template.view_landmarks(marker_face_colour='white', marker_edge_colour='black',
                        marker_size=4)
plt.gca().set_title('Template');
```
<center>
  <img src="media/atm_template.png" alt="Template image">
</center>

Let's also load the shapes of LFPW trainset that will be used in order to train the PDM:
```python
from menpo.visualize import print_progress

training_shapes = []
for lg in print_progress(mio.import_landmark_files(path_to_lfpw / '*.pts', verbose=True)):
    training_shapes.append(lg['all'])
```

The shapes can be visualized using a widget as:
```python
from menpowidgets import visualize_pointclouds
visualize_pointclouds(training_shapes)
```
<video width="100%" autoplay loop>
  <source src="media/visualize_pointclouds_lfpw.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="warp"></a>2. Warp Functions
With an abuse of notation, let us define
$$
\mathbf{t}(\mathcal{W}(\mathbf{p}))\equiv \mathcal{F}(\mathbf{I})(\mathcal{W}(\mathbf{p}))
$$
as the feature-based warped $$M\times 1$$ vector of an image $$\mathbf{I}$$ given its shape instance generated with parameters $$\mathbf{p}$$.

`menpofit` provides five different ATM versions, which differ on the way that this appearance warping $$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ is performed.
Specifically:

**HolisticATM**  
The `HolisticATM` uses a holistic appearance representation obtained by warping the texture into the `reference_shape`
with a non-linear warp function $$\mathcal{W}(\mathbf{p})$$. Two such warp functions are currently supported:
Piecewise Affine Warp and Thin Plate Spline.

**MaskedATM**  
The `MaskedATM` uses the same warp logic as the `HolsiticATM`. The only difference between them is that the
`reference_shape` is masked. The mask that is created by default consists of rectangular mask patches centered around the landmarks.

**LinearATM**  
The `LinearATM` utilizes a linear warp function $$\mathcal{W}(\mathbf{p})$$ in the motion model. The advantage is that the linear nature of such a warp
function makes the computation of its Jacobian trivial.

**LinearMaskedATM**  
Similar to the relation between `HolisticATM` and `MaskedATM`, a `LinearMaskedATM` is exactly the same with a
`LinearATM`, with the difference that the `reference_shape` is masked.

**PatchATM**  
A `PatchATM` represents the appearance in a patch-based fashion, i.e. rectangular patches are extracted around the landmark points.
Thus, the warp function $$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ simply _samples_ the patches centered around the landmarks of the shape instance generated with parameters $$\mathbf{p}$$.

Let's now create a `HolisticATM` using IGO features:
```python
from menpofit.atm import HolisticATM
from menpo.feature import igo

atm = HolisticATM(template, training_shapes, group='PTS',
                  diagonal=180, scales=(0.25, 1.0),
                  holistic_features=igo, verbose=True)
```
and visualize it:
```python
atm.view_shape_models_widget()
```
<video width="100%" autoplay loop>
  <source src="media/view_shape_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
atm.view_atm_widget()
```
<video width="100%" autoplay loop>
  <source src="media/atm_view_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="cost"></a>3. Cost Function and Optimization
Fitting an ATM on a test image involves the optimization of the following cost function
$$
\arg\min_{\mathbf{p}} \big\lVert \mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}} \big\rVert^{2}
$$
with respect to the shape parameters. Note that this cost function is exactly the same as in the case of [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") for Affine Image Alignment. The only difference has to do with the nature of the transform - and thus $$\mathbf{p}$$ - that is used in the motion model $$\mathcal{W}(\mathbf{p})$$. Similarly, the cost function is very similar to the one of an [Active Appearance Model](aam.md "Active Appearance Model (AAM)") with the difference that an ATM has no appearance subspace.

The optimization of the ATM deformable image alignment is performed with the Lucas-Kanade gradient descent algorithm.
This is the same as in the case of affine image transform, so you can refer to the [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") chapter
for more information. We currently support Inverse-Compositional and Forward-Compositional optimization.

Let's now create a `Fitter` using the ATM we created, as:
```python
from menpofit.atm import LucasKanadeATMFitter, InverseCompositional

fitter = LucasKanadeATMFitter(atm,
                              lk_algorithm_cls=InverseCompositional, n_shape=[5, 15])
```

Information about the fitter can be retrieved as:
```python
print(fitter)
```
which returns
```
Holistic Active Template Model
 - Images warped with DifferentiablePiecewiseAffine transform
 - Images scaled to diagonal: 180.00
 - Scales: [0.25, 1.0]
   - Scale 0.25
     - Holistic feature: igo
     - Template shape: (38, 38)
     - Shape model class: OrthoPDM
       - 132 shape components
       - 4 similarity transform parameters
   - Scale 1.0
     - Holistic feature: igo
     - Template shape: (133, 134)
     - Shape model class: OrthoPDM
       - 132 shape components
       - 4 similarity transform parameters
Inverse Compositional Algorithm
 - Scales: [0.25, 1.0]
   - Scale 0.25
     - 5 active shape components
     - 4 similarity transform components
   - Scale 1.0
     - 15 active shape components
     - 4 similarity transform components
```

Let's know fit the ATM on the `image` we loaded in the beggining.
We will use the DLib face detector from `menpodetect`, in order to acquire an initial bounding box, as:
```python
from menpodetect import load_dlib_frontal_face_detector

# Load detector
detect = load_dlib_frontal_face_detector()

# Detect
bboxes = detect(image)
print("{} detected faces.".format(len(bboxes)))

# View
if len(bboxes) > 0:
    image.view_landmarks(group='dlib_0', line_colour='white',
                         render_markers=False, line_width=3);
```
<center>
  <img src="media/atm_view_bbox.png" alt="Visualize detected bounding box">
</center>

and fit the ATM as:
```python
# initial bbox
initial_bbox = bboxes[0]

# fit image
result = fitter.fit_from_bb(image, initial_bbox, max_iters=20,
                            gt_shape=image.landmarks['PTS'].lms)

# print result
print(result)
```
which prints
```
Fitting result of 68 landmark points.
Initial error: 0.0877
Final error: 0.0196
```

The result can be visualized as:
```python
result.view(render_initial_shape=True)
```
<center>
  <img src="media/atm_view_result.png" alt="Visualize_fitting_result">
</center>

or using a widget as:
```python
result.view_widget()
```
<video width="100%" autoplay loop>
  <source src="media/atm_result_view_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="references"></a>4. References
<a name="1"></a>[1] I. Matthews, and S. Baker. "Active Appearance Models Revisited", International Journal of Computer Vision, vol. 60, no. 2, pp. 135-164, 2004.
