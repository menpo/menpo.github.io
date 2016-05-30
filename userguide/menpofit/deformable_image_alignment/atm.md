Active Template Model
=====================

1. [Definition](#definition)
2. [Warp Functions](#warp)
3. [Fitting](#fitting)
4. [References](#references)

---------------------------------------

### <a name="definition"></a>1. Definition
The aim of deformable image alignment is to find the optimal alignment between a constant template $$\bar{\mathbf{a}}$$ and an input image $$\mathbf{t}$$
with respect to the parameters of a parametric motion model. Note that both $$\bar{\mathbf{a}}$$ and $$\mathbf{t}$$ are vectorized.
The motion model consists of a Warp function $$\mathcal{W}(\mathbf{x},\mathbf{p})$$ which maps each point $$\mathbf{x}$$ within a target (reference) shape to its corresponding
location in a shape instance. The identity warp is defined as $$\mathcal{W}(\mathbf{x},\mathbf{0})=\mathbf{x}$$.
In the case of Active Template Model (ATM), the warp function is driven by a Point Distributon Model (PDM), where $$\mathbf{p}$$ is the set of *shape parameters*.
To read more about PDM, please refer to the [Point Distributon Model section](../pdm/index.md).

Note that we invented the name "Active Template Model" for the purpose of the Menpo Project. The term is not established in literature.
The cost function of an ATM is exactly the same as in the case of [Lucas-Kanade](../affine_image_alignment/lk.md) for Affine Image Alignment.
Specifically, it has the form
$$
\arg\min_{\mathbf{p}} \left\lVert \bar{\mathbf{a}} - \mathbf{t}(\mathcal{W}(\mathbf{p})) \right\rVert^{2}
$$
The difference has to do with the nature of the transform - and thus $$\mathbf{p}$$ - that is used in the motion model $$\mathcal{W}(\mathbf{p})$$.

Let's first load a test image $$\mathbf{t}$$ and a template image $$\bar{\mathbf{a}}$$. We'll load two images of the same person (Amanda Peet, actress)
from LFPW trainset (see [Importing Images](../basics/importing.md) for download instructions).
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
  <img src="template.png" alt="template">
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
  <source src="../pdm/visualize_pointclouds.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="warp"></a>2. Warp Functions
The warp function $$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ of an ATM aims to warp the texture related to
a shape instance generated with parameters $$\mathbf{p}$$ into a common `reference_shape`.
The `reference_shape` is usually the mean shape $$\bar{\mathbf{s}}$$, however you can pass in a `reference_shape` of your
preference during construction of the ATM.

`menpofit` provides five different ATM versions, which differ on the way that this appearance warping
$$\mathbf{t}(\mathcal{W}(\mathbf{p}))$$ is performed.
Specifically:

**HolisticATM**  
The `HolisticATM` uses a holistic appearance representation obtained by warping the texture into the `reference_shape`
with a non-linear warp function $$\mathcal{W}(\mathbf{p})$$. Two such warp functions are currently supported:
Piecewise Affine Warp and Thin Plate Spline.

**MaskedATM**  
The `MaskedATM` uses the same warp logic as the `HolsiticATM`. The only difference between them is that the
`reference_shape` is masked. The mask that is created by default consists of rectangular mask patches centered around the landmarks.

**LinearATM**  
The `LinearATM` utilizes a linear warp function $$\mathcal{W}(\mathbf{p})$$ in the motion model. The linear nature of such a warp
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
  <source src="../basics/view_shape_models_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

```python
atm.view_atm_widget()
```
<video width="100%" autoplay loop>
  <source src="view_atm_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="fitting"></a>3. Fitting
The optimization of the ATM deformable image alignment is performed with the Lucas-Kanade gradient descent algorithm.
This is the same as in the case of affine image transform, so you can refer to the [Lucas-Kanade](../affine_image_alignment/lk.md) chapter
for more information. We currently support Inverse-Compositional and Formard-Compositional optimization.

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
  <img src="view_bbox.png" alt="view_bbox">
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
  <img src="view_result.png" alt="view_result">
</center>

or using a widget as:
```python
result.view_widget()
```
<video width="100%" autoplay loop>
  <source src="result_view_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>


### <a name="references"></a>4. References
<a name="1"></a>[1] I. Matthews, and S. Baker. "Active Appearance Models Revisited", International Journal of Computer Vision, vol. 60, no. 2, pp. 135-164, 2004.
