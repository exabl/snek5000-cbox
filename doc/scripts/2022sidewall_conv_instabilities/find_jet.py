def find_jet_legths(field_base, prandtl, aspect_ratio):
    """
    Computes the horizontal and vertical lengths of a jet in a 2D thermal convection simulation.

    Parameters:
        field_base (xarray.Dataset): The field data from a Snek5000 simulation.
        prandtl (float): The Prandtl number of the simulation.
        aspect_ratio (float): The aspect ratio of the simulation.

    Returns:
        Tuple: A tuple of the horizontal and vertical lengths of the jet.

    """
    # Select the upper half of the field
    field_base = field_base.sel(y=slice(0.5, 1))

    # Set x-range for the slice depending on Prandtl and aspect ratio
    x_min = 0.09
    x_max = field_base.x.max()-0.1

    if prandtl == 0.1:
        if aspect_ratio == 0.5:
            x_min = 0.1
            x_max = field_base.x.max()-0.2
        elif aspect_ratio == 1.5:
            x_min = 0.07
        elif aspect_ratio == 2.0:
            x_min = 0.076

    elif prandtl == 0.2:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.2
        elif aspect_ratio == 1.5:
            x_min = 0.06
        elif aspect_ratio == 2.0:
            x_min = 0.06

    elif prandtl == 0.35:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.2
        elif aspect_ratio == 2.0:
            x_min = 0.06

    elif prandtl == 0.44:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.2
        
    elif prandtl == 0.53:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.2

    elif prandtl == 1.4:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.04
        else:
            x_max = field_base.x.max()-0.05

    elif prandtl == 2.0:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.02
        else:
            x_max = field_base.x.max()-0.05

    elif prandtl == 2.8:
        if aspect_ratio == 0.5:
            x_max = field_base.x.max()-0.01
        else:
            x_max = field_base.x.max()-0.02
    elif prandtl == 4.0:
        x_max = field_base.x.max()-0.01

    # Slice the field data according to the x-range
    field_base_tmp = field_base.sel(x=slice(x_min, x_max))

    # Compute the squared velocity magnitude
    v2 = field_base_tmp.ux**2 + field_base_tmp.uy**2

    # Find the y-coordinate of the maximum velocity magnitude
    y_jet = field_base_tmp.y.values[v2.argmax("y").values[0]]
        

    L_v = 1 - y_jet.min()
    
    # indices = list(np.where(y_jet == y_jet[y_jet.argmin()]))[0]
    # index = indices[-1]
    
    index = y_jet.argmin()
    x_jet = field_base_tmp.x.values[index]
    
    L_h = float(field_base.x.max() - x_jet)

    return L_h, L_v
