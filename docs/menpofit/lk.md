---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Lucas-Kanade Image Alignment

1. <a href="#definition">Definition</a>
2. <a href="#optimization">Optimization and Residuals</a>
3. <a href="#visualization">Alignment and Visualization</a>
4. <a href="#references">References</a>
5. <a href="http://menpofit.readthedocs.io/en/stable/api/menpofit/lk/index.html">API Documentation <i class="fa fa-external-link fa-lg"></i></a>

---------------------------------------

```{note}
Every code cell on this page is run when the website is built, against menpofit {{ menpofit_version }}, so the
samples are always current. In a Jupyter notebook, the [menpowidgets](../menpowidgets/index.md) visualizations
render best with the inline backend (`%matplotlib inline`, the default in JupyterLab).
```

<a id="definition"></a>

# 1. Definition
The aim of image alignment is to find the location of a constant template $\bar{\mathbf{a}}$ in an input image $\mathbf{t}$.
Note that both $\bar{\mathbf{a}}$ and $\mathbf{t}$ are vectorized.
This alignment is done by estimating the optimal parameters values of a parametric motion model. The motion model consists of a Warp function
$\mathcal{W}(\mathbf{x},\mathbf{p})$ which maps each point $\mathbf{x}$ within a target (reference) shape to its corresponding
location in a shape instance. The identity warp is defined as $\mathcal{W}(\mathbf{x},\mathbf{0})=\mathbf{x}$.
The warp function in this case is driven by an affine transform, thus $\mathbf{p}$ consists of 6 parameters.

The Lucas-Kanade (LK) optimization problem is expressed as minimizing the $\ell_{2}$ norm
$$
\arg\min_{\mathbf{p}} \big\lVert \bar{\mathbf{a}} - \mathbf{t}(\mathcal{W}(\mathbf{p})) \big\rVert^{2}
$$
with respect to the motion model parameters $\mathbf{p}$. Let's load an image $\mathbf{t}$ and create a template $\bar{\mathbf{a}}$ from it
```{code-cell} ipython3
import menpo.io as mio
takeo = mio.import_builtin_asset.takeo_ppm()
# Use a bounding box of ground truth landmarks to create template
takeo.landmarks['bounding_box'] = takeo.landmarks['PTS'].bounding_box()
template = takeo.crop_to_landmarks(group='bounding_box')
```

The image and template can be visualized as:
```{code-cell} ipython3
import matplotlib.pyplot as plt
plt.subplot(121)
takeo.view_landmarks(group='bounding_box', line_colour='r', line_width=2,
                     render_markers=False)
plt.subplot(122)
template.view()
plt.gca().set_title('Template');
```

<a id="optimization"></a>

## 2. Optimization and Residuals
The existing gradient descent optimization techniques [<a href="#1">1</a>] are categorized as:
(1) _forward_ or _inverse_ depending on the direction of the motion parameters estimation and
(2) _additive_ or _compositional_ depending on the way the motion parameters are updated.

### Forward-Additive
Lucas and Kanade proposed the FA gradient descent in [<a href="#2">2</a>]. By using an additive iterative update of the parameters,
i.e. $\mathbf{p}\leftarrow\mathbf{p}+\Delta\mathbf{p}$, and having an initial estimate of $\mathbf{p}$, the cost function is expressed as minimizing
$$
\arg\min_{\Delta\mathbf{p}}\big\lVert\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}+\Delta\mathbf{p}))\big\rVert^2
$$
with respect to $\Delta\mathbf{p}$.
The solution is given by first linearizing around $\mathbf{p}$, thus using first order Taylor series expansion at $\mathbf{p}+\Delta\mathbf{p}=\mathbf{p}\Rightarrow\Delta\mathbf{p}=\mathbf{0}$.
This gives
$\mathbf{t}(\mathcal{W}(\mathbf{p}+\Delta\mathbf{p}))\approx\mathbf{t}(\mathcal{W}(\mathbf{p}))+\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\Delta\mathbf{p}$,
where $\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}=\nabla\mathbf{t}\frac{\partial\mathcal{W}}{\partial\mathbf{p}}$ is the *image Jacobian*,
consisting of the *image gradient* evaluated at $\mathcal{W}(\mathbf{p})$ and the *warp jacobian* evaluated at $\mathbf{p}$.
The final solution is given by
$$\Delta\mathbf{p}=\mathbf{H}^{-1}\mathbf{J}^{\mathsf{T}}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\left[\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}))\right]$$
where $\mathbf{H}=\mathbf{J}^{\mathsf{T}}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{p}}$ is the Gauss-Newton approximation of the *Hessian matrix*.
This method is forward because the warp projects into the image coordinate frame and additive because the iterative update of the motion parameters is computed
by estimating a $\Delta\mathbf{p}$ incremental offset from the current parameters.

