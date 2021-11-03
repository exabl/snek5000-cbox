"""
To define environmental variable (in the terminal or in your .bashrc)
use something like: export FLUIDSIM_PATH="/fsnet/project/meige/2020/20CONVECTION/numerical/"

"""

import numpy as np

from snek5000_cbox.solver import Simul

# from phill.solver import Simul

params = Simul.create_default_params()

aspect_ratio = 1.0
Pr = 0.71  # Prandtl number

# for aspect ratio 1, Ra_c = 1.825E08
Ra = 1.83e08  # Rayleigh number

params.output.sub_directory = "examples_cbox/simple"

params.oper.nproc_min = 2
params.oper.dim = 2

# number of elements
nb_elements = 8
params.oper.nx = nb_elements
params.oper.ny = nb_elements
params.oper.nz = nb_elements

Lx = params.oper.Lx = 1.0
Ly = params.oper.Ly = Lx * aspect_ratio

params.oper.elem.order = 9

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

params.nek.general.num_steps = 20000
params.nek.general.write_interval = 100
params.nek.general.dt = 0.05
params.nek.general.time_stepper = "BDF3"

w_pert = write_interval_pert_field = 1000
w_hist = write_interval_hist_points = 10

params.nek.general.user_params = {2: Pr, 3: Ra, 4: w_pert, 5: w_hist}

sim = Simul(params)

# sim.make.exec(["run_fg"])
sim.make.exec(["run_fg"], resources={"nproc": 2})
