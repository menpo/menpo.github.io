# Notebooks

These notebooks are the hands-on companion to the guides: each one is a page of this website, and **every code cell is executed whenever the site is built**,
so they always run against the current releases. To run one yourself, use the download buttons at the top of the page (Jupyter notebook, `.ipynb`) or copy the code.

The notebooks that train models need annotated face images. They were written for the [LFPW](https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/)
database and look for it in `path_to_lfpw`; on this website that variable points at a small set of faces, so the numbers and pictures are rougher than with the whole of LFPW.
Set `path_to_lfpw` to your own copy to get the full result.

Install the packages first, see [Installation](../installation/index.md).

## menpo

* [Importing built-in assets](menpo/importing-builtin-assets.md)
* [Images: basics](menpo/images-basics.md)
* [Images: features](menpo/images-features.md)
* [Images: warping](menpo/images-warping.md)
* [Landmarks: basics](menpo/landmarks-basics.md)
* [Shapes: graphs](menpo/shape-graph.md)
* [Shapes: point graphs](menpo/shape-pointgraph.md)
* [Transforms: affine](menpo/transforms-affine.md)
* [Transforms: homogeneous](menpo/transforms-homogeneous.md)
* [Transforms: piecewise affine](menpo/transforms-piecewise-affine.md)
* [Transforms: thin plate splines](menpo/transforms-thin-plate-splines.md)
* [Transforms: generalized Procrustes analysis](menpo/transforms-generalized-procrustes-analysis.md)

## menpofit

* [Active Appearance Models: basics](menpofit/aams-basics.md)
* [Active Appearance Models: advanced](menpofit/aams-advanced.md)
* [Active Template Model](menpofit/atm-basics.md)
* [Constrained Local Models](menpofit/clms-basics.md)
* [Supervised Descent Method](menpofit/sdms-basics.md)
* [Lucas-Kanade](menpofit/lucas-kanade-basics.md)
* [Derivatives of a thin plate spline](menpofit/thin-plate-splines-derivatives.md)

## menpo3d

* [Offscreen rasterization](menpo3d/rasterization-basics.md)

## menpowidgets

* [Create your own widgets](menpowidgets/create-your-own-widgets.md)

```{toctree}
:titlesonly:
:hidden:

Importing built-in assets <menpo/importing-builtin-assets>
Images: basics <menpo/images-basics>
Images: features <menpo/images-features>
Images: warping <menpo/images-warping>
Landmarks: basics <menpo/landmarks-basics>
Shapes: graphs <menpo/shape-graph>
Shapes: point graphs <menpo/shape-pointgraph>
Transforms: affine <menpo/transforms-affine>
Transforms: homogeneous <menpo/transforms-homogeneous>
Transforms: piecewise affine <menpo/transforms-piecewise-affine>
Transforms: thin plate splines <menpo/transforms-thin-plate-splines>
Transforms: generalized Procrustes analysis <menpo/transforms-generalized-procrustes-analysis>
Active Appearance Models: basics <menpofit/aams-basics>
Active Appearance Models: advanced <menpofit/aams-advanced>
Active Template Model <menpofit/atm-basics>
Constrained Local Models <menpofit/clms-basics>
Supervised Descent Method <menpofit/sdms-basics>
Lucas-Kanade <menpofit/lucas-kanade-basics>
Derivatives of a thin plate spline <menpofit/thin-plate-splines-derivatives>
Offscreen rasterization <menpo3d/rasterization-basics>
Create your own widgets <menpowidgets/create-your-own-widgets>
```
