# Nonlinear simulations from rest

In this directory, we have different scripts to launch nonlinear simulations on a
cluster with initial condition defined in the
[`cbox.usr.f`](https://github.com/snek5000/snek5000-cbox/blob/main/src/snek5000_cbox/cbox.usr.f)
file.

## Computing the base state for linear studies

In order to computing the base state for
linear studies using
[Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/full/10.1063/1.2211705),
one needs to assign:

```python
enable_sfd = True
```

## List of scripts

### Scripts defining and launching simulations

- `run_simul.py`: nonlinear stimulation script,
- `run_simul_check_from_python.py`: nonlinear simulation script with checks from python.

### Scripts submitting simulations on a cluster

- `submit_multiple_sim_sidewall.py`: submit `run_simul.py` for multiple sidewall convection simulations,
- `submit_multiple_sim_RB.py`: submit `run_simul.py` for multiple Rayleigh-Bénard convection simulations,
- `submit_multiple_sim_mixed.py`: submit `run_simul.py` for multiple mixed case convection simulations,

- `submit_1simul_check.py`: submit `run_simul_check_from_python.py` for one simulation with checks from python,
- `submit_multiple_check_sidewall.py`: submit `run_simul_check_from_python.py` for multiple sidewall convection simulations with checks from python,
- `submit_multiple_check_RB.py`: submit `run_simul_check_from_python.py` for multiple Rayleigh-Bénard convection simulations with checks from python.
