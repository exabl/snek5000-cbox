from fluiddyn.clusters.legi import Calcul8 as Cluster

cluster = Cluster()

cluster.commands_setting_env = [
    "PROJET_DIR=/fsnet/project/meige/2020/20CONVECTION",
    "source /etc/profile",
    "source $PROJET_DIR/Software/miniconda3/etc/profile.d/conda.sh",
    "conda activate",
    "export NEK_SOURCE_ROOT=$HOME/Documents/Nek5000",
    "export PATH=$PATH:$NEK_SOURCE_ROOT/bin",
    "export FLUIDSIM_PATH=$PROJET_DIR/numerical/",
]

cluster.has_to_add_name_cluster = False

Ra_numbs = [1.0e07, 1.0e08]
num_elems = [16, 32]
orders = [10, 14]

for Ra_num in Ra_numbs:
    for num_elem in num_elems:
        for order in orders:

            cluster.submit_script(
                f"run_simul.py -R {Ra_num} -nx {num_elem} -ny {num_elem} -O {order}",
                name_run=f"test_Ra{Ra_num:.2e}_msh_{num_elem*order}_{num_elem*order}",
                nb_cores_per_node=10,
                omp_num_threads=1,
                ask=False,
            )
