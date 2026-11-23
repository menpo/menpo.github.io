# The Menpo Project website

Source for the Menpo Project site, built with [Sphinx](https://www.sphinx-doc.org) and
[MyST-NB](https://myst-nb.readthedocs.io). It is published to GitHub Pages by
`.github/workflows/docs.yml`; no built output is committed.

```
python -m venv .venv && . .venv/bin/activate
pip install -r docs/requirements.txt && pip install --no-deps -r docs/requirements-packages.txt
sphinx-build -b html docs docs/_build/html          # fast build, no code execution
sphinx-build -b html -D nb_execution_mode=force docs docs/_build/html   # run every code sample
```

Maths is written with `$...$` and `$$...$$` (MathJax).

## Package versions and releases

`docs/requirements.txt` has the tooling and the dependencies of the packages; `docs/requirements-packages.txt` installs the packages the site documents, with
`pip install --no-deps`. Until menpo 0.13 is released these are development branches (the unreleased PCA API). On release day:

1. Delete `docs/requirements-packages.txt` and the block of run-time dependencies in `docs/requirements.txt`, and add `-r versions.txt` to it.
2. Create `docs/versions.txt` with one exact pin per package (`menpo==0.13.0`, `menpofit==...`).

After that the `releases` workflow checks PyPI every day and opens a pull request when a package has a new release (`docs/_tools/bump_versions.py`).
The build of that pull request runs every code sample against the new release, so it fails exactly when a release breaks a page.

Face data for the examples that train models is read from `$MENPO_DOCS_FACES` (a directory of images with `.pts` files) or from the archive named in `docs/data.toml`;
see `docs/_ext/menpo_docs_data.py`.
