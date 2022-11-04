from fluiddyn.clusters.legi import Calcul8 as Cluster


dim = 2

if dim == 3:
    aspect_ratio_z = 1.0

aspect_ratio_y = 0.5

prandtl = 0.71
Ra_side = 1.0
Ra_vert = 0.0

nx = 32
order = 10
stretch_factor = 0.0

end_time = 4000
dt = 0.05

nb_procs = 10
nb_nodes = 1
walltime = "24:00:00"

x_periodicity = False
y_periodicity = False
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

ny = int(nx * aspect_ratio_y)
if nx * aspect_ratio_y - ny:
    raise ValueError
if dim == 3:
    nz = int(ny / aspect_ratio_z)
    if ny / aspect_ratio_z - nz:
        raise ValueError

command = (
    f"run_simul_check_from_python.py -Pr {prandtl} -nx {nx} --dim {dim} "
    f"--order {order} --dt-max {dt} --end-time {end_time} -np {nb_nodes*nb_procs} "
    f"-a_y {aspect_ratio_y} --stretch-factor {stretch_factor}"
)

if dim == 3:
    command += f" -a_z {aspect_ratio_z}"
if x_periodicity:
    command += " --x-periodicity"
if y_periodicity:
    command += " --y-periodicity"
if z_periodicity:
    command += " --z-periodicity"


if Ra_side > 0.0 and Ra_vert == 0.0:

    command += f"--Ra-side {Ra_side}"

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ra{Ra_side:.3e}_Pr{prandtl:.2f}_msh{nx*order}x"
        f"{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )

    name_run = "SW" + name_run

elif Ra_side == 0.0 and Ra_vert > 0.0:

    command += f"--Ra-vert {Ra_vert}"

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ra{Ra_vert:.3e}_Pr{prandtl:.2f}_msh{nx*order}x"
        f"{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )

    name_run = "RB" + name_run

elif Ra_side > 0.0 and Ra_vert > 0.0:

    command += f"--Ra-side {Ra_side} --Ra-vert {Ra_vert}"

    name_run = (
        f"_Ay{aspect_ratio_y:.1f}_Ras{Ra_side:.3e}_Rav{Ra_vert:.3e}_Pr{prandtl:.2f}_msh"
        f"{nx*order}x{round(nx*aspect_ratio_y)*order}"
    )
    if dim == 3:
        name_run = (
            f"_Az{aspect_ratio_z:.1f}" + name_run + f"x{round(ny/aspect_ratio_z)*order}"
        )
    name_run = "MC" + name_run

print(command)

cluster.submit_script(
    command,
    name_run=name_run,
    walltime=walltime,
    nb_nodes=nb_nodes,
    nb_cores_per_node=nb_procs,
    omp_num_threads=1,
    ask=False,
)
