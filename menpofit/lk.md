Lucas-Kanade Image Alignment
============================

1. [Definition](#definition)
2. [Gradient Descent Optimization](#optimization)
3. [Alignment and Visualization](#visualization)
4. [References](#references)
5. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/lk/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

### <a name="definition"></a>1. Definition
The aim of image alignment is to find the location of a constant template $$\bar{\mathbf{a}}$$ in an input image $$\mathbf{t}$$.
Note that both $$\bar{\mathbf{a}}$$ and $$\mathbf{t}$$ are vectorized.
This alignment is done by estimating the optimal parameters values of a parametric motion model. The motion model consists of a Warp function
$$\mathcal{W}(\mathbf{x},\mathbf{p})$$ which maps each point $$\mathbf{x}$$ within a target (reference) shape to its corresponding
location in a shape instance. The identity warp is defined as $$\mathcal{W}(\mathbf{x},\mathbf{0})=\mathbf{x}$$.
The warp function in this case is driven by an affine transform, thus $$\mathbf{p}$$ consists of 6 parameters.

The Lucas-Kanade (LK) optimization problem is expressed as minimizing the $$\ell_2$$ norm
$$
\arg\min_{\mathbf{p}} \left\lVert \bar{\mathbf{a}} - \mathbf{t}(\mathcal{W}(\mathbf{p})) \right\rVert^{2}
$$
with respect to the motion model parameters $$\mathbf{p}$$. Let's load an image $$\mathbf{t}$$ and create a template $$\bar{\mathbf{a}}$$ from it
```python
import menpo.io as mio

takeo = mio.import_builtin_asset.takeo_ppm()
# Use a bounding box of ground truth landmarks to create template
takeo.landmarks['bounding_box'] = takeo.landmarks['PTS'].lms.bounding_box()
template = takeo.crop_to_landmarks(group='bounding_box')
```

The image and template can be visualized as:
```python
%matplotlib inline
import matplotlib.pyplot as plt

plt.subplot(121)
takeo.view_landmarks(group='bounding_box', line_colour='r', line_width=2,
                     render_markers=False)
plt.subplot(122)
template.view()
plt.gca().set_title('Template');
```
<center>
  <img src="media/lk_template.png" alt="Template image">
</center>


### <a name="optimization"></a>2. Gradient Descent Optimization
The existing gradient descent optimization techniques [[1](#1)] are categorized as:
(1) _forward_ or _inverse_ depending on the direction of the motion parameters estimation and
(2) _additive_ or _compositional_ depending on the way the motion parameters are updated.

##### Forward-Additive
Lucas and Kanade proposed the FA gradient descent in [[2](#2)]. By using an additive iterative update of the parameters,
i.e. $$\mathbf{p}\leftarrow\mathbf{p}+\Delta\mathbf{p}$$, and having an initial estimate of $$\mathbf{p}$$, the cost function is expressed as minimizing
$$
\arg\min_{\Delta\mathbf{p}}\|\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}+\Delta\mathbf{p}))\|^2
$$
with respect to $$\Delta\mathbf{p}$$.
The solution is given by first linearizing around $$\mathbf{p}$$, thus using first order Taylor series expansion at $$\mathbf{p}+\Delta\mathbf{p}=\mathbf{p}\Rightarrow\Delta\mathbf{p}=\mathbf{0}$$.
This gives
$$\mathbf{t}(\mathcal{W}(\mathbf{p}+\Delta\mathbf{p}))\approx\mathbf{t}(\mathcal{W}(\mathbf{p}))+\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\Delta\mathbf{p}$$,
where $$\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}=\nabla\mathbf{t}\frac{\partial\mathcal{W}}{\partial\mathbf{p}}$$ is the *image Jacobian*,
consisting of the *image gradient* evaluated at $$\mathcal{W}(\mathbf{p})$$ and the *warp jacobian* evaluated at $$\mathbf{p}$$.
The final solution is given by
$$\Delta\mathbf{p}=\mathbf{H}^{-1}\mathbf{J}^T_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\left[\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}))\right]$$
where $$\mathbf{H}=\mathbf{J}^T_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}$$ is the Gauss-Newton approximation of the *Hessian matrix*.
This method is forward because the warp projects into the image coordinate frame and additive because the iterative update of the motion parameters is computed
by estimating a $$\Delta\mathbf{p}$$ incremental offset from the current parameters.

