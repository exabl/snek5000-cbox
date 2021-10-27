import argparse

from snek5000_cbox.solver import Simul


parser = argparse.ArgumentParser()

parser.add_argument("-a_y", "--asp_y", type=float, default=1.0, help="Y aspect ratio")

parser.add_argument("-a_z", "--asp_z", type=float, default=1.0, help="Z aspect ratio")

parser.add_argument("-Pr", "--Prandtl", type=float, default=0.71, help="Prandtl number")

parser.add_argument(
    "-Ra", "--Rayleigh", type=float, default=1.0e08, help="Rayleigh number"
)


def main(args):

    params = Simul.create_default_params()

    Lx = params.oper.Lx = 1.0
    params.oper.Ly = Lx * args.asp_y
    params.oper.Lz = Lx * args.asp_z

    params.oper.nproc_min = 2
    dim = params.oper.dim = 2  # 2D or 3D

    nx = params.oper.nx = 8  # Number of x elements
    ny = params.oper.ny = 8  # Number of y elements
    nz = params.oper.nz = 8  # Number of z elements

    order = params.oper.elem.order = 9

    params.output.sub_directory = f"examples_cbox/{dim}D/NL_sim/asp_{args.A_y:.2f}/mesh{nx*order}_{ny*order}/Ra_{args.Ra}"

    params.nek.general.user_params = {2: args.Pr, 3: args.Ra}

    params.nek.general.num_steps = 20000
    params.nek.general.write_interval = 100  # Dumping frequency

    params.nek.general.dt = 0.005
    params.nek.general.time_stepper = "BDF3"

    params.output.history_points.points = [(0.5, 0.2), (0.5, 0.8)]
    params.oper.max.hist = 3

    sim = Simul(params)

    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()

    params, sim = main(args)
