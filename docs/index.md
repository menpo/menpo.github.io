---
html_theme.sidebar_secondary.remove: true
---

# The Menpo Project

<div class="hero">
  <img class="hero_logo" src="_static/logo/menpoproject.png" alt="The Menpo Project">
  <div class="hero_text">
    <h1>The Menpo Project</h1>
    <p class="tagline">The Python framework for deformable modelling</p>
    <div class="hero_buttons">
      <a href="installation/index.html"><button class="download_button">Get started</button></a>
      <a href="https://github.com/menpo"><button class="download_button secondary_button">GitHub</button></a>
    </div>
    <pre><code>pip install menpo menpofit</code></pre>
  </div>
</div>

:::{div} hero_note
Python {{ menpo_requires_python }} on Linux, macOS and Windows
:::

The Menpo Project is a set of BSD licensed Python frameworks and associated tooling that provide end-to-end solutions for 2D and 3D deformable modelling.
The project includes training and fitting code for state-of-the-art methods such as:

::::{grid} 1 2 2 2
:gutter: 0

:::{grid-item}
* Active Appearance Model (AAM)
* Supervised Descent Method (SDM)
* Ensemble of Regression Trees (ERT), powered by [dlib](http://dlib.net/)
* Constrained Local Model (CLM)
:::
:::{grid-item}
* Active Shape Model (ASM)
* Active Pictorial Structures (APS)
* Lucas-Kanade (LK) and Active Template Model (ATM)
:::
::::

It also provides generic **object detection** in terms of a bounding box, an **elegant standard library** with simple dependencies that is useful for
many areas of computer vision, and sophisticated visualization with **interactive Jupyter widgets**.
All of the code is Open Source and can be found in the [Menpo GitHub organisation](https://github.com/menpo/).

## Packages

The Menpo Project is a family of packages, each designed to solve one problem well.

::::{grid} 1 2 3 3
:gutter: 3

:::{grid-item-card} menpo
:link: menpo/index
:link-type: doc
:img-top: _static/logo/menpo.png
:class-card: package-card

The heart of the project: the data containers, I/O, transforms, features and visualization that everything else is built on.
It has minimal dependencies and is useful for computer vision well beyond deformable modelling.
:::

:::{grid-item-card} menpofit
:link: menpofit/index
:link-type: doc
:img-top: _static/logo/menpofit.png
:class-card: package-card

State-of-the-art 2D deformable models, each with training and fitting code: AAM, ATM, APS, CLM, SDM, ERT and Lucas-Kanade.
:::

:::{grid-item-card} menpowidgets
:link: menpowidgets/index
:link-type: doc
:img-top: _static/logo/menpowidgets.png
:class-card: package-card

Interactive Jupyter widgets to explore images, shapes, models and fitting results.
:::

:::{grid-item-card} menpodetect
:link: menpodetect/index
:link-type: doc
:img-top: _static/logo/menpodetect.png
:class-card: package-card

Object detectors (dlib, OpenCV) that return the bounding boxes `menpofit` starts from. Check each detector's own licence.
:::

:::{grid-item-card} menpo3d
:link: menpo3d/index
:link-type: doc
:img-top: _static/logo/menpo3d.png
:class-card: package-card

Importing, visualizing, rasterizing and registering 3D meshes, with an interactive moderngl viewer.
:::

:::{grid-item-card} Notebooks
:link: notebooks/index
:link-type: doc
:img-top: _static/logo/menpoproject.png
:class-card: package-card

Jupyter notebooks that show how the packages are used together, from importing data to fitting a model.
:::
::::

## Next steps

Head to the [installation instructions](installation/index.md) to get started, then read the [menpo guide](menpo/index.md) for the core concepts,
and the [menpofit guide](menpofit/index.md) to train and fit your first model.

## User group and issues

If you have found a bug, or if any part of Menpo behaves in a way you do not expect, please raise an issue on the corresponding package on
[GitHub](https://github.com/menpo/). For theoretical questions, or if you are having problems setting up or using the Menpo Project,
visit the [user group](https://groups.google.com/g/menpo-users).

```{toctree}
:hidden:
:titlesonly:

Installation </installation/index>
menpo </menpo/index>
menpofit </menpofit/index>
menpowidgets </menpowidgets/index>
menpo3d </menpo3d/index>
menpodetect </menpodetect/index>
Notebooks </notebooks/index>
About </about>
```
