import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Slider
from bokeh.layouts import row, widgetbox


# Create the main plot
def create_figure():
    # Set up data
    t_in = np.array([0., 1.])
    f_in = np.array([2., 3.])
    diff_in = np.array([0., 0.])

    # cubic polynomialS
    polyDeg = 3

    A = np.zeros([polyDeg + 1, polyDeg + 1])
    for i in np.arange(0, polyDeg + 1):
        A[[0, 1], i] = np.power(t_in, polyDeg - i)

    A[2, :] = np.array([3 * np.square(t_in[0]), 2 * t_in[0], 1, 0])
    A[3, :] = np.array([3 * np.square(t_in[1]), 2 * t_in[1], 1, 0])

    t = np.arange(0, 1, 0.01)

    # Get data
    f_in[0] = f1_slider.value
    f_in[1] = f2_slider.value

    diff_in[0] = diff1_slider.value
    diff_in[1] = diff2_slider.value

    # Do calculations
    cubicParams = np.dot(np.linalg.inv(A), np.append(f_in, diff_in))
    y = np.polyval(cubicParams, t)

    # Set up Plot
    plot = figure(plot_width=400, plot_height=400, x_range=[-0.1,1.1], y_range=[0.9,5.1])
    plot.line(t, y, line_width=1, color="blue")
    plot.circle(t_in, f_in, size=8, fill_color="white")

    return plot


# Update the plot
def update(attr, old, new):
    layout.children[1] = create_figure()


# Controls
f1_slider = Slider(start=1, end=4, value=2, step=0.01, title="f(0)")
f2_slider = Slider(start=1, end=4, value=3, step=0.01, title="f(1)")
diff1_slider = Slider(start=-10, end=10, value=0, step=0.01, title="f'(1)")
diff2_slider = Slider(start=-10, end=10, value=0, step=0.01, title="f'(2)")

for io in [f1_slider, f2_slider, diff1_slider, diff2_slider]:
    io.on_change('value', update)

inputs = widgetbox(f1_slider, f2_slider, diff1_slider, diff2_slider)
layout = row(inputs, create_figure())

curdoc().add_root(layout)
curdoc().title = "Polynomial Fit"


