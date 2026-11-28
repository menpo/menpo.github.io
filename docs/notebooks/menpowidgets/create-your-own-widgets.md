---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.19.7
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# How To Create Your Own Widgets

This notebook provides a simple tutorial on how to create your own widgets using _MenpoWidgets_, similar to the ones in _Menpo Widgets.ipynb_ and _MenpoFit Widgets.ipynb_. New widgets can be synthesized using the components presented in _Options Widgets.ipynb_. So before continuing with this notebook, please go through that one first.

The widget we create here is very simple since the purpose of this tutorial is to provide a basic introduction. The aim of the widget will be to go through a `list` of images and crop them with respect to a proportion of their landmarks. The crop proportion will be controlled by the user using a slider. There will also be some information printing regarding each image's size.

We split the presentation in the following steps:

1. __Import Images__
2. __Required Widgets__
3. __Widgets Grouping and Styling__
4. __Define Render Function__
5. __Final Widget Function__

+++

## 1. Import Images

Firstly, we need to import a `list` of images. Let's import the first 20 images of LFPW's testset and convert them to grayscale.

```{code-cell}
%matplotlib inline
import menpo.io as mio

from menpo_docs_data import lfpw_like_directory
path_to_lfpw = str(lfpw_like_directory()) + '/'  # your data: '/path/to/lfpw/'

images = []
for i in mio.import_images(path_to_lfpw + 'testset/*', max_images=20, verbose=True):
    # convert it to greyscale if needed
    if i.n_channels == 3:
        i = i.as_greyscale(mode='luminosity')
    # append it to the list
    images.append(i)
```

### 2. Required Widgets

We need the `AnimationOptionsWidget` in order to be able to browse through the `list` of images. This takes a `dict` with the initial indexing options. Of course the maximum index value should be equal to the number of loaded images.

```{code-cell}
from menpowidgets.options import AnimationOptionsWidget

index = {'min': 0, 'max': len(images) - 1, 'step': 1, 'index': 0}

anim_wid = AnimationOptionsWidget(index, description='Image')
anim_wid
```

We also need a way to define the crop percentage. This can be done with a simple slider that selects `float` numbers and is bounded between `0.0` and `1.0`. Thus

```{code-cell}
from ipywidgets import FloatSlider, Layout

prop_wid = FloatSlider(value=1., min=0., max=1., step=0.1, 
                       description='Proportion:', layout=Layout(width='5.5cm'))
prop_wid
```

Moreover, we can also create a `TextPrintWidget` for printing some info regarding the cropped image. For example

```{code-cell}
from menpowidgets.options import TextPrintWidget

text_per_line = ['> Original size: ', '> Final size: ']

txt_wid = TextPrintWidget(text_per_line)
txt_wid
```

### 3. Widgets Grouping and Styling

We now need to group the widgets in a single box. This can be done using `ipywidgets`'s `VBox` and `HBox`.

```{code-cell}
from ipywidgets import HBox, VBox

# Create an initial box for the proportion slider and the print info widget
opts_box = HBox(children=[prop_wid, txt_wid], layout=Layout(align_items='center'))

# Create the final widget's box
wid = VBox(children=[anim_wid, opts_box])

wid
```

Now we can apply some styling on the final widget

```{code-cell}
from menpowidgets.style import map_styles_to_hex_colours

# Select some styles
final_widget_style = 'info'
print_widget_style = 'warning'
animation_widget_style = 'danger'

# Apply the selected final widget style
wid.box_style = final_widget_style
wid.layout.border = '1px solid ' + map_styles_to_hex_colours(final_widget_style)

# Apply the selected print text widget style
txt_wid.predefined_style(style=print_widget_style)

# Apply the selected animation options widget style
anim_wid.predefined_style(style=animation_widget_style)
```

### 4. Define Render Function

The final step is to define the rendering callback function that will get called everytime a widget value is changed. The function needs to get the image index and proportion value, copy the original image, crop it, visualize it and update the printed info. Remember that all funtions that are used as callbacks in IPython widgets need to get two arguments: _name_ and _value_.

```{code-cell}
from IPython.display import clear_output
from matplotlib.pyplot import show as pltshow

def render_function(change):
    # Clear current figure, but wait until the generation of the new data
    # that will be rendered
    clear_output(wait=True)
    
    # Get selected image index
    i = anim_wid.selected_values
    
    # Get selected crop proportion
    prop = prop_wid.value
    
    # Get a copy of the original image
    im_copy = images[i].copy()
    
    # Crop the copied image
    im_copy = im_copy.crop_to_landmarks_proportion(prop)
    
    # Visualize it
    im_copy.view_landmarks();
    
    # Update the printed info
    text_per_line = ['> Original size: {}x{}'.format(images[i].height, images[i].width), 
                     '> Final size: {}x{}'.format(im_copy.height, im_copy.width)]
    txt_wid.set_widget_state(text_per_line=text_per_line)
    
    # Make sure that image gets rendered
    pltshow()
```

Let's check that it works properly

```{code-cell}
render_function({})
```

### 5. Final Widget Function

Let's now define a function that summarizes the above steps. It will get as input the images `list` and a `style` argument that can be either `'coloured'` or `'minimal'`.

```{code-cell}
from IPython.display import display

def crop_images_widget(images, style='coloured'):
    # Create widgets
    index = {'min': 0, 'max': len(images) - 1, 'step': 1, 'index': 0}
    anim_wid = AnimationOptionsWidget(index, description='Image')
    prop_wid = FloatSlider(value=1., min=0., max=1., step=0.1, continuous_update=False,
                           description='Proportion:', layout=Layout(width='5.5cm'))
    text_per_line = ['> Original size: ', '> Final size: ']
    txt_wid = TextPrintWidget(text_per_line=text_per_line)
    
    # Group widgets
    opts_box = HBox(children=[prop_wid, txt_wid], layout=Layout(align_items='center'))
    wid = VBox(children=[anim_wid, opts_box])
    
    # Styling
    final_widget_style = ''
    border_width = 0
    print_widget_style = 'minimal'
    animation_widget_style = 'minimal'
    if style == 'coloured':
        final_widget_style = 'info'
        print_widget_style = 'warning'
        animation_widget_style = 'danger'
        border_width = 1
    wid.box_style = final_widget_style
    if border_width:
        wid.layout.border = '1px solid ' + map_styles_to_hex_colours(final_widget_style)
    txt_wid.predefined_style(style=print_widget_style)
    anim_wid.predefined_style(style=animation_widget_style)
    
    # Define render function
    def render_function(change):
        clear_output(wait=True)
        i = anim_wid.selected_values
        prop = prop_wid.value
        im_copy = images[i].copy()
        im_copy = im_copy.crop_to_landmarks_proportion(prop)
        im_copy.view_landmarks();
        pltshow()
        text_per_line = ['> Original size: {}x{}'.format(images[i].height, images[i].width), 
                         '> Final size: {}x{}'.format(im_copy.height, im_copy.width)]
        txt_wid.set_widget_state(text_per_line=text_per_line)
        
    # Add render_function to the animation widget
    anim_wid.add_render_function(render_function)
    
    # Assign render_function to the proportion slider's value trait
    prop_wid.observe(render_function, names='value', type='change')
    
    # Display the widget
    display(wid)
    
    # Trigger its initial rendering
    render_function({})
```

That's it! Let's see what we designed!

```{code-cell}
crop_images_widget(images, style='coloured')
```
