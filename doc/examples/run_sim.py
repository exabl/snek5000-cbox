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

params.oper.nproc_min = 2
params.oper.dim = 2  # 2D or 3D

params.output.sub_directory = f"examples_cbox/{params.oper.dim}D/A_{aspect_ratio:.2f}"

params.oper.nx = 8  # Number of x elements
params.oper.ny = 8  # Number of y elements
params.oper.nz = 8  # Number of z elements

params.output.history_points.points = [(0.5, 0.2), (0.5, 0.8)]
params.oper.max.hist = 3

Lx = params.oper.Lx = 1.0
params.oper.Ly = Lx * aspect_ratio  # Y aspect ratio

params.nek.general.user_params = {2: Pr_num, 3: Ra_num}

params.oper.elem.order = 9  # Number of points per element

params.nek.general.num_steps = 20000
params.nek.general.write_interval = 100  # Dumping frequency
params.nek.general.dt = 0.005
params.nek.general.time_stepper = "BDF3"  # Time scheme order

sim = Simul(params)

# sim.make.exec(["run_fg"])
sim.make.exec(resources={"nproc": 2})

