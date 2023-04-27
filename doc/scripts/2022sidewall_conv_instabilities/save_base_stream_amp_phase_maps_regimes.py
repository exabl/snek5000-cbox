import sys
import warnings

import numpy as np
import h5py

import matplotlib.pyplot as plt
from matplotlib import rc
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

from util import path_base, save_fig

from util_quantities import aspect_ratios, prandtls

rc("font", **{"family": "serif", "serif": ["Times"], "size": 16})
rc("text", usetex=True)

aspect_ratio = float(sys.argv[-2])
prandtl = float(sys.argv[-1])

if aspect_ratio not in aspect_ratios:
    raise ValueError(f"{aspect_ratio = } not in {aspect_ratios = }")

if prandtl not in prandtls:
    raise ValueError(f"{prandtl = } not in {prandtls = }")

dim = 2

mosaic_code = "ABCD\nEEFF"
figsize = (14, 9)
if aspect_ratio == 0.5:
    figsize = (17, 6)
elif aspect_ratio == 1.5:
    figsize = (13, 10)
elif aspect_ratio == 2.0:
    figsize = (12, 12)


path = (
    f"{path_base}/A_{aspect_ratio}_Pr{prandtl:.2f}_amplitude_phase_omega_sigma_base.h5"
)
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


fig, axes = plt.subplot_mosaic(mosaic_code, figsize=figsize, sharey=True)


def set_colorbar(im, ax):
    axins = inset_axes(
        ax,
        width="5%",
        height="100%",
        loc="lower left",
        bbox_to_anchor=(1.02, 0.0, 1, 1),
        bbox_transform=ax.transAxes,
        borderpad=0,
    )
    return fig.colorbar(im, cax=axins)


tmp_ux = A_ux * np.cos(Phi_ux)
tmp_uy = A_uy * np.cos(Phi_uy)
im1 = axes["A"].pcolormesh(x, y, theta_base, cmap="coolwarm", vmin=-0.5, vmax=0.5)
set_colorbar(im1, axes["A"])

speed = np.sqrt(ux_base**2 + uy_base**2)
lw = 5 * speed / speed.max()

density = (0.6, 0.8)

if prandtl > 1.0:
    density = (1.06, 0.8)
if prandtl > 3.0:
    density = (1.5, 0.8)

axes["A"].streamplot(
    x,
    y,
    ux_base,
    uy_base,
    density=density,
    color="k",
    linewidth=lw,
)
axes["A"].set_xlabel(r"x")
axes["A"].set_ylabel(r"z")

axes["A"].set_box_aspect(aspect_ratio)
axes["A"].set_title("base state")
im2 = axes["B"].pcolormesh(x, y, A_theta / A_theta.max(), cmap="magma_r")

set_colorbar(im2, axes["B"])

axes["B"].set_xlabel(r"$x$")
axes["B"].set_ylabel(r"$z$")
axes["B"].set_title(r"$A_{\theta'}$")
axes["B"].set_box_aspect(asp_ratio)

im3 = axes["C"].pcolormesh(x, y, Phi_theta, cmap="twilight")

set_colorbar(im3, axes["C"])

axes["C"].set_xlabel(r"$x$")
axes["C"].set_ylabel(r"$z$")
axes["C"].set_title(r"$\Phi_{\theta'}$")
axes["C"].set_box_aspect(asp_ratio)

period = 2 * np.pi / omega
nb_times = 4
time_n = np.linspace(0, period * (1 - 1 / nb_times), nb_times)


def empty_variable():
    return np.empty((time_n.size, y.size, x.size))


theta_p = empty_variable()
x_vel_p = empty_variable()
y_vel_p = empty_variable()
dudy_p = empty_variable()
dvdx_p = empty_variable()

for i in range(time_n.size):
    theta_p[i, :, :] = A_theta * np.cos(omega * time_n[i] + Phi_theta)
    x_vel_p[i, :, :] = A_ux * np.cos(omega * time_n[i] + Phi_ux)
    y_vel_p[i, :, :] = A_uy * np.cos(omega * time_n[i] + Phi_uy)
for i in range(time_n.size):
    dudy_p[i, :, :] = np.gradient(x_vel_p[i, :, :], y, axis=0, edge_order=2)
    dvdx_p[i, :, :] = np.gradient(y_vel_p[i, :, :], x, axis=1, edge_order=2)