#### Forward-Compositional
Compared to FA, in FC gradient descent we have the same warp direction for computing the parameters, but a compositional update of the form $\mathcal{W}(\mathbf{p})\leftarrow\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p})$. The minimization cost function in this case takes the form
$$
\arg\min_{\Delta\mathbf{p}}\big\lVert\bar{\mathbf{a}}-\mathbf{t}\left( \mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p}) \right)\big\rVert^2
$$
and the linearization is
$\|\bar{\mathbf{a}}-\mathbf{t}(\mathcal{W}(\mathbf{p}))-\mathbf{J}_{\mathbf{t}}|_{\Delta\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\|^2$,
where the composition with the identity warp is $\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\mathbf{0})=\mathcal{W}(\mathbf{p})$.
The image Jacobian in this case is expressed as $\mathbf{J}_{\mathbf{t}}|_{\mathbf{p}=\mathbf{0}}=\nabla\mathbf{t}(\mathcal{W}(\mathbf{p}))\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\Big|_{\mathbf{p}=\mathbf{0}}$.
Thus, with this formulation, the warp Jacobian is constant and can be precomputed, because it is evaluated at $\mathbf{p}=\mathbf{0}$.
This precomputation slightly improves the algorithm's computational complexity compared to the FA case, even though the compositional update is more expensive than the additive one.

##### Inverse-Compositional
In the IC optimization, the direction of the warp is reversed compared to the two previous techniques and the incremental warp is computed with respect to the template $\bar{\mathbf{a}}$ [<a href="#1">1</a>, <a href="#3">3</a>]. The goal in this case is to minimize
$$
\arg\min_{\Delta\mathbf{p}}\big\lVert\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}(\mathcal{W}(\Delta\mathbf{p}))\big\rVert^2
$$
with respect to $\Delta\mathbf{p}$. The incremental warp $\mathcal{W}(\Delta\mathbf{p})$ is computed with respect to the template $\bar{\mathbf{a}}$,
but the current warp $\mathcal{W}(\mathbf{p})$ is still applied on the input image. By linearizing around $\Delta\mathbf{p}=\mathbf{0}$ and using the identity warp,
we have $\|\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}-\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\Delta\mathbf{p}\|^2$
where $\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}=\nabla\bar{\mathbf{a}}\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\Big|_{\mathbf{p}=\mathbf{0}}$.
Consequently, similar to the FC case, the increment is $\Delta\mathbf{p}=\mathbf{H}^{-1}\mathbf{J}^{\mathsf{T}}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\left[\mathbf{t}(\mathcal{W}(\mathbf{p}))-\bar{\mathbf{a}}\right]$
where the Hessian matrix is $\mathbf{H}=\mathbf{J}^{\mathsf{T}}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}\mathbf{J}_{\bar{\mathbf{a}}}|_{\mathbf{p}=\mathbf{0}}$.
The compositional motion parameters update in each iteration is $\mathcal{W}(\mathbf{p})\leftarrow\mathcal{W}(\mathbf{p})\circ\mathcal{W}(\Delta\mathbf{p})^{-1}$.
Since the gradient is always taken at the template, the warp Jacobian $\frac{\partial\mathcal{W}}{\partial\mathbf{p}}\Big|_{\mathbf{p}=\mathbf{0}}$
and thus the Hessian matrix inverse remain constant and can be precomputed. This makes the IC algorithm both fast and efficient.

##### Residuals and Features
Apart from the Sum of Squared Differences (SSD) residual presented above, `menpofit` includes implementations for
SSD on Fourier domain [<a href="#4">4</a>], Enhanced Correlation Coefficient (ECC) [<a href="#5">5</a>], Image Gradient [<a href="#6">6</a>] and Gradient Correlation [<a href="#6">6</a>] residuals.
Additionally, all LK implementations can be applied using any kind of features. For a study on the effect of various feature functions on the LK image alignment, please
refer to [<a href="#7">7</a>].

