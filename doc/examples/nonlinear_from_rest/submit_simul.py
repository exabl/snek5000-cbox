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

delta_T_lateral = 1.0
delta_T_vertical = 0.0

x_periodicity = False
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
    Ra_c_guessed = 1.93e8 * aspect_ratio**-3.15

Ra_numbs = np.logspace(np.log10(0.99 * Ra_c_guessed), np.log10(1.02 * Ra_c_guessed), 5)

print(Ra_numbs)

nx = int(ny / aspect_ratio)
if ny / aspect_ratio - nx:
    raise ValueError

for Ra_num in Ra_numbs:

    command = (
        f"run_simul.py -R {Ra_num} -Pr {prandtl} -ny {ny} "
        f"--order {order} --dt-max {dt} --num-steps {num_steps} -np {nb_procs} "
        f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
        f"--delta-T-lateral {delta_T_lateral} --delta-T-vertical {delta_T_vertical}"
    )

    if x_periodicity:
        command += " --x-periodicity"
    elif y_periodicity:
        command += " --y-periodicity"
    elif z_periodicity:
        command += " --z-periodicity"

    print(command)

    name_run = f"_asp_{aspect_ratio:.3f}_Ra_{Ra_num:.3e}_Pr_{prandtl:.2f}_msh_{round(nx/aspect_ratio)*order}x{ny*order}"

    if delta_T_lateral == 1.0 and delta_T_vertical == 0.0:

        name_run = "VC" + name_run

    elif delta_T_lateral == 0.0 and delta_T_vertical == 1.0:

        name_run = "RB" + name_run

    elif delta_T_lateral == 1.0 and delta_T_vertical == 1.0:

        name_run = "MC" + name_run

    cluster.submit_script(
        command,
        name_run=name_run,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )
