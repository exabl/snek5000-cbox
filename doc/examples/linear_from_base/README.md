In this directory, we have the scripts to launch linear simulations around base state
previously computed on the clusters. For instance consider the script `submit_multiple_lin_sim_sidewall.py`. We define the directory of simulation that contains the base state computed
using SFD method. We use the last written field file as base state:

```python
restart_file = sorted(sim.output.path_session.glob("cbox0.f*"))[-1]
```
