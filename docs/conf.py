"""Sphinx configuration for the Menpo Project website."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project = "The Menpo Project"
author = "The Menpo Team"
copyright = "The Menpo Team"

extensions = [
    "menpo_meta",
    "myst_nb",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx_copybutton",
    "sphinx_design",
]

exclude_patterns = ["_build", "SUMMARY.md", "**/.ipynb_checkpoints"]
source_suffix = {".md": "myst-nb", ".ipynb": "myst-nb"}
root_doc = "index"

# --- Markdown / maths ----------------------------------------------------
myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "attrs_inline", "substitution", "html_image"]
myst_heading_anchors = 3
myst_substitutions = {}
myst_dmath_double_inline = True
mathjax3_config = {
    "tex": {"packages": {"[+]": ["ams"]}},
}

# --- Executed code samples ------------------------------------------------
# Every code cell in every page is run on each build; a failing cell fails
# the build, so the samples cannot drift away from the released code.
nb_execution_mode = "off"  # CI sets it with -D nb_execution_mode=force
nb_execution_raise_on_error = True
nb_execution_timeout = 600
nb_execution_excludepatterns = []
nb_merge_streams = True
nb_output_stderr = "remove"
nb_number_source_lines = False

# --- Cross references to the API documentation ----------------------------
intersphinx_mapping = {
    "menpo": ("https://menpo.readthedocs.io/en/stable/", None),
    "menpofit": ("https://menpofit.readthedocs.io/en/stable/", None),
    "menpo3d": ("https://menpo3d.readthedocs.io/en/stable/", None),
    "menpowidgets": ("https://menpowidgets.readthedocs.io/en/stable/", None),
    "menpodetect": ("https://menpodetect.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# --- HTML ------------------------------------------------------------------
html_theme = "furo"
html_title = "The Menpo Project"
html_static_path = ["_static"]
html_css_files = ["menpostyle.css"]
html_js_files = [("force-light.js", {"priority": 100})]


# --- Media referenced from raw HTML ------------------------------------------
# Pages use raw <img>/<video> tags (sizing, side-by-side figures). Sphinx only
# copies images it sees through Markdown/reST syntax, so copy the rest verbatim,
# keeping each file next to the page that refers to it.
_MEDIA = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".webm", ".pdf"}


def _copy_media(app, exception):
    if exception or app.builder.format != "html":
        return
    import shutil

    src, out = Path(app.srcdir), Path(app.outdir)
    for f in src.rglob("*"):
        rel = f.relative_to(src)
        if f.suffix.lower() in _MEDIA and rel.parts[0] not in ("_build", "_static"):
            dest = out / rel
            if not dest.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)


def setup(app):
    app.connect("build-finished", _copy_media)
