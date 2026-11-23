---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---


<div style="display: flex; align-items: center; flex-direction: column;">
  <img src="../_static/logo/menpowidgets.png" alt="menpowidgets" width="30%" style="display: flex;">
  </br>
  <div style="display: flex; align-items: center; justify-content: center; margin-top: 4px; margin-bottom: 20px">
    <a href="https://github.com/menpo/menpowidgets" style="display: flex;">
      <img src="http://img.shields.io/github/release/menpo/menpowidgets.svg?style=flat-square" alt="Github Release"/>
    </a>
    <a style="text-decoration: none; color: grey; margin: 5px 25px;" href="https://github.com/menpo/menpowidgets">
      <button class="download_button">View on Github</button>
    </a>
    <a href="https://github.com/menpo/menpowidgets/blob/master/LICENSE.txt" style="display: flex;">
      <img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/>
    </a>
  </div>
</div>

# Widget components

These are the building blocks of the [main widgets](main_menpo_widgets.md): `menpowidgets.options` has widgets for selecting groups of options (rendering,
landmarks, channels, patches, animation...) and `menpowidgets.tools` has the lower level ones (colour selection, zoom, axes, index selection...) that the options widgets are built from.
You only need them to build your own widget out of the same parts. They all share the [trait and render callback](index.md) interface.

The tables below are generated from the installed package, so they list exactly the classes of menpowidgets {{ menpowidgets_version }}.

```{code-cell} ipython3
:tags: [remove-input]

import inspect

from IPython.display import Markdown

import menpowidgets.options as options
import menpowidgets.tools as tools
from menpowidgets.abstract import MenpoWidget


def table(module):
    rows = ["| Class | What it is |", "|---|---|"]
    for name, cls in sorted(vars(module).items()):
        if inspect.isclass(cls) and issubclass(cls, MenpoWidget) and cls.__module__.startswith(module.__name__):
            doc = (inspect.getdoc(cls) or "").strip().splitlines()
            summary = next((line for line in doc if line.strip()), "").strip()
            rows.append("| `{}` | {} |".format(name, summary.replace("|", "/")))
    return "\n".join(rows)


Markdown("## Options widgets\n\n`menpowidgets.options`\n\n" + table(options)
         + "\n\n## Tools widgets\n\n`menpowidgets.tools`\n\n" + table(tools))
```

The [API documentation](https://menpowidgets.readthedocs.io/en/latest/) has the arguments of each class.