##### Example
In `menpofit`, an LK `Fitter` object with Inverse-Compositional optimization can be obtained as:
```{code-cell} ipython3
from menpofit.lk import LucasKanadeFitter, InverseCompositional, SSD
from menpo.feature import no_op

fitter = LucasKanadeFitter(template, group='bounding_box',
                           algorithm_cls=InverseCompositional, residual_cls=SSD,
                           scales=(0.5, 1.0), holistic_features=no_op)
```
where we can define different types of features and scales. Remember that most objects can print information about themselves:
```{code-cell} ipython3
print(fitter)
```


<a id="visualization"></a>

### 3. Alignment and Visualization
Fitting a `LucasKanadeFitter` to an image is as simple as calling its `fit_from_bb` method.
We will attempt to fit the cropped template we created earlier onto a perturbed version of the original image, by adding
noise to its ground truth bounding box (the random generator is seeded, so that the example is always the same). The template is a crop of this very image, so the best possible fit is an error of zero.
```{code-cell} ipython3
import numpy as np
from menpofit.fitter import noisy_shape_from_bounding_box

gt_bb = takeo.landmarks['bounding_box']
# generate perturbed bounding box
np.random.seed(4)
init_bb = noisy_shape_from_bounding_box(fitter.reference_shape, gt_bb,
                                        noise_percentage=0.05,
                                        allow_alignment_rotation=False)
# fit image
result = fitter.fit_from_bb(takeo, init_bb, gt_shape=gt_bb, max_iters=80)
print(result)
```

```{note}
Whether the fit converges depends on the start, and the start here is random (the generator is seeded, and this seed is one of the good ones). We tried 8 seeds on this image with `noise_percentage=0.05`: the fitter above
converged to an error of about zero for 5 of them, stopped at 0.09 for 2 and diverged for 1. With `noise_percentage=0.1` and rotation allowed, the Inverse-Compositional fitter ended
with a smaller error than it started with for half of the 8 seeds, and a Forward-Compositional fitter (`ForwardCompositional`, slower per iteration) for all of them.
```

The initial and final bounding boxes can be viewed as:
```{code-cell} ipython3
result.view(render_initial_shape=True);
```
and the alignment error per iteration as:
```{code-cell} ipython3
result.plot_errors();
```
Of course, the fitting result can also be viewed using a widget:
```python
from menpowidgets import visualize_fitting_results
visualize_fitting_results(result)
```
Finally, by using the following code
```python
from menpowidgets import visualize_images
visualize_images(fitter.warped_images(result.image, result.shapes))
```

we can visualize the warped image per iteration. Here, the first and the last, next to the template they are aligned to:
```{code-cell} ipython3
warped = fitter.warped_images(result.image, result.shapes)

plt.figure(figsize=(9, 3))
plt.subplot(131)
template.view()
plt.gca().set_title('Template')
plt.subplot(132)
warped[0].view()
plt.gca().set_title('Warped, iteration 0')
plt.subplot(133)
warped[-1].view()
plt.gca().set_title('Warped, last iteration');
```

<a id="references"></a>

### 4. References
<p id="1">[1] S. Baker, and I. Matthews. "Lucas-Kanade 20 years on: A unifying framework", International Journal of Computer Vision, vol. 56, no. 3, pp. 221-255, 2004.</p>

<p id="2">[2] B.D. Lucas, and T. Kanade, "An iterative image registration technique with an application to stereo vision", International Joint Conference on Artificial Intelligence, 1981.</p>

<p id="3">[3] S. Baker, and I. Matthews. "Equivalence and efficiency of image alignment algorithms", IEEE Conference on Computer Vision and Pattern Recognition, 2001.</p>

<p id="4">[4] A.B. Ashraf, S. Lucey, and T. Chen. "Fast Image Alignment in the Fourier Domain", IEEE Conference on Computer Vision and Pattern Recognition, 2010.</p>

<p id="5">[5] G.D. Evangelidis, and E.Z. Psarakis. "Parametric Image Alignment Using Enhanced Correlation Coefficient Maximization", IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 30, no. 10, pp. 1858-1865, 2008.</p>

<p id="6">[6] G. Tzimiropoulos, S. Zafeiriou, and M. Pantic. "Robust and Efficient Parametric Face Alignment", IEEE International Conference on Computer Vision, 2011.</p>

<p id="7">[7] E. Antonakos, J. Alabort-i-Medina, G. Tzimiropoulos, and S. Zafeiriou. "Feature-based Lucas-Kanade and Active Appearance Models", IEEE Transactions on Image Processing, vol. 24, no. 9, pp. 2617-2632, 2015.</p>
