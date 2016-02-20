Title: Windows Expert Installation
url: installation/windows/expert.html
save_as: installation/windows/expert.html

We assume you are very familiar with the Windows environment and with entering
commands in to the command prompt. If you feel uncomfortable with this, or at
any time you feel confused, please refer to the
[full instructions.](index.md)

**It is important to note that as part of the installation, you will be creating
an isolated environment to execute Python inside. Make sure that this
environment is activated in order to be able to use Menpo!**

  1. Download and install
     [Miniconda for Python 2](http://conda.pydata.org/miniconda.html)
     on Windows. Make sure to choose the correct architecture (32/64) for your
     copy of Windows.
  2. After following the instructions you should be able to access `python`
     and `conda` from a command prompt.
  3. Create a fresh conda environment by using

        :::console
        C:\>conda create -n menpo python

  4. Activate the environment by executing:

        :::console
        C:\>activate menpo
        [menpo] C:\>

  5. Install Menpo and **all** of it's dependencies:

        :::console
        [menpo] C:\>conda install -c menpo menpo

  6. Head over to the [notebooks page](../../notebooks.md) to begin
     experimenting with Menpo.
