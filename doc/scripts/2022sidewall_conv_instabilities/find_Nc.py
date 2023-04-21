import numpy as np


def find_Nc(field_base, prandtl, aspect_ratio):
    """
    Calculate the maximum vertical gradient of temperature and the corresponding
    maximum Brunt-Väisälä frequency in the central region of a simulation domain.

    Parameters:
        field_base (xarray dataset): The xarray dataset containing the simulation data.
        prandtl (float): The Prandtl number of the fluid.
        aspect_ratio (float): The aspect ratio of the simulation domain.

    Returns:
        tuple: A tuple containing the maximum Brunt-Väisälä frequency and the maximum
        vertical gradient of temperature in the central region of the simulation domain.
    """

    # Select the temperature field and compute its vertical gradient
    T = field_base.temperature[0]
    dTdy = T.differentiate("y")

    # Select the central region of the simulation domain
    gradT = dTdy.sel(
        x=slice(0.1 / aspect_ratio, 0.9 / aspect_ratio), y=slice(0.5, 0.51)
    )

    # Compute the Brunt-Väisälä frequency in the central region of the simulation domain
    N = np.sqrt(
        prandtl
        * dTdy.sel(x=slice(0.1 / aspect_ratio, 0.9 / aspect_ratio), y=slice(0.5, 0.51))
    )

    # Find the maximum Brunt-Väisälä frequency and the corresponding maximum vertical gradient of temperature
    Nc = N.values.max()
    gradTc = gradT.values.max()

    return Nc, gradTc
