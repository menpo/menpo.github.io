---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.7
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Offscreen Rasterization Basics

`menpo3d.rasterize` turns a 3D mesh into an image: the colour of the mesh as seen from a camera, or, for every pixel, which triangle covers it and where
inside that triangle (its barycentric coordinates). There are two rasterizers. `GLRasterizer` draws with OpenGL (through [moderngl](https://moderngl.readthedocs.io), offscreen,
so no window is needed). `rasterize_barycentric_coordinate_images` is a plain NumPy version for when there is no OpenGL.

To begin, we need a mesh. The camera of the default rasterizer looks along the z axis at the clip volume $[-1, 1]^3$, so we centre the bunny, scale it into that cube, and
colour each vertex by its position:

```{code-cell} ipython3
import numpy as np
import menpo3d.io as m3io
from menpo.shape import ColouredTriMesh
from menpo.transform import Translation, UniformScale

bunny = m3io.import_builtin_asset.bunny_obj()
centred = Translation(-bunny.centre()).apply(bunny)
scaled = UniformScale(0.9 / np.abs(centred.points).max(), 3).apply(centred)

colours = (scaled.points - scaled.points.min(axis=0)) / np.ptp(scaled.points, axis=0)
mesh = ColouredTriMesh(scaled.points, scaled.trilist, colours=colours)
mesh
```

## Rasterizing to an image
A `GLRasterizer` has the size of the output and the model, view and projection matrices of the camera (the identity by default):

```{code-cell} ipython3
from menpo3d.rasterize import GLRasterizer

rasterizer = GLRasterizer(width=400, height=400)
rgb_image = rasterizer.rasterize_mesh(mesh)
rgb_image
```

The result is a `MaskedImage`. The mask shows which pixels the mesh covers; the others were never touched by the shader.

```{code-cell} ipython3
rgb_image.view();
```

```{code-cell} ipython3
rgb_image.mask.view();
```

## Moving the camera
The camera is the 4x4 `view_matrix` (and `projection_matrix`, and the `model_matrix` of the mesh). Here we turn the camera by 60 degrees around the vertical axis:

```{code-cell} ipython3
theta = np.deg2rad(60)
view_matrix = np.eye(4)
view_matrix[:3, :3] = [[np.cos(theta), 0, np.sin(theta)],
                       [0, 1, 0],
                       [-np.sin(theta), 0, np.cos(theta)]]

turned = GLRasterizer(width=400, height=400, view_matrix=view_matrix)
turned.rasterize_mesh(mesh).view();
```

```{admonition} The camera of the interactive viewer
:class: note
`mesh.view()` has its own camera, described by an azimuth, an elevation, a distance, a target and a field of view. `renderer.figure.get_pose()` returns
it and `set_pose` restores it, see [menpo3d](../../menpo3d/index.md). The rasterizer takes matrices, not that description.
```

## Which triangle, and where in it
For every pixel the rasterizer can give the index of the triangle that covers it and the barycentric coordinates of the pixel in that triangle. These
two images are all that is needed to interpolate any per-vertex quantity (colours, normals, a shape) across the image:

```{code-cell} ipython3
tri_indices, bcoords = rasterizer.rasterize_barycentric_coordinate_image(mesh)
tri_indices.shape, bcoords.shape
```

```{code-cell} ipython3
mask = tri_indices.mask.pixels[0]
print("pixels covered by the mesh:", mask.sum())
print("largest triangle index:", tri_indices.pixels[0][mask].max(), "of", mesh.n_tris)
print("barycentric coordinates sum to one:", np.allclose(bcoords.pixels.sum(axis=0)[mask], 1, atol=1e-4))
```

## Without OpenGL
The NumPy rasterizer takes a mesh that is already in image coordinates (x and y are pixels, z is the depth) and returns the same two images.
`model_to_image_transform` of a `GLRasterizer` maps a mesh from the model to image coordinates:

```{code-cell} ipython3
from menpo3d.rasterize import rasterize_barycentric_coordinate_images

mesh_in_image = rasterizer.model_to_image_transform.apply(mesh)
bcoords_cpu, tri_indices_cpu = rasterize_barycentric_coordinate_images(mesh_in_image, (400, 400))

gl_mask = tri_indices.mask.pixels[0]
cpu_mask = tri_indices_cpu.mask.pixels[0]
print("the two rasterizers cover the same pixels (IoU): {:.3f}".format((gl_mask & cpu_mask).sum() / (gl_mask | cpu_mask).sum()))
```
