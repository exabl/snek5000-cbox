In this directory, we have have the scripts to restart simulations on the clusters. For instance consider [submit_restart.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_restart/submit_restart.py) script. We define the directory of simulation that we want to restart as:

```python
prandtl = 0.71
aspect_ratio = 1.0

dim = 3

dir_sim = (
    f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/NL_sim/"
    f"Pr_{prandtl:.2f}/asp_{aspect_ratio:.3f}"
)
path = Path(dir_sim)
sim_dirs = sorted(path.glob(f"*Az4.000_Ra_s*"))
path_sim = sim_dirs[0]
```

In [run_restart.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_restart/run_restart.py), we have two possibilities to restart:

-restart from one field file:

```python
params, Simul = load_for_restart(args.path_sim, use_start_from='cbox0.f00018')
```
-or restart using multiple check point files as in [KTH_framework](https://kth-nek5000.github.io/KTH_Framework/group__chkpoint.html):

```python
params, Simul = load_for_restart(args.path_sim, use_checkpoint=2)
```
