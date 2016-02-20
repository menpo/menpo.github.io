Setting Up A Development Environment
====================================

If you want to develop within the Menpo project you will need to follow a different workflow than the one described above. Although different developers follow different development workflows, we give the following advice on how to set up a **menpo** development environment. As above, the instructions for the Menpo subprojects is identical.

A brief outline of the required steps for setting up a **menpo** (or really any Python project hosted on Github) develoment environment is as follows:

  1. Clone the source code from Github
  2. Install the development requirements
  3. Install/build the **menpo** source code

#### Getting The Source Code
Go to [Github](https://github.com/menpo/menpo) and fork the **menpo** repository. This should provide you with a newly created git repository on your Github account that contains the **menpo** Python code. For the rest of the tutorial, let us assume the Github username is ``username``. You can now clone the **menpo** source to your machine:
```
$ git clone https://github.com/username/menpo.git
``` 
If you are using Windows you may want to use [Github Desktop](https://desktop.github.com/). You should now have a folder that contains all of the **menpo** source code.

#### Installing The Dependencies
We advise that you create a new ``conda`` environment for your Menpo development, which we will call ``menpo_dev``:

```
$ conda create -n menpo_dev python
$ source activate menpo_dev
(menpo_dev) $
```  
Now, it is necessary to acquire all of the **menpo** dependencies. The simplest way to do this is just ``conda install``, and then ``conda remove`` **menpo**!

```
(menpo_dev) $ conda install -c menpo menpo
(menpo_dev) $ conda remove menpo
``` 
Now all the **menpo** dependencies are satisfied and in your environment. We do this because we believe it is easier to use ``conda`` than pip to satsify the dependencies, particularly for packages such as ``vlfeat`` that have complex building processes.

### Installing A Development Copy Of **menpo**
To install a development copy of **menpo** (one that you can edit and then see those changes reflected in your environment) - we will use ``pip``. Now, it is important to note that this is contrary to the previous instructions whereby we are always using ``conda`` to satisfy our dependencies. However, ``pip`` has an excellent editable workflow and will create all the necessary ``egg`` links that are required for using source that doesn't exist directly within ``site-packages``. In short, we want to do:

```
(menpo_dev) $ conda install pip cython
(menpo_dev) $ pip install -e ./menpo --no-deps
```  
There are a few things to note:

  1. We installed ``pip`` *inside* the ``menpo_dev`` environment. ``conda`` and ``pip`` play well together - however you may only install a package using *either* ``conda`` installed *or* ``pip`` installed. If you install a package using both ``conda`` and ``pip``, the ``conda`` package will always be preferred. You can check the state of your environment by using the ``conda list`` command.
  2. We use ``pip`` to perform an editable install (``-e``), on the ``./menpo`` root source folder, and told ``pip`` **not to install any dependencies, since we already satisfied them with ``conda``**.
  3. We also installed ``Cython``. **menpo** contains a number of Cythonized files that provide access to more efficient C-based code. You will notice that during install, ``pip`` also uses ``Cython`` to build the code into Python extensions. On Linux, this should work out of the box. On OSX, you will need to install XCode. On Windows, you will need to have the correct version of Visual Studio installed for your chosen version of Python (Visual Studio 2008 for Python 2.7, Visual Studio 2010 for Python 3.4 and Visual Studio 2015 for Python 3.5). Note that setting up a working build environment on Windows is very complicated and for this reason Unix is recommended for development.
  
Now, any changes made in the **menpo** source folder will now be reflected by any Python interpreter run from within the ``menpo_dev`` ``conda`` environment.


*taken from website FAQs*
### How do I install a development version?
To install a development version of Menpo (or any of the libraries), we suggest
the following workflow:

  1. Install the latest *development* version of Menpo from conda. This will 
     install the most recently successful commit from the git repository and
     ensure you receive all the latest, correct dependencies:

        :::console
        $ conda create -n menpodev python
        $ source activate menpodev
        (menpodev) $ conda install -c menpo/channel/master menpo

  2. **Remove** Menpo so that we can install the development version from
     Github:

        :::console
        (menpodev) $ conda remove menpo

  3. Checkout the Menpo git repository. You may wish to fork the project
     on Github so that you can make pull requests back to the Menpo project. In
     this case, just replace ``https://github.com/menpo/menpo.git`` with
     ``https://github.com/GITHUB_USERNAME/menpo.git`` below:

        :::console
        (menpodev) $ git clone https://github.com/menpo/menpo.git

  4. Install *pip* **inside** the conda environment and then install an editable
     version of your Menpo repository inside:

        :::console
        (menpodev) $ conda install pip
        (menpodev) $ pip install -e ./menpo --no-deps

  5. Any edits you make within the ``./menpo`` folder will be reflected inside
     this conda environment! This procedure is identical for any of the Menpo
     libraries, primarily steps **3** and **4**.

The instructions above were specific to Unix operating systems, but Windows
should be identical outside of activating the conda environment.
