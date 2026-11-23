"""Take package facts from the installed Menpo packages, not from hand-written pages.

The docs environment installs the packages being documented, so their metadata
(version, Python requirement, dependencies, extras) is the one source of truth:

* MyST substitutions ``{{ menpo_version }}``, ``{{ menpofit_requires_python }}`` ...
* ``{package-extras} <package>`` renders the extras of a package as a table.

Extras have no description in packaging metadata, so ``extras.toml`` keeps one line per
extra. The build fails if an extra is added or removed in a package without updating it.
"""

import tomllib
from importlib.metadata import PackageNotFoundError, metadata, requires, version
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive
from packaging.requirements import Requirement
from sphinx.errors import ExtensionError

PACKAGES = ["menpo", "menpofit", "menpo3d", "menpowidgets", "menpodetect"]


def _release(v):
    """0.12.2.dev18 -> 0.12.2.dev18; keep as is, but give the public part for display."""
    return v


def _norm(name):
    return name.lower().replace("_", "-")


def _extras(package):
    """{extra: [requirement strings]} for a package, from its metadata."""
    out = {_norm(e): [] for e in (metadata(package).get_all("Provides-Extra") or [])}
    for line in requires(package) or []:
        req = Requirement(line)
        if req.marker is None:
            continue
        for extra in out:
            if req.marker.evaluate({"extra": extra}) and not req.marker.evaluate({"extra": ""}):
                spec = f"{req.name}{req.specifier}" if str(req.specifier) else req.name
                if req.extras:
                    spec = f"{req.name}[{','.join(sorted(req.extras))}]{req.specifier}"
                out[extra].append(spec)
    return out


class PackageExtras(Directive):
    required_arguments = 1
    has_content = False

    def run(self):
        package = self.arguments[0]
        env = self.state.document.settings.env
        descriptions = env.app.config._menpo_extra_descriptions.get(package, {})
        extras = _extras(package)

        missing = sorted(set(extras) - set(descriptions))
        stale = sorted(set(descriptions) - set(extras))
        if missing or stale:
            raise ExtensionError(
                f"docs/extras.toml is out of date for {package}: "
                f"add descriptions for {missing}, remove {stale}"
            )

        table = nodes.table()
        group = nodes.tgroup(cols=3)
        table += group
        for width in (14, 30, 56):
            group += nodes.colspec(colwidth=width)
        head = nodes.thead()
        group += head
        body = nodes.tbody()
        group += body

        def row(parent, cells, literal=(), markup=()):
            r = nodes.row()
            for i, text in enumerate(cells):
                entry = nodes.entry()
                para = nodes.paragraph()
                if i in literal:
                    para += nodes.literal(text=text)
                elif i in markup:  # inline MyST/rST: `code`, **bold** ...
                    inline, messages = self.state.inline_text(text, self.lineno)
                    para.extend(inline + messages)
                else:
                    para += nodes.Text(text)
                entry += para
                r += entry
            parent += r

        row(head, ["Extra", "Installs", "Enables"])
        for extra, reqs in extras.items():
            row(body, [extra, ", ".join(reqs), descriptions[extra]], literal=(0, 1), markup=(2,))
        title = nodes.rubric(text=f"{package}")
        return [title, table]


def _substitutions(app, config):
    subs = dict(config.myst_substitutions or {})
    for package in PACKAGES:
        try:
            m = metadata(package)
        except PackageNotFoundError:
            raise ExtensionError(f"{package} must be installed to build the docs")
        subs[f"{package}_version"] = version(package)
        subs[f"{package}_requires_python"] = m["Requires-Python"]
    config.myst_substitutions = subs
    path = Path(app.confdir) / "extras.toml"
    config._menpo_extra_descriptions = tomllib.loads(path.read_text())


def setup(app):
    app.add_config_value("_menpo_extra_descriptions", {}, "env")
    app.add_directive("package-extras", PackageExtras)
    app.connect("config-inited", _substitutions)
    return {"parallel_read_safe": True}
