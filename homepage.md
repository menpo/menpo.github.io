<center>
  <img src="logo/menpoproject_white_medium.png" alt="The Menpo Project" width="30%"></br>
  <strong style="font-size: 250%">The Menpo Project</strong>
</center>

<!---
MAIN DESCRIPTION
-->
The Menpo Project is an ecosystem of open-source software based on Python that provides end-to-end solution for 2D and 3D deformable modeling. The project includes training and fitting code for various state-of-the-art methods such as:

* **Active Appearance Model (AAM)**
* **Supervised Descent Method (SDM)**
* **Ensemble of Regression Trees (ERT)** (powered by [dlib](http://dlib.net/ "dlib C++ Library"))
* **Constrained Local Model (CLM)**
* **Active Shape Model (ASM)**
* **Active Pictorial Structures (APS)**
* **Lucas-Kanade (LK)** and **Active Template Model (ATM)**

The Menpo Project also provides:
* a web-based tool for **annotation of bulk data** for model training
* a **command line tool** for landmark localisation with state-of-the-art **pre-trained** models
* generic **object detection** in terms of a bounding box
* a **benchmarking suite** to fairly evalulate the performance of methods
* fancy visualization with **interactive widgets**

---------------------------------------

## Packages
<center>
  <a href="/menpo/index.md" title="menpo"><img src="logo/menpo_white_medium.png" alt="menpo" width="13%"></a>
  <a href="/menpofit/index.md" title="menpofit"><img src="logo/menpofit_white_medium.png" alt="menpofit" width="13%"></a>
  <a href="/menpodetect/index.md" title="menpodetect"><img src="logo/menpodetect_white_medium.png" alt="menpodetect" width="13%"></a>
  <a href="/menpowidgets/index.md" title="menpowidgets"><img src="logo/menpowidgets_white_medium.png" alt="menpowidgets" width="13%"></a>
  <a href="/menpo3d/index.md" title="menpo3d"><img src="logo/menpo3d_white_medium.png" alt="menpo3d" width="13%"></a>
  <a href="/menpocli/index.md" title="menpocli"><img src="logo/menpocli_white_medium.png" alt="menpocli" width="13%"></a>
  <a href="/landmarker.io/index.md" title="landmarker.io"><img src="logo/landmarkerio_white_medium.png" alt="landmarker.io" width="13%"></a>
</center>
The majority of the software exists within a family of Python packages, each designed to solve one problem well:

  - <strong style="font-size: 125%">``menpo``</strong> - The heart of the Menpo Project. `menpo` contains all core functionality needed for
    the project in well tested, mature, stable package. `menpo` is the `numpy` of the Menpo ecosystem - the foundation upon which all else is built.  
    [![Github Release][m_shield]][m_gh] [![BSD License][bsd_shield]][m_lic] ![Python 2.7 Support][python27] ![Python 3.4 Support][python34] ![Python 3.5 Support][python35] [![Coverage Status][cm_shield]][cm]

  - <strong style="font-size: 125%">``menpofit``</strong> - It includes implementations of state-of-the-art 2D deformable models. Each implementation
    includes training and fitting code. `menpofit` contains the crown jewels of the Menpo Project - most people are interested in using
    the Menpo Project for the `menpofit` package.  
    [![Github Release][mf_shield]][mf_gh] [![BSD License][bsd_shield]][mf_lic] ![Python 2.7 Support][python27] ![Python 3.4 Support][python34] ![Python 3.5 Support][python35]

  - <strong style="font-size: 125%">``menpodetect``</strong> - It wraps a number of existing projects that provide functionalities for training and
    fitting generic object detection techniques. It is designed in order to have full compatibility with `menpofit`. Not all of the wrapped
    projects fall under the same BSD license and so care must be taken when using this project to adhere to the sub-project licenses.  
    [![Github Release][md_shield]][md_gh] [![BSD License][bsd_shield]][md_lic] ![Python 2.7 Support][python27] ![Python 3.4 Support][python34] ![Python 3.5 Support][python35] [![Coverage Status][cmd_shield]][cmd]

  - <strong style="font-size: 125%">``menpo3d``</strong> - A specialized library for working with 3D data. It is largely separate from the
    core `menpo` library as it has dependencies on a number of large, 3D specific projects (like `VTK`, `mayavi`, `assimp`) which many people using
    the Menpo Project would have no use for. You'll want to install `menpo3d` if you need to import and export 3D mesh data or perform advanced mesh processing.  
    [![Github Release][m3d_shield]][m3d_gh] [![BSD License][bsd_shield]][m3d_lic] ![Python 2.7 Support][python27]

  - <strong style="font-size: 125%">``menpowidgets``</strong> - A key goal of the Menpo Project is to accelerate research in 2D and 3D computer vision by
    providing powerful visualization tools. `menpowidgets` contains a collection of Jupyter Notebook Widgets for fancy visualization and interactive
    inspection of the state of all Menpo objects.  
    [![Github Release][mw_shield]][mw_gh] [![BSD License][bsd_shield]][mw_lic] ![Python 2.7 Support][python27] ![Python 3.4 Support][python34] ![Python 3.5 Support][python35]

  - <strong style="font-size: 125%">``menpocli``</strong> - Command Line Interface (CLI) for the Menpo Project that allows to readily use pre-trained
    state-of-the-art `menpofit` facial models. This is useful for people that only care to quickly acquire facial landmarks on their images.  
    [![Github Release][mc_shield]][mc_gh] [![BSD License][bsd_shield]][mc_lic] ![Python 2.7 Support][python27] ![Python 3.4 Support][python34] ![Python 3.5 Support][python35]

  - <strong style="font-size: 125%"> [``landmarker.io``](https://www.landmarker.io)</strong> - An interactive web-based tool for manual annotation of
    2D images and 3D meshes. Useful to quickly landmark a single image, or organize a large annotation effort for thousands of files.
    Features like Snap Mode and Dropbox compatibility make it unique.  
    [![Github Release][lm_shield]][lm_gh] [![BSD License][bsd_shield]][lm_lic]


  [bsd_shield]: http://img.shields.io/badge/License-BSD-green.svg
  [m_shield]: http://img.shields.io/github/release/menpo/menpo.svg
  [m_gh]: http://github.com/menpo/menpo
  [m_lic]: https://github.com/menpo/menpo/blob/master/LICENSE.txt
  [mf_shield]: http://img.shields.io/github/release/menpo/menpofit.svg
  [mf_gh]: http://github.com/menpo/menpofit
  [mf_lic]: https://github.com/menpo/menpofit/blob/master/LICENSE.txt
  [m3d_shield]: http://img.shields.io/github/release/menpo/menpo3d.svg
  [m3d_gh]: http://github.com/menpo/menpo3d
  [m3d_lic]: https://github.com/menpo/menpo3d/blob/master/LICENSE.txt
  [md_shield]: http://img.shields.io/github/release/menpo/menpodetect.svg
  [md_gh]: http://github.com/menpo/menpodetect
  [md_lic]: https://github.com/menpo/menpodetect/blob/master/LICENSE.txt
  [mw_shield]: http://img.shields.io/github/release/menpo/menpowidgets.svg
  [mw_gh]: http://github.com/menpo/menpowidgets
  [mw_lic]: https://github.com/menpo/menpowidgets/blob/master/LICENSE.txt
  [mc_shield]: http://img.shields.io/github/release/menpo/menpocli.svg
  [mc_gh]: http://github.com/menpo/menpocli
  [mc_lic]: https://github.com/menpo/menpocli/blob/master/LICENSE.txt
  [mc_shield]: http://img.shields.io/github/release/menpo/menpocli.svg
  [mc_gh]: http://github.com/menpo/menpocli
  [mc_lic]: https://github.com/menpo/menpocli/blob/master/LICENSE.txt
  [lm_shield]: http://img.shields.io/github/release/menpo/landmarkerio.svg
  [lm_gh]: http://github.com/menpo/landmarker.io
  [lm_lic]: https://github.com/menpo/landmarker.io/blob/master/LICENSE
  [python27]: https://img.shields.io/badge/Python-2.7-green.svg
  [python34]: https://img.shields.io/badge/Python-3.4-green.svg
  [python35]: https://img.shields.io/badge/Python-3.5-green.svg
  [cm]: https://coveralls.io/r/menpo/menpo
  [cm_shield]: http://img.shields.io/coveralls/menpo/menpo.svg?style=flat
  [cmd]: https://coveralls.io/r/menpo/menpodetect
  [cmd_shield]: http://img.shields.io/coveralls/menpo/menpodetect.svg?style=flat


---------------------------------------

## Why 'Menpo'?

> Menpo were facial armours which covered all or part of the face and provided
> a way to secure the top-heavy kabuto (helmet). The Shinobi-no-o (chin cord)
> of the kabuto would be tied under the chin of the menpo. There were small
> hooks called ori-kugi or posts called odome located on various places to
> help secure the kabuto's chin cord.
>
> --- [Wikipedia, Menpo](https://en.wikipedia.org/wiki/Mempo)

---------------------------------------

## Get Started

The Menpo Project is written in **Python** and we provide a simple and easy method of installation using [Conda](http://conda.pydata.org/).
After setting up a Python ``conda`` environment, all the packages of the Menpo Project can be installed as
```
conda install -c menpo menpoproject
```
We _strongly_ suggest you head over to the [installation instructions](installation/index.md "Full Installation Instructions") to get started.
We recommend the use of ``conda`` due to the fact that the Menpo Project also includes compiled ``C/C++`` code
which may be complicated to compile on various platforms.

## User Group and Issues
If you wish to get in contact with the Menpo developers, you can do so via various channels.
If you have found a bug, or if any part of Menpo behaves in a way you do not expect, please raise an issue on the corresponding package on [Github](https://github.com/menpo/ "The Menpo Project on Github").

If you want to ask a theoretical question, or are having problems setting up or using the Menpo Project, please visit the [user group](https://groups.google.com/forum/#!forum/menpo-users "menpo-users").

Follow [@teammenpo](www.twitter.com/teammenpo "The Menpo Project on Twitter") for updates on the Menpo Project, or tweet at us any questions you have.
