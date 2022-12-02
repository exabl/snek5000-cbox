# Linear simulations

In this directory, we have the scripts to launch linear simulations around base state.

For instance, in `submit_multiple_lin_sim_sidewall.py`, we define the directory
of simulation that contains the base state computed using SFD method and use
the last written field file as base state:

```python
restart_file = sorted(sim.output.path_session.glob("cbox0.f*"))[-1]
```

## List of scripts

- `run_simul_linear.py`: run a linear simulation,
- `submit_multiple_lin_sim_sidewall.py`: submit multiple linear simulation.
