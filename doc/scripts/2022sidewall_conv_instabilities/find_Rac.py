import numpy as np

from compute_growth_frequency_linear_KE import (
    compute_growth_rate_frequency_linear as fgrl,
)

from snek5000 import load


def find_Rac(sim_dirs):
    """
    Given a list of simulation directories, calculates the critical Rayleigh number
    and critical Grashof number based on the growth rate of the linear instability.

    Parameters:
        sim_dirs (list): A list of strings representing the directories where the
                         simulations are located.

    Returns:
        Ra_c (float): The critical Rayleigh number.
        Gr_c (float): The critical Grashof number.
    """

    Ra = []
    sigma_r = []
    frequency = []

    for i in range(len(sim_dirs)):

        sim = load(sim_dirs[i])
        params = sim.params
        coords, df = sim.output.history_points.load()

        growth_rate, freq = fgrl(df, params, 0)
        sigma_r.append(growth_rate)
        frequency.append(freq)
        Ra.append(params.Ra_side)

    z = np.polyfit(Ra, sigma_r, 1)
    p = np.poly1d(z)
    Ra_c = p.r[-1]
    Gr_c = Ra_c / params.prandtl

    return Ra_c, Gr_c
