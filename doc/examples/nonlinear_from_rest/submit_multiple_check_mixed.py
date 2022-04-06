import numpy as np

from fluiddyn.clusters.legi import Calcul2 as Cluster
from critical_Ra import Ra_c as Ra_c_tests

prandtl = 1.0

dt_max = 0.005
end_time = 3000
nb_procs = 10

ny = 2
order = 10
stretch_factor = 0.0
dim = 2

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


for aspect_ratio, Ra_c_test in Ra_c_tests.items():

    nx = int(ny / aspect_ratio)
    if ny / aspect_ratio - nx:
        continue

    Ra_side_nums = np.logspace(np.log10(Ra_c_test), np.log10(1.04 * Ra_c_test), 4)
    Ra_vert_nums = np.logspace(np.log10(Ra_c_test), np.log10(1.04 * Ra_c_test), 4)

    for Ra_side_num in Ra_side_nums:
        for Ra_vert_num in Ra_vert_nums:

            command = (
                f"run_simul_check_from_python.py -Pr {prandtl} -ny {ny} "
                f"--order {order} --dt-max {dt_max} --end-time {end_time} -np {nb_procs} "
                f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
                f"--Ra-side {Ra_side_num} --Ra-vert {Ra_vert_num}"
            )

            if z_periodicity:
                command += " --z-periodicity"

            print(command)

            name_run = f"MC_asp{aspect_ratio:.3f}_Ra{Ra_side_num:.3e}_{Ra_vert_num:.3e}_Pr{prandtl:.2f}_msh{round(nx/aspect_ratio)*order}x{ny*order}"

            cluster.submit_script(
                command,
                name_run=name_run,
                nb_cores_per_node=nb_procs,
                omp_num_threads=1,
                ask=False,
            )
