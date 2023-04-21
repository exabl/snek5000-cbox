import numpy as np
import h5py
from scipy import optimize
from pathlib import Path
from snek5000 import load
from compute_growth_frequency_linear_KE import (
    compute_growth_rate_frequency_linear as grfl,
)

# Parameters
prandtl = 0.2
aspect = 1.0
dim = 2

# Directories
dir_base = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim/Pr_{prandtl:.2f}/asp_{aspect:.3f}"
path = Path(dir_base)
sim_dirs = sorted(path.glob("cbox_*"))
dir_sim = sim_dirs[0]
dir_save = "/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/2D/Lin_sim"

# Load simulation and data
sim = load(dir_sim)
fields = sim.output.phys_fields.load(prefix="p01", index="0017*")
field_base = sim.output.phys_fields.load()

# Create new x and y grids
x_new = np.linspace(field_base.x[0], field_base.x[-1], fields.x.size)
y_new = np.linspace(field_base.y[0], field_base.y[-1], fields.y.size)

# Remove duplicates and interpolate data
fields = fields.drop_duplicates(["x", "y"])
field_base = field_base.drop_duplicates(["x", "y"])
field_base = field_base.interp(x=x_new, y=y_new, method="cubic")
fields = fields.interp(x=x_new, y=y_new, method="cubic")

# Extract base values
ux_base = field_base.ux[0].values
uy_base = field_base.uy[0].values
theta_base = field_base.temperature[0].values
pressure_base = field_base.pressure[0].values

# Calculate N and Nc
dTdy = field_base.temperature.differentiate("y")
N = np.sqrt(
    prandtl * dTdy.sel(x=slice(0.1 / aspect, 0.9 / aspect), y=slice(0.45, 0.55))
)
N = N[0]
Nc = N.values.max()

# Calculate omega and sigma_r
omega = []
sigma_r = []
sim = load(dir_sim)
params = sim.params
coords, df = sim.output.history_points.load()

for i in range(11):
    growth, frequency = grfl(df, params, i)
    sigma_r.append(growth)
    omega.append(frequency)

sigma_r = np.mean(sigma_r)
omega = 2 * np.pi * np.mean(omega)
period = 1 / omega

# Prepare data for analysis
step1 = 0
step2 = -1
theta = fields.temperature[:, 0, :, :].values[step1:step2]
ux = fields.ux[:, 0, :, :].values[step1:step2]
uy = fields.uy[:, 0, :, :].values[step1:step2]
pressure = fields.pressure[:, 0, :, :].values[step1:step2]

# Initialize arrays for amplitudes and phases
shape_theta = fields.temperature[0, 0, :, :].values
shape_pressure = fields.pressure[0, 0, :, :].values
x = fields.x.values
y = fields.y.values
A_theta = np.empty_like(shape_theta)
A_ux = np.empty_like(shape_theta)
A_uy = np.empty_like(shape_theta)
A_pressure = np.empty_like(shape_pressure)

Phi_theta = np.empty_like(theta)
Phi_ux = np.empty_like(ux)
Phi_uy = np.empty_like(uy)
Phi_pressure = np.empty_like(pressure)

# Normalize data by growth rate
for iy in range(theta.shape[1]):
    for ix in range(theta.shape[2]):
        theta[:, iy, ix] /= np.exp(sigma_r * fields.time[step1:step2].values)
        ux[:, iy, ix] /= np.exp(sigma_r * fields.time[step1:step2].values)
        uy[:, iy, ix] /= np.exp(sigma_r * fields.time[step1:step2].values)

for iy in range(pressure.shape[1]):
    for ix in range(pressure.shape[2]):
        pressure[:, iy, ix] /= np.exp(sigma_r * fields.time[step1:step2].values)

# Compute amplitudes
for iy in range(theta.shape[1]):
    for ix in range(theta.shape[2]):
        A_theta[iy, ix] = np.abs(theta[:, iy, ix]).max()
        A_ux[iy, ix] = np.abs(ux[:, iy, ix]).max()
        A_uy[iy, ix] = np.abs(uy[:, iy, ix]).max()

