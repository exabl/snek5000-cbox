"""

One has to change the environment variable:

```
export MPIEXEC="mpirun --oversubscribe --report-pid PID.txt"
```

However, this has no impact for snek (see
https://snek5000.readthedocs.io/en/latest/configuring.html#overriding-configuration-with-environment-variable)
so one needs to create a config file `$HOME/.config/snek5000.yml` (copy the
default config file) and modify it as follow:

```
MPIEXEC_FLAGS: "--oversubscribe --report-pid PID.txt"
```

TODO: We should be able to set sensitivity to environment variables from the
launching script. Or to directly set environment variables from the function
`sim.make.exec`.

Example of commands:

```
python run_simul_check_from_python.py -nx 12 --order 10 -Ra 1.89e08 -np 4
```

"""

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
    "-Ra", "--Rayleigh", type=float, default=1.89e08, help="Rayleigh number"
)

parser.add_argument("-nx", type=int, default=12, help="number of x elements")
parser.add_argument("-nz", type=int, default=12, help="number of z elements")
parser.add_argument("--order", type=int, default=10, help="order")
parser.add_argument("--dim", type=int, default=2, help="2d or 3d")

parser.add_argument("--end-time", type=float, default=4000, help="End time")
parser.add_argument("--dt-max", type=float, default=0.1, help="Maximum dt")

parser.add_argument(
    "-np", "--nb-mpi-procs", type=int, default=4, help="Number of MPI processes"
)


def main(args):

    params = Simul.create_default_params()

    params.prandtl = args.Prandtl
    params.rayleigh = args.Rayleigh

    Lx = params.oper.Lx = 1.0
    Ly = params.oper.Ly = Lx * args.aspect_ratio_y
    params.oper.Lz = Lx * args.aspect_ratio_z

    params.oper.nproc_min = 2
    dim = params.oper.dim = args.dim

    nx = params.oper.nx = args.nx
    ny = params.oper.ny = int(nx * args.aspect_ratio_y)
    # nz = params.oper.nz = args.nz

    order = params.oper.elem.order = args.order
    params.oper.elem.order_out = order

    params.output.sub_directory = f"cbox/{dim}D/NL_sim/asp_{args.aspect_ratio_y:.3f}"
    params.short_name_type_run = f"asp{args.aspect_ratio_y:.3f}_Ra{args.Rayleigh:.3e}"

    params.nek.general.end_time = args.end_time
    params.nek.general.stop_at = "endTime"

    params.nek.general.write_control = "runTime"
    params.nek.general.write_interval = 20.0

    params.nek.general.dt = args.dt_max

    params.nek.general.variable_dt = True
    params.nek.general.target_cfl = 2.0
    params.nek.general.time_stepper = "BDF3"
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 1000
    params.output.history_points.write_interval = 10

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
        if n > 20:
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

        print(
            f"  {abs(temp0_std - temp1_std) / temp0_std = :.3f}, {temp1_std = :.3g}"
        )
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
