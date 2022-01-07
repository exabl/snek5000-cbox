"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/fsnet/project/meige/2020/20CONVECTION/numerical/"

"""
"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/fsnet/project/meige/2020/20CONVECTION/numerical/"

"""

from shutil import copyfile

from snek5000 import load_params
from snek5000_cbox.solver import Simul

sim_path = ""  # copy paste simulation path here
params = load_params(sim_path)

params.nek.general.start_from = "base_flow.restart"

params.nek.general.write_interval = params.nek.general.end_time
params.output.phys_fields.write_interval_pert_field = 1000
params.nek.problemtype.equation = "incompLinNS"
params.oper.elem.staggered = "auto"
params.NEW_DIR_RESULTS = True
restart_file = params.output.path_session + "/cbox0.f00100"
params.nek.general.extrapolation = "standard"

sim = Simul(params)

copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

sim.make.exec("run_fg", resources={"nproc": 4})
