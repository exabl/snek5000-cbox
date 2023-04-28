import numpy as np
import h5py

import matplotlib.pyplot as plt

from util import path_base, save_fig


aspect_ratio = 1.0
prandtl = 0.71

dim = 2

mosaic_code = "A"
figsize = (6, 5)
fig, axes = plt.subplot_mosaic(mosaic_code, figsize=figsize)


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


im1 = axes["A"].pcolormesh(x, y, Phi_theta, cmap="twilight")
axes["A"].set_axis_off()
plt.tight_layout()

save_fig(fig, "graphical_abstract.png")
