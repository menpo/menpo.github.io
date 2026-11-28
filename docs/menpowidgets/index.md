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

# menpowidgets

`menpowidgets` is the Menpo Project's Python package for sophisticated visualization within the Jupyter notebook using interactive widgets.
In the Menpo Project we take an opinionated stance that visualization is a key part of generating research. Therefore, we have tried to make the mental
overhead of visualizing objects as low as possible: data exploration, model observation and results demonstration should be a single function call.
This page describes menpowidgets {{ menpowidgets_version }}.

Install it with `pip install menpowidgets` (add the `menpofit` and `menpo3d` extras for the widgets of those packages, see [Installation](../installation/index.md)),
and use it in JupyterLab or the classic notebook.

## Widgets structure
`menpowidgets` has two levels:

1. [**Main widgets**](main_menpo_widgets.md) are the end-user functions, exposed at the top level of the package:
   * [for the objects of `menpo`](main_menpo_widgets.md) (images, shapes, landmarks, patches, graphs), and
   * [for the objects of `menpofit`](main_menpofit_widgets.md) (models and fitting results).
2. [**Widget components**](components.md) are the building blocks the main widgets are made of, for example the options for colours, zoom, landmarks or rendering.

## Trait and render callback
All the widgets are subclasses of `menpowidgets.abstract.MenpoWidget`, which is an `ipywidgets` box. They have:

* a `selected_values` trait that changes whenever the user changes something that should trigger a redraw. Its type depends on the widget;
* a `render_function`, passed in on construction, that is called on every change;
* four methods that manage the callback: `add_render_function`, `remove_render_function`, `replace_render_function` and `call_render_function`.

```{code-cell} ipython3
from menpowidgets.abstract import MenpoWidget

[name for name in ("add_render_function", "remove_render_function", "replace_render_function",
                   "call_render_function") if hasattr(MenpoWidget, name)]
```

A render function receives the change dictionary of `traitlets`:

```python
def render_function(change):
    change['name']   # the trait that changed ('selected_values')
    change['old']    # the previous value
    change['new']    # the new value
```

## Styling
The widgets of `menpowidgets.options` and `menpowidgets.tools` can be restyled with `style(...)` (fonts, borders, colours) and `predefined_style(...)`, which
applies one of the themes `'minimal'`, `'success'`, `'info'`, `'warning'` and `'danger'`. `set_widget_state(...)` changes the options of a widget, with the
`allow_callback` argument deciding whether the render function is called.

```{toctree}
:titlesonly:
:hidden:
:maxdepth: 2

Main Menpo widgets </menpowidgets/main_menpo_widgets>
Main MenpoFit widgets </menpowidgets/main_menpofit_widgets>
Components </menpowidgets/components>
```
