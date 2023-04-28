import sys
import warnings

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from util import path_base, save_fig
from util_quantities import aspect_ratios, prandtls

rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

prandtl = float(sys.argv[-1])

if prandtl not in prandtls:
    raise ValueError(f"{prandtl = } not in {prandtls = }")

fig, axes = plt.subplot_mosaic("AA\nBB\nCD", figsize=(7, 10))

for ax, aspect_ratio in zip(axes.values(), aspect_ratios):
    path = f"{path_base}/A_{aspect_ratio}_Pr{prandtl:.2f}_base_state.h5"
    with h5py.File(path, "r") as file:
        x = np.array(file["grid/x"])
        y = np.array(file["grid/y"])

        prandtl = np.array(file["quantity/prandtl"])
        aspect_ratio = np.array(file["quantity/asp_ratio"])
        rayleigh = np.array(file["quantity/rayleigh"])

        ux_base = np.array(file["base/ux_base"])
        uy_base = np.array(file["base/uy_base"])
        theta_base = np.array(file["base/theta_base"])
        pressure_base = np.array(file["base/pressure_base"])

    speed = np.sqrt(ux_base**2 + uy_base**2)
    lw = 5 * speed / speed.max()

    im = ax.pcolormesh(x, y, theta_base, cmap="coolwarm", vmin=-0.5, vmax=0.5)

    density = (0.8, 0.8)

    if aspect_ratio == 0.5:
        density = (1.9 / aspect_ratio, 0.75)

    ax.streamplot(
        x,
        y,
        ux_base,
        uy_base,
        density=density,
        color="k",
        linewidth=lw,
    )
    ax.set_xlabel(r"x")
    ax.set_ylabel(r"z")

    ax.set_box_aspect(aspect_ratio)
    ax.set_title(rf"$A={aspect_ratio:.1f}$, $Pr={prandtl:.2f}$")

cax = fig.add_axes([0.725, 0.37, 0.02, 0.28])
cbar = fig.colorbar(im, cax=cax, orientation="vertical")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.tight_layout()

for letter, ax in zip("abcd", fig.axes):
    bbox = ax.get_position()
    fig.text(bbox.x0 - 0.08, bbox.y1 + 0.02, f"({letter})")


save_fig(fig, f"base_state_stream_subplots_Pr{prandtl:.2f}.png")