vort_pert = dudy_p - dvdx_p

vmax = 0.4 * vort_pert.max()
vmin = -vmax

im4 = axes["D"].pcolormesh(x, y, vort_pert[0], cmap="Spectral", vmin=vmin, vmax=vmax)

set_colorbar(im4, axes["D"])

axes["D"].set_xlabel(r"x")
axes["D"].set_ylabel(r"z")
axes["D"].set_title(r"vorticity pert.")
axes["D"].set_box_aspect(aspect_ratio)

y_indx = np.where(y >= 0.5)[0][0]
y_indx = 0
x_indx = 0
scale = int(0.6 * (ux_base.max() / A_ux.max()))

vmax = (theta_base + scale * theta_p).max()
vmin = -vmax

im5 = axes["E"].pcolormesh(
    x[x_indx:],
    y[y_indx:],
    scale * theta_p[0, y_indx:, x_indx:] + theta_base[y_indx:, x_indx:],
    cmap="coolwarm",
    vmin=vmin,
    vmax=vmax,
)
set_colorbar(im5, axes["E"])

im6 = axes["F"].pcolormesh(
    x[x_indx:],
    y[y_indx:],
    scale * theta_p[1, y_indx:, x_indx:] + theta_base[y_indx:, x_indx:],
    cmap="coolwarm",
    vmin=vmin,
    vmax=vmax,
)
set_colorbar(im6, axes["F"])
speed = np.sqrt((scale * x_vel_p + ux_base) ** 2 + (scale * y_vel_p + uy_base) ** 2)
lw = 5 * speed[0] / speed.max()

if prandtl > 1.0:
    density = (1.5, 0.9)
if prandtl > 3.0:
    density = (1.6, 0.9)

axes["E"].streamplot(
    x[x_indx:],
    y[y_indx:],
    scale * x_vel_p[0, y_indx:, x_indx:] + ux_base[y_indx:, x_indx:],
    scale * y_vel_p[0, y_indx:, x_indx:] + uy_base[y_indx:, x_indx:],
    density=density,
    color="k",
    # arrowstyle='-',
    linewidth=lw[y_indx:, x_indx:],
)
axes["E"].set_xlabel(r"$x$")
axes["E"].set_ylabel(r"$z$")
axes["E"].set_title(rf"$b + \epsilon p$, $t={(time_n[0]/period):.1f}$")
axes["E"].set_box_aspect(
    (y[y_indx:].max() - y[y_indx:].min()) / (x[x_indx:].max() - x[x_indx:].min())
)

lw = 5 * speed[1] / speed.max()
axes["F"].streamplot(
    x[x_indx:],
    y[y_indx:],
    scale * x_vel_p[1, y_indx:, x_indx:] + ux_base[y_indx:, x_indx:],
    scale * y_vel_p[1, y_indx:, x_indx:] + uy_base[y_indx:, x_indx:],
    density=density,
    color="k",
    linewidth=lw[y_indx:, x_indx:],
)
axes["F"].set_xlabel(r"$x$")
axes["F"].set_ylabel(r"$z$")
axes["F"].set_title(rf"$b + \epsilon p$, $t={(time_n[1]/period):.2f}T$")
axes["F"].set_box_aspect(
    (y[y_indx:].max() - y[y_indx:].min()) / (x[x_indx:].max() - x[x_indx:].min())
)

plt.suptitle(rf"$A={asp_ratio}$, $Pr={prandtl}$, $\omega / N_c={omega_norm:.3f}$")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])

left = 0.05  # the left side of the subplots of the figure
right = 0.91  # the right side of the subplots of the figure
bottom = 0.08  # the bottom of the subplots of the figure
top = 0.95  # the top of the subplots of the figure
wspace = 0.35  # the amount of width reserved for blank space between subplots
hspace = 0.1  # the amount of height reserved for white space between subplots

plt.subplots_adjust(
    left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace
)

fig_name = f"base_stream_amp_phase_A{asp_ratio:.2f}_Pr{prandtl:.2f}.png"

for letter, ax in zip("abcdef", fig.axes):
    bbox = ax.get_position()
    fig.text(bbox.x0 - 0.02, bbox.y1 + 0.02, f"({letter})")

# plt.show()
save_fig(fig, fig_name)
