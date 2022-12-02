import numpy as np

from snek5000_cbox.solver import Simul

params = Simul.create_default_params()

aspect_ratio = 1.0
params.prandtl = 1.0

params.Ra_side = 1e5
params.Ra_vert = 1e5

params.output.sub_directory = "examples_cbox/simple/MC"

params.oper.dim = 2

nb_elements = ny = 8
params.oper.ny = nb_elements
nx = params.oper.nx = int(nb_elements / aspect_ratio)
params.oper.nz = int(nb_elements / aspect_ratio)

Ly = params.oper.Ly
Lx = params.oper.Lx = Ly / aspect_ratio
Lz = params.oper.Lz = Ly / aspect_ratio


order = params.oper.elem.order = params.oper.elem.order_out = 10

params.oper.mesh_stretch_factor = 0.0  # zero means regular

params.short_name_type_run = (
    f"Ra{params.Ra_side:.3e}_{params.Ra_vert:.3e}_{nx*order}x{ny*order}"
)

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

if params.oper.dim == 3:

    zs = np.linspace(0, Lz, n1d)
    zs[0] = small
    zs[-1] = Lz - small

    coords = [(x, y, z) for x in xs for y in ys for z in zs]


params.output.history_points.coords = coords
params.oper.max.hist = len(coords) + 1

params.nek.general.dt = 0.05
params.nek.general.end_time = 800
params.nek.general.stop_at = "endTime"

params.nek.general.write_control = "runTime"
params.nek.general.write_interval = 10.0

# params.nek.general.variable_dt = True
params.nek.general.target_cfl = 1.0
params.nek.general.time_stepper = "BDF3"
params.nek.general.extrapolation = "OIFS"

params.output.history_points.write_interval = 10

sim = Simul(params)

sim.make.exec("run_fg", nproc=4)
