Active Appearance Model
=======================

1. [Definition](#definition)
2. [Warp Functions](#warp)
3. [Cost Function](#cost)  
   3.1. [Lucas-Kanade Optimization](#lucas-kanade-fitting)  
   3.2. [Supervised Descent Optimization](#supervised-descent-fitting)
4. [References](#references)
5. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/aam/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

### <a name="definition"></a>1. Definition
Active Appearance Model (AAM) is a statistical deformable model of the shape and appearance of a deformable object class.
AAM is a generative model which during fitting aims to recover a parametric description of a certain object through optimization.
In this page, we provide a basic mathematical definition of an AAM and all its variations that are implemented within `menpofit`.
For a more in-depth explanation of AAM, please refer to the relevant literature in [References](#references) and especially [[1](#1)].

A shape instance of a deformable object is represented as $$\mathbf{s}=\left[x_1,y_1,\ldots,x_L,y_L\right]^T$$, a $$2L\times 1$$ vector consisting of $$L$$ landmark points coordinates $$(x_i,y_i),\forall i=1,\ldots,L$$. An AAM [[6](#6), [8](#8)] is trained using a set of $$N$$ images $$\{\mathbf{I}_1,\mathbf{I}_2,\ldots,\mathbf{I}_N\}$$ that are annotated with a set of
$$L$$ landmarks and it consists of the following parts:

* **Shape Model**  
  The shape model is trained as explained in the [Point Distributon Model section](pdm.md "Point Distribution Model basics"). The training shapes $$\{\mathbf{s}_1,\mathbf{s}_2,\ldots,\mathbf{s}_N\}$$ are first aligned using Generalized Procrustes Analysis and then an orthonormal basis is created using Principal Component Analysis (PCA) which is further augmented with four eigenvectors that represent the similarity transform (scaling, in-plane rotation and translation). This results in
  $$
  \{\bar{\mathbf{s}}, \mathbf{U}_s\}
  $$
  where $$\mathbf{U}_s\in\mathbb{R}^{2L\times n}$$ is the orthonormal basis of $$n$$ eigenvectors (including the four similarity components) and $$\bar{\mathbf{s}}\in\mathbb{R}^{2L\times 1}$$ is the mean shape vector. An new shape instance can be generated as $$\mathbf{s}_{\mathbf{p}}=\bar{\mathbf{s}} + \mathbf{U}_s\mathbf{p}$$, where $$\mathbf{p}=[p_1,p_2,\ldots,p_n]^T$$ is the vector of shape parameters.


  * **Motion Model**  
  The motion model consists of a warp function $$\mathcal{W}(\mathbf{p})$$ which is essential for warping the texture related to a shape instance generated with parameters $$\mathbf{p}$$ into a common `reference_shape`. The `reference_shape` is by default the mean shape $$\bar{\mathbf{s}}$$, however you can pass in a `reference_shape` of your preference during construction of the AAM.


  * **Appearance Model**  
  The appearance model is trained by:
    1. First extracting features from all the training images using the features function $$\mathcal{F}()$$ defined by `holistic_features`, i.e. $$\mathcal{F}(\mathbf{I}_i)$$, $$\forall i=1,\ldots,N$$
    2. Warping the feature-based images into the `reference_shape` in order to get $$\mathcal{F}(\mathbf{I}_i)(\mathcal{W}(\mathbf{p}_i))$$, $$\forall i=1,\ldots,N$$
    3. Vectorizing the warped images as $$\mathbf{a}_i= \mathcal{F}(\mathbf{I}_i)(\mathcal{W}(\mathbf{p}_i))$$, $$\forall i=1,\ldots,N$$ where $$\mathbf{a}_i\in\mathbb{R}^{M\times 1}$$
    4. Applying PCA on the acquired vectors which results in
    $$
    \{\bar{\mathbf{a}}, \mathbf{U}_a\}
    $$
    where $$\mathbf{U}_a\in\mathbb{R}^{M\times m}$$ is the orthonormal basis of $$m$$ eigenvectors and $$\bar{\mathbf{a}}\in\mathbb{R}^{M\times 1}$$ is the mean appearance vector.

  A new appearance instance can be generated as $$\mathbf{a}_{\mathbf{c}}=\bar{\mathbf{a}} + \mathbf{U}_a\mathbf{c}$$, where $$\mathbf{c}=[c_1,c_2,\ldots,c_m]^T$$ is the vector of appearance parameters.

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
and visualize them using an interactive widget:
```python
%matplotlib inline
from menpowidgets import visualize_images
visualize_images(training_images)
```
<video width="100%" autoplay loop>
  <source src="media/visualize_images_lfpw.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="warp"></a>2. Warp Functions
With an abuse of notation, let us define
$$
\mathbf{t}(\mathcal{p})\equiv \mathcal{F}(\mathbf{I})(\mathcal{W}(\mathbf{p}))
$$
as the feature-based warped $$M\times 1$$ vector of an image $$\mathbf{I}$$ given its shape instance generated with parameters $$\mathbf{p}$$.

`menpofit` provides five different AAM versions, which differ on the way that this appearance warping $$\mathbf{t}(\mathcal{p})$$ is performed.
Specifically:

**HolisticAAM**  
The `HolisticAAM` uses a holistic appearance representation obtained by warping the texture into the `reference_shape`
with a non-linear warp function $$\mathcal{W}(\mathbf{p})$$. Two such warp functions are currently supported:
Piecewise Affine Warp and Thin Plate Spline.

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

Let's now create a `HolisticAAM` using Dense SIFT features:
```python
from menpofit.aam import HolisticAAM
from menpo.feature import fast_dsift

aam = HolisticAAM(training_images, group='face_ibug_68_trimesh',
                  diagonal=150, scales=(0.5, 1.0), holistic_features=fast_dsift,
                  max_shape_components=20, max_appearance_components=150, verbose=True)
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
  <source src="media/view_shape_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
aam.view_aam_widget()
```
<video width="100%" autoplay loop>
  <source src="media/atm_view_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="cost"></a>3. Cost Function
Fitting an AAM on a test image involves the optimization of the following cost function
$$
\arg\min_{\mathbf{p}, \mathbf{c}} \left\lVert \mathbf{t}(\mathbf{p}) - \bar{\mathbf{a}} - \mathbf{U}_a\mathbf{c} \right\rVert^{2}
$$
with respect to the shape and appearance parameters. Note that this cost function is very similar to the one of [Lucas-Kanade](lk.md "Lucas-Kanade Affine Image Alignment") for Affine Image Alignment and [Active Template Model](atm.md "Active Template Model (ATM)") for Deformabe Image Alignment. The only difference has to do with the fact that an AAM aims to align the test image with a linear appearance model.

This optimization can be solved by two approaches:
1. [Lucas-Kanade Optimization](#lucas-kanade-fitting)  
2. [Supervised Descent Optimization](#supervised-descent-fitting)

#### <a name="lucas-kanade-fitting"></a>3.1. Lucas-Kanade Optimization


#### <a name="supervised-descent-fitting"></a>3.2. Supervised Descent Optimization


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
