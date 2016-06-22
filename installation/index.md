Installation
============


<center>
  <div>Here is a div</div>
  <a href="http://github.com/menpo/menpofit"><img src="http://img.shields.io/github/release/menpo/menpofit.svg" alt="Github Release"/></a>
  <a href="https://github.com/menpo/menpofit/blob/master/LICENSE.txt"><img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/></a>
  <img src="https://img.shields.io/badge/Python-2.7-green.svg" alt="Python 2.7 Support"/>
  <img src="https://img.shields.io/badge/Python-3.4-green.svg" alt="Python 3.4 Support"/>
  <img src="https://img.shields.io/badge/Python-3.5-green.svg" alt="Python 3.5 Support"/>
  <iframe src="https://ghbtns.com/github-btn.html?user=menpo&repo=menpofit&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>
  </br>
</center>

The _Menpo Project_ supports Windows, macOS, and Linux.
Given that the Menpo project is designed to provide a suite of tools to
solve complex problems, it therefore has a complex set of dependencies.
In order to make things as simple as possible for Python developers (new and experienced),
we advocate the use of [Conda](http://conda.pydata.org/). Therefore, our
installation instructions focus on getting Conda installed on each of the
platforms.

#### Installation Instructions
We provide detailed guides for installing the Menpo Project.
Choose an operating system:

  - [Windows](windows/index.md)
  - [macOS](macos/index.md)
  - [Linux](linux/index.md)

#### Expert Quick Start
If you are an advanced user who is comfortable in the terminal, use the following quick start guide:
  - [Quick Start](expert_quick_start.md)

#### Setting Up A Development Environment
If you want to develop within the Menpo Project, please read the following guide:
  - [Development Setup](development.md)

---------------------------------------

Upgrading
=========
Assuming you have followed the installation instructions above, you may need
to upgrade your version of the Menpo Project packages to the latest. You can check if you
have the latest version by running the following commands within a Python
interpreter:

```python
>>> import menpo
>>> print(menpo.__version__)
```
Similarly for `menpofit`, `menpodetect`, `menpowidgets`, `menpo3d` and `menpocli`.
If you need to upgrade, you can do this using `conda` **(make
sure the `menpo` environment is activated)**.

##### macOS/Linux
To upgrade all packages (`menpofit`, `menpodetect`, `menpowidgets`, `menpocli`) do:
```
$ source activate menpo
(menpo) $ conda update -c menpo menpoproject
```
To explicitly upgrade a specific package do:
```
$ source activate menpo
(menpo) $ conda update -c menpo menpo
(menpo) $ conda update -c menpo menpofit
(menpo) $ conda update -c menpo menpodetect
(menpo) $ conda update -c menpo menpowidgets
(menpo) $ conda update -c menpo menpocli
(menpo) $ conda update -c menpo menpo3d
```

##### Windows
To upgrade all packages (`menpofit`, `menpodetect`, `menpowidgets`, `menpocli`) do:
```
C:\>activate menpo
[menpo] C:\>conda update -c menpo menpoproject
```
To explicitly upgrade a specific package do:
```
C:\>activate menpo
[menpo] C:\>conda update -c menpo menpo
[menpo] C:\>conda update -c menpo menpofit
[menpo] C:\>conda update -c menpo menpodetect
[menpo] C:\>conda update -c menpo menpowidgets
[menpo] C:\>conda update -c menpo menpocli
[menpo] C:\>conda update -c menpo menpo3d
```
