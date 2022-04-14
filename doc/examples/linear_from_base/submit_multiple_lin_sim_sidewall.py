import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster


prandtl = 0.71

dim = 2

aspect_ratio = 1.0
nx = 28
order = 10
stretch_factor = 0.0

end_time = 5000
dt = 0.05
nb_procs = 10

y_periodicity = False
z_periodicity = False

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

Ra_numbs = [1.835e8, 1.840e8, 1.845e8, 1.850e8]

ny = int(nx * aspect_ratio)
if nx * aspect_ratio - ny:
    raise ValueError

for Ra_side_num in Ra_numbs:

    command = (
        f"run_simul_linear.py -Pr {prandtl} -nx {nx} --dim {dim} "
        f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_procs} "
        f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
        f"--Ra-side {Ra_side_num}"
    )

    if y_periodicity:
        command += " --y-periodicity"
    elif z_periodicity:
        command += " --z-periodicity"

    print(command)

    name_run = f"LSW_asp{aspect_ratio:.3f}_Ra{Ra_side_num:.3e}_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio)*order}"

    cluster.submit_script(
        command,
        name_run=name_run,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )
