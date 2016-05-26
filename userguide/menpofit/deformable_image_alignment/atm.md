Active Template Model
=====================

1. [Definition](#definition)
2. [Parametric Shape Model](#shape_model)
3. [References](#references)

---------------------------------------

### <a name="definition"></a>1. Definition
The aim of deformable image alignment is to find the optimal alignment between a constant template $$\bar{\mathbf{a}}$$ and an input image $$\mathbf{t}$$
with respect to the parameters of a parametric motion model. Note that both $$\bar{\mathbf{a}}$$ and $$\mathbf{t}$$ are vectorized.
The motion model consists of a Warp function $$\mathcal{W}(\mathbf{x},\mathbf{p})$$ which maps each point $$\mathbf{x}$$ within a target (reference) shape to its corresponding
location in a shape instance. The identity warp is defined as $$\mathcal{W}(\mathbf{x},\mathbf{0})=\mathbf{x}$$.
In the case of Active Template Model (ATM), the warp function is driven by a parametric shape model, where $$\mathbf{p}$$ is the set of *shape parameters*.

Note that we invented the name "Active Template Model" for the purpose of the Menpo Project. The term is not established in literature.
The cost function of an ATM is exactly the same as in the case of [Lucas-Kanade](../affine_image_alignment/lk.md) for Affine Image Alignment.
Specifically, it has the form
$$
\arg\min_{\mathbf{p}} \left\lVert \bar{\mathbf{a}} - \mathbf{t}(\mathcal{W}(\mathbf{p})) \right\rVert^{2}
$$
The difference has to do with the nature of the transform - and thus $$\mathbf{p}$$ - that is used in the motion model $$\mathcal{W}(\mathbf{p})$$.

with respect to the motion model parameters $$\mathbf{p}$$. Let's load an image $$\mathbf{t}$$ and create a template from it $$\bar{\mathbf{a}}$$
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
  <img src="template.png" alt="template">
</center>


### <a name="shape_model"></a>2. Parametric Shape Model
