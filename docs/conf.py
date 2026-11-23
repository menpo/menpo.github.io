"""Sphinx configuration for the Menpo Project website."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "_ext"))
# the notebook kernels import the helpers in _ext too
os.environ["PYTHONPATH"] = os.pathsep.join(
    [str(Path(__file__).parent / "_ext"), os.environ.get("PYTHONPATH", "")]
)

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

# Unresolvable references to the API docs fail the build, so renamed or removed names are caught.
nitpicky = True

# --- Cross references to the API documentation ----------------------------
intersphinx_mapping = {
    "menpo": ("https://menpo.readthedocs.io/en/latest/", None),
    "menpofit": ("https://menpofit.readthedocs.io/en/latest/", None),
    "menpo3d": ("https://menpo3d.readthedocs.io/en/latest/", None),
    "menpowidgets": ("https://menpowidgets.readthedocs.io/en/latest/", None),
    "menpodetect": ("https://menpodetect.readthedocs.io/en/latest/", None),
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
}

# --- HTML ------------------------------------------------------------------
html_theme = "pydata_sphinx_theme"
html_title = "The Menpo Project"
html_static_path = ["_static"]
html_css_files = ["menpo.css"]
html_favicon = "_static/logo/menpo.png"
html_context = {"default_mode": "light"}
templates_path = ["_templates"]
html_sidebars = {"index": [], "**": ["section-title", "sidebar-nav-bs"]}
html_theme_options = {
    "logo": {"image_light": "_static/logo/menpo.png", "image_dark": "_static/logo/menpo.png", "text": "The Menpo Project"},
    "navbar_start": ["navbar-logo"],
    "navbar_center": ["navbar-nav"],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "navbar_persistent": ["search-button"],
    "header_links_before_dropdown": 7,
    "icon_links": [
        {"name": "GitHub", "url": "https://github.com/menpo", "icon": "fa-brands fa-github"},
    ],
    "show_nav_level": 1,
    "navigation_depth": 3,
    "collapse_navigation": True,
    "show_toc_level": 2,
    "secondary_sidebar_items": ["page-toc"],
    "footer_start": ["copyright"],
    "footer_end": [],
    "navigation_with_keys": True,
}

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


# --- Section title in the sidebar ---------------------------------------------
# page -> (section title, the section's overview page). Pages in the top directories below belong to
# that package; the loose pages at the root belong to "About".
_SECTIONS = {
    "installation": ("Installation", "installation/index"),
    "menpo": ("menpo", "menpo/index"),
    "menpofit": ("menpofit", "menpofit/index"),
    "menpowidgets": ("menpowidgets", "menpowidgets/index"),
    "menpo3d": ("menpo3d", "menpo3d/index"),
    "menpodetect": ("menpodetect", "menpodetect/index"),
    "examples": ("Examples", "examples/index"),
}
_ABOUT = ("About", "about")


def _section_title(app, pagename, templatename, context, doctree):
    top = pagename.split("/")[0]
    title, index = _SECTIONS.get(top, _ABOUT if pagename != "index" else (None, None))
    if title:
        context["section_title"] = title
        context["section_url"] = context["pathto"](index)
        context["section_is_current"] = pagename == index


def setup(app):
    app.connect("build-finished", _copy_media)
    app.connect("html-page-context", _section_title, priority=100)  # before the theme drops templates that render empty
