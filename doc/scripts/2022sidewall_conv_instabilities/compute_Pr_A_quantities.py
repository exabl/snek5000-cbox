import numpy as np
import h5py
from pathlib import Path

from snek5000 import load

from find_jet import find_jet_lengths
from find_Nc import find_Nc
from find_Rac import find_Rac
from read_Ra import read_Ra
from find_omega import find_freq

# Define variables
asp_ratios = [0.5, 1.0, 1.5, 2.0]
prandtls = [0.1, 0.2, 0.35, 0.44, 0.53, 0.62, 0.69, 0.71, 1.0, 1.4, 2.0, 2.8, 4.0]
dim = 2
dir_save = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim"
path = Path(dir_save)

# Create dictionary to hold data
data_dict = {}
for quantity in ["Lh", "Lv", "omega", "Nc", "omega_norm", "Rac", "Grc", "Ra", "Gr"]:
    data_dict[f"{quantity}_Prs"] = [[] for i in range(len(prandtls))]
    data_dict[f"{quantity}_As"] = [[] for i in range(len(asp_ratios))]

# Loop through simulations
for asp_ratio in asp_ratios:
    for prandtl in prandtls:
        if (asp_ratio in [0.5, 1.5, 2.0]) and prandtl == 4.0:
            continue
        else:
            # Load simulation
            dir_base = f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/Lin_sim/Pr_{prandtl:.2f}/asp_{asp_ratio:.3f}"
            path_sim = Path(dir_base)
            sim_dirs = sorted(path_sim.glob("cbox_*"))
            dir_sim = sim_dirs[0]
            sim = load(dir_sim)

            # Process data
            params = sim.params
            coords, df = sim.output.history_points.load()
            field_base = sim.output.phys_fields.load()
            x_new = np.linspace(field_base.x[0], field_base.x[-1], field_base.x.size)
            y_new = np.linspace(field_base.y[0], field_base.y[-1], field_base.y.size)
            field_base = field_base.drop_duplicates(["x", "y"])
            field_base = field_base.interp(x=x_new, y=y_new, method="cubic")
            Ra, Gr = read_Ra(sim)
            omega = find_freq(df, params, 0)
            N_c, gradT_c = find_Nc(field_base, prandtl, asp_ratio)
            L_h, L_v = find_jet_lengths(field_base, prandtl, asp_ratio)
            Ra_c, Gr_c = find_Rac(sim_dirs)

            # Append data to dictionary
            for i in range(len(asp_ratios)):

                if asp_ratio == asp_ratios[i]:

                    if omega is not None and N_c is not None:
                        data_dict["omega_norm_As"][i].append(omega / N_c)

                    data_dict["omega_As"][i].append(omega)
                    data_dict["Nc_As"][i].append(N_c)
                    data_dict["Lh_As"][i].append(L_h)
                    data_dict["Lv_As"][i].append(L_v)
                    data_dict["Rac_As"][i].append(Ra_c)
                    data_dict["Grc_As"][i].append(Gr_c)
                    data_dict["Ra_As"][i].append(Ra)
                    data_dict["Gr_As"][i].append(Gr)

            for j in range(len(prandtls)):

                if prandtl == prandtls[j]:

                    if omega is not None and N_c is not None:
                        data_dict["omega_norm_Prs"][j].append(omega / N_c)

                    data_dict["omega_Prs"][j].append(omega)
                    data_dict["Nc_Prs"][j].append(N_c)
                    data_dict["Lh_Prs"][j].append(L_h)
                    data_dict["Lv_Prs"][j].append(L_v)
                    data_dict["Rac_Prs"][j].append(Ra_c)
                    data_dict["Grc_Prs"][j].append(Gr_c)
                    data_dict["Ra_Prs"][j].append(Ra)
                    data_dict["Gr_Prs"][j].append(Gr)

# Update the lists with NaN values as needed
for quantity in ["Lh", "Lv", "omega", "Nc", "omega_norm", "Rac", "Grc", "Ra", "Gr"]:
    data_dict[f"{quantity}_Prs"][-1] = [
        np.nan,
        data_dict[f"{quantity}_Prs"][-1][0],
        np.nan,
        np.nan,
    ]
    data_dict[f"{quantity}_As"][0].append(np.nan)
    data_dict[f"{quantity}_As"][2].append(np.nan)
    data_dict[f"{quantity}_As"][3].append(np.nan)

# Write data to HDF5 file
path_file = f"{path}/Prs_As_quantities.h5"
with h5py.File(path_file, "w") as out:

    quantity = out.create_group("quantity")

    quantity.create_dataset("asp_ratios", data=np.array(asp_ratios, dtype=np.float64))
    quantity.create_dataset("prandtls", data=np.array(prandtls, dtype=np.float64))

    for quantity in ["Lh", "Lv", "omega", "Nc", "omega_norm", "Rac", "Grc", "Ra", "Gr"]:
        quantity_Prs = data_dict[f"{quantity}_Prs"]
        quantity_As = data_dict[f"{quantity}_As"]

        quantity.create_dataset(
            f"{quantity}_Prs", data=np.array(quantity_Prs, dtype=np.float64)
        )
        quantity.create_dataset(
            f"{quantity}_As", data=np.array(quantity_As, dtype=np.float64)
        )
