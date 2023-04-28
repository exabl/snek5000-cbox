import sys
import warnings

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from util import path_base, save_fig
from util_quantities import aspect_ratios


rc("font", **{"family": "serif", "serif": ["Times"], "size": 14})
rc("text", usetex=True)

aspect_ratio = float(sys.argv[-1])

if aspect_ratio not in aspect_ratios:
    raise ValueError(f"{aspect_ratio = } not in {aspect_ratios = }")

mosaic_code = "ABC\nDEF"
figsize = (10, 6)
if aspect_ratio == 0.5:
    mosaic_code = "AB\nCD\nEF"
    figsize = (9, 8)
elif aspect_ratio == 1.5:
    mosaic_code = "AB\nCD\nEF"
    figsize = (5, 8)
elif aspect_ratio == 2.0:
    mosaic_code = "ABC\nDEF"
    figsize = (9, 8)

fig, axes = plt.subplot_mosaic(mosaic_code, figsize=figsize)

selected_prandtls = [0.1, 0.35, 0.44, 0.71, 1.0, 1.4]

if aspect_ratio == 2.0:
    selected_prandtls = [0.35, 0.53, 0.71, 1.4, 2.0, 2.8]

for ax, prandtl in zip(axes.values(), selected_prandtls):
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

    density = (0.6, 0.6)

    if prandtl > 2.0:
        density = (0.5, 0.7)

    speed = np.sqrt(ux_base**2 + uy_base**2)
    lw = 5 * speed / speed.max()

    im = ax.pcolormesh(x, y, theta_base, cmap="coolwarm", vmin=-0.5, vmax=0.5)

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

cax = fig.add_axes([0.925, 0.25, 0.02, 0.6])
cbar = fig.colorbar(im, cax=cax, orientation="vertical")


with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.tight_layout()

plt.subplots_adjust(wspace=0.0)

for letter, ax in zip("abcdef", fig.axes):
    bbox = ax.get_position()
    fig.text(bbox.x0 - 0.07, bbox.y1 + 0.02, f"({letter})")

save_fig(fig, f"base_state_stream_subplots_A{aspect_ratio:.2f}.png")
