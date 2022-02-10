from fluiddyn.clusters.legi import Calcul8 as Cluster

sim_path = ""  # base flow directory

end_time = 8000
aspect_ratio = 1.0
prandtl = 0.71
Ra = 1.820e8
nx = 32
order = 10

nb_procs = 20

cluster = Cluster()

cluster.commands_setting_env = [
    "PROJET_DIR=/fsnet/project/meige/2020/20CONVECTION",
    "source /etc/profile",
    "source $PROJET_DIR/Software/miniconda3/etc/profile.d/conda.sh",
    "conda activate",
    "export NEK_SOURCE_ROOT=$HOME/Dev/snek5000-old/lib/Nek5000",
    "export PATH=$PATH:$NEK_SOURCE_ROOT/bin",
    "export FLUIDSIM_PATH=$PROJET_DIR/numerical/",
]

command = (
    f"run_simul_linear.py --sim-path {sim_path} --end-time {end_time} "
    f"-Ra {Ra} -np {nb_procs}"
)

print(command)

cluster.submit_script(
    command,
    name_run=f"lin_asp_{aspect_ratio:.3f}_Ra_{Ra:.3e}_Pr_{prandtl:.2f}_msh_"
    f"{nx*order}x{round(nx*aspect_ratio)*order}",
    nb_cores_per_node=nb_procs,
    omp_num_threads=1,
    ask=False,
)