for iy in range(pressure.shape[1]):
    for ix in range(pressure.shape[2]):
        A_pressure[iy, ix] = np.abs(pressure[:, iy, ix]).max()

# Test functions
def test_func1(t, Phi_theta):
    return A_theta[iy, ix] * np.sin(omega * t + Phi_theta)


def test_func2(t, Phi_ux):
    return A_ux[iy, ix] * np.sin(omega * t + Phi_ux)


def test_func3(t, Phi_uy):
    return A_uy[iy, ix] * np.sin(omega * t + Phi_uy)


def test_func4(t, Phi_pressure):
    return A_pressure[iy, ix] * np.sin(omega * t + Phi_pressure)


# Compute phases
for iy in range(theta.shape[1]):
    for ix in range(theta.shape[2]):
        params, _ = optimize.curve_fit(
            test_func1, fields.time[step1:step2].values, theta[:, iy, ix]
        )
        Phi_theta[:, iy, ix] = params[0]

        params, _ = optimize.curve_fit(
            test_func2, fields.time[step1:step2].values, ux[:, iy, ix]
        )
        Phi_ux[:, iy, ix] = params[0]

        params, _ = optimize.curve_fit(
            test_func3, fields.time[step1:step2].values, uy[:, iy, ix]
        )
        Phi_uy[:, iy, ix] = params[0]

for iy in range(pressure.shape[1]):
    for ix in range(pressure.shape[2]):
        params, _ = optimize.curve_fit(
            test_func4, fields.time[step1:step2].values, pressure[:, iy, ix]
        )
        Phi_pressure[:, iy, ix] = params[0]

# Extract values
Phi_theta = Phi_theta[0]
Phi_ux = Phi_ux[0]
Phi_uy = Phi_uy[0]
Phi_pressure = Phi_pressure[0]

# Save results
asp_ratio = sim.params.oper.Ly / sim.params.oper.Lx
x_msh = sim.params.oper.nx * sim.params.oper.elem.order
y_msh = sim.params.oper.ny * sim.params.oper.elem.order

fname = f"{path}/A_{asp_ratio}_Pr{prandtl:.2f}_amplitude_phase_omega_sigma_base.h5"
with h5py.File(fname, "w") as out:  # open hdf5 file for writing

    grid = out.create_group("grid")
    grid.create_dataset("x", data=x)
    grid.create_dataset("y", data=y)
    # grid.create_dataset("z", data=z)

    phase = out.create_group("phase")
    phase.create_dataset("phase_theta", data=Phi_theta)
    phase.create_dataset("phase_ux", data=Phi_ux)
    phase.create_dataset("phase_uy", data=Phi_uy)
    phase.create_dataset("phase_pr", data=Phi_pressure)

    amplitude = out.create_group("amplitude")
    amplitude.create_dataset("amplitude_theta", data=A_theta)
    amplitude.create_dataset("amplitude_ux", data=A_ux)
    amplitude.create_dataset("amplitude_uy", data=A_uy)
    amplitude.create_dataset("amplitude_pr", data=A_pressure)

    quantity = out.create_group("quantity")
    quantity.create_dataset("omega", data=omega)
    quantity.create_dataset("Nc", data=Nc)
    quantity.create_dataset("omega_norm", data=omega / Nc)
    quantity.create_dataset("sigma_r", data=sigma_r)
    quantity.create_dataset("prandtl", data=prandtl)
    quantity.create_dataset("asp_ratio", data=asp_ratio)
    quantity.create_dataset("rayleigh", data=sim.params.Ra_side)

    base = out.create_group("base")
    base.create_dataset("ux_base", data=ux_base)
    base.create_dataset("uy_base", data=uy_base)
    base.create_dataset("theta_base", data=theta_base)
    base.create_dataset("pressure_base", data=pressure_base)
