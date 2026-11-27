"""Show the outputs of cells that were run on data that is not in this repository.

The pages that train a model run their code in CI on a small set of faces, which only shows that the code
runs. What the page should *show* (the printed model, the plots, the fitting results) comes from the same
code run on the 300-W training set, by ``docs/_tools/render_examples.py record``. A cell is marked with a
tag and its recorded output is placed after it::

    ```{code-cell} ipython3
    :tags: [remove-output, record-aam]
    aam = HolisticAAM(training_images, ...)
    print(aam)
    ```

    ```{recorded-output} aam
    ```

``remove-output`` hides what the cell gives in the build. The recording stores a hash of the code of the cell,
and the build fails (a warning, which CI treats as an error) when the cell has changed since, or has not been
recorded: record the page again.
"""

import hashlib
import json
import re
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util import logging

logger = logging.getLogger(__name__)

OUTPUTS = Path("_static") / "examples" / "outputs"
CELL = re.compile(r"```\{code-cell\}[^\n]*\n(.*?)```", re.S)


def cell_hash(code):
    return hashlib.sha256("\n".join(line.rstrip() for line in code.strip().splitlines()).encode()).hexdigest()[:16]


def recorded_cells(text):
    """``{name: code}`` of the cells of a page that are tagged ``record-<name>``."""
    cells = {}
    for match in CELL.finditer(text):
        lines = match.group(1).splitlines()
        options = " ".join(line for line in lines if line.startswith(":"))
        code = "\n".join(line for line in lines if not line.startswith(":"))
        for name in re.findall(r"record-([\w-]+)", options):
            cells[name] = code
    return cells


def recording_path(srcdir, docname):
    return Path(srcdir) / OUTPUTS / f"{docname.replace('/', '__')}.json"


class RecordedOutput(Directive):
    required_arguments = 1
    has_content = False

    def run(self):
        env = self.state.document.settings.env
        name = self.arguments[0]
        where = f"{env.docname}: recorded output '{name}'"
        path = recording_path(env.srcdir, env.docname)
        recorded = json.loads(path.read_text()).get(name) if path.exists() else None
        if recorded is None:
            logger.warning(f"{where} has not been recorded: run docs/_tools/render_examples.py record {env.docname}",
                           location=(env.docname, self.lineno))
            return []
        cell = recorded_cells(Path(env.doc2path(env.docname)).read_text()).get(name)
        if cell is None or cell_hash(cell) != recorded["hash"]:
            logger.warning(f"{where}: the code of the cell has changed since it was recorded: run "
                           f"docs/_tools/render_examples.py record {env.docname}", location=(env.docname, self.lineno))
        container = nodes.container(classes=["recorded-output"])
        container += nodes.paragraph(
            "", "Output with the model trained on the LFPW training set (the cell above runs in the build on a "
            "small set of faces, which only shows that it works):", classes=["recorded-output-caption"])
        for output in recorded["outputs"]:
            if output["type"] == "text":
                container += nodes.literal_block(output["text"], output["text"], classes=["output", "stream"])
            else:
                container += nodes.image("", uri="/" + (OUTPUTS / output["file"]).as_posix(), alt=name)
        return [container]


def setup(app):
    app.add_directive("recorded-output", RecordedOutput)
    return {"parallel_read_safe": True}
