# Restart nonlinear simulations

In this directory, we have the scripts to restart simulations on the clusters. For
instance consider
[submit_restart.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_restart/submit_restart.py)
script. We define the directory of simulation that we want to restart. In
[run_restart.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_restart/run_restart.py),
we have two possibilities to restart:

1. restart from one field file:

    ```python
    params, Simul = load_for_restart(args.path_sim, use_start_from='cbox0.f00018')
    ```

2. restart using multiple check point files as in
[KTH_framework](https://kth-nek5000.github.io/KTH_Framework/group__chkpoint.html):

    ```python
    params, Simul = load_for_restart(args.path_sim, use_checkpoint=2)
    ```
## List of scripts

- submit_retart.py: Script to submit multiple restart on the clusters.
- run_restart.py: Restart simualtion script.