##### Forward-Compositional
Compared to FA, in FC gradient descent we have the same warp direction for computing the parameters, but a compositional update of the form $$\mathcal{W}(\mathbf{p})\leftarrow\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p})$$. The minimization cost function in this case takes the form
$$
\arg\min_{\Delta\mathbf{p}}\|\bar{\mathbf{a}}-\mathbf{t}\left( \mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p}) \right)\|^2
$$
and the linearization is
$$\|\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}))-\mathbf{J}_{\mathbf{t}}|_{\Delta\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\|^2$$,
where the composition with the identity warp is $$\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\mathbf{0})=\mathcal{W}(\mathbf{p})$$.
The image Jacobian in this case is expressed as $$\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{0}}=\nabla\mathbf{t}(\mathcal{W}(\mathbf{p}))\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|_{\mathbf{p}=\mathbf{0}}$$.
Thus, with this formulation, the warp Jacobian is constant and can be precomputed, because it is evaluated at $$\mathbf{p}=\mathbf{0}$$.
This precomputation slightly improves the algorithm's computational complexity compared to the FA case, even though the compositional update is more expensive than the additive one.

##### Inverse-Compositional
In the IC optimization, the direction of the warp is reversed compared to the two previous techniques and the incremental warp is computed with respect to the template $$\bar{\mathbf{a}}$$ [[1](#1), [3](#3)]. The goal in this case is to minimize
$$
\arg\min_{\Delta\mathbf{p}}\|\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p}))\|^2
$$
with respect to $$\Delta\mathbf{p}$$. The incremental warp $$\mathcal{W}(\Delta\mathbf{p})$$ is computed with respect to the template $$\bar{\mathbf{a}}$$,
but the current warp $$\mathcal{W}(\mathbf{p})$$ is still applied on the input image. By linearizing around $$\Delta\mathbf{p}=\mathbf{0}$$ and using the identity warp,
we have $$\|\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}-\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\|^2$$
where $$\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}=\nabla\bar{\mathbf{a}}\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|_{\mathbf{p}=\mathbf{0}}$$.
Consequently, similar to the FC case, the increment is $$\Delta\mathbf{p}=\mathbf{H}^{-1}\mathbf{J}^T_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\left[\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}\right]$$
where the Hessian matrix is $$\mathbf{H}=\mathbf{J}^T_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}$$.
The compositional motion parameters update in each iteration is $$\mathcal{W}(\mathbf{p})\leftarrow\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p})^{-1}$$.
Since the gradient is always taken at the template, the warp Jacobian $$\left.\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\right|_{\mathbf{p}=\mathbf{0}}$$
and thus the Hessian matrix inverse remain constant and can be precomputed. This makes the IC algorithm both fast and efficient.

