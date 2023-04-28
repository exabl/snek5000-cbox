import numpy as np
from scipy import interpolate

import matplotlib.pylab as plt
from matplotlib import rc
import matplotlib.patches as patches


from util import save_fig, figsize_halfpage, add_letter

from util_sketch import get_fig_ax_with_cavity, x_left, x_right, y_top

fig, ax = get_fig_ax_with_cavity()


def bspline(cv, n=100, degree=3):
    """Calculate n samples on a bspline

    cv :      Array ov control vertices
    n  :      Number of samples to return
    degree:   Curve degree
    """
    cv = np.asarray(cv)
    count = cv.shape[0]

    # Prevent degree from exceeding count-1, otherwise splev will crash
    degree = np.clip(degree, 1, count - 1)

    # Calculate knot vector
    kv = np.array(
        [0] * degree + list(range(count - degree + 1)) + [count - degree] * degree,
        dtype="int",
    )

    # Calculate query range
    u = np.linspace(0, (count - degree), n)

    # Calculate result
    return np.array(interpolate.splev(u, (kv, cv.T, degree))).T


points = np.array(
    [
        (1, 0.15),
        (0.98, 0.32),
        (0.96, 0.63),
        (0.95, 0.85),
        (0.94, 0.91),
        (0.90, 0.93),
        (0.865, 0.87),
        (0.85, 0.8),
        (0.79, 0.74),
        (0.73, 0.82),
        (0.685, 0.92),
        (0.55, 0.97),
        (0.405, 0.982),
        (0.30, 0.985),
        (0.14, 0.992),
    ]
)

# ax.plot(points[:, 0], points[:, 1], "ob")

p = bspline(points, n=100, degree=3)
x, y = p.T

ax.plot(x, y, color="red", linewidth=2)
ax.plot(1 - x, 1 - y, color="blue", linewidth=2)

# Add a double-sided arrow
arrows = patches.FancyArrowPatch(
    (0.79, 0.75),
    (1, 0.75),
    arrowstyle="<->",
    mutation_scale=15,
    shrinkA=0,
    shrinkB=0,
)
ax.add_patch(arrows)

x0, y0 = 0.9727, 0.4419
ax.arrow(x0, y0, 0.9681 - x0, 0.5132 - y0, head_width=0.025, color="red")
x0 = 1 - x0
y0 = 1 - y0
ax.arrow(x0, y0, 1 - 0.9681 - x0, 1 - 0.5132 - y0, head_width=0.025, color="blue")

ax.text(0.85, 0.68, r"$L_h$", fontsize=18)

ax.scatter(0.5, 0.5, marker="o", color="k")
ax.text(0.53, 0.5, r"$N_c$", fontsize=18)

ax.scatter(0.1, 0.2, marker="o", color="k")
ax.text(0.115, 0.22, r"$\omega$", fontsize=18)

ax.set_axis_off()
add_letter(fig, "b")
save_fig(fig, "diagnostic_sketch.png")
