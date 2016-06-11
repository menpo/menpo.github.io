<center>
  <img src="../../logo/menpo.png" alt="menpo" width="30%">
  </br>
  </br>
  <a href="http://github.com/menpo/menpo"><img src="http://img.shields.io/github/release/menpo/menpo.svg" alt="Github Release"/></a>
  <a href="https://github.com/menpo/menpo/blob/master/LICENSE.txt"><img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/></a>
  <a href="https://coveralls.io/r/menpo/menpo"><img src="http://img.shields.io/coveralls/menpo/menpo.svg?style=flat" alt="Coverage Status"/></a>
  <img src="https://img.shields.io/badge/Python-2.7-green.svg" alt="Python 2.7 Support"/>
  <img src="https://img.shields.io/badge/Python-3.4-green.svg" alt="Python 3.4 Support"/>
  <img src="https://img.shields.io/badge/Python-3.5-green.svg" alt="Python 3.5 Support"/>
  <iframe src="https://ghbtns.com/github-btn.html?user=menpo&repo=menpo&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>
  </br>
</center>

`menpo` is a Python package designed from the ground up to make importing, manipulating and visualizing image and mesh data as simple as possible.
In particular, sparse locations on either images or meshes, referred to as **landmarks** within `menpo`, are tightly coupled with their reference objects.
Thus, `menpo` focuses on **annotated** data which is common within the fields of Machine Learning and Computer Vision.
All core types are `Landmarkable` and visualizing these landmarks is very simple. Since landmarks are first class
citizens within the Menpo Project, it makes tasks like masking images, cropping images
inside landmarks and aligning images very simple.

Note that `menpo` is designed to be a core library for implementing algorithms within the Machine Learning and Computer Vision fields.
It is a very powerful toolkit and even though it can be used as a stand-alone package,
its main purpose is to serve as the base library for the rest of the Menpo Project's packages,
such as [`menpofit`](../menpofit/index.md), [`menpodetect`](../menpodetect/index.md),
[`menpowidgets`](../menpowidgets/index.md), [`menpo3d`](../menpo3d/index.md) etc.

The following user guide is a general introduction to `menpo`, aiming to provide a bird's eye of `menpo`'s design.
It is also very helpful for understanding the main philosophy behind all the packages of the Menpo Project.
The contents of this user guide are:
1. [Introduction](introduction.md)
2. [Data Types](datatypes.md)
3. [Consistency](consistency.md)
4. [Vectorizing](vectorizing.md)
5. [Visualization](visualization.md)
