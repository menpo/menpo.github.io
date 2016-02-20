Installation
============

We provide detailed guides for installing ``menpo`` on each of the 3 major 
operating systems. The Menpo project is designed to provide a suite of tools to 
solve a complex problem and therefore has a complex set of dependencies. In 
order to make things as simple as possible for Python developers (new and experienced), we 
advocate the use of [Conda](http://conda.pydata.org/). Therefore, our 
installation instructions focus on getting Conda installed on each of the 
platforms.

**Before we begin, please choose an operating system:**

  - [Windows](windows/index.md)
  - [OS X](osx/index.md)
  - [Linux](linux/index.md)

Upgrading
---------
Assuming you have followed the installation instructions above, you may need
to upgrade your version of Menpo to that latest. You can check if you
have the latest version by running the following commands within a Python
interpreter:

```python
>>> import menpo
>>> print(menpo.__version__)
```
If you need to upgrade, you can do this using `conda` using the command **(make
the sure the `menpo` environment is activated)**:

**OSX/Linux**

```
$ source activate menpo
(menpo) $ conda update -c menpo menpo
```
**Windows**

```
C:\>activate menpo
[menpo] C:\>conda update -c menpo menpo
``` 


Expert quick start
------------------

If you are an advanced user who is comfortable in the terminal, here's the TL;DR:

  1. Download and install
     [Miniconda](http://conda.pydata.org/miniconda.html) for your platform and architecture.
  2. Install Conda by executing the installer you just downloaded. On Linux/OS X it's a bash script:
```
$ cd ~/Downloads
$ chmod +x Miniconda-3.4.2-Linux-x86_64.sh
$ ./Miniconda-3.4.2-Linux-x86_64.sh
```
On Windows, just double-click and follow the instructions. After installing, open a terminal/command prompt and confirm you can access the `conda` command.
  4. Create a fresh conda environment by using
```
$ conda create -n menpo python
```
  5. Activate the environment. Linux/OS X:
```
$ source activate menpo
(menpo)$
```
Windows:
```
$  activate menpo
[menpo]C:\>
```
Note that post installation, when you want to come back to use Menpo, you will need to re-run this activation command to gain access to the code you are about to install. Although you might think this is a pain, it's the price to be paid for having a totally isolated Python install for Menpo.
 6. Install Menpo and **all** of it's dependencies:
```
(menpo)$ conda install -c menpo menpo
```
  7. Head over to the [notebooks page](../../notebooks.md) to begin
     experimenting with Menpo.

### Installing The Other Libraries
All of the Menpo project libraries rely on the ``menpo`` core. Therefore,
you are encouraged to follow the instructions above before attempting to install
any of the Menpo libraries. Once you have verified that ``menpo`` is correctly
installed, you can install any of the Menpo libraries within your Menpo 
environment by running one of the following commands:

**OSX/Linux**
```
$ source activate menpo
(menpo) $ conda install -c menpo menpofit
(menpo) $ conda install -c menpo menpo3d
(menpo) $ conda install -c menpo menpodetect
(menpo) $ conda install -c menpo menpowidgets
```
**Windows**

```
$ source activate menpo
(menpo) C:\>conda install -c menpo menpofit
(menpo) C:\>conda install -c menpo menpo3d
(menpo) C:\>conda install -c menpo menpodetect
(menpo) C:\>conda install -c menpo menpowidgets
```
