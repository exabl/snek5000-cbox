# Nonlinear simulations

In this directory, we have different scripts to launch non-linear simulations on the
clusters with initial condition defined in the
[`cbox.usr.f`](https://github.com/snek5000/snek5000-cbox/blob/main/src/snek5000_cbox/cbox.usr.f)
file. We mainly focus on the scripts to launch sidewall convection simulations. For
instance, in the script
[submit_multiple_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_from_rest/submit_multiple_sim_sidewall.py), we first import the type of job scheduling on clusters using
[fluiddyn](https://fluiddyn.readthedocs.io/en/latest/generated/fluiddyn.clusters.html),
then we define the parameters of simulation.

## Computing the base state for linear studies

In order to computing the base state for
linear studies using
[Selective Frequency Damping (SFD) method](https://aip.scitation.org/doi/full/10.1063/1.2211705),
one needs to assign:

```python
enable_sfd = True
```

## List of scripts

- submit_multiple_sim_sidewall.py: Script to submit multiple non-linear sidewall convection simulations on the clusters.
- submit_multiple_sim_RB.py: Script to submit multiple non-linear Rayleigh-Bénard convection simulations on the clusters.
- submit_multiple_sim_mixed.py: Script to submit multiple non-linear mixed case convection simulations on the clusters.
- run_simul.py: Non-linear simualtion script.
- submit_1simul_check.py: Script to submit one non-linear simulation with check from python on the clusters.
- submit_multiple_check_sidewall.py: Script to submit multiple non-linear sidewall convection simulations with check from python on the clusters.
- submit_multiple_check_RB.py: Script to submit multiple non-linear Rayleigh-Bénard convection simulations with check from python on the clusters.
- run_simul_check_from_python.py: Non-linear simualtion script with check from python.
