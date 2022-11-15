import argparse

from snek5000.util.restart import load_for_restart
from snek5000.make import unlock


parser = argparse.ArgumentParser()

parser.add_argument(
    "-np", "--nb-mpi-procs", type=int, default=4, help="Number of MPI processes"
)

parser.add_argument("--path-sim", help="Path to the the simulation directory")


def main(args):

    # unlock(args.path_sim)
    params, Simul = load_for_restart(args.path_sim, use_checkpoint=2)
    # params, Simul = load_for_restart(args.path_sim, use_start_from='cbox0.f00018')

    sim = Simul(params)

    sim.make.exec("run_fg", nproc=args.nb_mpi_procs)

    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()
    params, sim = main(args)
