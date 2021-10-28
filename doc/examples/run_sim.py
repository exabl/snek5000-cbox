"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/.fsnet/project/meige/2020/20CONVECTION/numerical/"

"""

from snek5000_cbox.solver import Simul
# from phill.solver import Simul

params = Simul.create_default_params()

aspect_ratio = 1.
Pr_num = 0.71  # Prandtl number
Ra_num = 1.0e08  # Rayleigh number

params.output.sub_directory = "examples_cbox"

params.oper.nproc_min = 2
params.oper.dim = 2

# number of elements
params.oper.nx = 8
params.oper.ny = 8
params.oper.nz = 8

Lx = params.oper.Lx = 1.0
params.oper.Ly = Lx * aspect_ratio

params.oper.elem.order = 9

coords = params.output.history_points.coords = [(0.5, 0.2), (0.5, 0.8)]
params.oper.max.hist = len(coords) + 1

params.nek.general.user_params = {2: Pr_num, 3: Ra_num}

params.nek.general.num_steps = 20000
params.nek.general.write_interval = 100
params.nek.general.dt = 0.005
params.nek.general.time_stepper = "BDF3"

sim = Simul(params)

# sim.make.exec(["run_fg"])
sim.make.exec(resources={"nproc": 2})

