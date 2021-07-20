from snek5000_cbox.solver import Simul

params = Simul.create_default_params()

params.oper.nproc_min = 2
params.output.sub_directory = "examples_cbox"

sim = Simul(params)

print(sim.path_run)

# sim.make.list()

sim.make.exec()
