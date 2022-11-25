In this directory, we have different scripts to launch non-linear simulations on the clusters with initial condition defined in the [`cbox.usr.f`](https://github.com/snek5000/snek5000-cbox/blob/main/src/snek5000_cbox/cbox.usr.f) file. We mainly focus on the scripts to launch sidewall convection simulations. For instance consider [submit_multiple_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_from_rest/submit_multiple_sim_sidewall.py) script.


In this script, we first import the type of job scheduling on clusters using [fluiddyn](https://fluiddyn.readthedocs.io/en/latest/generated/fluiddyn.clusters.html), then we define the parameters of simulation. 

-----------------------------
####Dimension of the problem

One can launch a two or three dimensional simulation:

```python
dim = 2

if dim == 3:
    aspect_ratio_z = 1.0

aspect_ratio_y = 0.5
```
For a three dimensional simulation, one needs to define `aspect_ratio_z`. `aspect_ratio_y` and `aspect_ratio_z` are `Ly/Lx` and `Ly/Lz` respectively.

####Control parameters

```python
prandtl = 0.71
Ra_numbs = [1.8e8]
```
One can define multiple Rayleigh numbers here.

####Mesh
For the number of elements in `y` direction, the polynomial order in each element, and mesh stretch factor, one needs to change the following parameters:

```python
ny = 32
order = 10
stretch_factor = 0.0
```

####Integration time

```python
end_time = 4000
dt = 0.05
```

####
One can specify the number of nodes, the number of processors on each node, and walltime of the simulation as following:

```python
nb_procs = 10
nb_nodes = 1
walltime = "24:00:00"
```

####Boundary condition
In the sidewall configuration, one can put the periodic boundary condition in `y` and `z` directions.

```python
y_periodicity = True
z_periodicity = True
```
####Computing the base state for linear studies
In order to computing the base state for linear studies using [Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/full/10.1063/1.2211705), one needs to assign:

```python
enable_sfd = True
```
-----------------------------


