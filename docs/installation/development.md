# Setting up a development environment

The steps are the same for every package of the Menpo Project (`menpo`, `menpofit`, `menpodetect`,
`menpo3d`, `menpowidgets`); they are shown here for `menpo`.

## 1. Clone the source

Fork the repository on [GitHub](https://github.com/menpo/menpo) so that you can open pull requests,
then clone your fork and add the Menpo organisation as `upstream`:

```bash
git clone https://github.com/<username>/menpo.git
cd menpo
git remote add upstream https://github.com/menpo/menpo.git
```

## 2. Install in editable mode

The packages are pure Python, so there is nothing to build. Create an environment and install the
package with its development dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . --group dev
```

The version is taken from the git tag with `setuptools-scm`, so keep the tags from `upstream`
(`git fetch upstream --tags`) to get a sensible `menpo.__version__`.

The other packages depend on `menpo`. To work on, for example, `menpofit` against your checkout of
`menpo`, install both in editable mode in the same environment.

## 3. Run the tests and checks

```bash
MPLBACKEND=Agg pytest          # the tests live inside the package
ruff format --check && ruff check
```

Continuous integration runs the same checks on Linux, macOS and Windows for every pull request.

## 4. Open a pull request

Create a branch from `master`, commit, push it to your fork and open a pull request against
`menpo/menpo`. Add a line to `docs/source/changelog.rst` in the repository for user-visible changes.
