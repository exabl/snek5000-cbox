import numpy as np

from fluiddyn.clusters.legi import Calcul2 as Cluster

prandtl = 0.71

aspect_ratio = 1.0
ny = 12
order = 10
stretch_factor = 0.0

num_steps = 4000000
dt = 0.05
nb_procs = 10

Ra_side = 1000

y_periodicity = False
z_periodicity = False

better_Ra_c_numbers = {1.0: 1.825e8}

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

if aspect_ratio in better_Ra_c_numbers:
    Ra_c_guessed = better_Ra_c_numbers[aspect_ratio]
else:
    Ra_c_guessed = 1.93e8 * aspect_ratio ** -3.15

Ra_numbs = np.logspace(np.log10(0.99 * Ra_c_guessed), np.log10(1.02 * Ra_c_guessed), 5)

print(Ra_numbs)

nx = int(ny / aspect_ratio)
if ny / aspect_ratio - nx:
    raise ValueError

for Ra_side_num in Ra_numbs:

    command = (
        f"run_simul.py -Pr {prandtl} -ny {ny} "
        f"--order {order} --dt-max {dt} --num-steps {num_steps} -np {nb_procs} "
        f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
        f"--Ra-side {Ra_side_num}"
    )

    if y_periodicity:
        command += " --y-periodicity"
    elif z_periodicity:
        command += " --z-periodicity"

    print(command)

    name_run = f"SW_asp{aspect_ratio:.3f}_Ra{Ra_side_num:.3e}_Pr{prandtl:.2f}_msh{round(nx/aspect_ratio)*order}x{ny*order}"

    cluster.submit_script(
        command,
        name_run=name_run,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )
