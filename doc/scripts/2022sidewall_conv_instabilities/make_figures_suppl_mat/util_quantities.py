import numpy as np
import h5py

from util import path_base

path_data = f"{path_base}/Prs_As_quantities.h5"

with h5py.File(path_data, "r") as file:
    aspect_ratios = np.array(file["quantity/asp_ratios"])
    prandtls = np.array(file["quantity/prandtls"])


def get_quantity(key):
    with h5py.File(path_data, "r") as file:
        return np.array(file[f"quantity/{key}"])
