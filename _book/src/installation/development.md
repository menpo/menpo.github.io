Setting Up A Development Environment
====================================
A brief outline of the required steps for setting up a develoment environment is as follows:

  1. [Clone the source code from Github](#clone)
  2. [Install the dependencies](#dependencies)
  3. [Install and build the source code](#install)

The steps below are focused on the `menpo` package. However, the procedure is identical
for all the packages of the Menpo Project (`menpofit`, `menpodetect`, `menpocli`, `menpo3d`).

---------------------------------------

### 1. Clone The Source Code From Github {#clone}
Go to [Github](https://github.com/menpo/menpo) and fork the `menpo` repository,
so that you can make pull requests back to the Menpo project.
This should provide you with a newly created repository on your Github
account that contains the `menpo` Python code. For the rest of the tutorial,
let us assume the Github username is ``username``. You can now clone the `menpo`
source to your machine:
```
$ git clone https://github.com/username/menpo.git
```
You can also add an `upstream` remote that links to the `menpo` repository of the Menpo organization.
```
$ git remote add upstream https://github.com/menpo/menpo.git
```
This will allow you to fetch/merge the latest changes on our repository.
If you are using Windows you may want to use [Github Desktop](https://desktop.github.com/).
You should now have a folder that contains all of the `menpo` source code.


### 2. Install The Dependencies {#dependencies}
We advise that you create a new `conda` environment for your Menpo development,
which we will call ``menpo_dev``:
```
$ conda create -n menpo_dev python
$ source activate menpo_dev
(menpo_dev) $
```  
Now, it is necessary to acquire all of the `menpo` dependencies. The simplest way to do
this is just ``conda install`` and then ``conda remove`` the `menpo` package!
Additionally, it is preferable to install the latest *development* version of `menpo`
from `conda`. This will install the most recently successful commit from the `git`
repository and ensure you receive all the latest, correct dependencies.
```
(menpo_dev) $ conda install -c menpo/channel/master menpo
(menpo_dev) $ conda remove menpo
```
Now all the `menpo` dependencies are satisfied and in your environment. We do
this because we believe it is easier to use `conda` than `pip` to satisfy the dependencies,
particularly for packages such as ``vlfeat`` that have complex building processes.


### 3. Install And Build The Source Code {#install}
To install a development copy of `menpo` (one that you can edit and then see those
changes reflected in your environment) - we will use `pip`. Now, it is important
to note that this is contrary to the previous instructions whereby we are always using `conda`
to satisfy our dependencies. However, `pip` has an excellent editable workflow and
will create all the necessary ``egg`` links that are required for using source that
doesn't exist directly within ``site-packages``. In short, we want to do:
```
(menpo_dev) $ conda install pip cython
(menpo_dev) $ pip install -e ./menpo --no-deps
```  
There are a few things to note:

  1. We installed `pip` *inside* the ``menpo_dev`` environment. `conda` and `pip` play well
  together - however you may only install a package using *either* `conda` installed *or* `pip` installed.
  If you install a package using both `conda` and `pip`, the `conda` package will always be preferred.
  You can check the state of your environment by using the ``conda list`` command.
  2. We use `pip` to perform an editable install (``-e``), on the ``./menpo`` root source folder,
  and told `pip` **not to install any dependencies, since we already satisfied them with `conda`**.
  3. We also installed `cython`. `menpo` contains a number of Cythonized files that provide
  access to more efficient C-based code. You will notice that during install, `pip` also uses `cython`
  to build the code into Python extensions. On Linux, this should work out of the box. On macOS,
  you will need to install XCode. On Windows, you will need to have the correct version of
  Visual Studio installed for your chosen version of Python (Visual Studio 2008 for Python 2.7,
  Visual Studio 2010 for Python 3.4 and Visual Studio 2015 for Python 3.5). Note that
  setting up a working build environment on Windows is very complicated and
  for this reason Unix is recommended for development.

**Congratulations! You successfully installed a development version of `menpo`!**
Now, any changes you make within the `./menpo` source folder will be reflected by any Python
interpreter run from within the ``menpo_dev`` `conda` environment.
