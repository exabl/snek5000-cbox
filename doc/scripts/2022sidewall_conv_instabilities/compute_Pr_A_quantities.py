import numpy as np
import h5py

from pathlib import Path

from snek5000 import load

from find_jet import find_jet_lengths
from find_Nc import find_Nc
from find_Rac import find_Rac
from read_Ra import read_Ra
from find_omega import find_freq


asp_ratios = [0.5, 1.0, 1.5, 2.0]
prandtls = [0.1, 0.2, 0.35, 0.44, 0.53, 0.62, 0.69, 0.71, 1.0, 1.4, 2.0, 2.8, 4.0]
dim = 2

dir_save = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim"
path = Path(dir_save)

Lh_Prs = [[] for i in range(len(prandtls))]
Lh_As = [[] for i in range(len(asp_ratios))]

Lv_Prs = [[] for i in range(len(prandtls))]
Lv_As = [[] for i in range(len(asp_ratios))]

omega_Prs = [[] for i in range(len(prandtls))]
omega_As = [[] for i in range(len(asp_ratios))]

Nc_Prs = [[] for i in range(len(prandtls))]
Nc_As = [[] for i in range(len(asp_ratios))]

omega_norm_Prs = [[] for i in range(len(prandtls))]
omega_norm_As = [[] for i in range(len(asp_ratios))]

Rac_Prs = [[] for i in range(len(prandtls))]
Grc_Prs = [[] for i in range(len(prandtls))]

Rac_As = [[] for i in range(len(asp_ratios))]
Grc_As = [[] for i in range(len(asp_ratios))]

Ra_Prs = [[] for i in range(len(prandtls))]
Gr_Prs = [[] for i in range(len(prandtls))]

Ra_As = [[] for i in range(len(asp_ratios))]
Gr_As = [[] for i in range(len(asp_ratios))]


for asp_ratio in asp_ratios:

    for prandtl in prandtls:
        if (asp_ratio in [0.5, 1.5, 2.0]) and prandtl == 4.0:
            continue
        else:
            dir_base = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim/Pr_{prandtl:.2f}/asp_{asp_ratio:.3f}"
            path_sim = Path(dir_base)
            sim_dirs = sorted(path_sim.glob("cbox_*"))

            dir_sim = sim_dirs[0]

            sim = load(dir_sim)

            params = sim.params
            coords, df = sim.output.history_points.load()
            i = 0

            field_base = sim.output.phys_fields.load()
            x_new = np.linspace(field_base.x[0], field_base.x[-1], field_base.x.size)
            y_new = np.linspace(field_base.y[0], field_base.y[-1], field_base.y.size)

            field_base = field_base.drop_duplicates(["x", "y"])
            field_base = field_base.interp(x=x_new, y=y_new, method="cubic")

            Ra, Gr = read_Ra(sim)
            omega = find_freq(df, params, i)
            N_c, gradT_c = find_Nc(field_base, prandtl, asp_ratio)
            L_h, L_v = find_jet_lengths(field_base, prandtl, asp_ratio)

            Ra_c, Gr_c = find_Rac(sim_dirs)

            for i in range(len(asp_ratios)):

                if asp_ratio == asp_ratios[i]:

                    if omega is not None and N_c is not None:
                        omega_norm_As[i].append(omega / N_c)

                    omega_As[i].append(omega)
                    Nc_As[i].append(N_c)
                    Lh_As[i].append(L_h)
                    Lv_As[i].append(L_v)
                    Rac_As[i].append(Ra_c)
                    Grc_As[i].append(Gr_c)
                    Ra_As[i].append(Ra)
                    Gr_As[i].append(Gr)

            for j in range(len(prandtls)):

                if prandtl == prandtls[j]:

                    if omega is not None and N_c is not None:
                        omega_norm_Prs[j].append(omega / N_c)

                    omega_Prs[j].append(omega)
                    Nc_Prs[j].append(N_c)
                    Lh_Prs[j].append(L_h)
                    Lv_Prs[j].append(L_v)
                    Rac_Prs[j].append(Ra_c)
                    Grc_Prs[j].append(Gr_c)
                    Ra_Prs[j].append(Ra)
                    Gr_Prs[j].append(Gr)


