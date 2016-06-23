IPython Notebooks
=================

  - **menpo v0.6.2** - [browse online](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.6.2/notebooks/) - [download](https://github.com/menpo/menpo-notebooks/archive/v0.6.2.zip)
  - **menpofit v0.3.1** - [browse online](http://nbviewer.jupyter.org/github/menpo/menpofit-notebooks/tree/v0.3.1/notebooks/) - [download](https://github.com/menpo/menpofit-notebooks/archive/v0.3.1.zip)

As part of the project, we maintain a set of Jupyter notebooks that help
illustrate how Menpo should be used.

The notebooks for each of the core four Menpo Libraries are kept inside their
own Github repositories.
If you wish to view the static output of the notebooks, feel free to browse
them online using the provided links. This gives a great way to passively read
the notebooks without needing a full Python environment. Note that these copies
of the notebook contain only static output and thus cannot be run directly - to
execute them you need to download them, install menpo, and open the notebook in
Jupyter.

### Running The Notebooks Locally
In order to experiment with the Menpo codebase, we suggest you download the
notebooks and run them yourself. Before being able to run the notebooks you
**must install menpo**. Head to the
[installation instructions](installation/index.md) before
continuing.

 1. Start by downloading the notebooks and extracting the zip somewhere on your
    local disk. Please substitute **NOTEBOOKS_PATH** with this path in the
    following instructions.
 2. We then need to run the notebooks using the `jupyter notebook` application.
    Begin by opening a command prompt/terminal and changing to the directory
    where you extracted the notebooks:

    **macOS/Linux**

        ::console
        $ cd NOTEBOOKS_PATH
        $ source activate menpo
        (menpo) $ jupyter notebook

    **Windows**

        ::console
        C:\>cd NOTEBOOKS_PATH
        NOTEBOOKS_PATH>activate menpo
        [menpo] NOTEBOOKS_PATH>jupyter notebook

 3. A browser should open and show the Jupyter notebook browser. Click a
    notebook to open it. You can now run the notebooks by executing each code
    cell and following the documentation provided inside the notebook. If you
    are unfamiliar with the Jupyter notebook environment, please consult
    their [documentation](http://jupyter.org).

### Previous Notebooks
These notebooks are versioned in an identical manner
to the main Menpo project. Therefore, you should make sure to use the version
of the notebooks that matches the version of Menpo you are using.

To check which version of Menpo you are using, run:

    :::python
    >>> import menpo
    >>> print(menpo.__version__)


inside of a Python interpreter.

#### menpo
  - **v0.6.1** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.6.1/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.6.1.zip)
  - **v0.6.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.6.0/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.6.0.zip)
  - **v0.5.2** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.5.2/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.5.2.zip)
  - **v0.5.1** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.5.1/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.5.1.zip)
  - **v0.5.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.5.0/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.5.0.zip)
  - **v0.4.4** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.4.4/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.4.4.zip)
  - **v0.4.3** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.4.3/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.4.3.zip)
  - **v0.4.2** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.4.2/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.4.2.zip)
  - **v0.4.1** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.4.1/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.4.1.zip)
  - **v0.4.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.4.0/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.4.0.zip)
  - **v0.3.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpo-notebooks/tree/v0.3.0/notebooks/) [download](https://github.com/menpo/menpo-notebooks/archive/v0.3.0.zip)

#### menpofit
  - **v0.3.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpofit-notebooks/tree/v0.3.0/notebooks/) [download](https://github.com/menpo/menpofit-notebooks/archive/v0.3.0.zip)
  - **v0.2.1** [browse](http://nbviewer.jupyter.org/github/menpo/menpofit-notebooks/tree/v0.2.1/notebooks/) [download](https://github.com/menpo/menpofit-notebooks/archive/v0.2.1.zip)
  - **v0.2.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpofit-notebooks/tree/v0.2.0/notebooks/) [download](https://github.com/menpo/menpofit-notebooks/archive/v0.2.0.zip)
  - **v0.1.0** [browse](http://nbviewer.jupyter.org/github/menpo/menpofit-notebooks/tree/v0.1.0/notebooks/) [download](https://github.com/menpo/menpofit-notebooks/archive/v0.1.0.zip)

