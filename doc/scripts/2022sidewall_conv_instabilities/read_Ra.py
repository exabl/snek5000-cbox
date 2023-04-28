def read_Ra(sim):
    """
    Reads the Rayleigh and Grashof numbers of a simulation.

    Parameters:
        sim (Simulation): the simulation object containing the relevant parameters

    Returns:
        Ra (float): the Rayleigh number
        Gr (float): the Grashof number
    """
    prandtl = sim.params.prandtl
    aspect = sim.params.oper.Ly / sim.params.oper.Lx
    Ra = sim.params.Ra_side

    Gr = Ra / prandtl

    return Ra, Gr
