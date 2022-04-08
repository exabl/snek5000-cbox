from fluiddyn.clusters.legi import Calcul8 as Cluster

from critical_Ra_sidewall import Ra_c as Ra_c_tests

prandtl = 1.0
aspect_ratio = 1.25
dim = 2

dt_max = 0.005
end_time = 3000
nb_procs = 10

ny = 2
order = 10
stretch_factor = 0.0
dim = 2

Ra_side = 1.0
Ra_vert = 0.0

x_periodicity = False
y_periodicity = False
z_periodicity = False

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

nx = int(ny / aspect_ratio)
if ny / aspect_ratio - nx:
    raise ValueError

command = (
    f"run_simul_check_from_python.py -Pr {prandtl} -ny {ny} --dim {dim} "
    f"--order {order} --dt-max {dt_max} --end-time {end_time} -np {nb_procs} "
    f"-a_y {aspect_ratio} --stretch-factor {stretch_factor} "
    f"--Ra-side {Ra_side} --Ra-vert {Ra_vert}"
)

if x_periodicity:
    command += " --x-periodicity"
elif y_periodicity:
    command += " --y-periodicity"
elif z_periodicity:
    command += " --z-periodicity"

print(command)

name_run = f"_asp{aspect_ratio:.3f}_Ra{Ra_c_test:.3e}_Pr{prandtl:.2f}_msh{round(nx/aspect_ratio)*order}x{ny*order}"

if Ra_side > 0.0 and Ra_vert == 0.0:

    name_run = "SW" + name_run

elif Ra_side == 0.0 and Ra_vert > 0.0:

    name_run = "RB" + name_run

elif Ra_side > 0.0 and Ra_vert > 0.0:

    name_run = "MC" + name_run

cluster.submit_script(
    command,
    name_run=name_run,
    nb_cores_per_node=nb_procs,
    omp_num_threads=1,
    ask=False,
)
