import numpy as np
from scipy import stats
from scipy.signal import argrelmax, hilbert


def compute_growth_rate_frequency_linear(df, params, index_point):
    """
    Computes the growth rate and frequency of a linear signal from a DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        A DataFrame containing the time history of the ux, uy, theta variables.
    params : object
        An object containing the simulation parameters.
    index_point : int
        The index of the point for which the growth rate and frequency are computed.

    Returns
    -------
    sigma_r : float
        The computed growth rate of the signal.
    frequency : float
        The computed frequency of the signal.
    """

    df_point = df[df.index_points == index_point]

    time = df_point["time"].to_numpy()
    ux = df_point["ux"].to_numpy()
    uy = df_point["uy"].to_numpy()

    fs = time.shape[0] / time.max()  # sampling frequency

    step1 = np.where(time > 200)[0][0]
    step2 = np.where(time < time.max())[0][-1]

    time = time[step1:step2]
    ux = ux[step1:step2]
    uy = uy[step1:step2]

    kinetic_energy = 0.5 * (ux**2 + uy**2)
    signal = kinetic_energy

    local_maxima = argrelmax(signal)
    time_loc_max = time[local_maxima]
    signal_loc_max = signal[local_maxima]

    slope, intercept, _, _, _ = stats.linregress(time_loc_max, np.log(signal_loc_max))
    sigma_r = slope / 2

    step_for_filter = int((step2 - step1) / 10)
    filter_hyp_tangent = ((1 + np.tanh((time - time[step_for_filter]) / 30)) / 5) - (
        (1 + np.tanh((time - time[-step_for_filter]) / 30)) / 5
    )

    filtered_signal = ux * filter_hyp_tangent
    analytic_signal = hilbert(filtered_signal)
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_angle = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = np.diff(instantaneous_angle) / (2.0 * np.pi) * fs

    step3 = np.where(time > time[9 * step_for_filter])[0][0]
    step4 = np.where(time < time[int(9.3 * step_for_filter)])[0][-1]

    frequency = instantaneous_frequency[step3:step4].mean()

    return sigma_r, frequency
