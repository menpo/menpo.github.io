Windows Expert Installation
===========================

**It is important to note that as part of the installation, you will be creating
an isolated environment to execute Python inside. Make sure that this
environment is activated in order to be able to use Menpo!**

  1. Download and install [Miniconda](http://conda.pydata.org/miniconda.html)
     either for Python 2 or for Python 3 on Windows. Make sure to choose the correct architecture (32/64) for your copy of Windows.
  2. After following the instructions you should be able to access `python`
     and `conda` from a command prompt.
  3. Create a fresh conda environment by using

        ```
        C:\>conda create -n menpo python
        ```

  4. Activate the environment by executing:

        ```
        C:\>activate menpo
        [menpo] C:\>
        ```

  5. Install the whole Menpo Project and **all** of its dependencies:

        ```
        [menpo] C:\>conda install -c menpo menpoproject
        ```

     If you don't need all the packages, you can explicitly install a specific package
     with its dependencies as:

        ```
        [menpo] C:\>conda install -c menpo menpo
        [menpo] C:\>conda install -c menpo menpofit
        [menpo] C:\>conda install -c menpo menpodetect
        [menpo] C:\>conda install -c menpo menpowidgets
        [menpo] C:\>conda install -c menpo menpocli
        [menpo] C:\>conda install -c menpo menpo3d
        ```

  6. Head over to the [Examples](../../examples/index.md) page to begin
     experimenting with Menpo.

     We strongly advise you to read the _User Guides_ for all the packages in order to
     understand the basic concepts behind the Menpo Project. They can be found in:
     - [`menpo`](../../menpo/index.md)
     - [`menpodetect`](../../menpodetect/index.md)
     - [`menpofit`](../../menpofit/index.md)
     - [`menpowidgets`](../../menpowidgets/index.md)
     - [`menpocli`](../../menpocli/index.md)
     - [`menpo3d`](../../menpo3d/index.md)
