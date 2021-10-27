from fluiddyn.clusters.legi import Calcul8 as Cluster

cluster = Cluster()

cluster.commands_setting_env = [
    "source /etc/profile",
    "source /.fsnet/data/legi/calcul9/home/khoubani8a/useful/project/20CONVECTION/Software/miniconda3/etc/profile.d/conda.sh",
    "conda activate",
    'export NEK_SOURCE_ROOT="/.fsnet/data/legi/calcul9/home/khoubani8a/Documents/Nek5000"',
    'export PATH="$PATH:$NEK_SOURCE_ROOT/bin"',
    'export FLUIDSIM_PATH="/.fsnet/project/meige/2020/20CONVECTION/numerical/',
]

cluster.has_to_add_name_cluster = False

Ra_numbs = [1.0e07, 1.0e08]

for Ra_num in Ra_numbs:

    cluster.submit_command(
        f"python run_simul.py -Ra {Ra_num} ",
        name_run="test",
        nb_cores_per_node=10,
        omp_num_threads=1,
        ask=False,
        run_with_exec=True,
    )
