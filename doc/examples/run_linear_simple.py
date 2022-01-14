"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/fsnet/project/meige/2020/20CONVECTION/numerical/"

"""
import numpy as np
from shutil import copyfile

from snek5000 import load_params
from snek5000_cbox.solver import Simul

## nonlinear simulation

params = Simul.create_default_params()

aspect_ratio = 1.0
params.prandtl = 0.71

# for aspect ratio 1, Ra_c = 1.825e08
params.rayleigh = 1.830e08

params.output.sub_directory = "examples_cbox/simple"

params.oper.nproc_min = 2
params.oper.dim = 2

nb_elements = nx = ny = 8
params.oper.nx = nb_elements
params.oper.ny = int(nb_elements * aspect_ratio)
params.oper.nz = nb_elements

Lx = params.oper.Lx = 1.0
Ly = params.oper.Ly = Lx * aspect_ratio

order = params.oper.elem.order = params.oper.elem.order_out = 10

params.oper.mesh_stretch_factor = 0.08  # zero means regular

params.short_name_type_run = f"Ra{params.rayleigh:.3e}_{nx*order}x{ny*order}"

# creation of the coordinates of the points saved by history points
n1d = 5
small = Lx / 10

xs = np.linspace(0, Lx, n1d)
xs[0] = small
xs[-1] = Lx - small

ys = np.linspace(0, Ly, n1d)
ys[0] = small
ys[-1] = Ly - small

coords = [(x, y) for x in xs for y in ys]

params.output.history_points.coords = coords
params.oper.max.hist = len(coords) + 1

params.nek.general.dt = 0.005
params.nek.general.time_stepper = "BDF3"

params.nek.general.end_time = 1000
params.nek.general.stop_at = "endTime"

params.nek.general.write_control = "runTime"
params.nek.general.write_interval = 10.0

params.output.history_points.write_interval = 10

sim = Simul(params)

sim.make.exec("run_fg", resources={"nproc": 4})

## linear simulation

params = load_params(sim.path_run)

params.nek.general.start_from = "base_flow.restart"

params.rayleigh = 1.835e08
params.nek.general.write_interval = params.nek.general.end_time
params.output.phys_fields.write_interval_pert_field = 100
params.nek.problemtype.equation = "incompLinNS"
params.oper.elem.staggered = "auto"
params.NEW_DIR_RESULTS = True
restart_file = params.output.path_session + "/cbox0.f00100"
params.nek.general.extrapolation = "standard"

sim = Simul(params)

copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

sim.make.exec("run_fg", resources={"nproc": 4})
