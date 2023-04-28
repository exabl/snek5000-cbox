import numpy as np
import matplotlib.pylab as plt
from matplotlib import rc

from util import save_fig, figsize_halfpage, add_letter

from util_sketch import get_fig_ax_with_cavity


fig, ax = get_fig_ax_with_cavity()

plt.arrow(-0.15, 0.0, 0, 0.05, head_width=0.03, color="k")
plt.arrow(-0.15, 0.0, 0.05, 0, head_width=0.03, color="k")

# Adjusted text positions
ax.text(-0.08, -0.05, "x", fontsize=18)
ax.text(-0.19, 0.1, "z", fontsize=18)

ax.text(-0.33, 0.5, r"$T = - 0.5$", fontsize=18)
ax.text(1.05, 0.5, r"$T = 0.5$", fontsize=18)

ax.text(0.9, 0.3, r"$H$", fontsize=18)
ax.text(0.8, -0.1, r"$W$", fontsize=18)

ax.text(
    0.3,
    1.01,
    r"$\frac{\partial T}{\partial z} = 0$",
    fontsize=18,
    transform=ax.transAxes,
)
ax.text(
    0.3,
    -0.03,
    r"$\frac{\partial T}{\partial z} = 0$",
    fontsize=18,
    transform=ax.transAxes,
)

ax.text(0.5, 0.5, r"$t_0$", fontsize=18)

ax.set_axis_off()
add_letter(fig, "a")
save_fig(fig, "geometry_sketch.png")
