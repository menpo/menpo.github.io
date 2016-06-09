Active Appearance Model
=======================

1. [Definition](#definition)
2. [Warp Functions](#warp)
3. [Cost Function and Optimization](#cost)  
   3.1. [Lucas-Kanade Optimization](#lucas-kanade-fitting)  
   3.2. [Supervised Descent Optimization](#supervised-descent-fitting)
4. [Fitting Example](#fitting)
5. [References](#references)
6. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/aam/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

### <a name="definition"></a>1. Definition
Active Appearance Model (AAM) is a statistical deformable model of the shape and appearance of a deformable object class.
It is a generative model which during fitting aims to recover a parametric description of a certain object through optimization.
In this page, we provide a basic mathematical definition of an AAM and all its variations that are implemented within `menpofit`.
For a more in-depth explanation of AAM, please refer to the relevant literature in [References](#references) and especially [[1](#1)].

A shape instance of a deformable object is represented as $$\mathbf{s}=\big[x_1,y_1,\ldots,x_L,y_L\big]^{\mathsf{T}}$$, a $$2L\times 1$$ vector consisting of $$L$$ landmark points coordinates $$(x_i,y_i),\forall i=1,\ldots,L$$. An AAM [[6](#6), [8](#8)] is trained using a set of $$N$$ images $$\big\lbrace\mathbf{I}_1,\mathbf{I}_2,\ldots,\mathbf{I}_N\big\rbrace$$ that are annotated with a set of
$$L$$ landmarks and it consists of the following parts:

* **Shape Model**  
  The shape model is trained as explained in the [Point Distributon Model section](pdm.md "Point Distribution Model basics"). The training shapes $$\big\lbrace\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\big\rbrace$$ are first aligned using Generalized Procrustes Analysis and then an orthonormal basis is created using Principal Component Analysis (PCA) which is further augmented with four eigenvectors that represent the similarity transform (scaling, in-plane rotation and translation). This results in
  $$
  \big\lbrace\bar{\mathbf{s}}, \mathbf{U}_s\big\rbrace
  $$
  where $$\mathbf{U}_s\in\mathbb{R}^{2L\times n}$$ is the orthonormal basis of $$n$$ eigenvectors (including the four similarity components) and $$\bar{\mathbf{s}}\in\mathbb{R}^{2L\times 1}$$ is the mean shape vector. An new shape instance can be generated as $$\mathbf{s}_{\mathbf{p}}=\bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}$$, where $$\mathbf{p}=\big[p_1,p_2,\ldots,p_n\big]^{\mathsf{T}}$$ is the vector of shape parameters.


  * **Motion Model**  
  The motion model consists of a warp function $$\mathcal{W}(\mathbf{p})$$ which is essential for warping the texture related to a shape instance generated with parameters $$\mathbf{p}$$ into a common `reference_shape`. The `reference_shape` is by default the mean shape $$\bar{\mathbf{s}}$$, however you can pass in a `reference_shape` of your preference during construction of the AAM.


  * **Appearance Model**  
  The appearance model is trained by:
    1. First extracting features from all the training images using the features function $$\mathcal{F}()$$ defined by `holistic_features`, i.e. $$\mathcal{F}(\mathbf{I}_i)$$, $$\forall i=1,\ldots,N$$
    2. Warping the feature-based images into the `reference_shape` in order to get $$\mathcal{F}(\mathbf{I}_i)(\mathcal{W}(\mathbf{p}_i))$$, $$\forall i=1,\ldots,N$$
    3. Vectorizing the warped images as $$\mathbf{a}_i= \mathcal{F}(\mathbf{I}_i)(\mathcal{W}(\mathbf{p}_i))$$, $$\forall i=1,\ldots,N$$ where $$\mathbf{a}_i\in\mathbb{R}^{M\times 1}$$
    4. Applying PCA on the acquired vectors which results in
    $$
    \big\lbrace\bar{\mathbf{a}}, \mathbf{U}_a\big\rbrace
    $$
    where $$\mathbf{U}_a\in\mathbb{R}^{M\times m}$$ is the orthonormal basis of $$m$$ eigenvectors and $$\bar{\mathbf{a}}\in\mathbb{R}^{M\times 1}$$ is the mean appearance vector.

  A new appearance instance can be generated as $$\mathbf{a}_{\mathbf{c}}=\bar{\mathbf{a}} + \mathbf{U}_a\mathbf{c}$$, where $$\mathbf{c}=\big[c_1,c_2,\ldots,c_m\big]^{\mathsf{T}}$$ is the vector of appearance parameters.

Before continuing, let's load the trainset of LFPW (see [Importing Images](importing.md "Basics on how to import images") for download instructions) as
```python
import menpo.io as mio
from menpo.visualize import print_progress
from menpo.landmark import labeller, face_ibug_68_to_face_ibug_68_trimesh

path_to_images = '/path/to/lfpw/trainset/'
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
    # define a TriMesh which will be useful for Piecewise Affine Warp of HolisticAAM
    labeller(img, 'PTS', face_ibug_68_to_face_ibug_68_trimesh)
    # append to list
    training_images.append(img)
```
Note that we labeled the images using `face_ibug_68_to_face_ibug_68_trimesh`, in order to
get a manually defined `TriMesh` for the Piecewise Affine Warp. However, this is not necessary and it only applies
for `HolisticAAM`. We can visualize the images using an interactive widget as:
```python
%matplotlib inline
from menpowidgets import visualize_images
visualize_images(training_images)
```
<video width="100%" autoplay loop>
  <source src="media/visualize_images_lfpw_trimesh.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="warp"></a>2. Warp Functions
With an abuse of notation, let us define
$$
\mathbf{t}(\mathcal{W}(\mathbf{p}))\equiv \mathcal{F}(\mathbf{I})(\mathcal{W}(\mathbf{p}))
$$
as the feature-based warped $$M\times 1$$ vector of an image $$\mathbf{I}$$ given its shape instance generated with parameters $$\mathbf{p}$$.

`menpofit` provides five different AAM versions, which differ on the way that this appearance warping $$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ is performed.
Specifically:

**HolisticAAM**  
The `HolisticAAM` uses a holistic appearance representation obtained by warping the texture into the `reference_shape`
with a non-linear warp function $$\mathcal{W}(\mathbf{p})$$. Two such warp functions are currently supported:
Piecewise Affine Warp and Thin Plate Spline.
Let's create a `HolisticAAM` using Dense SIFT features:
```python
from menpofit.aam import HolisticAAM
from menpo.feature import fast_dsift

aam = HolisticAAM(training_images, group='face_ibug_68_trimesh', diagonal=150,
                  scales=(0.5, 1.0), holistic_features=fast_dsift, verbose=True,
                  max_shape_components=20, max_appearance_components=150)
```
and visualize it:
```python
aam.view_shape_models_widget()
```
<video width="100%" autoplay loop>
  <source src="media/view_shape_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
aam.view_appearance_models_widget()
```
<video width="100%" autoplay loop>
  <source src="media/holistic_aam_view_appearance_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
aam.view_aam_widget()
```
<video width="100%" autoplay loop>
  <source src="media/holistic_aam_view_aam_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

**MaskedAAM**  
The `MaskedAAM` uses the same warp logic as the `HolsiticAAM`. The only difference between them is that the
`reference_shape` is masked. The mask that is created by default consists of rectangular mask patches centered around the landmarks.

**LinearAAM**  
The `LinearAAM` utilizes a linear warp function $$\mathcal{W}(\mathbf{p})$$ in the motion model. The advantage is that the linear nature of such a warp
function makes the computation of its Jacobian trivial.

**LinearMaskedAAM**  
Similar to the relation between `HolisticAAM` and `MaskedAAM`, a `LinearMaskedAAM` is exactly the same with a
`LinearAAM`, with the difference that the `reference_shape` is masked.

**PatchAAM**  
A `PatchAAM` represents the appearance in a patch-based fashion, i.e. rectangular patches are extracted around the landmark points.
Thus, the warp function $$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ simply _samples_ the patches centered around the landmarks of the shape instance generated with parameters $$\mathbf{p}$$.
Let's create a `PatchAAM` using Dense SIFT features:
```python
from menpofit.aam import PatchAAM
from menpo.feature import fast_dsift

patch_aam = PatchAAM(training_images, group='PTS', patch_shape=[(15, 15), (23, 23)],
                     diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift,
                     max_shape_components=20, max_appearance_components=200,
                     verbose=True)
```
and visualize it:
```python
patch_aam.view_appearance_models_widget()
```
<video width="100%" autoplay loop>
  <source src="media/patch_aam_view_appearance_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
patch_aam.view_aam_widget()
```
<video width="100%" autoplay loop>
  <source src="media/patch_aam_view_aam_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>



### <a name="cost"></a>3. Cost Function and Optimization
Fitting an AAM on a test image involves the optimization of the following cost function
$$
\arg\min_{\mathbf{p}, \mathbf{c}} \big\lVert \mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}} - \mathbf{U}_a\mathbf{c} \big\rVert^{2}
$$
with respect to the shape and appearance parameters. Note that this cost function is very similar to the one of [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") for Affine Image Alignment and [Active Template Model](atm.md "Active Template Model (ATM)") for Deformabe Image Alignment. The only difference has to do with the fact that an AAM aims to align the test image with a linear appearance model.

This optimization can be solved by two approaches:
1. [Lucas-Kanade Optimization](#lucas-kanade-fitting)  
2. [Supervised Descent Optimization](#supervised-descent-fitting)

#### <a name="lucas-kanade-fitting"></a>3.1. Lucas-Kanade Optimization
The Lucas-Kanade optimization belongs to the family of gradient-descent algorithms. In general, the existing gradient descent optimization techniques are categorized as: (1) _forward_ or _inverse_ depending on the direction of the motion parameters estimation and (2) _additive_ or _compositional_ depending on the way the motion parameters are updated. `menpofit` currently provides the **Forward-Compositional** and **Inverse-Compositional** version of five different algorithms. All these algorithms are iterative and the shape parameters are updated at each iteration in a compositional manner as
$$
\mathcal{W}(\mathbf{p})\leftarrow\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p})^{-1}
$$

Below we briefly present the Inverse-Compositional of each one of them, however the Forward-Compositional can be derived in a similar fashion.

* **Project-Out**  
  The Project-Out Inverse-Compositional algorithm [[8](#8)] decouples shape and appearance by solving the AAM optimization problem in a subspace orthogonal to the appearance variation. This is achieved by "projecting-out" the appearance variation, thus working on the orthogonal complement of the appearance subspace $$\hat{\mathbf{U}}_a=\mathbf{I}_{eye}-\mathbf{U}_a\mathbf{U}_a^{\mathsf{T}}$$. The cost function has the form
  $$
  \arg\min_{\Delta\mathbf{p}} \Big\lVert \mathbf{t}\left(\mathcal{W}\left(\mathbf{p}\right)\right) - \bar{\mathbf{a}}\left(\mathcal{W}\left(\Delta\mathbf{p}\right)\right) \Big\rVert^{2}_{\hat{\mathbf{U}}_a}
  $$
  By taking the first-order Taylor expansion on the part of the model over $$\Delta\mathbf{p} = \mathbf{0}$$ we get $$\bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p})) \approx \bar{\mathbf{a}} + \nabla{\bar{\mathbf{a}}}{\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|}_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}$$.
  Thus, the incermental update of the shape parameters is computed as
  $$
  \Delta\mathbf{p} = \mathbf{H}^{-1}\mathbf{J}^{\mathsf{T}}\big[\mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}}\big]
  $$
  where $$\mathbf{H}=\mathbf{J}^{\mathsf{T}}\mathbf{J}$$ is the Gauss-Newton approximation of the Hessian matrix and
  $$\mathbf{J} = \hat{\mathbf{U}}_a\nabla{\bar{\mathbf{a}}}{\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|}_{\mathbf{p}=\mathbf{0}}$$ is the projected-out Jacobian. The appearance parameters can be retrieved at the end of the iterative optimization as $$\mathbf{c}=\mathbf{U}_a^{\mathsf{T}}\big[\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}\big]$$ in order to reconstruct the appearance. Note that the Jacobian, Hessian and its inverse are constant and can be pre-computed, which makes the Project Out Inverse Compositional fast with computational cost $$\mathcal{O}(nM+n^2)$$.


* **Simultaneous**  
  In the Simultaneous Inverse-Compositional algorithm [[7](#7)], we aim to optimize simultaneously for the shape $$\mathbf{p}$$ and the appearance $$\mathbf{c}$$ parameters. The cost function has the form
  $$
  \arg\min_{\Delta\mathbf{p},\Delta\mathbf{c}} \Big\lVert  \mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p})) - \sum_{i=1}^{m} (c_i + \Delta c_i) \mathbf{u}_i(\mathcal{W}(\Delta\mathbf{p})) \Big\rVert^{2}
  $$
  where $$\mathbf{u}_i$$ are the appearance eigenvectors, i.e. $$\mathbf{U}_a = \big[\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_m\big]$$. Note that the appearance parameters are updated in an additive manner, i.e. $$\mathbf{c}\leftarrow\mathbf{c}+\Delta\mathbf{c}$$. We denote by $$\Delta\mathbf{q}=\big[\Delta\mathbf{p}^{\mathsf{T}},\Delta\mathbf{c}^{\mathsf{T}}\big]^{\mathsf{T}}$$ the vector of concatenated parameters increments with length $$n+m$$. The linearization of the model part around $$\Delta\mathbf{p}=\mathbf{0}$$ consists of two parts:
  the mean appearance vector approximation
  $$\bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p})) \approx \bar{\mathbf{a}} + \nabla{\bar{\mathbf{a}}}{\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|}_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}$$
  and the linearized basis $$\sum_{i=1}^{m} (c_i + \Delta c_i) \mathbf{u}_i(\mathcal{W}(\Delta\mathbf{p})) \approx \sum_{i=1}^{m} (c_i + \Delta c_i) \left(\mathbf{u}_i + \nabla\mathbf{u}_i{\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|}_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\right)$$. Then the final solution at each iteration is
  $$
  \Delta\mathbf{q} = \mathbf{H}^{-1}\mathbf{J}^{\mathsf{T}}\big[\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}-\mathbf{U}_a\mathbf{c}\big]
  $$
  where the Hessian matrix is $$\mathbf{H}=\mathbf{J}^{\mathsf{T}}\mathbf{J}$$ and the Jacobian is given by $$\mathbf{J}=\big[\mathbf{U}_a, \mathbf{J}_a\big]$$ with $$\mathbf{J}_a = \nabla{\bar{\mathbf{a}}}{\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|}_{\mathbf{p}=\mathbf{0}} + \sum_{i=1}^{m}c_i{\left.\mathbf{J}_{\mathbf{u}_i}\right|}_{\mathbf{p}=\mathbf{0}}$$.
  The Jacobian of the mean appearance vector and the eigenvectors are constant and can be precomputed. However, the total Jacobian $$\mathbf{J}_a$$ and hence the Hessian matrix depend on the current estimate of the appearance parameters $$\mathbf{c}$$, thus they need to be computed at every iteration. The computational complexity is $$\mathcal{O}((n+m)^2M+(n+m)^3)$$.


* **Alternating**  
  In the Alternating Inverse-Compositional algorithm [[9](#9), [12](#12), [13](#13), [2](#2)], the cost function has the same form as in the case of Simultaneous Inverse-Compositional, i.e.
  $$
  \arg\min_{\Delta\mathbf{p},\Delta\mathbf{c}} \Big\lVert  \mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p})) - \sum_{i=1}^{m} (c_i + \Delta c_i) \mathbf{u}_i(\mathcal{W}(\Delta\mathbf{p})) \Big\rVert^{2}
  $$
  where $$\mathbf{u}_i$$ are the appearance eigenvectors, i.e. $$\mathbf{U}_a = \big[\mathbf{u}_1, \mathbf{u}_2, \ldots, \mathbf{u}_m\big]$$. The linearization also has the exact same formulation. The only difference is that we optimize with respect to $$\Delta\mathbf{p}$$ and $$\Delta\mathbf{c}$$ in an alternated manner instead of simultaneously. Specifically, assuming that we have the current estimation of $$\Delta\mathbf{p}$$, the appearance parameters incremental is computed as
  $$
  \Delta\mathbf{c} = \mathbf{U}_a^{\mathsf{T}}\big[\mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}} - \mathbf{U}_a\mathbf{c} - \mathbf{J}\Delta\mathbf{p}\big]
  $$
  Then, given the current estiamte of $$\Delta\mathbf{c}$$, the shape parameters incerment is comptuted as
  $$
  \Delta\mathbf{p}=\mathbf{H}^{-1}\mathbf{J}^{\mathsf{T}}\big[\mathbf{t}(\mathcal{W}(\mathbf{p})) - \bar{\mathbf{a}} - \mathbf{U}_a(\mathbf{c}+\Delta\mathbf{c})\big]
  $$


* **Modified Alternating**  
  blah blah blah


* **Wiberg**  
  blah blah blah

Let's now create a Lucas-Kanade Fitter for the patch-based AAM that we trained above using the Wiberg Inverse-Compositional algorithm, as
```python
from menpofit.aam import LucasKanadeAAMFitter, WibergInverseCompositional

fitter = LucasKanadeAAMFitter(patch_aam, lk_algorithm_cls=WibergInverseCompositional,
                              n_shape=[5, 20], n_appearance=[30, 150])
```

Remember that you can always retrieve information about any trained model by:
```python
print(fitter)
```


#### <a name="supervised-descent-fitting"></a>3.2. Supervised Descent Optimization


### <a name="fitting"></a>4. Fitting Example
Let's load a test image from LFPW testset and convert it to grayscale
```python
from pathlib import Path
import menpo.io as mio

path_to_lfpw = Path('/home/ea1812/Desktop/images/lfpw/testset/')

image = mio.import_image(path_to_lfpw / 'image_0018.png')
image = image.as_greyscale()
```

Let's also load a pre-trained face detector from `menpodetect` and try to find the face's bounding box in order to initialize the AAM fitting
```python
from menpodetect import load_dlib_frontal_face_detector

# Load detector
detect = load_dlib_frontal_face_detector()

# Detect
bboxes = detect(image)
print("{} detected faces.".format(len(bboxes)))

# View
if len(bboxes) > 0:
    image.view_landmarks(group='dlib_0', line_colour='red',
                         render_markers=False, line_width=4);
```
<center>
  <img src="media/aam_view_bbox.png" alt="Visualize bounding box initialization">
</center>

The fitting can be executed as
```python
# initial bbox
initial_bbox = bboxes[0]

# fit image
result = fitter.fit_from_bb(image, initial_bbox, max_iters=[15, 5],
                            gt_shape=image.landmarks['PTS'].lms)

# print result
print(result)
```
which prints
```python
Fitting result of 68 landmark points.
Initial error: 0.1689
Final error: 0.0213
```

The fitting result can be visualized as
```python
result.view(render_initial_shape=True)
```
<center>
  <img src="media/aam_view_result.png" alt="Visualize fitting result">
</center>

and the fitting iterations as
```python
result.view_iterations()
```
<center>
  <img src="media/aam_view_iterations.png" alt="Visualize fitting iterations">
</center>

Also, you can plot the fitting error per iteration as
```python
result.plot_errors()
```
<center>
  <img src="media/aam_plot_errors.png" alt="Plot fitting error per iteration">
</center>

and of course the fitting result widget can be called as
```python
result.view_widget()
```
<video width="100%" autoplay loop>
  <source src="media/patch_aam_view_result_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

Let's try an image with a more challenging head pose
```python
import matplotlib.pyplot as plt

# Load and convert to grayscale
image = mio.import_image(path_to_lfpw / 'image_0117.png')
image = image.as_greyscale()

# Detect face
bboxes = detect(image)

if len(bboxes) > 0:
    # Fit AAM
    result = fitter.fit_from_bb(image, bboxes[0], max_iters=[15, 5],
                                gt_shape=image.landmarks['PTS'].lms)
    print(result)

    # Visualize
    plt.subplot(131);
    image.view()
    bboxes[0].view(line_width=3, render_markers=False)
    plt.gca().set_title('Bounding box')

    plt.subplot(132)
    image.view()
    result.initial_shape.view(marker_size=4)
    plt.gca().set_title('Initial shape')

    plt.subplot(133)
    image.view()
    result.final_shape.view(marker_size=4, figure_size=(15, 13))
    plt.gca().set_title('Final shape')
```
<center>
  <img src="media/aam_view_result_2.png" alt="Visualize fitting result">
</center>

and trigger the widget
```python
result.view_widget()
```
<video width="100%" autoplay loop>
  <source src="media/patch_aam_view_result_widget_2.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="references"></a>5. References
<a name="1"></a>[1] J. Alabort-i-Medina, and S. Zafeiriou. "A Unified Framework for Compositional Fitting of Active Appearance Models", arXiv:1601.00199.

<a name="2"></a>[2] J. Alabort-i-Medina, and S. Zafeiriou. "Bayesian Active Appearance Models", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014.

<a name="3"></a>[3] E. Antonakos, J. Alabort-i-Medina, G. Tzimiropoulos, and S. Zafeiriou. "Feature-based Lucas-Kanade and Active Appearance Models", IEEE Transactions on Image Processing, vol. 24, no. 9, pp. 2617-2632, 2015.

<a name="4"></a>[4] E. Antonakos, J. Alabort-i-Medina, G. Tzimiropoulos, and S. Zafeiriou. "HOG Active Appearance Models", IEEE International Conference on Image Processing (ICIP), 2014.

<a name="5"></a>[5] S. Baker, and I. Matthews. "Lucas-Kanade 20 years on: A unifying framework", International Journal of Computer Vision, vol. 56, no. 3, pp. 221-255, 2004.

<a name="6"></a>[6] T.F. Cootes, G.J. Edwards, and C.J. Taylor. "Active Appearance Models", IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 23, no. 6, pp. 681–685, 2001.

<a name="7"></a>[7] R. Gross, I. Matthews, and S. Baker. "Generic vs. person specific Active Appearance Models", Image and Vision Computing, vol. 23, no. 12, pp. 1080-1093, 2005.

<a name="8"></a>[8] I. Matthews, and S. Baker. "Active Appearance Models Revisited", International Journal of Computer Vision, vol. 60, no. 2, pp. 135-164, 2004.

<a name="9"></a>[9] G. Papandreou, and P. Maragos. "Adaptive and constrained algorithms for  inverse compositional active appearance model fitting", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2008.

<a name="10"></a>[10] G. Tzimiropoulos, J. Alabort-i-Medina, S. Zafeiriou, and M. Pantic. "Active Orientation Models for Face Alignment in-the-wild", IEEE Transactions on Information Forensics and Security, Special Issue on Facial Biometrics in-the-wild, vol. 9, no. 12, pp. 2024-2034, 2014.

<a name="11"></a>[11] G. Tzimiropoulos, and M. Pantic. "Gauss-Newton Deformable Part Models for Face Alignment In-the-Wild", IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2014.

<a name="12"></a>[12] G. Tzimiropoulos, J. Alabort-i-Medina, S. Zafeiriou, and M. Pantic. "Generic Active Appearance Models Revisited", Asian Conference on Computer Vision, Springer, 2012.

<a name="13"></a>[13] G. Tzimiropoulos, M. Pantic. "Optimization problems for fast AAM fitting in-the-wild", IEEE International Conference on Computer Vision (ICCV), 2013.