##### Residuals and Features
Apart from the Sum of Squared Differences (SSD) residual presented above, `menpofit` includes implementations for
SSD on Fourier domain [[4](#4)], Enhanced Correlation Coefficient (ECC) [[5](#5)], Image Gradient [[6](#6)] and Gradient Correlation [[6](#6)] residuals.
Additionally, all LK implementations can be applied using any kind of features. For a study on the effect of various feature functions on the LK image alignement, please
refere to [[7](#7)].

##### Example
In `menpofit`, an LK `Fitter` object with Inverse-Compositional optimization can be obtained as:
```python
from menpofit.lk import LucasKanadeFitter, InverseCompositional
from menpo.feature import no_op

fitter = LucasKanadeFitter(template, group='bounding_box',
                           algorithm_cls=InverseCompositional, residual_cls=SSD,
                           scales=(0.5, 1.0), holistic_features=no_op)
```
where we can define different types of features and scales. Remember that most objects can print information about themselves:
```python
print(fitter)
```
which returns
```
Lucas-Kanade Inverse Compositional Algorithm
 - Sum of Squared Differences Residual
 - Images warped with DifferentiableAlignmentAffine transform
 - Images scaled to diagonal: 128.35
 - Scales: [0.5, 1.0]
   - Scale 0.5
     - Holistic feature: no_op
     - Template shape: (44, 48)
   - Scale 1.0
     - Holistic feature: no_op
     - Template shape: (87, 96)
```


### <a name="visualization"></a>3. Alignment and Visualization
Fitting a `LucasKanadeFitter` to an image is as simple as calling its `fit_from_bb` method.
We will attempt to fit the cropped template we created earlier onto a perturbed version of the original image, by adding
noise to its ground truth bounding box. Note that `noise_percentage` is too large in order to create a very challenging initialization.
```python
from menpofit.fitter import noisy_shape_from_bounding_box

gt_bb = takeo.landmarks['bounding_box'].lms
# generate perturbed bounding box
init_bb = noisy_shape_from_bounding_box(fitter.reference_shape, gt_bb,
                                        noise_percentage=0.12,
                                        allow_alignment_rotation=True)
# fit image
result = fitter.fit_from_bb(takeo, init_bb, gt_shape=gt_bb, max_iters=80)
```

The initial and final bounding boxes can be viewed as:
```
result.view(render_initial_shape=True)
```

and the alignment error per iteration as:
```python
result.plot_errors()
```

Of course, the fitting result can also be viewed using a widget:
```python
result.view_widget()
```
<video width="100%" autoplay loop>
  <source src="media/lk_result_view_widget.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

Finally, by using the following code
```python
from menpowidgets import visualize_images

visualize_images(fitter.warped_images(fr.image, fr.shapes))
```

we can visualize the warped image per iteration as:
<video width="100%" autoplay loop>
  <source src="media/lk_warped_images.mp4" type="video/mp4">
Your browser does not support the video tag.
</video>

### <a name="references"></a>4. References
<a name="1"></a>[1] S. Baker, and I. Matthews. "Lucas-Kanade 20 years on: A unifying framework", International Journal of Computer Vision, vol. 56, no. 3, pp. 221-255, 2004.

<a name="2"></a>[2] B.D. Lucas, and T. Kanade, "An iterative image registration technique with an application to stereo vision", International Joint Conference on Artificial Intelligence, 1981.

<a name="3"></a>[3] S. Baker, and I. Matthews. "Equivalence and efficiency of image alignment algorithms", IEEE Conference on Computer Vision and Pattern Recognition, 2001.

<a name="4"></a>[4] A.B. Ashraf, S. Lucey, and T. Chen. "Fast Image Alignment in the Fourier Domain", IEEE Conference on Computer Vision and Pattern Recognition, 2010.

<a name="5"></a>[5] G.D. Evangelidis, and E.Z. Psarakis. "Parametric Image Alignment Using Enhanced Correlation Coefficient Maximization", IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 30, no. 10, pp. 1858-1865, 2008.

<a name="6"></a>[6] G. Tzimiropoulos, S. Zafeiriou, and M. Pantic. "Robust and Efficient Parametric Face Alignment", IEEE International Conference on Computer Vision, 2011.

<a name="7"></a>[7] E. Antonakos, J. Alabort-i-Medina, G. Tzimiropoulos, and S. Zafeiriou. "Feature-based Lucas-Kanade and Active Appearance Models", IEEE Transactions on Image Processing, vol. 24, no. 9, pp. 2617-2632, 2015.
