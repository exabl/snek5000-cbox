# Examples of scripts using the snek5000-cbox solver

This solver can simulate convective flows in rectangular cavities in three principal
configurations: sidewall convection, Rayleigh-Bénard convection, and mixed case
convection, where we include both sidewall and Rayleigh-Bénard convection. This
directory provides different scripts to launch simple simulations in various
configurations for non-linear and linear formulations.

## 2 dimensions or 3 dimensions

To activate 2D/3D configuration one, needs to assign:

```python
params.oper.dim = 2  # or 3
```

## Boundary conditions

We have three possibilities:

1. **Insulated walls in y and z directions**

    The default is insulated walls in two other directions.

2. **Periodic boundary conditions in z direction**

    One should assign:

    ```python
    params.oper.z_periodicity = True
    ```

    In this case, we have periodic boundary conditions in z direction and insulated walls in
    y direction.

3. **Periodic boundary conditions in y and z direction**

    One should assign:

    ```python
    params.oper.y_periodicity = True
    params.oper.z_periodicity = True
    ```

## Different forcing mechanisms

### Sidewall convection

One can launch a non-linear simulation in this configuration by command `python run_side_simple.py`.
In this script, we first create the default parameters, then, we change the parameters,
such as the dimension of problem, aspect ratio of the cavity, Prandtl and Rayleigh
numbers, according to our needs. One can deside where to save the simulation and short
name of the directory. Also one can change
[other parameters](https://nek5000.github.io/NekDoc/problem_setup/case_files.html#parameter-file-par):

### Rayleigh-Bénard convection

One can launch a non-linear simulation in this configuration by command `python run_RB_simple.py`.
In fact, to simulate the flow in a Rayleigh-Bénard cavity (bottom plate heated and top
cooled) one needs to activate it by assigning vertical Rayleigh number, for example in

```python
params.Ra_vert = 1750
```

### Mixed case (sidewall convection + Rayleigh-Bénard convection)

One can launch a non-linear simulation in this configuration by command `python run_mixed_simple.py`.
In order to simulate the flow in a cavity that both sidewalls and horizontal ones are
differentially heated and cooled, one needs to to activate it by assigning both sidewall
and vertical Rayleigh numbers, for example:

```python
params.Ra_side = 5000
params.Ra_vert = 5000
```

## Non-linear or linear simulations

### Linear

One can launch a linear simulation in this configuration by command `python run_linear_side_simple.py`.
For doing a linear simulation, one needs a base state. For this simple example we
provide the base state.

````{admonition} Note on computing the base state

In general, we use
[Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/abs/10.1063/1.2211705)
as implemented in
[KTH-framework](https://kth-nek5000.github.io/KTH_Framework/group__baseflow.html) to
compute the base state. In order to compute the base state with our solver, one needs to
launch a non-linear simulation with SFD enabled in parameters:

```python
params.oper.enable_sfd = float(True)
```

````

## List of files and directories

### Directories

- nonlinear_from_rest: scripts to launch non-linear simulations on the computational clusters,
- nonlinear_restart: script to launch restart non-linear simulations on the computational clusters,
- linear_from_base: scripts to launch linear simulations on the computational clusters.

### Files

- `base_flow_side_simple.restart`: base state used in `run_linear_side_simple.py`, computed with `run_side_simple.py`,
- `run_side_short.py`: launch a short non-linear sidewall convection simulation,
- `run_side_simple.py`: launch a non-linear sidewall convection simulation,
- `run_linear_side_simple.py`: launch a linear sidewall convection simulation with provided base state `base_flow_side_simple.restart`,
- `run_RB_simple.py`: launch a non-linear Rayleigh-Bénard convection simulation,
- `run_linear_RB_simple.py`: launch a linear Rayleigh-Bénard convection simulation (analytical base state),
- `run_mixed_simple.py`: launch a non-linear mixed case convection simulation.
