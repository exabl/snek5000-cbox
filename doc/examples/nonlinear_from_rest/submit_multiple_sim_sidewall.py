import numpy as np

from fluiddyn.clusters.legi import Calcul8 as Cluster

from critical_Ra_sidewall import Ra_c_SW as Ra_c_SW_tests

prandtl = 0.71

dim = 2

aspect_ratio = 1.0
nx = 32
order = 10
stretch_factor = 0.0

end_time = 8000
dt = 0.05
nb_procs = 10

y_periodicity = False
z_periodicity = False

sfd_activation = 0.0

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

if aspect_ratio in Ra_c_SW_tests.items():
    Ra_c_guessed = Ra_c_SW_tests[aspect_ratio]
else:
    Ra_c_guessed = 1.93e8 * aspect_ratio ** -3.15

Ra_c_guessed = 2e8
Ra_numbs = np.logspace(np.log10(0.9 * Ra_c_guessed), np.log10(1.6 * Ra_c_guessed), 5)
Ra_numbs = [1.8e8]
ny = int(nx * aspect_ratio)
if nx * aspect_ratio - ny:
    raise ValueError

for Ra_side_num in Ra_numbs:

    command = (
        f"run_simul.py -Pr {prandtl} -nx {nx} --dim {dim} "
        f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_procs} "
        f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
        f"--Ra-side {Ra_side_num} --sfd-activation {sfd_activation}"
    )

    if y_periodicity:
        command += " --y-periodicity"
    elif z_periodicity:
        command += " --z-periodicity"

    print(command)

    name_run = f"SW_asp{aspect_ratio:.3f}_Ra{Ra_side_num:.3e}_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio)*order}"

    cluster.submit_script(
        command,
        name_run=name_run,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )
