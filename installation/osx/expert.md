Title: OS X Expert Installation
url: installation/osx/expert.html
save_as: installation/osx/expert.html

We assume you are very familiar with the OS X environment and with entering
commands inside a terminal. If you feel uncomfortable with this, or at
any time you feel confused, please refer to the
[full instructions.](index.md)

**It is important to note that as part of the installation, you will be creating
an isolated environment to execute Python inside. Make sure that this
environment is activated in order to be able to use Menpo!**

  1. Download and install
     [Miniconda for Python 2](http://conda.pydata.org/miniconda.html)
     on OS X.
  2. Install Conda by executing the installation script you just downloaded:

        ::console
        $ cd ~/Downloads
        $ chmod +x Miniconda-3.4.2-MacOSX-x86_64.sh
        $ ./Miniconda-3.4.2-MacOSX-x86_64.sh

  3. After following the instructions you should be able to access `conda` from
     a terminal.
  4. Create a fresh conda environment by using

        :::console
        $ conda create -n menpo python

  5. Activate the environment by executing:

        :::console
        $ source activate menpo
        (menpo)$

  6. Install Menpo and **all** of it's dependencies:

        :::console
        (menpo)$ conda install -c menpo menpo

  7. Head over to the [notebooks page](../../notebooks.md) to begin
     experimenting with Menpo.
