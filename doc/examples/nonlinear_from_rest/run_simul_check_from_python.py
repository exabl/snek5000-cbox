import argparse
from time import sleep
import os
import signal
from time import perf_counter
import builtins

import numpy as np

from fluiddyn.util import time_as_str

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
    "--Ra-side", type=float, default=0.0, help="Sidewall Rayleigh number"
)
parser.add_argument(
    "--Ra-vert", type=float, default=0.0, help="Vertical Rayleigh number"
)

parser.add_argument("-ny", type=int, default=12, help="Number of y elements")
parser.add_argument("-nz", type=int, default=12, help="Number of z elements")
parser.add_argument("--order", type=int, default=10, help=" Polynomial order")
parser.add_argument("--dim", type=int, default=2, help="2D or 3D")
parser.add_argument("--stretch-factor", type=float, default=0.0, help="Stretch factor")

parser.add_argument(
    "--x-periodicity",
    action="store_true",
    help="Periodic boundary condition in x direction",
)
parser.add_argument(
    "--y-periodicity",
    action="store_true",
    help="Periodic boundary condition in y direction",
)
parser.add_argument(
    "--z-periodicity",
    action="store_true",
    help="Periodic boundary condition in z direction",
)

parser.add_argument("--end-time", type=float, default=4000, help="End time")
parser.add_argument("--num-steps", type=int, default=4000, help="Number of time steps")
parser.add_argument("--dt-max", type=float, default=0.1, help="Maximum dt")

parser.add_argument(
    "-np", "--nb-mpi-procs", type=int, default=4, help="Number of MPI processes"
)


def main(args):

    params = Simul.create_default_params()

    params.prandtl = args.Prandtl
    params.Ra_side = args.Ra_side
    params.Ra_vert = args.Ra_vert

    Ly = params.oper.Ly
    Lx = params.oper.Lx = Ly / args.aspect_ratio_y
    Lz = params.oper.Lz = Ly / args.aspect_ratio_z

    params.oper.x_periodicity = args.x_periodicity
    params.oper.y_periodicity = args.y_periodicity
    params.oper.z_periodicity = args.z_periodicity

    params.oper.mesh_stretch_factor = args.stretch_factor
    params.oper.aspect_ratio = args.aspect_ratio_y

    params.oper.nproc_min = 2
    dim = params.oper.dim = args.dim

    ny = params.oper.ny = args.ny
    nx = params.oper.nx = int(ny / args.aspect_ratio_y)
    # nz = params.oper.nz = int(ny / args.aspect_ratio_z)

    order = params.oper.elem.order = args.order
    params.oper.elem.order_out = order

    if params.Ra_side > 0 and params.Ra_vert == 0:
        params.output.sub_directory = f"SW_check/{dim}D/NL_sim/Pr_{args.Prandtl:.2f}/asp_{args.aspect_ratio_y:.3f}"
        params.short_name_type_run = (
            f"asp{args.aspect_ratio_y:.3f}_Ra_s{args.Ra_side:.3e}_Pr{args.Prandtl:.2f}"
        )
    elif params.Ra_side == 0 and params.Ra_vert > 0:
        params.output.sub_directory = f"RB_check/{dim}D/NL_sim/Pr_{args.Prandtl:.2f}/asp_{args.aspect_ratio_y:.3f}"
        params.short_name_type_run = (
            f"asp{args.aspect_ratio_y:.3f}_Ra_v{args.Ra_vert:.3e}_Pr{args.Prandtl:.2f}"
        )
    elif params.Ra_side > 0 and params.Ra_vert > 0:
        params.output.sub_directory = f"MC_check/{dim}D/NL_sim/Pr_{args.Prandtl:.2f}/asp_{args.aspect_ratio_y:.3f}"
        params.short_name_type_run = f"asp{args.aspect_ratio_y:.3f}_Ra_s{args.Ra_side:.3e}_Ra_v{args.Ra_vert:.3e}_Pr{args.Prandtl:.2f}"

    params.nek.general.dt = args.dt_max
    params.nek.general.time_stepper = "BDF3"

    params.nek.general.end_time = args.end_time
    params.nek.general.stop_at = "endTime"

    params.nek.general.write_control = "runTime"
    params.nek.general.write_interval = 20.0

    # params.nek.general.target_cfl = 2.0
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 10
    params.output.history_points.write_interval = 5

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

    sim = Simul(params)
    sim.output.write_snakemake_config(
        custom_env_vars={"MPIEXEC_FLAGS": "--report-pid PID.txt"}
    )

    sim.make.exec("run", resources={"nproc": args.nb_mpi_procs})
    return params, sim


if __name__ == "__main__":
    args = parser.parse_args()
    params, sim = main(args)

    pid_file = sim.path_run / "PID.txt"

    n = 0
    while not pid_file.exists():
        sleep(1)
        n += 1
        if n > 60:
            raise RuntimeError(f"{pid_file} does not exist.")

    with open(pid_file) as file:
        pid = int(file.read().strip())

    path_log_py = sim.path_run / f"log_py_{time_as_str()}.txt"

    def print(*args, sep=" ", end="\n", **kwargs):
        builtins.print(*args, **kwargs)
        with open(path_log_py, "a") as file:
            file.write(sep.join(str(arg) for arg in args) + end)

    print(f"{pid = }")

    def check_running():
        """Check For the existence of a unix pid."""
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        else:
            return True

    while check_running():
        sleep(10)
        # TODO: make this call faster even for large .his file
        # see https://github.com/exabl/snek5000/issues/108
        # and https://github.com/exabl/snek5000/tree/faster-history-points-load
        t0 = perf_counter()
        coords, df = sim.output.history_points.load_1point(
            index_point=5, key="temperature"
        )
        t_last = df.time.max()
        print(
            f"{time_as_str()}, {t_last = :.2f}: "
            f"history_points loaded in {perf_counter() - t0:.2f} s"
        )

        if t_last < 800:
            continue

        temperature = df.temperature
        times = df.time

        duration_avg = 200.0

        temp0_std = np.std(
            temperature[
                (t_last - 2 * duration_avg < times) & (times < t_last - duration_avg)
            ]
        )
        temp1_std = np.std(
            temperature[(t_last - duration_avg < times) & (times < t_last)]
        )

        print(f"  {abs(temp0_std - temp1_std) / temp0_std = :.3f}, {temp1_std = :.3g}")
        if temp1_std < 1.0e-14:
            print(
                f"Steady state (stable) detected at t = {t_last}\n"
                "Terminate simulation."
            )

            os.kill(pid, signal.SIGTERM)
            break

        if abs(temp0_std - temp1_std) / temp0_std < 0.2 and temp1_std > 0.0004:
            print(
                f"Saturation of the instability detected at t = {t_last}\n"
                "Terminate simulation."
            )

            os.kill(pid, signal.SIGTERM)
            break
