import numpy as np
from matplotlib import rc
import matplotlib.pylab as plt


rc("font", **{"family": "serif", "serif": ["Times"], "size": 16})
rc("text", usetex=True)


x_left = 0
x_right = 1
y_bottom = 0
y_top = 1


def get_fig_ax_with_cavity():

    fig, ax = plt.subplots()
    ax.axis("equal")

    # Draw the cavity
    ax.plot([x_left, x_right], [y_bottom, y_bottom], color="black", linewidth=3)
    ax.plot([x_left, x_right], [y_top, y_top], color="black", linewidth=3)
    ax.plot([x_left, x_left], [y_bottom, y_top], color="blue", linewidth=3)
    ax.plot([x_right, x_right], [y_bottom, y_top], color="red", linewidth=3)

    return fig, ax
