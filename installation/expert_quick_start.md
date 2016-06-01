Expert Quick Start
==================

If you are an advanced user who is comfortable in the terminal, here is a quick start guide:

  1. Download and install
     [Miniconda](http://conda.pydata.org/miniconda.html) for your platform and architecture.
  2. Install Conda by executing the installer you just downloaded. On Linux/OS X it's a bash script:
     ```
     $ cd ~/Downloads
     $ chmod +x Miniconda3-latest-Linux-x86_64.sh
     $ ./Miniconda3-latest-Linux-x86_64.sh
     ```
     On Windows, just double-click and follow the instructions. After installing,
     open a terminal/command prompt and confirm you can access the `conda` command.
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
     C:\>activate menpo
     [menpo]C:\>
     ```
     Note that post installation, when you want to come back to use Menpo, you will
     need to re-run this activation command to gain access to the code you are about
     to install. Although you might think this is a pain, it's the price to be paid
     for having a totally isolated Python install for Menpo.
  6. Install all the Menpo Project packages and **all** of their dependencies:
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
  7. Head over to the [Examples](../examples/index.md) page to begin experimenting with Menpo.

     We strongly advise you to read the _User Guides_ for all the packages in order to
     understand the basic concepts behind the Menpo Project. They can be found in:
     - [`menpo`](../menpo/index.md)
     - [`menpodetect`](../menpodetect/index.md)
     - [`menpofit`](../menpofit/index.md)
     - [`menpowidgets`](../menpowidgets/index.md)
     - [`menpocli`](../menpocli/index.md)
     - [`menpo3d`](../menpo3d/index.md)
