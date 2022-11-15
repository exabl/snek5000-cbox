import numpy as np
from shutil import copyfile

from snek5000_cbox.solver import Simul


params = Simul.create_default_params()

aspect_ratio = 1.0 / 6.0
params.prandtl = 1.0

# for an infinite layer of fluid with Pr = 1.0, the onset of convection is at Ra_c = 1708
params.Ra_vert = 1725

params.output.sub_directory = "examples_cbox/simple/RB"

params.oper.dim = 2

params.oper.x_periodicity = True

nb_elements = ny = 2
params.oper.ny = nb_elements
nx = params.oper.nx = int(nb_elements / aspect_ratio)
nx = 20
params.oper.nz = int(nb_elements / aspect_ratio)

Ly = params.oper.Ly
Lx = params.oper.Lx = Ly / aspect_ratio
Lz = params.oper.Lz = Ly / aspect_ratio


order = params.oper.elem.order = params.oper.elem.order_out = 8

params.oper.mesh_stretch_factor = 0.0  # zero means regular

params.short_name_type_run = f"Ra{params.Ra_vert:.3e}_{nx*order}x{ny*order}"


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

params.nek.general.dt = 0.5
params.nek.general.time_stepper = "BDF3"
params.nek.general.stop_at = "endTime"
params.nek.general.write_control = "runTime"
params.nek.general.extrapolation = "standard"
params.nek.general.write_interval = params.nek.general.end_time = 3000
params.output.history_points.write_interval = 10
params.output.phys_fields.write_interval_pert_field = 70

params.nek.problemtype.equation = "incompLinNS"
params.oper.elem.staggered = "auto"
params.short_name_type_run = f"lin_Ra{params.Ra_vert:.3e}_{nx*order}x{ny*order}"

sim = Simul(params)

sim.make.exec("run_fg", nproc=4)
