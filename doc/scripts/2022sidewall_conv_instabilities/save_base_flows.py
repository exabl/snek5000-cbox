from pathlib import Path

import numpy as np
import h5py

from snek5000 import load


asp_ratios = [0.5, 1.0, 1.5, 2.0]
prandtls = [0.1, 0.2, 0.35, 0.44, 0.53, 0.62, 0.69, 0.71, 1.0, 1.4, 2.8]

dim = 2

dir_save = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim"

path_save = Path(dir_save)

for asp_ratio in asp_ratios:

    for prandtl in prandtls:

        dir_base = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim/Pr_{prandtl:.2f}/asp_{asp_ratio:.3f}"
        path = Path(dir_base)
        sim_dirs = sorted(path.glob("cbox_*"))
        dir_sim = sim_dirs[0]

        sim = load(dir_sim)

        prandtl = sim.params.prandtl
        aspect = sim.params.oper.Lx / sim.params.oper.Ly
        rayleigh = sim.params.Ra_side

        field_base = sim.output.phys_fields.load()

        x_new = np.linspace(field_base.x[0], field_base.x[-1], field_base.x.size)
        y_new = np.linspace(field_base.y[0], field_base.y[-1], field_base.y.size)

        field_base = field_base.drop_duplicates(["x", "y"])
        field_base = field_base.interp(x=x_new, y=y_new, method="cubic")

        x = field_base.x.values
        y = field_base.y.values

        ux_base = field_base.ux[0].values
        uy_base = field_base.uy[0].values

        theta_base = field_base.temperature[0].values
        pressure_base = field_base.pressure[0].values

        fname = f"{path_save}/A_{asp_ratio}_Pr{prandtl:.2f}_base_state.h5"
        with h5py.File(fname, "w") as out:  # open hdf5 file for writing

            grid = out.create_group("grid")
            grid.create_dataset("x", data=x)
            grid.create_dataset("y", data=y)
            # grid.create_dataset("z", data=z)

            quantity = out.create_group("quantity")
            quantity.create_dataset("prandtl", data=prandtl)
            quantity.create_dataset("asp_ratio", data=asp_ratio)
            quantity.create_dataset("rayleigh", data=sim.params.Ra_side)

            base = out.create_group("base")
            base.create_dataset("ux_base", data=ux_base)
            base.create_dataset("uy_base", data=uy_base)
            base.create_dataset("theta_base", data=theta_base)
            base.create_dataset("pressure_base", data=pressure_base)
