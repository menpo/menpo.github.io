Tools Widgets
===============
Herein, we present `menpowidgets`'s basic widget tools that implement lower level widget functionalities, such as colour selection, zoom options, axes options, etc. These are the main ingredients in order to synthesize higher-level widget classes, such as the ones presented in [Options Widgets](options_widgets.md). All the widgets of this category live in `menpowidgets.tools`.

Below we present the functionalities of each one of them separately. Specifically we split this notebook in the following subsections:

1. [Basics](#basics)
2. [Menpo Logo](#logo)
3. [List Definition and Slicing](#list)
4. [Colour Selection](#colour)
5. [Index Selection](#index)
6. [Zoom](#zoom)
7. [Image Options](#image)
8. [Line Options](#line)
9. [Marker Options](#marker)
10. [Numbering Options](#numbering)
11. [Axes Options](#axes)
12. [Legend Options](#legend)
13. [Grid Options](#grid)
14. [HOG, DSIFT, Daisy, LBP, IGO Options](#features)

---------------------------------------

### <a name="basics"></a>1. Basics
All the widgets presented here are subclasses of `menpo.abstract.MenpoWidget`, thus they follow the same rules, which are:

* They expect as input the initial options, as well as the rendering callback function.
* They implement `add_render_function()`, `remove_render_function()`, `replace_render_function()` and `call_render_function()`.
* They implement `set_widget_state()`, which updates the widget state with a new set of options.
* They implement `style()` which takes a set of options that change the style of the widget, such as font-related options, border-related options, etc.

Before presenting each widget separately, let's first import the things that are required.

```python
from menpowidgets.tools import (LogoWidget, ListWidget, SlicingCommandWidget, ColourSelectionWidget,
                                IndexButtonsWidget, IndexSliderWidget, ZoomOneScaleWidget, ZoomTwoScalesWidget,
                                ImageOptionsWidget, LineOptionsWidget, MarkerOptionsWidget, NumberingOptionsWidget,
                                AxesLimitsWidget, AxesTicksWidget, AxesOptionsWidget, LegendOptionsWidget,
                                GridOptionsWidget, HOGOptionsWidget, DSIFTOptionsWidget, DaisyOptionsWidget,
                                LBPOptionsWidget, IGOOptionsWidget)
from menpowidgets.style import map_styles_to_hex_colours
```

Let us also define a generic print function that will be the callback trigger when the `selected_values` _trait_ of all the widgets changes.

The function must have a single argument, which will be a `dict` with the following keys:
* `'name'`: The name of the _trait_ that is monitored and triggers the callback. In the case of a `MenpoWidget` subclass, this is always `'selected_values'`.
* `'type'`: The type of event that happens on the _trait_. In the case of a `MenpoWidget` subclass, this is always `'change'`.
* `'new'`: The currently selected value attached to `selected_values`.
* `'old'`: The previous value of `selected_values`.
* `'owner'`: Pointer to the widget object.

Consequently, the selected values of a widget object (e.g. `wid`) can be retrieved in any of the following 3 equivalent ways:
1. `wid.selected_values`
2. `change['new']`
3. `change['owner'].selected_values`

For this notebook, we choose the second way which is independent of the widget object.

```python
from menpo.visualize import print_dynamic

def render_function(change):
    print(change['new'])
```

### <a name="logo"></a>2. Menpo Logo
This is a simple widget that can be used for embedding an image into an `ipywidgets` widget are using the `ipywidgets.Image` class.

```python
wid = LogoWidget(scale=0.6, style='info')
wid
```

### <a name="list"></a>3. List Definition and Slicing
_MenpoWidgets_ has a widget for defining a `list` of numbers. The widget is smart enough to accept any valid python command, such as
```python
'range(10)', '[1, 2, 3]', '10'
```
and complain about syntactic mistakes. It can be defined to expect either `int` or `float` numbers and has an optional example as guide.

```python
list_cmd = [0, 1, 2]

wid = ListWidget(list_cmd, mode='int', description='List:', render_function=render_function, example_visible=True)
wid
```

    [0, 1, 2, 3]
    [20, 16, 11]


Note that you need to press _Enter_ in order to pass a new value into the textbox. Also, try typing a wrong command, such as
```python
'10, 20,,', '10, a, None'
```
to see the corresponding error messages.

The styling of the widget can be changed using the `style()` method.

```python
wid.style(box_style='danger', font_size=15)
```

The state of the widget can be updated with the `set_widget_state()` method. Note that since `allow_callback=False`, nothing gets printed after running the command, even though `selected_values` is updated.

```python
wid.set_widget_state([20, 16], allow_callback=False)
```

Similar to the `list` widget, _MenpoWidgets_ has a widget for defining a command for slicing a `list` (or `numpy.array`). Commands can have any vald Python syntax, such as
```python
':3:', '::2', '1:2:10', '-1::', '0, 3, 7', 'range(5)'
```
The widget gets as argument a `dict` with the initial slicing command as well as the length of the `list`.

```python
# Initial options
slice_cmd = {'command': ':3',
             'length': 10}

# Create widget
wid = SlicingCommandWidget(slice_cmd, description='Command:', render_function=render_function,
                           example_visible=True, orientation='horizontal')

# Display widget
wid
```

    [0, 1, 2, 3, 4, 5, 6]


Note that by defining a single `int` number, then an `ipywidget.IntSlider` appears that allows to select the index. Similarly, by inserting any slicing command with a constant step, then an `ipywidgets.IntRangeSlider` appears. The sliders are disabled when inserting a slicing command with non-constant step. The placement of the sliders with respect to the textbox is controlled by the `orientation` argument.

Additionally, similar to the `ListWidget`, the widget is smart enough to detect any syntactic errors and print a relevant message.

The styling of the widget can be changed as

```python
wid.style(border_visible=True, border_style='dashed', font_weight='bold')
```

To update the widget's state, you need to pass in a new `dict` of options, as

```python
wid.set_widget_state({'command': ':40', 'length': 40}, allow_callback=True)
```

    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]


### <a name="colour"></a>4. Colour Selection
`menpowidgets` is using the standard Java colour picker defined in `ipywidgets.ColorPicker`. However, `ColourSelectionWidget` has the additional functionality to select colours for a set of objects. Thus the widget constructor gets a `list` of colours (either the colour name `str` or the RGB values), as well as the `labels` `list` that has the names of the objects.

```python
wid = ColourSelectionWidget([[255, 38, 31], 'blue', 'green'], labels=['a', 'b', 'c'],
                            render_function=render_function)

# Set styling
wid.style(box_style='warning', apply_to_all_style='info', label_colour='black',
          label_background_colour=map_styles_to_hex_colours('info', background=True), font_weight='bold')

# Display widget
wid
```

    [[255, 38, 31], 'blue', 'black']


The _Apply to all_ button sets the currently selected colour to all the labels.

The colours can also be updated with the `set_colours()` function as


```python
wid.set_colours(['red', 'orange', 'pink'], allow_callback=True)
```

    ['red', 'orange', 'pink']


In case there is only one label, defined either with a `list` of length ``1`` or by setting `labels=None`, then the drop-down menu to select object does not appear. For example, let's update the state of the widget:


```python
wid.set_widget_state(['red'], None)
```

    ['red']


### <a name="index"></a>5. Index Selection
The following two widgets give the ability to select a single integer number from a specified range. Thus, they can be seen as index selectors. The user must pass in a `dict` that defines the minimum, maximum and step of the allowed range, as well as the initially selected index. Then the `selected_values` _trait_ always keeps track of the selected index, thus it has `int` type.

An index selection widget, where the selector is an `ipywidgets.IntSlider` can be created as

```python
# Initial options
index = {'min': 0,
         'max': 100,
         'step': 1,
         'index': 10}

# Crete widget
wid = IndexSliderWidget(index, description='Index: ', render_function=render_function, continuous_update=False)

# Set styling
wid.style(box_style='danger', slider_handle_colour=map_styles_to_hex_colours('danger'),
          slider_bar_colour=map_styles_to_hex_colours('danger'))

# Display widget
wid
```

    43
    17


As with all widgets, the state can be updated as:

```python
wid.set_widget_state({'min': 10, 'max': 500, 'step': 2, 'index': 50}, allow_callback=True)
```

    50


An index selection widget where the selection can be performed with -/+ (previous/next) buttons can be created as:

```python
index = {'min': 0, 'max': 100, 'step': 1, 'index': 10}

wid = IndexButtonsWidget(index, render_function=render_function, loop_enabled=False, text_editable=True)
wid
```

    11
    12
    13
    14
    15


Note that since `text_editable` is ``True``, you can actually edit the index directly from the textbox. Additionally, by setting `loop_enabled=True` means that by pressing '+' when the textbox is at the last index, it takes you to the minimum index.

Let's update the styling of the widget:

```python
wid.style(box_style='danger', plus_style='success', minus_style='danger', text_colour='blue',
          text_background_colour=map_styles_to_hex_colours('info', background=True))
```

Let's also update its state with a new set of options:

```python
wid.set_widget_state({'min': 20, 'max': 500, 'step': 2, 'index': 50}, loop_enabled=True, text_editable=True,
                     allow_callback=True)
```

    50


### <a name="zoom"></a>6. Zoom
There are two widgets for zooming into a figure. Both are using `ipywidgets.FloatSLider` and get as input a `dict` with the minimum and maximum values, the step of the slider(s) and the initial zoom value.

The first one defines a single zoom `float`, as

```python
# Initial options
zoom_options = {'min': 0.1,
                'max': 4.,
                'step': 0.05,
                'zoom': 1.}

# Create widget
wid = ZoomOneScaleWidget(zoom_options, render_function=render_function)

# Set styling
wid.style(box_style='danger')
wid.zoom_slider.background_color = map_styles_to_hex_colours('info')
wid.zoom_slider.slider_color = map_styles_to_hex_colours('danger')

# Display widget
wid
```

    1.75
    2.95


and its state can be updated as:

```python
wid.set_widget_state({'zoom': 0.5, 'min': 0., 'max': 4., 'step': 0.2}, allow_callback=True)
```

    0.5


The second one defines two zoom values that are intended to control the height and width of a figure.

```python
# Initial options
zoom_options = {'min': 0.1,
                'max': 4.,
                'step': 0.1,
                'zoom': [1., 1.],
                'lock_aspect_ratio': False}

# Create widget
wid = ZoomTwoScalesWidget(zoom_options, render_function=render_function, continuous_update=True)

# Set styling
wid.style(box_style='danger')

# Display widget
wid
```

    [2.9, 1.0]
    [2.9, 0.5]
    [5.3, 3.0]


Note that the sliders can be linkedd in order to preserve the aspect ratio of the figure. The state can be updated as:

```python
zoom_options = {'min': 0.5, 'max': 10., 'step': 0.3, 'zoom': [2., 3.]}
wid.set_widget_state(zoom_options, allow_callback=True)
```

    [2.0, 3.0]


### <a name="image"></a>7. Image Options
This is a widget for selecting options related to rendering an image. It defines the colourmap, the alpha value for transparency as well as the interpolation. Specifically:

```python
# Initial options
image_options = {'alpha': 1.,
                 'interpolation': 'bilinear',
                 'cmap_name': None}

# Create widget
wid = ImageOptionsWidget(image_options, render_function=render_function)

# Set styling
wid.style(box_style='success', padding=10, border_visible=True, border_radius=45)

# Display widget
wid
```

    {'interpolation': 'bilinear', 'alpha': 0.35, 'cmap_name': None}
    {'interpolation': 'none', 'alpha': 0.35, 'cmap_name': None}


The widget can be updated with a new `dict` of options as:

```python
wid.set_widget_state({'alpha': 0.8, 'interpolation': 'none', 'cmap_name': 'gray'}, allow_callback=True)
```

    {'interpolation': 'none', 'alpha': 0.8, 'cmap_name': None}


### <a name="line"></a>8. Line Options
The following widget allows the selection of options for rendering line objects. The initial options are passed in as a `dict` and control the width, style and colour of the lines. Note that a different colour can be defined for different objects using the `labels` argument.

```python
# Initial options
line_options = {'render_lines': True,
                'line_width': 1,
                'line_colour': ['blue', 'red'],
                'line_style': '-'}

# Create widget
wid = LineOptionsWidget(line_options, render_function=render_function,
                        labels=['menpo', 'widgets'])

# Set styling
wid.style(box_style='danger', padding=6)

# Display widget
wid
```

    {'render_lines': True, 'line_style': '-', 'line_colour': ['orange', 'red'], 'line_width': 1.0}
    {'render_lines': True, 'line_style': '-', 'line_colour': ['orange', 'red'], 'line_width': 10.0}
    {'render_lines': True, 'line_style': '--', 'line_colour': ['orange', 'red'], 'line_width': 10.0}


The _Render lines_ tick box also controls the visibility of the rest of the options. So by updating the state with `render_lines=False`, the options disappear.

```python
wid.set_widget_state({'render_lines': False, 'line_width': 5, 'line_colour': ['purple'], 'line_style': '--'},
                     allow_callback=True, labels=None)
```

    {'render_lines': False, 'line_style': '--', 'line_colour': ['purple'], 'line_width': 5.0}


### <a name="marker"></a>9. Marker Options
Similar to the `LineOptionsWidget`, this widget allows to selecting options for rendering markers. The options define the edge width, face colour, edge colour, style and size of the markers.

```python
# Initial options
marker_options = {'render_markers': True,
                  'marker_size': 20,
                  'marker_face_colour': ['red', 'green'],
                  'marker_edge_colour': ['black', 'blue'],
                  'marker_style': 'o',
                  'marker_edge_width': 1}

# Create widget
wid = MarkerOptionsWidget(marker_options, render_function=render_function,
                          labels=['a', 'b'])

# Set styling
wid.style(box_style='info', padding=6)

# Display widget
wid
```

    {'marker_edge_colour': ['black', 'blue'], 'marker_size': 200, 'render_markers': True, 'marker_style': 'o', 'marker_face_colour': ['red', 'green'], 'marker_edge_width': 1.0}
    {'marker_edge_colour': ['black', 'blue'], 'marker_size': 200, 'render_markers': True, 'marker_style': '>', 'marker_face_colour': ['red', 'green'], 'marker_edge_width': 1.0}
    {'marker_edge_colour': ['black', 'blue'], 'marker_size': 200, 'render_markers': True, 'marker_style': 'p', 'marker_face_colour': ['red', 'green'], 'marker_edge_width': 1.0}



```python
wid.set_widget_state({'render_markers': True, 'marker_size': 20, 'marker_face_colour': ['red'],
                     'marker_edge_colour': ['black'], 'marker_style': 'o', 'marker_edge_width': 1},
                     labels=None, allow_callback=True)
```

    {'marker_edge_colour': ['black'], 'marker_size': 20, 'render_markers': True, 'marker_style': 'o', 'marker_face_colour': ['red'], 'marker_edge_width': 1.0}


### <a name="numbering"></a>10. Numbering Options
The `NumberingOptionsWidget` is used in case you want to render some numbers next to the plotted points.

```python
# Initial options
numbers_options = {'render_numbering': True,
                   'numbers_font_name': 'serif',
                   'numbers_font_size': 10,
                   'numbers_font_style': 'normal',
                   'numbers_font_weight': 'normal',
                   'numbers_font_colour': ['black'],
                   'numbers_horizontal_align': 'center',
                   'numbers_vertical_align': 'bottom'}

# Create widget
wid = NumberingOptionsWidget(numbers_options, render_function=render_function)

# Set styling
wid.style(box_style='success', border_visible=True, border_colour='black', border_style='solid', border_width=1,
          border_radius=0, padding=10, margin=10)

# Display widget
wid
```

    {'numbers_font_size': 10, 'render_numbering': False, 'numbers_font_weight': 'normal', 'numbers_horizontal_align': 'center', 'numbers_font_colour': 'black', 'numbers_vertical_align': 'bottom', 'numbers_font_name': 'serif', 'numbers_font_style': 'normal'}
    {'numbers_font_size': 10, 'render_numbering': True, 'numbers_font_weight': 'normal', 'numbers_horizontal_align': 'center', 'numbers_font_colour': 'black', 'numbers_vertical_align': 'bottom', 'numbers_font_name': 'serif', 'numbers_font_style': 'normal'}


Of course the state of the widget can be updated as:

```python
wid.set_widget_state({'render_numbering': True, 'numbers_font_name': 'serif', 'numbers_font_size': 10,
                      'numbers_font_style': 'normal', 'numbers_font_weight': 'normal',
                      'numbers_font_colour': ['green'], 'numbers_horizontal_align': 'center',
                      'numbers_vertical_align': 'bottom'}, allow_callback=True)
```

    {'numbers_font_size': 10, 'render_numbering': True, 'numbers_font_weight': 'normal', 'numbers_horizontal_align': 'center', 'numbers_font_colour': 'green', 'numbers_vertical_align': 'bottom', 'numbers_font_name': 'serif', 'numbers_font_style': 'normal'}


### <a name="axes"></a>11. Axes Options
Before presenting the `AxesOptionsWidget`, let's first see two widgets that are ued as its basic components for selecting the axes limits as well as the axes ticks.

`AxesLimitsWidget` has 3 basic functions per axis:
* `auto`: Allows `matplotlib` to automatically set the limits.
* `percentage`: It expects a `float` that defines the percentage of padding to allow around the rendered object's region.
* `range`: It expects two numbers that define the minimum and maximum values of the limits.

```python
# Create widget
wid = AxesLimitsWidget(axes_x_limits=[0, 10], axes_y_limits=0.1, render_function=render_function)

# Set styling
wid.style(box_style='danger')

# Display widget
wid
```

    {'y': 0.1, 'x': 0.0}
    {'y': [0.0, 100.0], 'x': 0.0}
    {'y': [0.0, 100.0], 'x': None}


Note that the `percentage` mode is accompanied by a [`ListWidget`](#list) that expects a single `float`, whereas the `range` mode invokes a [`ListWidget`](#list) that expects two `float` numbers. The state of the widget can be changed as:

```python
wid.set_widget_state([-200, 200], None, allow_callback=True)
```

    {'y': None, 'x': [-200, 200]}


On the other hand, `AxesTicksWidget` has two functionalities per axis:
* `auto`: Allows `matplotlib` to automatically set the ticks.
* `list`: Enables a [`ListWidget`](#list) to select the ticks.

```python
# Initial options
axes_ticks = {'x': [],
              'y': [10., 20., 30.]}

# Create widget
wid = AxesTicksWidget(axes_ticks, render_function=render_function)

# St styling
wid.style(box_style='danger')

# Display widget
wid
```

    {'y': [10.0, 20.0, 30.0], 'x': None}
    {'y': [], 'x': None}


The state can be updated as:

```python
wid.set_widget_state({'x': list(range(5)), 'y': None}, allow_callback=True)
```

    {'y': None, 'x': [0, 1, 2, 3, 4]}


The `AxesOptionsWidget` involves the `AxesLimitsWidget` and `AxesTicksWidget` widgets and also allows the selection of font-related options. As always, the initial options are provided in a `dict`:

```python
# Initial options
axes_options = {'render_axes': True,
                'axes_font_name': 'serif',
                'axes_font_size': 10,
                'axes_font_style': 'normal',
                'axes_font_weight': 'normal',
                'axes_x_limits': None,
                'axes_y_limits': None,
                'axes_x_ticks': [0, 100],
                'axes_y_ticks': None}

# Create widget
wid = AxesOptionsWidget(axes_options, render_function=render_function)

# Set styling
wid.style(box_style='warning', padding=6, border_visible=True, border_colour=map_styles_to_hex_colours('warning'))

# Display widget
wid
```

    {'axes_font_name': 'serif', 'axes_font_size': 100, 'axes_font_weight': 'normal', 'axes_y_limits': None, 'axes_x_limits': None, 'render_axes': True, 'axes_font_style': 'normal', 'axes_y_ticks': None, 'axes_x_ticks': [0, 100]}
    {'axes_font_name': 'serif', 'axes_font_size': 100, 'axes_font_weight': 'normal', 'axes_y_limits': None, 'axes_x_limits': None, 'render_axes': False, 'axes_font_style': 'normal', 'axes_y_ticks': None, 'axes_x_ticks': [0, 100]}


The state of the widget can be updated as:

```python
axes_options = {'render_axes': True, 'axes_font_name': 'serif',
                'axes_font_size': 10, 'axes_font_style': 'normal', 'axes_font_weight': 'normal',
                'axes_x_limits': [0., 0.05], 'axes_y_limits': 0.1, 'axes_x_ticks': [0, 100], 'axes_y_ticks': None}
wid.set_widget_state(axes_options, allow_callback=True)
```

    {'axes_font_name': 'serif', 'axes_font_size': 10, 'axes_font_weight': 'normal', 'axes_y_limits': 0.1, 'axes_x_limits': [0.0, 0.05], 'render_axes': True, 'axes_font_style': 'normal', 'axes_y_ticks': None, 'axes_x_ticks': [0, 100]}


### <a name="legend"></a>12. Legend Options
`LegendOptionsWidget` allows to control the (many) options of renderinf the legend of a figure.

```python
# Initial options
legend_options = {'render_legend': True,
                  'legend_title': '',
                  'legend_font_name': 'serif',
                  'legend_font_style': 'normal',
                  'legend_font_size': 10,
                  'legend_font_weight': 'normal',
                  'legend_marker_scale': 1.,
                  'legend_location': 2,
                  'legend_bbox_to_anchor': (1.05, 1.),
                  'legend_border_axes_pad': 1.,
                  'legend_n_columns': 1,
                  'legend_horizontal_spacing': 1.,
                  'legend_vertical_spacing': 1.,
                  'legend_border': True,
                  'legend_border_padding': 0.5,
                  'legend_shadow': False,
                  'legend_rounded_corners': True}

# Create widget
wid = LegendOptionsWidget(legend_options, render_function=render_function)

# Set styling
wid.style(border_visible=True, font_size=15)

# Display widget
wid
```

```python
legend_options = {'render_legend': True, 'legend_title': 'asd', 'legend_font_name': 'sans-serif',
                  'legend_font_style': 'normal', 'legend_font_size': 60, 'legend_font_weight': 'normal',
                  'legend_marker_scale': 2., 'legend_location': 7, 'legend_bbox_to_anchor': (1.05, 1.),
                  'legend_border_axes_pad': 1., 'legend_n_columns': 2, 'legend_horizontal_spacing': 3.,
                  'legend_vertical_spacing': 7., 'legend_border': False,
                  'legend_border_padding': 0.5, 'legend_shadow': True, 'legend_rounded_corners': True}
wid.set_widget_state(legend_options, allow_callback=True)
```

    {'legend_font_size': 60, 'legend_font_weight': 'normal', 'legend_font_style': 'normal', 'legend_vertical_spacing': 7.0, 'legend_font_name': 'sans-serif', 'legend_marker_scale': 2.0, 'legend_shadow': True, 'legend_border': False, 'legend_border_axes_pad': 1.0, 'legend_title': 'asd', 'render_legend': True, 'legend_bbox_to_anchor': (1.05, 1.0), 'legend_horizontal_spacing': 3.0, 'legend_location': 7, 'legend_n_columns': 2, 'legend_rounded_corners': True, 'legend_border_padding': 0.5}


### <a name="grid"></a>13. Grid Options
The following simple widget controls the rendering of the grid lines of a plot, their style and width.

```python
# Initial options
grid_options = {'render_grid': True,
                'grid_line_width': 1,
                'grid_line_style': '-'}

# Create widget
wid = GridOptionsWidget(grid_options, render_function=render_function)

# Set styling
wid.style(box_style='warning')

# Display widget
wid
```

    {'grid_line_width': 1.0, 'render_grid': True, 'grid_line_style': '-.'}
    {'grid_line_width': 10.0, 'render_grid': True, 'grid_line_style': '-.'}


```python
wid.set_widget_state({'render_grid': True, 'grid_line_width': 10, 'grid_line_style': ':'})
```

    {'grid_line_width': 10.0, 'render_grid': True, 'grid_line_style': ':'}


### <a name="features"></a>14. HOG, DSIFT, Daisy, LBP, IGO Options
The following widgets allow to select options regarding HOG, DSIFT, Daisy, LBP and IGO features.

```python
# Initial options
hog_options = {'mode': 'dense',
               'algorithm': 'dalaltriggs',
               'num_bins': 9,
               'cell_size': 8,
               'block_size': 2,
               'signed_gradient': True,
               'l2_norm_clip': 0.2,
               'window_height': 1,
               'window_width': 1,
               'window_unit': 'blocks',
               'window_step_vertical': 1,
               'window_step_horizontal': 1,
               'window_step_unit': 'pixels',
               'padding': True}

# Create widget
wid = HOGOptionsWidget(hog_options, render_function=render_function)

# Set styling
wid.style('info')

# Display widget
wid
```

    {'mode': 'dense', 'window_unit': 'blocks', 'l2_norm_clip': 0.2, 'window_height': 1, 'window_width': 1, 'padding': False, 'signed_gradient': True, 'window_step_unit': 'pixels', 'num_bins': 9, 'window_step_vertical': 1, 'cell_size': 8, 'block_size': 2, 'algorithm': 'dalaltriggs', 'window_step_horizontal': 1}


```python
# Initial options
dsift_options = {'window_step_horizontal': 1,
                 'window_step_vertical': 1,
                 'num_bins_horizontal': 2,
                 'num_bins_vertical': 2,
                 'num_or_bins': 9,
                 'cell_size_horizontal': 6,
                 'cell_size_vertical': 6,
                 'fast': True}

# Create widget
wid = DSIFTOptionsWidget(dsift_options, render_function=render_function)

# Set styling
wid.style('success')

# Display widget
wid
```

    {'cell_size_horizontal': 6, 'cell_size_vertical': 6, 'num_or_bins': 9, 'window_step_vertical': 1, 'fast': False, 'num_bins_horizontal': 2, 'window_step_horizontal': 1, 'num_bins_vertical': 2}


```python
# Initial options
daisy_options = {'step': 1,
                 'radius': 15,
                 'rings': 2,
                 'histograms': 2,
                 'orientations': 8,
                 'normalization': 'l1',
                 'sigmas': None,
                 'ring_radii': None}

# Create widget
wid = DaisyOptionsWidget(daisy_options, render_function=render_function)

# Set styling
wid.style('danger')

# Display widget
wid
```

    {'step': 1, 'rings': 2, 'sigmas': None, 'radius': 15, 'normalization': 'daisy', 'histograms': 2, 'orientations': 8, 'ring_radii': None}


```python
# Initial options
lbp_options = {'radius': list(range(1, 5)),
               'samples': [8] * 4,
               'mapping_type': 'u2',
               'window_step_vertical': 1,
               'window_step_horizontal': 1,
               'window_step_unit': 'pixels',
               'padding': True}

# Create widget
wid = LBPOptionsWidget(lbp_options, render_function=render_function)

# Set styling
wid.style(box_style='warning')

# Display widget
wid
```

    {'samples': [8, 8, 8, 8], 'window_step_unit': 'pixels', 'padding': True, 'window_step_vertical': 1, 'mapping_type': 'ri', 'radius': [1, 2, 3, 4], 'window_step_horizontal': 1}


```python
wid = IGOOptionsWidget({'double_angles': True}, render_function=render_function)
wid
```

    {'double_angles': False}
