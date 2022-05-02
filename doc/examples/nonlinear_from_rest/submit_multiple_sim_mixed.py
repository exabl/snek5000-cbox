import numpy as np

from fluiddyn.clusters.legi import Calcul2 as Cluster

prandtl = 0.71

dim = 2

aspect_ratio = 1.0
nx = 12
order = 10
stretch_factor = 0.0

end_time = 3000
dt = 0.05
nb_procs = 10

Ra_side = 1000
Ra_vert = 1000

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


Ra_side_numbs = np.logspace(np.log10(0.99 * Ra_side), np.log10(1.02 * Ra_side), 5)
Ra_vert_numbs = np.logspace(np.log10(0.99 * Ra_vert), np.log10(1.02 * Ra_vert), 5)


ny = int(nx * aspect_ratio)
if nx * aspect_ratio - ny:
    raise ValueError

for Ra_side_num in Ra_side_numbs:
    for Ra_vert_num in Ra_vert_numbs:

        command = (
            f"run_simul.py -Pr {prandtl} -nx {nx} --dim {dim} "
            f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_procs} "
            f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
            f"--Ra-side {Ra_side_num} --Ra-vert {Ra_vert_num} --sfd-activation {sfd_activation}"
        )

        if z_periodicity:
            command += " --z-periodicity"

        print(command)

        name_run = f"MC_asp{aspect_ratio:.3f}_Ra{Ra_side_num:.3e}_{Ra_vert_num:.3e}_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio)*order}"

        cluster.submit_script(
            command,
            name_run=name_run,
            nb_cores_per_node=nb_procs,
            omp_num_threads=1,
            ask=False,
        )
