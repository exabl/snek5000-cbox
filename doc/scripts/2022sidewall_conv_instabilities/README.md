- The base states are computed from launching [`submit_multiple_sim_sidewall.py`](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_from_rest/submit_multiple_sim_sidewall.py) with `enable_sfd = True`. 

- The linear simulations are performed using [submit_multiple_lin_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/linear_from_base/submit_multiple_lin_sim_sidewall.py).

## List of scripts

- `compute_amplitude_phase_maps.py`: save the amplitude, phase, frequency, and growth rate of the leading linear mode by defining the directory of the linear simulations.

- `compute_growth_frequency_linear_KE.py`: function for computing the growth rate of the linear mode.

-`save_base_flows.py`: save the base states,

- `find_jet.py`: function for finding the length of oscillation of plume,

- `find_Nc.py`: function for finding the Brunt-Väisälä frequency at the center,

- `find_omega.py`: function for finding the angular frequency of the linear mode,

- `find_Rac.py`: function for finding the critical Rayleigh and Grashhof numebrs.