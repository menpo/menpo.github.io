Conda installation
==================

[Conda](http://conda.pydata.org/) is a popular open-source framework for distributing Python applications.

It's an alternative to _PyPI_ and `pip` which addresses some shortcomings in these models by adding the ability to ship pre-compiled code for native modules _and_ to ship binary dependencies (like OpenCV, VTK and FFMPEG). Although this is more work for the maintainers of projects (i.e. us!), if we put the work in, we can ship code that simply unpacks and works on Windows, macOS, and Linux.

Given that the Menpo project is designed to provide a suite of tools to
solve complex problems, it therefore has a complex set of dependencies.
In order to make things as simple as possible for Python developers (new and experienced),
we strongly advocate the use of [Conda](http://conda.pydata.org/). 

Once you have conda installed, getting the latest stable version of menpo is a one line command:
```
> conda install -c conda-forge menpo
```
Therefore, our installation instructions focus on getting Conda installed on each of the platforms we support.

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
Similarly for `menpofit`, `menpodetect`, `menpo3d` and `menpocli`.
If you need to upgrade, you can do this using `conda` **(make
sure the `menpo` environment is activated)**.

##### macOS/Linux
To upgrade all packages (`menpofit`, `menpodetect`, `menpo`, `menpo3d`) do:
```
$ source activate menpo
(menpo) $ conda update -c conda-forge menpo menpodetect menpofit menpo3d
```
To explicitly upgrade a specific package do:
```
$ source activate menpo
(menpo) $ conda update -c conda-forge menpo
(menpo) $ conda update -c conda-forge menpofit
(menpo) $ conda update -c conda-forge menpodetect
(menpo) $ conda update -c conda-forge menpocli
(menpo) $ conda update -c conda-forge menpo3d
```

##### Windows
Maintaining and building packages for Windows is very difficult for Open Source
projects - particularly when none of the core developers maintain Windows
development machines. For this reason, the Menpo Project is not maintained for
Windows and we do not test nor provide automated builds on this platform.