from time import sleep

import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster
from critical_Ra import Ra_c as Ra_c_tests

nx = 16
order = 10
# end_time = 4000
num_steps = 4000000
dt_max = 0.005
nb_procs = 10

cluster = Cluster()

cluster.commands_setting_env = [
    "PROJET_DIR=/fsnet/project/meige/2020/20CONVECTION",
    "source /etc/profile",
    "source $PROJET_DIR/Software/miniconda3/etc/profile.d/conda.sh",
    "conda activate",
    "export NEK_SOURCE_ROOT=$HOME/Documents/Nek5000",
    "export PATH=$PATH:$NEK_SOURCE_ROOT/bin",
    "export FLUIDSIM_PATH=$PROJET_DIR/numerical/",
]


for aspect_ratio, Ra_c_test in Ra_c_tests.items():

    ny = int(nx * aspect_ratio)
    if nx * aspect_ratio - ny:
        continue

    Ra_numbers = np.logspace(np.log10(Ra_c_test), np.log10(1.04 * Ra_c_test), 4)
    # Ra_numbers = Ra_numbers[:2]
    for Ra in Ra_numbers:

        command = (
            f"run_simul_check_from_python.py -R {Ra} -nx {nx} "
            f"--order {order} --dt-max {dt_max} --num-steps {num_steps} "
            f"-np {nb_procs} -a_y {aspect_ratio}"
        )

        print(command)

        cluster.submit_script(
            command,
            name_run=f"asp_{aspect_ratio:.3f}_Ra_{Ra:.3e}_msh_"
            f"{nx*order}_{round(nx*aspect_ratio)*order}",
            nb_cores_per_node=nb_procs,
            omp_num_threads=1,
            ask=False,
        )

        # sleep(2)
