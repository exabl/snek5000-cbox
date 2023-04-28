import sys

import numpy as np
import h5py

import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from util import path_base, save_anim
from util_quantities import aspect_ratios, prandtls


aspect_ratio = float(sys.argv[-2])
prandtl = float(sys.argv[-1])

if aspect_ratio not in aspect_ratios:
    raise ValueError(f"{aspect_ratio = } not in {aspect_ratios = }")

if prandtl not in prandtls:
    raise ValueError(f"{prandtl = } not in {prandtls = }")

path = (
    f"{path_base}/A_{aspect_ratio}_Pr{prandtl:.2f}"
    "_amplitude_phase_omega_sigma_base.h5"
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

step = int(len(y) / 40)
step = 7
scale = int(0.5 * (ux_base.max() / A_ux.max()))

height = 8
width = height / asp_ratio

fig, ax = plt.subplots(1, figsize=(width, height))
fig.gca()

period = 2 * np.pi / omega
nb_times = 20
times = np.linspace(0, period * (1 - 1 / nb_times), nb_times)


def empty_variable():
    return np.empty((nb_times, y.size, x.size))


theta_p = empty_variable()
x_vel_p = empty_variable()
y_vel_p = empty_variable()

for i in range(times.size):
    theta_p[i, :, :] = A_theta * np.cos(omega * times[i] + Phi_theta)
    x_vel_p[i, :, :] = A_ux * np.cos(omega * times[i] + Phi_ux)
    y_vel_p[i, :, :] = A_uy * np.cos(omega * times[i] + Phi_uy)

vmax = (scale * theta_p + theta_base).max()
vmin = -vmax

speed = np.sqrt(
    (scale * x_vel_p + ux_base) ** 2 + (scale * y_vel_p + uy_base) ** 2
)
lw = 5 * speed / speed.max()

if asp_ratio >= 2:
    str_break = "\n"
else:
    str_break = " "


def make_title(it):
    return (
        rf"base $+ \epsilon$ pert.,{str_break}$A={asp_ratio:.2f}, Pr={prandtl:.2f},"
        rf"\omega/N_c = {omega_norm:.2f}$, $t/T = ${times[it]/period:.2f}"
    )


it = 0
image = ax.pcolormesh(
    x, y, scale * theta_p[it, :, :] + theta_base, shading="auto", cmap="coolwarm"
)

vx = scale * x_vel_p[it, ::step, ::step] + ux_base[::step, ::step]
vy = scale * y_vel_p[it, ::step, ::step] + uy_base[::step, ::step]
vectors = ax.quiver(x[::step], y[::step], vx, vy, pivot="middle")

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$z$")
ax.set_ylim(bottom=0)
ax.set_box_aspect(aspect_ratio)
ax.set_title(make_title(it))

fig.tight_layout()


def anim_frame(it):
    array = scale * theta_p[it, :, :] + theta_base
    image.set_array(array.flatten())
    vx = scale * x_vel_p[it, ::step, ::step] + ux_base[::step, ::step]
    vy = scale * y_vel_p[it, ::step, ::step] + uy_base[::step, ::step]
    vectors.set_UVC(vx, vy)
    ax.set_title(make_title(it))


anim_frame(0)
anim = FuncAnimation(
    fig,
    func=anim_frame,
    frames=np.arange(nb_times),
    interval=int(2000 / nb_times),
)
anim_name = f"anim_base_pert_A{asp_ratio:.2f}_Pr{prandtl:.2f}.gif"

save_anim(anim, anim_name)

# plt.show()
