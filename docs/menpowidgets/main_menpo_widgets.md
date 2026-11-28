---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---


<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../_static/logo/menpowidgets.png" alt="menpowidgets" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpowidgets" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpowidgets.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpowidgets">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpowidgets/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

# Main Menpo widgets

These are the widgets for visualizing the objects of [`menpo`](../menpo/index.md). They are functions of `menpowidgets`:

| Function | Shows |
|---|---|
| `visualize_images` | a list of images, with their landmarks and options for channels, rendering and saving |
| `visualize_shapes_2d`, `visualize_shapes_3d` | a list of point clouds, graphs or meshes |
| `visualize_landmarks_2d`, `visualize_landmarks_3d` | the landmark groups of an object |
| `visualize_patches`, `visualize_patch_appearance_model` | patches extracted around landmarks |
| `visualize_shape_model_2d`, `visualize_shape_model_3d` | a multi-scale linear shape model, with a slider per component |
| `visualize_appearance_model` | a multi-scale linear appearance model |
| `visualize_meshes_3d`, `visualize_morphable_model` | 3D meshes and morphable models (with the `menpo3d` extra) |
| `plot_graph` | curves, with options for lines, markers, legend and axes |
| `view_widget` | any of the above, chosen from the type of the object |

```{note}
The widgets on this page were created when the website was built, so what you see is the initial state of each one, drawn by the real code.
The controls do not respond here, because the plots are drawn by Python: run the code in a Jupyter notebook for the interactive version.
```

## Images
`visualize_images` browses a list of images. Use `browser_style='slider'` for a slider instead of plus/minus buttons.

```{code-cell} ipython3
import menpo.io as mio
from menpowidgets import visualize_images

images = [mio.import_builtin_asset.lenna_png(), mio.import_builtin_asset.takeo_ppm()]
visualize_images(images)
```

## Shapes and landmarks

```{code-cell} ipython3
from menpowidgets import visualize_shapes_2d

shapes = [mio.import_builtin_asset.einstein_pts()['PTS'],
          mio.import_builtin_asset.takeo_pts()['PTS']]
visualize_shapes_2d(shapes)
```

```{code-cell} ipython3
from menpowidgets import visualize_landmarks_2d

visualize_landmarks_2d([image.landmarks for image in images])
```

## Patches
`visualize_patches` takes the patches in either of the two formats that `Image.extract_patches` and `Image.extract_patches_around_landmarks` return, and the centres they were taken around.

```{code-cell} ipython3
from menpowidgets import visualize_patches

image = images[0]
centres = image.landmarks['LJSON']
patches = image.extract_patches(centres, patch_shape=(16, 16))
visualize_patches([patches], [centres])
```

## Graphs

```{code-cell} ipython3
from menpowidgets import plot_graph

x = list(range(20))
plot_graph(x, [[v ** 2 for v in x], [v ** 1.5 for v in x]], legend_entries=['x squared', 'x to the 1.5'])
```

## The `view_widget` methods
The images, shapes and landmarks of `menpo` have a `view_widget()` method, which is the same as calling the function above with a list of one object:

```python
image.view_widget()
pointcloud.view_widget()
```
