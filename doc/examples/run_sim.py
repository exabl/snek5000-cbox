from snek5000_cbox.solver import Simul

params = Simul.create_default_params()

sim = Simul(params)

print(sim.path_run)

sim.make.list()

sim.make.exec()