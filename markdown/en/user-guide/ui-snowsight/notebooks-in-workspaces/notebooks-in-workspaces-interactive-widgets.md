# Using interactive widgets

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

You can use `ipywidgets` and `FigureWidget` in Notebooks to bring interactive controls such as sliders, buttons,
dropdowns, and text inputs. By connecting Python code to browser-based widgets, you can build dynamic visualizations,
parameter exploration, and interactive applications.

## Installation

### Runtime v2.6 and above

`ipywidgets` and `anywidget` are pre-installed. No extra setup is needed: skip straight to [importing](#imports).

### Runtime v2.5 and below

Install the packages at the top of your notebook before importing:

Copy code

```
%pip install ipywidgets
%pip install anywidget  # required for FigureWidget and other anywidget-backed libraries
```

Run those cells once per session. After installation, proceed to the imports below.

## Imports

Copy code

```
import ipywidgets as widgets  # interactive controls
import plotly.graph_objects as go  # FigureWidget (backed by anywidget)
```

For common helpers used in the examples below:

Copy code

```
from IPython.display import display
```

## Basic controls

### Slider

Copy code

```
slider = widgets.IntSlider(value=5, min=0, max=10, description='Count:')
display(slider)
```

### Dropdown

Copy code

```
mode = widgets.Dropdown(
    options=['Standard', 'Enterprise', 'Business Critical'],
    value='Standard',
    description='Edition:',
)
display(mode)
```

### Checkbox

Copy code

```
enabled = widgets.Checkbox(value=True, description='Enable feature')
display(enabled)
```

### Button

Copy code

```
btn = widgets.Button(description='Apply', button_style='primary')

def on_click(b):
    print('Clicked!')

btn.on_click(on_click)
display(btn)
```

### Text input

Copy code

```
name = widgets.Text(value='Snowflake', description='Name:')
display(name)
```

## Laying out widgets

Use `HBox` (horizontal) and `VBox` (vertical) to arrange controls:

Copy code

```
display(widgets.VBox([
    widgets.HBox([slider, mode]),
    widgets.HBox([enabled, btn]),
]))
```

## FigureWidget (Plotly)

`FigureWidget` is a Plotly figure that supports live in-place updates, making it ideal for linking controls to a chart
without re-rendering the whole figure.

**Prerequisite:** `anywidget` must be installed.

### Basic line chart

Copy code

```
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
fig = go.FigureWidget(data=[go.Scatter(x=x, y=np.sin(x), mode='lines')])
display(fig)
```

## Supported widget types

| Category | Widgets |
| --- | --- |
| Numeric | IntSlider, FloatSlider, IntRangeSlider, FloatRangeSlider, IntText, FloatText, BoundedIntText, BoundedFloatText |
| Selection | Dropdown, SelectMultiple, RadioButtons, ToggleButtons |
| Boolean | Checkbox, ToggleButton |
| Text | Text, Textarea, Label, HTML |
| Button | Button |
| Display | Output, IntProgress, FloatProgress, Valid |
| Layout | HBox, VBox, Tab, Accordion |
| Date / Color | DatePicker, ColorPicker |
| anywidget | FigureWidget (Plotly) and other anywidget-backed libraries |

Expand

Show lessSee more

## Notes

- Widgets require an active kernel to sync state. If you refresh the page, re-run the cell to restore the widget.
- While another cell is executing, interactive controls (sliders, dropdowns, buttons) are temporarily disabled to
  prevent state drift between the UI and the running kernel.
- Cache isn’t supported with different sessions.

## Known unsupported ipywidgets

The following widgets show an “Unsupported widget” message:

- **Play (PlayModel):** Timer-based auto-increment not implemented.
- **Image (ImageModel):** Binary buffer support not implemented.
- **FileUpload (FileUploadModel):** Binary buffer and security review needed.
