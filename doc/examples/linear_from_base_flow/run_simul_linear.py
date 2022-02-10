import argparse

from shutil import copyfile

from snek5000 import load_params
from snek5000_cbox.solver import Simul

parser = argparse.ArgumentParser()

parser.add_argument(
    "--sim-path", type=str, default="", help="nonlinear simulation path"
)

parser.add_argument("--end-time", type=float, default=4000, help="End time")
parser.add_argument(
    "--num-steps", type=int, default=2000000, help="number of time steps"
)
parser.add_argument("--dt-max", type=float, default=0.1, help="Maximum dt")

parser.add_argument(
    "-np", "--nb-mpi-procs", type=int, default=4, help="Number of MPI processes"
)

parser.add_argument(
    "-Ra", "--Rayleigh", type=float, default=1.89e08, help="Rayleigh number"
)


def main(args):

    sim_path = args.sim_path

    params = load_params(sim_path)

    params.nek.general.start_from = "base_flow.restart"

    params.rayleigh = args.Rayleigh
    params.nek.general.write_interval = params.nek.general.end_time
    params.nek.general.end_time = args.end_time

    params.output.phys_fields.write_interval_pert_field = 500
    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"
    
    dim = params.oper.dim
    Ly = params.oper.Ly
    prandtl = params.prandtl
    
    params.output.sub_directory = f"cbox_stretched/{dim}D/lin_sim/Pr_{prandtl:.2f}/asp_{Ly:.3f}"
    params.short_name_type_run = (
        f"asp{Ly:.3f}_Pr{prandtl:.2f}_Ra{args.Rayleigh:.3e}"
    )

    params.NEW_DIR_RESULTS = True
    restart_file = params.output.path_session + "/cbox0.f00298"
    params.nek.general.extrapolation = "standard"

    sim = Simul(params)

    copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

    sim.make.exec("run_fg", resources={"nproc": args.nb_mpi_procs})
    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()
    params, sim = main(args)

    