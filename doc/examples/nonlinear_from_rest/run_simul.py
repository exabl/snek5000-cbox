"""

Example of calls:

```
python run_simul.py

python run_simul.py -Ra 1.4e08

```

"""


import argparse

from snek5000_cbox.solver import Simul


parser = argparse.ArgumentParser()

parser.add_argument("-a_y", "--aspect-ratio-y", type=float, default=1.0, help="Y aspect ratio")
parser.add_argument("-a_z", "--aspect-ratio-z", type=float, default=1.0, help="Z aspect ratio")

parser.add_argument("-Pr", "--Prandtl", type=float, default=0.71, help="Prandtl number")

parser.add_argument(
    "-Ra", "--Rayleigh", type=float, default=1.0e08, help="Rayleigh number"
)

parser.add_argument("-nx", type=int, default=8, help="number of x elements")
parser.add_argument("-ny", type=int, default=8, help="number of y elements")
parser.add_argument("-nz", type=int, default=8, help="number of z elements")
parser.add_argument("--order", type=int, default=9, help="order")
parser.add_argument("--dim", type=int, default=2, help="2d or 3d")


def main(args):

    params = Simul.create_default_params()

    Lx = params.oper.Lx = 1.0
    params.oper.Ly = Lx * args.aspect_ratio_y
    params.oper.Lz = Lx * args.aspect_ratio_z

    params.oper.nproc_min = 2
    dim = params.oper.dim = args.dim

    nx = params.oper.nx = args.nx
    ny = params.oper.ny = args.ny
    # nz = params.oper.nz = args.nz

    order = params.oper.elem.order = args.order

    params.output.sub_directory = f"examples_cbox/{dim}D/NL_sim/asp_{args.asp_y:.2f}/mesh{nx*order}_{ny*order}/Ra_{args.Rayleigh}"

    params.nek.general.user_params = {2: args.Prandtl, 3: args.Rayleigh}

    params.nek.general.num_steps = 20000
    params.nek.general.write_interval = 100  # dumping frequency

    params.nek.general.dt = 0.005
    params.nek.general.time_stepper = "BDF3"

    params.output.history_points.coords = [(0.5, 0.2), (0.5, 0.8)]
    params.oper.max.hist = 3

    sim = Simul(params)

    sim.make.exec(["run"])

    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()

    params, sim = main(args)
