from snek5000_cbox.solver import Simul
# from phill.solver import Simul

params = Simul.create_default_params()

params.oper.nproc_min = 2
params.output.sub_directory = "examples_cbox"

params.oper.nx = 8
params.oper.ny = 8
params.oper.nz = 8

sim = Simul(params)

print(sim.path_run)

# sim.make.list()

sim.make.exec(["run_fg"], resources={"nproc": 2})
