import numpy as np

from fluiddyn.clusters.legi import Calcul2 as Cluster
from critical_Ra_RB import Ra_c_RB as Ra_c_RB_tests

prandtl = 1.0

dim = 2

dt_max = 0.005
end_time = 30
nb_procs = 10

nx = 8
order = 10
stretch_factor = 0.0

Ra_vert = 1750

x_periodicity = False
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


for aspect_ratio, Ra_c_test in Ra_c_RB_tests.items():

    ny = int(nx * aspect_ratio)
    if nx * aspect_ratio - ny:
        continue

    Ra_vert_nums = np.logspace(np.log10(Ra_c_test), np.log10(1.04 * Ra_c_test), 4)

    for Ra_vert_num in Ra_vert_nums:

        command = (
            f"run_simul_check_from_python.py -Pr {prandtl} -nx {nx} --dim {dim} "
            f"--order {order} --dt-max {dt_max} --end-time {end_time} -np {nb_procs} "
            f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
            f"--Ra-vert {Ra_vert_num}"
        )

        if x_periodicity:
            command += " --x-periodicity"
        elif z_periodicity:
            command += " --z-periodicity"

        print(command)

        name_run = f"RB_asp{aspect_ratio:.3f}_Ra{Ra_vert_num:.3e}_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio)*order}"

        cluster.submit_script(
            command,
            name_run=name_run,
            nb_cores_per_node=nb_procs,
            omp_num_threads=1,
            ask=False,
        )
