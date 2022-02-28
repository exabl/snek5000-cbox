import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster

aspect_ratio = 1.0
nb_elements = 16
order = 10
num_steps = 4000000
dt = 0.005

better_Ra_c_numbers = {1.0: 1.825e8}

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

if aspect_ratio in better_Ra_c_numbers:
    Ra_c_guessed = better_Ra_c_numbers[aspect_ratio]
else:
    Ra_c_guessed = 1.93e8 * aspect_ratio**-3.15

Ra_numbs = np.logspace(np.log10(0.99 * Ra_c_guessed), np.log10(1.02 * Ra_c_guessed), 5)

print(Ra_numbs)

for Ra_num in Ra_numbs:

    cluster.submit_script(
        f"run_simul.py -R {Ra_num} -nx {nb_elements} "
        f"--order {order} --num-steps {num_steps} --dt {dt} "
        f"-a_y {aspect_ratio}",
        name_run=f"asp_{aspect_ratio:.2f}_Ra{Ra_num:.3e}_msh_ "
        f"{nb_elements*order}_{int(nb_elements*aspect_ratio*order)}",
        nb_cores_per_node=10,
        omp_num_threads=1,
        ask=False,
    )
