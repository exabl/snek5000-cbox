import sys
import warnings

import numpy as np
import h5py

import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from util import path_base, save_fig

rc("font", **{"family": "serif", "serif": ["Times"], "size": 16})
rc("text", usetex=True)

aspect_ratio = 1.0
prandtl_values = [0.53, 0.71, 2.8, 4.0]

dim = 2

mosaic_code = "ABCD\nEFGH"
figsize = (12, 7)
fig, axes = plt.subplot_mosaic(mosaic_code, figsize=figsize, sharey=True)

for i, prandtl in enumerate(prandtl_values):
    path = f"{path_base}/A_{aspect_ratio}_Pr{prandtl:.2f}_amplitude_phase_omega_sigma_base.h5"

    with h5py.File(path, "r") as file:
        x = np.array(file["grid/x"])
        y = np.array(file["grid/y"])

        Phi_theta = np.array(file["phase/phase_theta"])
        Phi_ux = np.array(file["phase/phase_ux"])
        Phi_uy = np.array(file["phase/phase_uy"])
        Phi_pressure = np.array(file["phase/phase_pr"])

        A_theta = np.array(file["amplitude/amplitude_theta"])
        A_ux = np.array(file["amplitude/amplitude_ux"])
        A_uy = np.array(file["amplitude/amplitude_uy"])
        A_pressure = np.array(file["amplitude/amplitude_pr"])

        omega = np.array(file["quantity/omega"])
        Nc = np.array(file["quantity/Nc"])
        omega_norm = np.array(file["quantity/omega_norm"])
        sigma_r = np.array(file["quantity/sigma_r"])
        prandtl = np.array(file["quantity/prandtl"])
        asp_ratio = np.array(file["quantity/asp_ratio"])
        rayleigh = np.array(file["quantity/rayleigh"])

        ux_base = np.array(file["base/ux_base"])
        uy_base = np.array(file["base/uy_base"])
        theta_base = np.array(file["base/theta_base"])
        pressure_base = np.array(file["base/pressure_base"])

    def set_colorbar(im, ax):
        axins = inset_axes(
            ax,
            width="5%",
            height="100%",
            loc="lower left",
            bbox_to_anchor=(1.07, 0.0, 1, 1),
            bbox_transform=ax.transAxes,
            borderpad=0,
        )
        return fig.colorbar(im, cax=axins)

    y_indx = np.where(y >= 0.75)[0][0]
    x_indx = np.where(x >= 0.75)[0][0]
    if prandtl > 2.0:
        y_indx = np.where(y >= 0.75)[0][0]
        x_indx = np.where(x >= 0.95)[0][0]
    # y_indx = 0
    # x_indx = 0

    ax_base = axes[f"{chr(ord('A') + i )}"]
    im1 = ax_base.pcolormesh(
        x[x_indx:],
        y[y_indx:],
        theta_base[y_indx:, x_indx:],
        cmap="coolwarm",
        vmin=0.2,
        vmax=0.5,
    )

    speed = np.sqrt(ux_base**2 + uy_base**2)
    lw = 5 * speed / speed.max()

    density = (0.6, 0.8)

    ax_base.streamplot(
        x[x_indx:],
        y[y_indx:],
        ux_base[y_indx:, x_indx:],
        uy_base[y_indx:, x_indx:],
        density=density,
        color="k",
        linewidth=lw[y_indx:, x_indx:],
    )

    ax_base.set_xlim(x[x_indx:].min(), x[x_indx:].max())
    ax_base.set_ylim(y[y_indx:].min(), y[y_indx:].max())
    ax_base.axes.xaxis.set_ticklabels([])

    ax_base.set_title(rf"$Pr={prandtl}$")

    ax_amp = axes[f"{chr(ord('E') + i )}"]

    im2 = ax_amp.pcolormesh(
        x[x_indx:],
        y[y_indx:],
        A_theta[y_indx:, x_indx:] / A_theta.max(),
        cmap="magma_r",
    )

    if prandtl == 4:
        set_colorbar(im1, ax_base)
        set_colorbar(im2, ax_amp)

    ax_amp.set_xlabel(r"$x$")

axes["A"].set_ylabel(r"$z$")
axes["E"].set_ylabel(r"$z$")

fig.text(0.935, 0.502, r"$\Theta_b$")
fig.text(0.935, 0.042, r"$A_{\theta}$")

plt.subplots_adjust(bottom=0.08, top=0.94, left=0.08, right=0.92, hspace=0.15)

for letter, ax in zip("abcdefgh", fig.axes):
    bbox = ax.get_position()
    fig.text(bbox.x0 - 0.02, bbox.y1 + 0.02, f"({letter})")


save_fig(fig, "base_amp_maps_corner_regimes.png")
