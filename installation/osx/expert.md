OS X Expert Installation
========================

**It is important to note that as part of the installation, you will be creating
an isolated environment to execute Python inside. Make sure that this
environment is activated in order to be able to use Menpo!**

  1. Download and install [Miniconda](http://conda.pydata.org/miniconda.html)
     either for Python 2 or for Python 3 on OS X.
  2. Install Conda by executing the installation script you just downloaded:

        ```
        $ cd ~/Downloads
        $ chmod +x Miniconda3-latest-MacOSX-x86_64.sh
        $ ./Miniconda3-latest-MacOSX-x86_64.sh
        ```

  3. After following the instructions you should be able to access `conda` from
     a terminal.
  4. Create a fresh conda environment by using

        ```
        $ conda create -n menpo python
        ```

  5. Activate the environment by executing:

        ```
        $ source activate menpo
        (menpo)$
        ```

  6. Install the whole Menpo Project and **all** of its dependencies:

        ```
        (menpo)$ conda install -c menpo menpoproject
        ```

     If you don't need all the packages, you can explicitly install a specific package
     with its dependencies as:

        ```
        (menpo)$ conda install -c menpo menpo
        (menpo)$ conda install -c menpo menpofit
        (menpo)$ conda install -c menpo menpodetect
        (menpo)$ conda install -c menpo menpowidgets
        (menpo)$ conda install -c menpo menpocli
        (menpo)$ conda install -c menpo menpo3d
        ```

  7. Head over to the [Examples](../../examples/index.md) page to begin
     experimenting with Menpo.

     We strongly advise you to read the _User Guides_ for all the packages in order to
     understand the basic concepts behind the Menpo Project. They can be found in:
     - [`menpo`](../../menpo/index.md)
     - [`menpodetect`](../../menpodetect/index.md)
     - [`menpofit`](../../menpofit/index.md)
     - [`menpowidgets`](../../menpowidgets/index.md)
     - [`menpocli`](../../menpocli/index.md)
     - [`menpo3d`](../../menpo3d/index.md)
