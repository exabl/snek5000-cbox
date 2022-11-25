In this directory, we have different scripts to launch non-linear simulations on the clusters with initial condition defined in the [`cbox.usr.f`](https://github.com/snek5000/snek5000-cbox/blob/main/src/snek5000_cbox/cbox.usr.f) file. We mainly focus on the scripts to launch sidewall convection simulations. For instance consider [submit_multiple_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_from_rest/submit_multiple_sim_sidewall.py) script.


In this script, we first import the type of job scheduling on clusters using [fluiddyn](https://fluiddyn.readthedocs.io/en/latest/generated/fluiddyn.clusters.html), then we define the parameters of simulation. 

####Computing the base state for linear studies
In order to computing the base state for linear studies using [Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/full/10.1063/1.2211705), one needs to assign:

```python
enable_sfd = True
```
-----------------------------


