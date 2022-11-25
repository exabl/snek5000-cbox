In this directory, we have the scripts to launch linear simulations around base state previously computed on the clusters. For instance consider [submit_multiple_lin_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/linear_from_base/submit_multiple_lin_sim_sidewall.py) script. We define the directory of simulation that contains the base state computed using SFD method:

```python
prandtl = 0.2
aspect_ratio = 2.0
dim = 2

dir_sim = (
    f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/SFD/"
    f"Pr_{prandtl:.2f}/asp_{aspect_ratio:.3f}"
)
path = Path(dir_sim)
sim_dirs = sorted(path.glob("cbox_*"))
```

we use the last written field file as base state:

```python
restart_file = sorted(sim.output.path_session.glob("cbox0.f*"))[-1]
```

