import numpy as np
from compute_growth_frequency_linear_KE import (
    compute_growth_rate_frequency_linear as fgrl,
)


def find_freq(df, params, i):
    """
    Computes the frequency of the i-th history point in a Snek5000 simulation.

    Parameters:
        df (pandas.DataFrame): The data frame containing the history points from a Snek5000 simulation.
        params (sim.params): The parameters of the Snek5000 simulation.
        i (int): The index of the history point to compute the frequency for.

    Returns:
        float: The frequency of the i-th history point.
    """
    growth_rate, freq = fgrl(df, params, i)

    omega = freq * 2 * np.pi

    return omega
