# The Menpo Project website

Source for the Menpo Project site, built with [Sphinx](https://www.sphinx-doc.org) and
[MyST-NB](https://myst-nb.readthedocs.io). It is published to GitHub Pages by
`.github/workflows/docs.yml`; no built output is committed.

```
python -m venv .venv && . .venv/bin/activate
pip install -r docs/requirements.txt
sphinx-build -b html docs docs/_build/html          # fast build, no code execution
sphinx-build -b html -D nb_execution_mode=force docs docs/_build/html   # run every code sample
```

Maths is written with `$...$` and `$$...$$` (MathJax).
