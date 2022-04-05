from time import sleep

from fluiddyn.clusters.legi import Calcul8 as Cluster

from critical_Ra import Ra_c as Ra_c_tests

aspect_ratio = 1.25
nx = 12
order = 10
end_time = 4000
nb_procs = 10

# Ra_c_tests = {0.5: 1.0e10, 0.75: 5.0e9, 0.875: 2.855e8, 1.0: 1.875e8}
Ra_c_test = Ra_c_tests[aspect_ratio]

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

ny = int(nx * aspect_ratio)
if nx * aspect_ratio - ny:
    raise ValueError


cluster.submit_script(
    f"run_simul_check_from_python.py -R {Ra_c_test} -nx {nx} "
    f"--order {order} --end-time {end_time} -np {nb_procs} "
    f"-a_y {aspect_ratio}",
    name_run=f"test_algorithm_asp_{aspect_ratio:.2f}_Ra_{Ra_c_test:.3e}_msh_"
    f"{nx*order}_{int(nx*aspect_ratio)*order}",
    nb_cores_per_node=nb_procs,
    omp_num_threads=1,
    ask=False,
)

sleep(2)
