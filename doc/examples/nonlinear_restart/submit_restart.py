import numpy as np
from pathlib import Path

from fluiddyn.clusters.legi import Calcul8 as Cluster
from snek5000 import load


prandtl = 0.71
aspect_ratio = 1.0

dim = 3

dir_sim = (
    f"/.fsnet/project/meige/2020/20CONVECTION/numerical/SW/{dim}D/NL_sim/"
    f"Pr_{prandtl:.2f}/asp_{aspect_ratio:.3f}"
)
path = Path(dir_sim)
sim_dirs = sorted(path.glob(f"*Az4.000_Ra_s*"))

nb_procs = 10
nb_nodes = 1
walltime = "24:00:00"

path_sim = sim_dirs[0]

sim = load(path_sim)

cluster = Cluster()

cluster.commands_setting_env = [
    "PROJET_DIR=/fsnet/project/meige/2020/20CONVECTION",
    "source /etc/profile",
    "source $PROJET_DIR/miniconda3/etc/profile.d/conda.sh",
    "conda activate env-snek",
    "export NEK_SOURCE_ROOT=$HOME/Dev/snek5000/lib/Nek5000",
    "export PATH=$PATH:$NEK_SOURCE_ROOT/bin",
    "export FLUIDSIM_PATH=$PROJET_DIR/numerical/",
]

command = f"run_restart.py --path-sim {path_sim} -np {nb_nodes*nb_procs}"

# print(command)

Ra_side = sim.params.Ra_side
Ra_vert = sim.params.Ra_vert

prandtl = sim.params.prandtl

aspect_ratio_y = sim.params.oper.Ly / sim.params.oper.Lx

if dim == 3:
    aspect_ratio_z = sim.params.oper.Ly / sim.params.oper.Lz

nx = sim.params.oper.nx
ny = sim.params.oper.ny
nz = sim.params.oper.nz

order = sim.params.oper.elem.order

if Ra_side > 0.0 and Ra_vert == 0.0:

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ra{Ra_side:.3e}_Pr{prandtl:.2f}_msh{nx*order}x"
        f"{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )

    name_run = "SW" + name_run

elif Ra_side == 0.0 and Ra_vert > 0.0:

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ra{Ra_vert:.3e}_Pr{prandtl:.2f}_msh{nx*order}x"
        f"{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )

    name_run = "RB" + name_run

elif Ra_side > 0.0 and Ra_vert > 0.0:

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ras{Ra_side:.3e}_Rav{Ra_vert:.3e}_Pr{prandtl:.2f}_msh"
        f"{nx*order}x{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )

cluster.submit_script(
    command,
    name_run=name_run,
    walltime=walltime,
    nb_nodes=nb_nodes,
    nb_cores_per_node=nb_procs,
    omp_num_threads=1,
    ask=False,
)
