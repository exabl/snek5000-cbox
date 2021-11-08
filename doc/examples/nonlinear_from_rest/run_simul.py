"""

Example of calls:

```
python run_simul.py

python run_simul.py -Ra 1.4e08

```

"""

import argparse

import numpy as np

from snek5000_cbox.solver import Simul


parser = argparse.ArgumentParser()

parser.add_argument(
    "-a_y", "--aspect-ratio-y", type=float, default=1.0, help="Y aspect ratio"
)
parser.add_argument(
    "-a_z", "--aspect-ratio-z", type=float, default=1.0, help="Z aspect ratio"
)

parser.add_argument("-Pr", "--Prandtl", type=float, default=0.71, help="Prandtl number")

parser.add_argument(
    "-Ra", "--Rayleigh", type=float, default=1.0e08, help="Rayleigh number"
)

parser.add_argument("-nx", type=int, default=8, help="number of x elements")
parser.add_argument("-nz", type=int, default=8, help="number of z elements")
parser.add_argument("--order", type=int, default=9, help="order")
parser.add_argument("--dim", type=int, default=2, help="2d or 3d")

parser.add_argument(
    "--num-steps", type=int, default=2000000, help="number of time steps"
)
parser.add_argument("--dt", type=float, default=0.005, help="time step")


def main(args):

    params = Simul.create_default_params()

    Lx = params.oper.Lx = 1.0
    Ly = params.oper.Ly = Lx * args.aspect_ratio_y
    params.oper.Lz = Lx * args.aspect_ratio_z

    params.oper.nproc_min = 2
    dim = params.oper.dim = args.dim

    nx = params.oper.nx = args.nx
    ny = params.oper.ny = int(nx*args.aspect_ratio_y)
    # nz = params.oper.nz = args.nz

    order = params.oper.elem.order = args.order
    params.oper.elem.order_out = order

    params.output.sub_directory = (
        f"cbox2/{dim}D/NL_sim/asp_{args.aspect_ratio_y:.3f}"
        f"/msh_{nx*order}_{ny*order}/Ra_{args.Rayleigh:.3e}"
    )

    params.nek.general.num_steps = args.num_steps
    params.nek.general.write_interval = 1000  # dumping frequency

    params.nek.general.dt = args.dt
    params.nek.general.time_stepper = "BDF3"

    w_pert = write_interval_pert_field = 1000
    w_hist = write_interval_hist_points = 100

    params.nek.general.user_params = {
        2: args.Prandtl,
        3: args.Rayleigh,
        4: w_pert,
        5: w_hist,
    }

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

    sim = Simul(params)
    sim.make.exec(["run_fg"])

    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()
    params, sim = main(args)

