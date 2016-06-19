<center>
  <img src="../../logo/menpowidgets.png" alt="menpowidgets" width="30%">
  </br>
  </br>
  <a href="http://github.com/menpo/menpowidgets"><img src="http://img.shields.io/github/release/menpo/menpowidgets.svg" alt="Github Release"/></a>
  <a href="https://github.com/menpo/menpowidgets/blob/master/LICENSE.txt"><img src="http://img.shields.io/badge/License-BSD-green.svg" alt="BSD License"/></a>
  <img src="https://img.shields.io/badge/Python-2.7-green.svg" alt="Python 2.7 Support"/>
  <img src="https://img.shields.io/badge/Python-3.4-green.svg" alt="Python 3.4 Support"/>
  <img src="https://img.shields.io/badge/Python-3.5-green.svg" alt="Python 3.5 Support"/>
  <iframe src="https://ghbtns.com/github-btn.html?user=menpo&repo=menpowidgets&type=star&count=true" frameborder="0" scrolling="0" width="170px" height="20px"></iframe>
  </br>
</center>

`menpowidgets` is the Menpo Project’s Python package for fancy visualization within the Jupyter notebook using interactive widgets. In the Menpo Project we take an opinionated stance that visualization is a key part of generating research. Therefore, we have tried to make the mental overhead of visualizing objects as low as possible. MenpoWidgets makes tasks like data exploration, model observation and results demonstration as simple as possible.


#### Widgets Structure
`menpowidgets` can be separated into a 2-level hierarchy:

1. [**Main Widgets**](main_widgets.md)    
   These are the end user widget functions and the only ones that are exposed at the highest level of `menpowidgets`. They are further split into:  
   1.1. [**Main Menpo Widgets**](main_menpo_widgets.md): These include widgets functions for visualizing the [`menpo`](../menpo/index.md) package objects.  
   1.2. [**Main MenpoFit Widgets**](main_menpofit_widgets.md): These include widgets functions for visualizing the [`menpofit`](../menpofit/index.md) package objects.

2. [**Widgets Components**](components.md)  
   These are the main ingredients for synthesizing the main widgets. They consist of a 2-level hierarchy:  
   2.1. [**Options Widgets**](options_widgets.md): These are classes that implement widgets for selecting various options, such as rendering options, landmark options, channels options etc. They can be seen as the main components of all top level widgets.  
   2.2. [**Tools Widgets**](tools_widgets.md): These are classes that implement lower level widget functionalities, such as colour selection, zoom options, axes options, etc. They are the main ingredients of the options widgets.


#### Trait and render callback
All our widgets are subclasses of **`menpowidgets.abstract.MenpoWidget`** which is an `ipywidgets.FlexBox`. Thus all our widgets have the following functionalities:

* An additional `trait` named **`selected_values`** is added, which is monitoring any change that takes place in the widget and which should trigger a rendering function. The type of the trait can vary among widgets (e.g. `Int`, `Dict`, etc.) and its role is to store the selected values of the various widget components.
* The rendering function is passed in as the **`render_function`** argument.
* There are 4 basic methods on each widget:
 - **`add_render_function()`**: It attaches a new rendering function as callback to the `selected_values` `trait`.
 - **`remove_render_function()`**: It removes the current rendering function callback.
 - **`replace_render_function()`**: It replaces the current rendering function callback with a new one.
 - **`call_render_function()`**: It triggers the attached rendering function.
 > Note that `render_function()` must have the following signature:
   ```python
   input_dict = {'type': 'change', 'name': type_value, 'owner': '',
                  'old': old_value, 'new': new_value}
   render_function(input_dict)
   ```

#### Styling and set state
Additionally, all widgets have the following functions:
* **`set_widget_state()`**: It updates the widget state with a new set of options (i.e., `selected_values`). It has an `allow_callback` argument that defines whether the render function is allowed to be triggered if required.
* **`style()`**: It takes a set of options that change the style of the widget, such as font-related options, border-related options, etc.
* **`predefined_style()`**: It sets some predefined styles (themes) on the widget. Possible options are `'minimal'`, `'success'`, `'info'`, `'warning'` and `'danger'`.
