from time import sleep

import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster
from critical_Ra import Ra_c as Ra_c_tests

nb_elements = 16
order = 10
end_time = 4000
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

    nb_elements_y = int(nb_elements * aspect_ratio)
    if nb_elements * aspect_ratio - nb_elements_y:
        continue

    Ra_numbers = np.logspace(np.log10(Ra_c_test), np.log10(1.04 * Ra_c_test), 4)

    for Ra in Ra_numbers:

        cluster.submit_script(
            f"run_simul_check_from_python.py -R {Ra} -nx {nb_elements} "
            f"--order {order} --end-time {end_time} -np {nb_procs} "
            f"-a_y {aspect_ratio}",
            name_run=f"asp_{aspect_ratio:.3f}_Ra_{Ra:.3e}_msh_"
            f"{nb_elements*order}_{round(nb_elements*aspect_ratio)*order}",
            nb_cores_per_node=nb_procs,
            omp_num_threads=1,
            ask=False,
        )

        sleep(2)