Lh_Prs[-1] = [np.nan, Lh_Prs[-1][0], np.nan, np.nan]
Lh_As[0].append(np.nan)
Lh_As[2].append(np.nan)
Lh_As[3].append(np.nan)

Lv_Prs[-1] = [np.nan, Lv_Prs[-1][0], np.nan]
Lv_As[0].append(np.nan)
Lv_As[2].append(np.nan)
Lv_As[3].append(np.nan)

omega_Prs[-1] = [np.nan, omega_Prs[-1][0], np.nan, np.nan]
omega_As[0].append(np.nan)
omega_As[2].append(np.nan)
omega_As[3].append(np.nan)

Nc_Prs[-1] = [np.nan, Nc_Prs[-1][0], np.nan, np.nan]
Nc_As[0].append(np.nan)
Nc_As[2].append(np.nan)
Nc_As[3].append(np.nan)

omega_norm_Prs[-1] = [np.nan, omega_norm_Prs[-1][0], np.nan, np.nan]
omega_norm_As[0].append(np.nan)
omega_norm_As[2].append(np.nan)
omega_norm_As[3].append(np.nan)

Rac_Prs[-1] = [np.nan, Rac_Prs[-1][0], np.nan, np.nan]
Grc_Prs[-1] = [np.nan, Grc_Prs[-1][0], np.nan, np.nan]

Rac_As[0].append(np.nan)
Rac_As[2].append(np.nan)
Rac_As[3].append(np.nan)
Grc_As[0].append(np.nan)
Grc_As[2].append(np.nan)
Grc_As[3].append(np.nan)

Ra_Prs[-1] = [np.nan, Ra_Prs[-1][0], np.nan, np.nan]
Gr_Prs[-1] = [np.nan, Gr_Prs[-1][0], np.nan, np.nan]

Ra_As[0].append(np.nan)
Ra_As[2].append(np.nan)
Ra_As[3].append(np.nan)
Gr_As[0].append(np.nan)
Gr_As[2].append(np.nan)
Gr_As[3].append(np.nan)

fname = f"{path}/Prs_As_quantities.h5"
with h5py.File(fname, "w") as out:  # open hdf5 file for writing

    quantity = out.create_group("quantity")

    quantity.create_dataset("asp_ratios", data=np.array(asp_ratios, dtype=np.float64))
    quantity.create_dataset("prandtls", data=np.array(prandtls, dtype=np.float64))

    quantity.create_dataset("Lh_Prs", data=(np.array(Lh_Prs, dtype=np.float64)))
    quantity.create_dataset("Lh_As", data=(np.array(Lh_As, dtype=np.float64)))

    quantity.create_dataset("Lv_Prs", data=(np.array(Lv_Prs, dtype=np.float64)))
    quantity.create_dataset("Lv_As", data=(np.array(Lv_As, dtype=np.float64)))

    quantity.create_dataset("omega_Prs", data=(np.array(omega_Prs, dtype=np.float64)))
    quantity.create_dataset("omega_As", data=(np.array(omega_As, dtype=np.float64)))

    quantity.create_dataset("Nc_Prs", data=(np.array(Nc_Prs, dtype=np.float64)))
    quantity.create_dataset("Nc_As", data=(np.array(Nc_As, dtype=np.float64)))

    quantity.create_dataset(
        "omega_norm_Prs", data=(np.array(omega_norm_Prs, dtype=np.float64))
    )
    quantity.create_dataset(
        "omega_norm_As", data=(np.array(omega_norm_As, dtype=np.float64))
    )

    quantity.create_dataset("Rac_Prs", data=(np.array(Rac_Prs, dtype=np.float64)))
    quantity.create_dataset("Rac_As", data=(np.array(Rac_As, dtype=np.float64)))

    quantity.create_dataset("Grc_Prs", data=(np.array(Grc_Prs, dtype=np.float64)))
    quantity.create_dataset("Grc_As", data=(np.array(Grc_As, dtype=np.float64)))

    quantity.create_dataset("Ra_Prs", data=(np.array(Ra_Prs, dtype=np.float64)))
    quantity.create_dataset("Ra_As", data=(np.array(Ra_As, dtype=np.float64)))

    quantity.create_dataset("Gr_Prs", data=(np.array(Gr_Prs, dtype=np.float64)))
    quantity.create_dataset("Gr_As", data=(np.array(Gr_As, dtype=np.float64)))
