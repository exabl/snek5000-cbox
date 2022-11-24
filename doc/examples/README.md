This solver can simulate convective flows in rectangular cavities in three principal configurations: sidewall convection, Rayleigh-Bénard convection, and mixed case convection, where we include both sidewall and Rayleigh-Bénard convection. This directory provides different scripts to launch simple simulations in various configurations for non-linear and linear formulations.


-------------------------
# 1- Sidewall convection
-------------------------

##Non-linear
-------------------------
One can launch a non-linear simulation in this configuration by command `python` [run_side_simple.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/run_side_simple.py). In this script, we first create the default parameters:

```python
from snek5000_cbox.solver import Simul

params = Simul.create_default_params()
```
then, we change the parameters, such as the dimension of problem, aspect ratio of the cavity, Prandtl and Rayleigh numbers, according to our needs:

```python
params.oper.dim = 2

aspect_ratio = 1.0
params.prandtl = 0.71
params.Ra_side = 1.86e8
```
One can deside where to save the simulation and short name of the directory as:
```python
params.output.sub_directory = "examples_cbox/simple/SW"
params.short_name_type_run = f"Ra{params.Ra_side:.3e}_{nx*order}x{ny*order}"
```
If one wants to change the mesh (number of elements and the polynomial order):

```python
params.oper.ny = nb_elements
params.oper.nx = int(nb_elements / aspect_ratio)
params.oper.elem.order = params.oper.elem.order_out = 8
```
and the geometry (size of the box in deifferent directions):

```python
Ly = params.oper.Ly
Lx = params.oper.Lx = Ly / aspect_ratio
```

It is possible to define probes as history points:

```python
n1d = 5
small = Lx / 10

xs = np.linspace(0, Lx, n1d)
xs[0] = small
xs[-1] = Lx - small

ys = np.linspace(0, Ly, n1d)
ys[0] = small
ys[-1] = Ly - small

coords = [(x, y) for x in xs for y in ys]

if params.oper.dim == 3:

    zs = np.linspace(0, Lz, n1d)
    zs[0] = small
    zs[-1] = Lz - small

    coords = [(x, y, z) for x in xs for y in ys for z in zs]


params.output.history_points.coords = coords
params.oper.max.hist = len(coords) + 1
```
also one wishes to change [other parameters](https://nek5000.github.io/NekDoc/problem_setup/case_files.html#parameter-file-par):
```python
params.nek.general.end_time = 800
params.nek.general.stop_at = "endTime"
params.nek.general.target_cfl = 2.0
params.nek.general.time_stepper = "BDF3"
params.nek.general.extrapolation = "OIFS"

params.nek.general.write_control = "runTime"
params.nek.general.write_interval = 10

params.output.history_points.write_interval = 10
```
Finally, we create the `sim` object and execute the simulation on 4 processors:

```python
sim = Simul(params)

sim.make.exec("run_fg", nproc=4)
```

### 2D
-------------------------

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
We have two possiblities:

1- **Insulated walls in y direction**

The default is insulated horizontal walls.

2- **Periodic boundary conditions in y direction**

One should assign:

```python
params.oper.y_periodicity = True
```

### 3D
-------------------------

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have three possiblities:

1- **Insulated walls in y and z directions**

The default is insulated walls in two other directions.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction and insulated walls in y direction.


3- **Periodic boundary conditions in y and z direction** 

One should assign:

```python
params.oper.y_periodicity = True
params.oper.z_periodicity = True
```

##Linear
-------------------------
One can launch a linear simulation in this configuration by command `python` [run_linear_side_simple.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/run_linear_side_simple.py). For doing a linear simulation, one needs a base state. For this simple example we provide the base state. After creating the default parameters, one needs to define the equation type as:

```python
params.nek.problemtype.equation = "incompLinNS"
```
and restart from the base state:

```python
params.nek.general.start_from = "base_flow.restart"
```
Because [NEK5000](https://nek5000.github.io/NekDoc/) does not support [PnPn formulation](https://nek5000.github.io/NekDoc/faq.html) for linear case yet:

```python
params.oper.elem.staggered = "auto"
```
After creating the `sim` object, we copy the base state field file to the created simulation directory:

```python
restart_file = "./base_flow_side_simple.restart"

sim = Simul(params)

copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")
```

Finally, we execute the linear simulation as:

```python
sim.make.exec("run_fg", nproc=4)
```

##Note on computing the base state
-------------------------
In general, we use [Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/abs/10.1063/1.2211705) as implemented in [KTH-framework](https://kth-nek5000.github.io/KTH_Framework/group__baseflow.html) to compute the base state. In order to compute the base state with our solver, one needs to launch a non-linear simulation with SFD enabled in parameters:

```python
params.oper.enable_sfd = float(True)
```

# 2- Rayleigh-Bénard convection
-------------------------
One can launch a non-linear simulation in this configuration by command `python` [run_RB_simple.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/run_RB_simple.py).
In fact, to simulate the flow in a Rayleigh-Bénard cavity (bottom plate heated and top cooled) one needs to activate it by assigning vertical Rayleigh number, for example in 

```python
params.Ra_vert = 1750
```

In this case, it is possible to have different configuration based on the dimension of the problem and boundary conditions:

## 2D
-------------------------

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
We have two possiblities:

1- **Insulated walls in x direction**

The default is insulated vertical walls.

2- **Periodic boundary conditions in x direction**

One should assign:

```python
params.oper.x_periodicity = True
```

## 3D
-------------------------

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have three possiblities:

1- **Insulated walls in x and z directions**

The default is insulated walls in two other directions.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction and insulated walls in x direction.

3- **Periodic boundary conditions in x and z direction** 

One should assign:

```python
params.oper.x_periodicity = True
params.oper.z_periodicity = True
```
-------------------------
# 3- Mixed case (sidewall convection + Rayleigh-Bénard convection)
-------------------------
One can launch a non-linear simulation in this configuration by command `python` [run_mixed_simple.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/run_mixed_simple.py).
In order to simulate the flow in a cavity that both sidewalls and horizontal ones are differentially heated and cooled, one needs to to activate it by assigning both sidewall and vertical Rayleigh numbers, for example:
```python
params.Ra_side = 5000
params.Ra_vert = 5000
```
In this case, it is possible to have different configuration based on the dimension of the problem and boundary conditions:

## 2D
-------------------------

To activate 2D configuration one needs to assign:
```python
params.oper.dim = 2
```
## 3D
-------------------------

To activate 3D configuration one needs to assign:
```python
params.oper.dim = 3
```
We have two possiblities:

1- **Insulated walls in z direction**

The default is insulated walls in z direction.

2- **Periodic boundary conditions in z direction**

One should assign:

```python
params.oper.z_periodicity = True
```

In this case, we have periodic boundary conditions in z direction.