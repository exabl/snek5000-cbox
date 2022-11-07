import numpy as np

from fluiddyn.clusters.legi import Calcul2 as Cluster


dim = 2

if dim == 3:
    aspect_ratio_z = 1.0

aspect_ratio_y = 0.5

prandtl = 0.71
Ra_numbs = [1.8e8]

ny = 32
order = 10
stretch_factor = 0.0

end_time = 4000
dt = 0.05

nb_procs = 10
nb_nodes = 1
walltime = "24:00:00"

y_periodicity = False
z_periodicity = False

enable_sfd = False

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


nx = int(ny / aspect_ratio_y)
if ny / aspect_ratio_y - nx:
    raise ValueError
if dim == 3:
    nz = int(ny / aspect_ratio_z)
    if ny / aspect_ratio_z - nz:
        raise ValueError

for Ra_side_num in Ra_numbs:

    command = (
        f"run_simul_check_from_python.py -Pr {prandtl} -ny {ny} --dim {dim} "
        f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_nodes*nb_procs} "
        f"-a_y {aspect_ratio_y} --stretch-factor {stretch_factor} "
        f"--Ra-side {Ra_side_num}"
    )

    if dim == 3:
        command += f" -a_z {aspect_ratio_z}"
    if y_periodicity:
        command += " --y-periodicity"
    if z_periodicity:
        command += " --z-periodicity"
    if enable_sfd:
        command += " --enable-sfd"

    print(command)

    name_run = (
        f"SW_asp{aspect_ratio_y:.1f}_Ra{Ra_side_num:.3e}_Pr{prandtl:.2f}"
        f"_msh{nx*order}x{round(nx*aspect_ratio_y)*order}"
    )

    if dim == 3:
        name_run = (
            f"SW_Ay{aspect_ratio_y:.1f}_Az{aspect_ratio_z:.1f}_Ra{Ra_side_num:.3e}"
            f"_Pr{prandtl:.2f}_msh{nx*order}x{round(nx*aspect_ratio_y)*order}x"
            f"{round(ny/aspect_ratio_z)*order}"
        )

    cluster.submit_script(
        command,
        name_run=name_run,
        walltime=walltime,
        nb_nodes=nb_nodes,
        nb_cores_per_node=nb_procs,
        omp_num_threads=1,
        ask=False,
    )
