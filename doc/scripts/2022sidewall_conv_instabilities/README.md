- The base states are computed from launching [`submit_multiple_sim_sidewall.py`](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/nonlinear_from_rest/submit_multiple_sim_sidewall.py) with `enable_sfd = True`. 

- The linear simulations are performed using [submit_multiple_lin_sim_sidewall.py](https://github.com/snek5000/snek5000-cbox/blob/main/doc/examples/linear_from_base/submit_multiple_lin_sim_sidewall.py).

## List of scripts to create datasets

- `compute_amplitude_phase_maps.py`: save the amplitude, phase, frequency, and growth rate of the leading linear mode by defining the directory of the linear simulations,

- `compute_growth_frequency_linear_KE.py`: function for computing the growth rate of the linear mode,

- `compute_Pr_A_quantities.py`: function for computing the simulation quantities,
- 
- `save_base_flows.py`: save the base states,

- `find_jet.py`: function for finding the length of oscillation of plume,

- `find_Nc.py`: function for finding the Brunt-Väisälä frequency at the center,

- `find_omega.py`: function for finding the angular frequency of the linear mode,

- `find_Rac.py`: function for finding the critical Rayleigh and Grashhof numebrs,

- `read_Ra.py`: function for reading the Rayleigh and Grashof numbers of a simulation.

## List of scripts to produce figures

- `util.py`: utilities for producing the figures; one needs to define the path of datasets in this script. 

- `make_figures.py`: produce all the figures,
   
- `make_suppl_mat.py`: produce all the supplementary material,
     
- `util_sketch.py`: utilities for the sketch of problem,
  
- `util_quantities.py`: utilities for reading quantities,

- `save_geometry_sketch.py`: geometry sketch of problem,

- `save_diagnostic_sketch.py`: diagnostic sketch of problem,
  
- `save_graphical_abstract.py`:  one figure for graphical abstract,

- `save_anim_base_pert.py`: animations of the base state plus perturbation,
  
- `save_anim_base_pert_stream.py`: animations of the base state plus perturbation with stream lines,

- `save_anim_vort_pert.py`: animations of the perturbation vorticity,

- `save_base_flow_stream_subplotsA.py`: base states for different aspect ratios,

- `save_base_flow_stream_subplotsPr.py`: base states for different Prandtl numbers,

- `save_base_stream_amp_phase_maps_regimes.py`: different subfigures; base state, amplitude and phase map, perturbation vorticity, base state plus perturbation,

- `save_base_amp_maps_corner_regimes.py`: zoom on corner regimes,

- `save_Grc_vs_Pr.py`: critical Grashof number versus Prandtl,

- `save_Rac_vs_Pr.py`: critical Rayleigh number versus Prandtl,
  
- `save_Rec_vs_Pr.py`: critical Reynolds number versus Prandtl,
- 
- `save_Lh_vs_Pr.py`: length of oscillation versus Prandtl,

- `save_Nc_vs_Pr.py`: Brunt–Väisälä frequency at center of cavity versus Prandtl,

- `save_omega_vs_Pr.py`: angular frequency versus Prandtl,

- `save_omega_norm_vs_Pr.py`: normalized angular frequency versus Prandtl,

- `save_regimes_A_vs_Pr.py`: regime diagram.
  
