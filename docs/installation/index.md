# Installation

The Menpo Project is pure Python (Python {{ menpo_requires_python }}) and runs on Linux, macOS (Intel and Apple Silicon)
and Windows. Install it with `pip` or from conda-forge; there are no compilers or system libraries to set up.

## pip

Create an environment and install the packages you need:

```bash
python -m venv menpo-env
source menpo-env/bin/activate        # Windows: menpo-env\Scripts\activate
pip install menpo menpofit menpowidgets menpodetect menpo3d
```

Each package is independent, so install only what you use. `menpo` is the core library;
the others depend on it.

## conda

All five packages are on [conda-forge](https://conda-forge.org):

```bash
conda create -n menpo -c conda-forge python menpo menpofit menpowidgets menpodetect menpo3d
conda activate menpo
```

The old `menpo` channel on anaconda.org is retired and no longer updated. Use conda-forge.

## Optional dependencies

Some features need a third-party library. They are installed through extras, for example
`pip install "menpo[imageio,opencv]"`. Current releases: menpo {{ menpo_version }}, menpofit {{ menpofit_version }}, menpo3d {{ menpo3d_version }}, menpowidgets {{ menpowidgets_version }}, menpodetect {{ menpodetect_version }}.

```{package-extras} menpo
```

```{package-extras} menpofit
```

```{package-extras} menpodetect
```

```{package-extras} menpowidgets
```

```{package-extras} menpo3d
```

## Check the install

```bash
python -c "import menpo; print(menpo.__version__)"
```

To use the interactive widgets, install [JupyterLab](https://jupyter.org) (or the classic notebook) in
the same environment and `import menpowidgets` there.

## Development version

See [Setting up a development environment](development.md) to work on the code.

```{toctree}
:hidden:

development
```
