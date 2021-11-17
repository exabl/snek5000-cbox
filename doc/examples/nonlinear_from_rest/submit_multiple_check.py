from time import sleep

from fluiddyn.clusters.legi import Calcul8 as Cluster

aspect_ratios = [0.875, 1.0]
nb_elements = 16
order = 10
end_time = 4000
nb_procs = 10

Ra_c_tests = {0.875: 2.855e8, 1.0: 1.875e8}

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


for aspect_ratio in aspect_ratios:

    nb_elements_y = int(nb_elements * aspect_ratio)
    if nb_elements * aspect_ratio - nb_elements_y:
        raise ValueError

    Ra_c_test = Ra_c_tests[aspect_ratio]

    cluster.submit_script(
        f"run_simul_check_from_python.py -R {Ra_c_test} -nx {nb_elements} "
        f"--order {order} --end-time {end_time} -np {nb_procs} "
        f"-a_y {aspect_ratio}",
        name_run=f"asp_{aspect_ratio:.2f}_Ra_{Ra_c_test:.3e}_msh_"
        f"{nb_elements*order}_{int(nb_elements*aspect_ratio)*order}",
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )

    sleep(2)
